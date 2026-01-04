<?php

namespace App\Jobs;

use App\Core\Domain\Repositories\VulnerabilityRepository;
use App\Core\Services\AiRemediationService;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class GenerateAiFixJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        private string $vulnerabilityId
    ) {}

    public function handle(
        VulnerabilityRepository $vulnerabilityRepository,
        AiRemediationService $aiService
    ): void {
        $vulnerability = $vulnerabilityRepository->findById($this->vulnerabilityId);
        
        if (!$vulnerability) {
            return;
        }

        $aiService->generateFix($vulnerability);
    }

    public function retryUntil(): \DateTime
    {
        return now()->addHours(1);
    }

    public function backoff(): array
    {
        return [10, 30, 60, 300];
    }
}
