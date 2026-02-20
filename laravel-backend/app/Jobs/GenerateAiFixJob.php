<?php

namespace App\Jobs;

use App\Core\Domain\Repositories\VulnerabilityRepository;
use App\Core\Domain\Repositories\AiFixRepository;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Support\Facades\Http;

class GenerateAiFixJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable;

    public function __construct(
        private string $vulnerabilityId,
        private array $options = []
    ) {}


    public function handle(
        VulnerabilityRepository $vulnerabilityRepository,
        AiFixRepository $aiFixRepository
    ): void {
        try {
            // Find vulnerability
            $vulnerability = $vulnerabilityRepository->findById($this->vulnerabilityId);
            if (!$vulnerability) {
                \Log::error('Vulnerability not found', [
                    'vulnerability_id' => $this->vulnerabilityId,
                    'job' => __CLASS__
                ]);
                return;
            }

            // Get vulnerable code
            $codeContent = $this->getVulnerableCode($vulnerability);
            if (empty($codeContent)) {
                \Log::warning('Vulnerable code not found or empty', [
                    'vulnerability_id' => $this->vulnerabilityId,
                    'file_path' => $vulnerability->location['path'] ?? null,
                    'job' => __CLASS__
                ]);
            }

            // Generate AI fix
            $fixResult = $this->sendToAiFixService($codeContent, $vulnerability->identifier);
            if (!is_array($fixResult) || empty($fixResult['fixed_code'])) {
                throw new \Exception('AI fix service returned invalid result');
            }

            // Store the fix
            $aiFixRepository->create([
                'id' => \Illuminate\Support\Str::uuid(),
                'vulnerability_id' => $this->vulnerabilityId,
                'fixed_code' => $fixResult['fixed_code'],
                'confidence' => $fixResult['confidence'] ?? null,
                'explanation' => $fixResult['explanation'] ?? '',
                'recommendations' => $fixResult['recommendations'] ?? [],
                'status' => 'generated',
                'created_at' => now(),
            ]);

            // Update vulnerability status
            $vulnerabilityRepository->update($this->vulnerabilityId, ['status' => 'fixing']);

            \Log::info('AI fix generated', [
                'vulnerability_id' => $this->vulnerabilityId,
                'confidence' => $fixResult['confidence'] ?? null,
                'fix_id' => $fixResult['fix_id'] ?? null,
                'job' => __CLASS__
            ]);

        } catch (\Exception $e) {
            \Log::error('AI fix generation failed', [
                'vulnerability_id' => $this->vulnerabilityId,
                'error' => $e->getMessage(),
                'job' => __CLASS__
            ]);
            // Update vulnerability status to indicate failure
            $vulnerabilityRepository->update($this->vulnerabilityId, ['status' => 'fix_failed']);
        }
    }

    private function getVulnerableCode($vulnerability): string
    {
        $filePath = $vulnerability->location['path'] ?? '';
        if (file_exists($filePath)) {
            return file_get_contents($filePath);
        }
        
        return '';
    }

    private function sendToAiFixService(string $content, string $vulnerabilityType): array
    {
        $response = Http::timeout(120)->post(
            config('services.ai_service.url') . '/api/ai-fix/generate-fix',
            [
                'content' => $content,
                'vulnerability_type' => $vulnerabilityType
            ]
        );
        
        if (!$response->successful()) {
            throw new \Exception('AI fix service failed: ' . $response->body());
        }
        
        return $response->json();
    }
}
