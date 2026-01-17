<?php

namespace App\Core\Application\Services;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Redis;
use Carbon\Carbon;
use App\Models\User;

class SecurityLogger
{
    private const LOG_LEVELS = [
        'INFO' => 'info',
        'WARNING' => 'warning',
        'ERROR' => 'error',
        'CRITICAL' => 'critical'
    ];

    /**
     * Log security events with comprehensive context.
     */
    public function logSecurityEvent(Request $request, string $event, array $context = [], string $level = 'INFO')
    {
        $logData = [
            'timestamp' => now()->toISOString(),
            'event' => $event,
            'ip_address' => $request->ip(),
            'user_agent' => $request->userAgent(),
            'method' => $request->method(),
            'url' => $request->fullUrl(),
            'user_id' => $request->user()?->id,
            'session_id' => session()->getId(),
            'request_id' => $request->header('X-Request-ID', uniqid()),
            'context' => $context,
            'geo_location' => $this->getGeoLocation($request->ip()),
            'fingerprint' => $this->generateFingerprint($request)
        ];

        // Log to Laravel logger
        Log::log(self::LOG_LEVELS[$level] ?? 'info', $event, $logData);

        // Store in Redis for real-time monitoring
        $this->storeSecurityEvent($logData);

        // Trigger alerts for critical events
        if ($level === 'CRITICAL') {
            $this->triggerSecurityAlert($logData);
        }
    }

    /**
     * Log suspicious activity.
     */
    public function logSuspiciousActivity(Request $request, string $description, array $context = [])
    {
        $this->logSecurityEvent($request, 'SUSPICIOUS_ACTIVITY', array_merge([
            'description' => $description,
            'risk_score' => $this->calculateRiskScore($request, $context)
        ], $context), 'WARNING');
    }

    /**
     * Log abuse attempts.
     */
    public function logAbuse(Request $request, string $description, array $context = [])
    {
        $this->logSecurityEvent($request, 'ABUSE_ATTEMPT', array_merge([
            'description' => $description,
            'abuse_type' => $context['type'] ?? 'unknown'
        ], $context), 'ERROR');
    }

    /**
     * Log authentication events.
     */
    public function logAuthEvent(Request $request, string $event, ?User $user = null, array $context = [])
    {
        $this->logSecurityEvent($request, 'AUTH_' . strtoupper($event), array_merge([
            'user_id' => $user?->id,
            'user_email' => $user?->email,
            'auth_method' => $context['method'] ?? 'standard'
        ], $context), $event === 'failure' ? 'WARNING' : 'INFO');
    }

    /**
     * Log vulnerability detection.
     */
    public function logVulnerabilityDetection(Request $request, string $vulnerabilityType, array $findings)
    {
        $this->logSecurityEvent($request, 'VULNERABILITY_DETECTED', [
            'vulnerability_type' => $vulnerabilityType,
            'findings_count' => count($findings),
            'severity_distribution' => $this->getSeverityDistribution($findings),
            'top_cwe_ids' => $this->getTopCweIds($findings)
        ], 'WARNING');
    }

    /**
     * Log pattern matches.
     */
    public function logPatternMatch(Request $request, string $patternType, string $pattern)
    {
        $this->logSecurityEvent($request, 'PATTERN_MATCH', [
            'pattern_type' => $patternType,
            'pattern' => $pattern,
            'matched_content' => $this->extractMatchedContent($request, $pattern)
        ], 'WARNING');
    }

    /**
     * Store security event in Redis for monitoring.
     */
    private function storeSecurityEvent(array $logData)
    {
        $key = 'security_events:' . Carbon::now()->format('Ymd');
        Redis::lpush($key, json_encode($logData));
        Redis::expire($key, 86400 * 30); // Keep for 30 days

        // Store real-time metrics
        $this->updateSecurityMetrics($logData);
    }

    /**
     * Update security metrics.
     */
    private function updateSecurityMetrics(array $logData)
    {
        $event = $logData['event'];
        $hour = Carbon::now()->format('YmdH');
        
        // Increment event counter
        Redis::hincrby("security_metrics:{$hour}", $event, 1);
        Redis::expire("security_metrics:{$hour}", 86400 * 7); // Keep for 7 days

        // Update IP-based metrics
        $ip = $logData['ip_address'];
        Redis::hincrby("ip_metrics:{$hour}", $ip, 1);
        Redis::expire("ip_metrics:{$hour}", 86400 * 7);

        // Update risk score
        if (isset($logData['context']['risk_score'])) {
            Redis::hset("risk_scores:{$hour}", $ip, $logData['context']['risk_score']);
            Redis::expire("risk_scores:{$hour}", 86400 * 7);
        }
    }

