<?php

declare(strict_types=1);

namespace App\Jobs;

use App\Core\Application\Services\SecurityMetricsService;
use App\Core\Domain\Organizations\Organization;
use App\Core\Domain\Repositories\Repository;
use App\Core\Domain\Vulnerabilities\Vulnerability;
use App\Core\Domain\AiFixes\AiFix;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Http;

final class NotifySecurityEventJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $timeout = 60; // 1 minute
    public int $tries = 3;
    public int|array $backoff = [10, 30, 60]; // Exponential backoff

    public function __construct(
        private readonly string $eventType,
        private readonly array $eventData,
        private readonly array $notificationChannels = ['slack', 'email']
    ) {
        $this->onQueue('notifications');
    }

    public function handle(): void
    {
        Log::info('Processing security event notification', [
            'event_type' => $this->eventType,
            'channels' => $this->notificationChannels
        ]);

        try {
            foreach ($this->notificationChannels as $channel) {
                $this->sendNotification($channel);
            }

            Log::info('Security event notifications sent successfully', [
                'event_type' => $this->eventType,
                'channels' => $this->notificationChannels
            ]);

        } catch (\Exception $e) {
            Log::error('Failed to send security event notifications', [
                'event_type' => $this->eventType,
                'error' => $e->getMessage()
            ]);

            $this->fail($e);
        }
    }

    private function sendNotification(string $channel): void
    {
        switch ($channel) {
            case 'slack':
                $this->sendSlackNotification();
                break;
            case 'email':
                $this->sendEmailNotification();
                break;
            case 'webhook':
                $this->sendWebhookNotification();
                break;
            case 'teams':
                $this->sendTeamsNotification();
                break;
            default:
                Log::warning('Unknown notification channel', ['channel' => $channel]);
        }
    }

    private function sendSlackNotification(): void
    {
        $webhookUrl = config('services.slack.webhook_url');
        
        if (!$webhookUrl) {
            Log::warning('Slack webhook URL not configured');
            return;
        }

        $payload = $this->buildSlackPayload();

        $response = Http::post($webhookUrl, $payload);

        if (!$response->successful()) {
            throw new \Exception('Slack notification failed: ' . $response->status());
        }

        Log::info('Slack notification sent successfully');
    }

    private function buildSlackPayload(): array
    {
        $color = $this->getSlackColor();
        $title = $this->getNotificationTitle();
        $message = $this->getNotificationMessage();

        return [
            'attachments' => [
                [
                    'color' => $color,
                    'title' => $title,
                    'text' => $message,
                    'fields' => $this->getSlackFields(),
                    'footer' => 'DevGuardian AI',
                    'ts' => now()->timestamp
                ]
            ]
        ];
    }

    private function getSlackColor(): string
    {
        return match ($this->eventType) {
            'vulnerability_detected' => 'warning',
            'critical_vulnerability' => 'danger',
            'fix_generated' => 'good',
            'fix_applied' => 'good',
            'security_breach' => 'danger',
            'scan_completed' => '#36a64f',
            default => '#6b7280'
        };
    }

    private function getNotificationTitle(): string
    {
        return match ($this->eventType) {
            'vulnerability_detected' => '🔍 New Vulnerability Detected',
            'critical_vulnerability' => '🚨 Critical Security Alert',
            'fix_generated' => '🤖 AI Fix Generated',
            'fix_applied' => '✅ Security Fix Applied',
            'security_breach' => '🚨 Security Breach Detected',
            'scan_completed' => '✅ Security Scan Completed',
            default => '🔔 Security Event'
        };
    }

    private function getNotificationMessage(): string
    {
        return match ($this->eventType) {
            'vulnerability_detected' => $this->formatVulnerabilityDetectedMessage(),
            'critical_vulnerability' => $this->formatCriticalVulnerabilityMessage(),
            'fix_generated' => $this->formatFixGeneratedMessage(),
            'fix_applied' => $this->formatFixAppliedMessage(),
            'security_breach' => $this->formatSecurityBreachMessage(),
            'scan_completed' => $this->formatScanCompletedMessage(),
            default => $this->formatGenericMessage()
        };
    }

    private function getSlackFields(): array
    {
        $fields = [];

        if (isset($this->eventData['repository'])) {
            $fields[] = [
                'title' => 'Repository',
                'value' => $this->eventData['repository']['name'],
                'short' => true
            ];
        }

        if (isset($this->eventData['vulnerability'])) {
            $vuln = $this->eventData['vulnerability'];
            $fields[] = [
                'title' => 'Severity',
                'value' => strtoupper($vuln['severity']),
                'short' => true
            ];
            
            if (isset($vuln['cvss_score'])) {
                $fields[] = [
                    'title' => 'CVSS Score',
                    'value' => $vuln['cvss_score'],
                    'short' => true
                ];
            }
        }

        if (isset($this->eventData['fix'])) {
            $fix = $this->eventData['fix'];
            $fields[] = [
                'title' => 'Confidence',
                'value' => round(($fix['confidence_score'] * 100), 1) . '%',
                'short' => true
            ];
        }

        if (isset($this->eventData['organization'])) {
            $fields[] = [
                'title' => 'Organization',
                'value' => $this->eventData['organization']['name'],
                'short' => true
            ];
        }

        return $fields;
    }

    private function formatVulnerabilityDetectedMessage(): string
    {
        $vuln = $this->eventData['vulnerability'];
        $repo = $this->eventData['repository'];
        
        return "A new vulnerability was detected in *{$repo['name']}*: \n*{$vuln['title']}* ({$vuln['severity']})";
    }

    private function formatCriticalVulnerabilityMessage(): string
    {
        $vuln = $this->eventData['vulnerability'];
        $repo = $this->eventData['repository'];
        
        return "🚨 *CRITICAL* vulnerability detected in *{$repo['name']}*: \n*{$vuln['title']}* \nImmediate action required!";
    }

    private function formatFixGeneratedMessage(): string
    {
        $vuln = $this->eventData['vulnerability'];
        $fix = $this->eventData['fix'];
        
        return "AI fix generated for *{$vuln['title']}* with " . round(($fix['confidence_score'] * 100), 1) . "% confidence.";
    }

    private function formatFixAppliedMessage(): string
    {
        $vuln = $this->eventData['vulnerability'];
        $pr = $this->eventData['pull_request'] ?? null;
        
        $message = "Security fix applied for *{$vuln['title']}*";
        
        if ($pr) {
            $message .= "\n📋 Pull Request: <{$pr['url']}|##{$pr['number']}>";
        }
        
        return $message;
    }

    private function formatSecurityBreachMessage(): string
    {
        $breach = $this->eventData['breach'];
        
        return "🚨 Security breach detected: *{$breach['type']}* \n{$breach['description']}";
    }

    private function formatScanCompletedMessage(): string
    {
        $scan = $this->eventData['scan'];
        $repo = $this->eventData['repository'];
        
        return "Security scan completed for *{$repo['name']}*: \nFound {$scan['vulnerabilities_found']} vulnerabilities";
    }

    private function formatGenericMessage(): string
    {
        return "Security event: {$this->eventType}";
    }

    private function sendEmailNotification(): void
    {
        // Implementation for email notifications
        Log::info('Email notification sent (placeholder implementation)');
    }

    private function sendWebhookNotification(): void
    {
        $webhookUrl = config('services.webhook.security_events_url');
        
        if (!$webhookUrl) {
            Log::warning('Security events webhook URL not configured');
            return;
        }

        $payload = [
            'event_type' => $this->eventType,
            'event_data' => $this->eventData,
            'timestamp' => now()->toISOString(),
            'source' => 'devguardian-ai'
        ];

        $response = Http::post($webhookUrl, $payload);

        if (!$response->successful()) {
            throw new \Exception('Webhook notification failed: ' . $response->status());
        }

        Log::info('Webhook notification sent successfully');
    }

    private function sendTeamsNotification(): void
    {
        // Implementation for Microsoft Teams notifications
        Log::info('Teams notification sent (placeholder implementation)');
    }

    public function failed(\Throwable $exception): void
    {
        Log::error('Security event notification job failed permanently', [
            'event_type' => $this->eventType,
            'error' => $exception->getMessage(),
            'attempts' => $this->attempts()
        ]);
    }

    public function tags(): array
    {
        return [
            'notify-security-event',
            'event-type:' . $this->eventType,
            'channels:' . implode(',', $this->notificationChannels)
        ];
    }

    // Static factory methods for common events
    public static function vulnerabilityDetected(Vulnerability $vulnerability): self
    {
        return new self('vulnerability_detected', [
            'vulnerability' => [
                'id' => $vulnerability->id,
                'title' => $vulnerability->title,
                'severity' => $vulnerability->severity->value,
                'cvss_score' => $vulnerability->cvss_score,
                'detected_at' => $vulnerability->detected_at->toISOString()
            ],
            'repository' => [
                'id' => $vulnerability->repository->id,
                'name' => $vulnerability->repository->full_name,
                'provider' => $vulnerability->repository->provider->value
            ],
            'organization' => [
                'id' => $vulnerability->repository->organization->id,
                'name' => $vulnerability->repository->organization->name
            ]
        ]);
    }

    public static function criticalVulnerability(Vulnerability $vulnerability): self
    {
        return new self('critical_vulnerability', [
            'vulnerability' => [
                'id' => $vulnerability->id,
                'title' => $vulnerability->title,
                'severity' => $vulnerability->severity->value,
                'cvss_score' => $vulnerability->cvss_score,
                'detected_at' => $vulnerability->detected_at->toISOString()
            ],
            'repository' => [
                'id' => $vulnerability->repository->id,
                'name' => $vulnerability->repository->full_name,
                'provider' => $vulnerability->repository->provider->value
            ],
            'organization' => [
                'id' => $vulnerability->repository->organization->id,
                'name' => $vulnerability->repository->organization->name
            ]
        ], ['slack', 'email', 'teams']);
    }

    public static function fixGenerated(AiFix $aiFix): self
    {
        return new self('fix_generated', [
            'fix' => [
                'id' => $aiFix->id,
                'confidence_score' => $aiFix->confidence_score,
                'status' => $aiFix->status->value,
                'created_at' => $aiFix->created_at->toISOString()
            ],
            'vulnerability' => [
                'id' => $aiFix->vulnerability->id,
                'title' => $aiFix->vulnerability->title,
                'severity' => $aiFix->vulnerability->severity->value
            ],
            'repository' => [
                'id' => $aiFix->repository->id,
                'name' => $aiFix->repository->full_name
            ]
        ]);
    }

    public static function fixApplied(AiFix $aiFix, ?array $pullRequest = null): self
    {
        $data = [
            'fix' => [
                'id' => $aiFix->id,
                'confidence_score' => $aiFix->confidence_score,
                'applied_at' => now()->toISOString()
            ],
            'vulnerability' => [
                'id' => $aiFix->vulnerability->id,
                'title' => $aiFix->vulnerability->title
            ],
            'repository' => [
                'id' => $aiFix->repository->id,
                'name' => $aiFix->repository->full_name
            ]
        ];

        if ($pullRequest) {
            $data['pull_request'] = $pullRequest;
        }

        return new self('fix_applied', $data);
    }

    public static function scanCompleted(Repository $repository, array $scanResults): self
    {
        return new self('scan_completed', [
            'scan' => $scanResults,
            'repository' => [
                'id' => $repository->id,
                'name' => $repository->full_name,
                'last_scanned_at' => $repository->last_scanned_at?->toISOString()
            ],
            'organization' => [
                'id' => $repository->organization->id,
                'name' => $repository->organization->name
            ]
        ]);
    }
}
