<?php

declare(strict_types=1);

namespace App\Core\Application\Services;

use App\Core\Domain\Vulnerabilities\Vulnerability;
use App\Core\Domain\AiFixes\AiFix;
use App\Core\Domain\AiFixes\AiFixStatus;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Queue;
use Exception;

final class AiRemediationService
{
    public function __construct(
        private readonly string $aiServiceUrl,
        private readonly int $maxRetries = 3,
        private readonly int $retryDelayMs = 1000
    ) {}

    public function generateFixForVulnerability(Vulnerability $vulnerability): ?AiFix
    {
        Log::info('Starting AI fix generation', [
            'vulnerability_id' => $vulnerability->id,
            'repository_id' => $vulnerability->repository_id
        ]);

        try {
            // Mark vulnerability as analyzing
            $vulnerability->markAsAnalyzing();

            // Prepare request for AI service
            $request = $this->prepareFixRequest($vulnerability);

            // Call AI service
            $response = $this->callAIService('/api/v1/generate-fix', $request);

            if (!$response->successful()) {
                throw new Exception('AI service request failed: ' . $response->status());
            }

            $fixData = $response->json();

            // Create AI fix record
            $aiFix = $this->createAiFix($vulnerability, $fixData);

            // Validate the fix
            $this->validateFix($aiFix);

            Log::info('AI fix generated successfully', [
                'vulnerability_id' => $vulnerability->id,
                'fix_id' => $aiFix->id,
                'confidence_score' => $aiFix->confidence_score
            ]);

            return $aiFix;

        } catch (Exception $e) {
            Log::error('AI fix generation failed', [
                'vulnerability_id' => $vulnerability->id,
                'error' => $e->getMessage()
            ]);

            // Mark vulnerability back to detected if fix generation failed
            $vulnerability->update(['status' => 'detected']);

            return null;
        }
    }

    public function processVulnerabilityWithRetry(Vulnerability $vulnerability): void
    {
        $attempt = 0;
        
        while ($attempt < $this->maxRetries) {
            try {
                $aiFix = $this->generateFixForVulnerability($vulnerability);
                
                if ($aiFix && $aiFix->isSuccessful()) {
                    // Mark vulnerability as fixing
                    $vulnerability->markAsFixing();
                    return;
                }

                $attempt++;
                
                if ($attempt < $this->maxRetries) {
                    // Exponential backoff
                    $delay = $this->retryDelayMs * pow(2, $attempt - 1);
                    usleep($delay * 1000); // Convert to microseconds
                }

            } catch (Exception $e) {
                $attempt++;
                
                if ($attempt >= $this->maxRetries) {
                    // Create failed fix record
                    $this->createFailedFix($vulnerability, $e->getMessage());
                    return;
                }
                
                $delay = $this->retryDelayMs * pow(2, $attempt - 1);
                usleep($delay * 1000);
            }
        }
    }

    public function batchProcessVulnerabilities(array $vulnerabilityIds): void
    {
        foreach ($vulnerabilityIds as $vulnerabilityId) {
            $vulnerability = Vulnerability::find($vulnerabilityId);
            
            if ($vulnerability && $vulnerability->canBeFixed()) {
                // Queue for processing to avoid blocking
                Queue::push(function () use ($vulnerability) {
                    $this->processVulnerabilityWithRetry($vulnerability);
                });
            }
        }
    }

    private function prepareFixRequest(Vulnerability $vulnerability): array
    {
        $location = $vulnerability->location;
        $repository = $vulnerability->repository;

        // Get source code around the vulnerability
        $sourceCode = $this->getSourceCodeContext($vulnerability);

        return [
            'vulnerability_context' => [
                'repository_id' => $vulnerability->repository_id,
                'vulnerability_id' => $vulnerability->id,
                'cve_id' => $vulnerability->cve_id,
                'identifier' => $vulnerability->identifier,
                'title' => $vulnerability->title,
                'description' => $vulnerability->description,
                'severity' => $vulnerability->severity->value,
                'cvss_score' => $vulnerability->cvss_score ? [
                    'score' => $vulnerability->cvss_score,
                    'vector' => $vulnerability->cvss_vector
                ] : null,
                'location' => [
                    'file_path' => $location['file_path'] ?? '',
                    'line_number' => $location['line_number'] ?? 1,
                    'column_number' => $location['column_number'] ?? null,
                    'function_name' => $location['function_name'] ?? null,
                    'class_name' => $location['class_name'] ?? null
                ],
                'source_code' => $sourceCode,
                'language' => $this->detectLanguage($location['file_path'] ?? ''),
                'framework' => $this->detectFramework($repository),
                'dependencies' => $this->getRepositoryDependencies($repository),
                'metadata' => $vulnerability->metadata ?? []
            ],
            'additional_context' => $this->getAdditionalContext($vulnerability),
            'fix_style' => 'comprehensive',
            'include_tests' => true,
            'max_attempts' => 3
        ];
    }

