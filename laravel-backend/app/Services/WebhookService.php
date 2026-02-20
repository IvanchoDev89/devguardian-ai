<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class WebhookService
{
    private $webhooks = [];

    public function register(string $event, callable $handler): void
    {
        $this->webhooks[$event][] = $handler;
    }

    public function trigger(string $event, array $data): void
    {
        Log::info("Webhook triggered: {$event}", $data);

        if (isset($this->webhooks[$event])) {
            foreach ($this->webhooks[$event] as $handler) {
                try {
                    $handler($data);
                } catch (\Exception $e) {
                    Log::error("Webhook handler failed", [
                        'event' => $event,
                        'error' => $e->getMessage()
                    ]);
                }
            }
        }
    }

    public function sendToUrl(string $url, string $event, array $data): bool
    {
        try {
            $response = Http::timeout(30)->post($url, [
                'event' => $event,
                'timestamp' => now()->toIso8601String(),
                'data' => $data,
            ]);

            return $response->successful();
        } catch (\Exception $e) {
            Log::error('Webhook delivery failed', [
                'url' => $url,
                'event' => $event,
                'error' => $e->getMessage()
            ]);
            return false;
        }
    }

    public function sendScanComplete(string $webhookUrl, array $scanResult): bool
    {
        return $this->sendToUrl($webhookUrl, 'scan.complete', [
            'scan_id' => $scanResult['scan_id'] ?? null,
            'repository' => $scanResult['repository'] ?? null,
            'vulnerabilities_found' => $scanResult['vulnerabilities_found'] ?? 0,
            'status' => $scanResult['status'] ?? 'completed',
        ]);
    }

    public function sendVulnerabilityFound(string $webhookUrl, array $vulnerability): bool
    {
        return $this->sendToUrl($webhookUrl, 'vulnerability.found', [
            'vulnerability_id' => $vulnerability['id'] ?? null,
            'title' => $vulnerability['title'] ?? null,
            'severity' => $vulnerability['severity'] ?? null,
            'cwe_id' => $vulnerability['cwe_id'] ?? null,
            'location' => $vulnerability['location'] ?? null,
        ]);
    }

    public function sendUserRegistered(string $webhookUrl, array $user): bool
    {
        return $this->sendToUrl($webhookUrl, 'user.registered', [
            'user_id' => $user['id'] ?? null,
            'email' => $user['email'] ?? null,
            'name' => $user['name'] ?? null,
        ]);
    }

    public function sendSubscriptionChanged(string $webhookUrl, array $subscription): bool
    {
        return $this->sendToUrl($webhookUrl, 'subscription.changed', [
            'user_id' => $subscription['user_id'] ?? null,
            'plan' => $subscription['plan'] ?? null,
            'status' => $subscription['status'] ?? null,
        ]);
    }
}
