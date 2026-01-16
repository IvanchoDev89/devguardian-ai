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
            $vulnerability = $vulnerabilityRepository->findById($this->vulnerabilityId);
            
            if (!$vulnerability) {
                \Log::error("Vulnerability not found: {$this->vulnerabilityId}");
                return;
            }

            // Get vulnerable code
            $codeContent = $this->getVulnerableCode($vulnerability);
            
            // Generate AI fix
            $fixResult = $this->sendToAiFixService($codeContent, $vulnerability->identifier);
            
            // Store the fix
            $aiFixRepository->create([
                'id' => \Illuminate\Support\Str::uuid(),
                'vulnerability_id' => $this->vulnerabilityId,
                'fixed_code' => $fixResult['fixed_code'],
                'confidence' => $fixResult['confidence'],
                'explanation' => $fixResult['explanation'],
                'recommendations' => $fixResult['recommendations'],
                'status' => 'generated',
                'created_at' => now(),
            ]);

            // Update vulnerability status
            $vulnerabilityRepository->update($this->vulnerabilityId, ['status' => 'fixing']);
            
            \Log::info("AI fix generated for vulnerability {$this->vulnerabilityId}", [
                'confidence' => $fixResult['confidence'],
                'fix_id' => $fixResult['fix_id']
            ]);

        } catch (\Exception $e) {
            \Log::error("AI fix generation failed for vulnerability {$this->vulnerabilityId}: " . $e->getMessage());
            
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