    /**
     * Calculate risk score for request.
     */
    private function calculateRiskScore(Request $request, array $context): float
    {
        $score = 0.0;

        // Base score for suspicious patterns
        if (isset($context['suspicious_patterns'])) {
            $score += count($context['suspicious_patterns']) * 10;
        }

        // IP-based risk
        $ip = $request->ip();
        if ($this->isKnownMaliciousIp($ip)) {
            $score += 50;
        }

        // User agent analysis
        $userAgent = $request->userAgent();
        if ($this->isSuspiciousUserAgent($userAgent)) {
            $score += 20;
        }

        // Request frequency analysis
        if ($this->isHighFrequencyRequester($ip)) {
            $score += 30;
        }

        // Geographic risk
        $geoLocation = $this->getGeoLocation($ip);
        if ($this->isHighRiskCountry($geoLocation['country'] ?? '')) {
            $score += 15;
        }

        return min(100.0, $score);
    }

    /**
     * Generate request fingerprint.
     */
    private function generateFingerprint(Request $request): string
    {
        $elements = [
            $request->ip(),
            $request->userAgent(),
            $request->header('Accept-Language'),
            $request->header('Accept-Encoding'),
        ];

        return hash('sha256', implode('|', $elements));
    }

    /**
     * Get geo location for IP.
     */
    private function getGeoLocation(string $ip): array
    {
        // This would integrate with a GeoIP service
        // For now, return placeholder data
        return [
            'country' => 'Unknown',
            'city' => 'Unknown',
            'latitude' => 0.0,
            'longitude' => 0.0
        ];
    }

    /**
     * Extract matched content for logging.
     */
    private function extractMatchedContent(Request $request, string $pattern): string
    {
        $content = $request->getContent() . ' ' . $request->getRequestUri();
        
        if (preg_match($pattern, $content, $matches)) {
            return substr($matches[0] ?? '', 0, 100); // Limit to 100 chars
        }

        return '';
    }

    /**
     * Get severity distribution of findings.
     */
    private function getSeverityDistribution(array $findings): array
    {
        $distribution = ['critical' => 0, 'high' => 0, 'medium' => 0, 'low' => 0];
        
        foreach ($findings as $finding) {
            $severity = strtolower($finding['severity'] ?? 'low');
            if (isset($distribution[$severity])) {
                $distribution[$severity]++;
            }
        }

        return $distribution;
    }

    /**
     * Get top CWE IDs from findings.
     */
    private function getTopCweIds(array $findings): array
    {
        $cweCounts = [];
        
        foreach ($findings as $finding) {
            if (isset($finding['cwe_id'])) {
                $cweId = $finding['cwe_id'];
                $cweCounts[$cweId] = ($cweCounts[$cweId] ?? 0) + 1;
            }
        }

        arsort($cweCounts);
        return array_slice(array_keys($cweCounts), 0, 5, true);
    }

    /**
     * Trigger security alert for critical events.
     */
    private function triggerSecurityAlert(array $logData)
    {
        // This would integrate with alerting systems
        // For now, just log with critical level
        Log::critical('SECURITY ALERT', $logData);

        // Store alert for dashboard
        Redis::lpush('security_alerts', json_encode($logData));
        Redis::expire('security_alerts', 86400); // Keep for 24 hours
    }

    /**
     * Check if IP is known malicious.
     */
    private function isKnownMaliciousIp(string $ip): bool
    {
        // This would check against threat intelligence feeds
        return Redis::sismember('malicious_ips', $ip);
    }

    /**
     * Check if user agent is suspicious.
     */
    private function isSuspiciousUserAgent(string $userAgent): bool
    {
        $suspiciousPatterns = [
            '/bot/i',
            '/crawler/i',
            '/scanner/i',
            '/curl/i',
            '/wget/i',
            '/python/i',
            '/perl/i'
        ];

        foreach ($suspiciousPatterns as $pattern) {
            if (preg_match($pattern, $userAgent)) {
                return true;
            }
        }

        return false;
    }

    /**
     * Check if IP is making high-frequency requests.
     */
    private function isHighFrequencyRequester(string $ip): bool
    {
        $currentMinute = Carbon::now()->format('YmdHi');
        $requestCount = Redis::get("requests:{$ip}:{$currentMinute}") ?? 0;
        
        return $requestCount > 50; // More than 50 requests per minute
    }

    /**
     * Check if country is high risk.
     */
    private function isHighRiskCountry(string $country): bool
    {
        // This would check against a list of high-risk countries
        $highRiskCountries = ['CN', 'RU', 'KP', 'IR'];
        
        return in_array($country, $highRiskCountries);
    }

    /**
     * Get security metrics for dashboard.
     */
    public function getSecurityMetrics(): array
    {
        $currentHour = Carbon::now()->format('YmdH');
        $metrics = Redis::hgetall("security_metrics:{$currentHour}");
        
        return [
            'timestamp' => Carbon::now()->toISOString(),
            'metrics' => $metrics,
            'total_events' => array_sum($metrics),
            'top_events' => $this->getTopEvents($metrics),
            'alert_count' => Redis::llen('security_alerts')
        ];
    }

    /**
     * Get top events from metrics.
     */
    private function getTopEvents(array $metrics): array
    {
        arsort($metrics);
        return array_slice($metrics, 0, 5, true);
    }
}
