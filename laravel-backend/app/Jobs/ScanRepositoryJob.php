<?php

declare(strict_types=1);

namespace App\Jobs;

use App\Core\Application\Services\VulnerabilityScannerService;
use App\Core\Domain\Repositories\Repository;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;

final class ScanRepositoryJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $timeout = 600; // 10 minutes
    public int $tries = 3;
    public int|array $backoff = [30, 60, 120]; // Exponential backoff

    public function __construct(
        private readonly Repository $repository,
        private readonly array $options = []
    ) {
        $this->onQueue('scanning');
    }

    public function handle(VulnerabilityScannerService $scanner): void
    {
        Log::info('Starting repository scan job', [
            'repository_id' => $this->repository->id,
            'repository_name' => $this->repository->full_name,
            'job_id' => $this->job->getJobId()
        ]);

        try {
            // Check if repository is still active
            if (!$this->repository->isActive()) {
                Log::info('Skipping scan for inactive repository', [
                    'repository_id' => $this->repository->id
                ]);
                return;
            }

            // Perform the scan
            $vulnerabilities = $scanner->scanRepository($this->repository);

            // Store vulnerabilities
            foreach ($vulnerabilities as $vulnerability) {
                $vulnerability->save();
            }

            // Queue AI fix generation for new vulnerabilities if enabled
            if ($this->options['generate_fixes'] ?? true) {
                foreach ($vulnerabilities as $vulnerability) {
                    if ($vulnerability->canBeFixed()) {
                        ProcessVulnerabilityJob::dispatch($vulnerability);
                    }
                }
            }

            Log::info('Repository scan completed successfully', [
                'repository_id' => $this->repository->id,
                'vulnerabilities_found' => $vulnerabilities->count()
            ]);

        } catch (\Exception $e) {
            Log::error('Repository scan job failed', [
                'repository_id' => $this->repository->id,
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString()
            ]);

            $this->fail($e);
        }
    }

    public function failed(\Throwable $exception): void
    {
        Log::error('Repository scan job failed permanently', [
            'repository_id' => $this->repository->id,
            'error' => $exception->getMessage(),
            'attempts' => $this->attempts()
        ]);

        // Update repository status to indicate scan failure
        $this->repository->setScanSetting('last_scan_failed', true);
        $this->repository->setScanSetting('last_scan_error', $exception->getMessage());
        $this->repository->save();
    }

    public function tags(): array
    {
        return [
            'scan-repository',
            'repository:' . $this->repository->id,
            'organization:' . $this->repository->organization_id
        ];
    }
}