    private function getSourceCodeContext(Vulnerability $vulnerability): string
    {
        $location = $vulnerability->location;
        $filePath = $location['file_path'] ?? '';
        $lineNumber = $location['line_number'] ?? 1;

        try {
            $repository = $vulnerability->repository;
            $gitUrl = $repository->getGitRepositoryUrl();
            
            // Clone repository temporarily or use cached version
            $tempPath = $this->getRepositoryTempPath($repository);
            
            $fullPath = $tempPath . '/' . $filePath;
            if (!file_exists($fullPath)) {
                return "// Source file not found";
            }

            $lines = file($fullPath, FILE_IGNORE_NEW_LINES);
            
            // Get context lines (5 before and after)
            $start = max(0, $lineNumber - 6);
            $end = min(count($lines), $lineNumber + 5);
            
            $contextLines = [];
            for ($i = $start; $i < $end; $i++) {
                $contextLines[] = $lines[$i];
            }

            return implode("\n", $contextLines);

        } catch (Exception $e) {
            Log::warning('Failed to get source code context', [
                'vulnerability_id' => $vulnerability->id,
                'error' => $e->getMessage()
            ]);
            
            return "// Unable to retrieve source code context";
        }
    }

    private function detectLanguage(string $filePath): string
    {
        $extension = strtolower(pathinfo($filePath, PATHINFO_EXTENSION));
        
        return match ($extension) {
            'php' => 'php',
            'js' => 'javascript',
            'ts' => 'typescript',
            'py' => 'python',
            'java' => 'java',
            'go' => 'go',
            'rb' => 'ruby',
            'cs' => 'csharp',
            'cpp', 'cc', 'cxx' => 'cpp',
            'c' => 'c',
            'rs' => 'rust',
            default => 'unknown'
        };
    }

    private function detectFramework($repository): ?string
    {
        // Check for common framework indicators
        $scanConfig = $repository->scan_config ?? [];
        
        if (isset($scanConfig['framework'])) {
            return $scanConfig['framework'];
        }

        // Could scan for composer.json, package.json, etc. to detect framework
        // For now, return null
        return null;
    }

    private function getRepositoryDependencies($repository): array
    {
        // Extract dependencies from package files
        // This is a simplified implementation
        return [];
    }

    private function getAdditionalContext(Vulnerability $vulnerability): string
    {
        $context = "This vulnerability was detected in a production codebase. ";
        
        if ($vulnerability->isCritical()) {
            $context .= "It has been marked as critical and should be fixed immediately. ";
        }
        
        $context .= "Please ensure the fix maintains backward compatibility and follows security best practices.";

        return $context;
    }

    private function callAIService(string $endpoint, array $data)
    {
        $correlationId = uniqid('devguardian_', true);
        
        return Http::withHeaders([
            'Content-Type' => 'application/json',
            'X-Correlation-ID' => $correlationId,
            'User-Agent' => 'DevGuardian-AI/1.0'
        ])->post($this->aiServiceUrl . $endpoint, $data);
    }

    private function createAiFix(Vulnerability $vulnerability, array $fixData): AiFix
    {
        return AiFix::create([
            'vulnerability_id' => $vulnerability->id,
            'repository_id' => $vulnerability->repository_id,
            'diff_content' => $fixData['diff_content'],
            'confidence_score' => $fixData['confidence_score'],
            'status' => AiFixStatus::GENERATED,
            'validation_results' => null,
            'error_message' => null,
            'retry_count' => 0,
            'test_results' => $fixData['test_cases'] ?? null,
            'metadata' => [
                'fix_id' => $fixData['fix_id'],
                'explanation' => $fixData['explanation'],
                'potential_side_effects' => $fixData['potential_side_effects'] ?? [],
                'generation_time_ms' => $fixData['generation_time_ms'] ?? 0
            ]
        ]);
    }

    private function validateFix(AiFix $aiFix): void
    {
        try {
            $aiFix->markAsValidating();

            $response = $this->callAIService('/api/v1/validate-fix', [
                'fix_id' => $aiFix->metadata['fix_id']
            ]);

            if (!$response->successful()) {
                throw new Exception('Fix validation failed: ' . $response->status());
            }

            $validationResult = $response->json();

            if ($validationResult['is_valid']) {
                $aiFix->markAsValidated($validationResult);
            } else {
                $aiFix->markAsFailed($validationResult['error_message'] ?? 'Validation failed');
            }

        } catch (Exception $e) {
            $aiFix->markAsFailed('Validation error: ' . $e->getMessage());
            Log::error('Fix validation failed', [
                'fix_id' => $aiFix->id,
                'error' => $e->getMessage()
            ]);
        }
    }

    private function createFailedFix(Vulnerability $vulnerability, string $errorMessage): void
    {
        AiFix::create([
            'vulnerability_id' => $vulnerability->id,
            'repository_id' => $vulnerability->repository_id,
            'diff_content' => '',
            'confidence_score' => 0.0,
            'status' => AiFixStatus::FAILED,
            'error_message' => $errorMessage,
            'retry_count' => $this->maxRetries,
            'metadata' => [
                'failed_at' => now()->toISOString(),
                'max_retries_reached' => true
            ]
        ]);
    }

    private function getRepositoryTempPath($repository): string
    {
        // Implementation for getting/creating temporary repository path
        // This would involve caching repositories for performance
        return sys_get_temp_dir() . '/devguardian_repo_' . $repository->id;
    }
}
