<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Cache\RateLimiter;
use Illuminate\Support\Facades\Redis;
use Carbon\Carbon;
use App\Core\Application\Services\SecurityLogger;

class AdvancedRateLimit
{
    private $rateLimiter;
    private $securityLogger;

    public function __construct(RateLimiter $rateLimiter, SecurityLogger $securityLogger)
    {
        $this->rateLimiter = $rateLimiter;
        $this->securityLogger = $securityLogger;
    }

    /**
     * Handle an incoming request with advanced rate limiting.
     */
    public function handle(Request $request, Closure $next, $maxAttempts = 60, $decayMinutes = 1)
    {
        $key = $this->resolveRequestSignature($request);
        
        // Check multiple rate limits
        if (!$this->checkRateLimits($request, $key, $maxAttempts, $decayMinutes)) {
            return $this->buildResponse($request, 'Rate limit exceeded');
        }

        // Check for suspicious patterns
        if ($this->isSuspiciousRequest($request)) {
            $this->securityLogger->logSuspiciousActivity($request, 'Suspicious request pattern detected');
            
            // Apply stricter limits for suspicious requests
            if (!$this->checkRateLimits($request, $key . ':suspicious', 10, 1)) {
                return $this->buildResponse($request, 'Suspicious activity detected - access denied', 429);
            }
        }

        // Check for abuse patterns
        if ($this->isAbusiveRequest($request)) {
            $this->securityLogger->logAbuse($request, 'Abusive request pattern detected');
            return $this->buildResponse($request, 'Abusive activity detected - access denied', 429);
        }

        $response = $next($request);

        // Add rate limit headers
        $this->addRateLimitHeaders($response, $key, $maxAttempts, $decayMinutes);

        return $response;
    }

    /**
     * Resolve request signature for rate limiting.
     */
    private function resolveRequestSignature(Request $request): string
    {
        // Use IP + User Agent for better fingerprinting
        $fingerprint = $request->ip() . '|' . $request->userAgent();
        
        // If user is authenticated, include user ID
        if ($request->user()) {
            $fingerprint .= '|' . $request->user()->id;
        }

        return hash('sha256', $fingerprint);
    }

    /**
     * Check multiple rate limits.
     */
    private function checkRateLimits(Request $request, string $key, int $maxAttempts, int $decayMinutes): bool
    {
        // Per-minute limit
        if (!$this->rateLimiter->attempt($key . ':minute', $maxAttempts, $decayMinutes * 60)) {
            return false;
        }

        // Per-hour limit (10x the minute limit)
        if (!$this->rateLimiter->attempt($key . ':hour', $maxAttempts * 10, 3600)) {
            return false;
        }

        // Per-day limit (100x the minute limit)
        if (!$this->rateLimiter->attempt($key . ':day', $maxAttempts * 100, 86400)) {
            return false;
        }

        return true;
    }

    /**
     * Check for suspicious request patterns.
     */
    private function isSuspiciousRequest(Request $request): bool
    {
        $suspiciousPatterns = [
            'sql_injection' => ['/union\s+select/i', '/or\s+1\s*=\s*1/i', '/drop\s+table/i'],
            'xss' => ['/<script/i', '/javascript:/i', '/on\w+\s*=/i'],
            'path_traversal' => ['/\.\.\//i', '/%2e%2e%2f/i', '/etc\/passwd/i'],
            'command_injection' => ['/[;&|]\s*rm/i', '/[;&|]\s*cat/i', '/`[^`]*`/'],
            'excessive_length' => '/^.{10000,}/', // Very long requests
            'unusual_headers' => '/^(x-|sec-)/i', // Suspicious headers
        ];

        $content = $request->getContent() . ' ' . $request->getRequestUri();
        
        foreach ($suspiciousPatterns as $type => $patterns) {
            foreach ($patterns as $pattern) {
                if (preg_match($pattern, $content)) {
                    $this->securityLogger->logPatternMatch($request, $type, $pattern);
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for abusive request patterns.
     */
    private function isAbusiveRequest(Request $request): bool
    {
        $ip = $request->ip();
        $currentMinute = Carbon::now()->format('YmdHi');
        
        // Check Redis for rapid-fire requests
        $requestCount = Redis::get("requests:{$ip}:{$currentMinute}") ?? 0;
        
        if ($requestCount > 100) { // More than 100 requests per minute
            return true;
        }

        // Increment request counter
        Redis::incr("requests:{$ip}:{$currentMinute}");
        Redis::expire("requests:{$ip}:{$currentMinute}", 120); // 2 minutes expiry

        // Check for distributed attacks from similar IPs
        $ipPrefix = substr($ip, 0, strrpos($ip, '.'));
        $networkRequests = Redis::get("network:{$ipPrefix}:{$currentMinute}") ?? 0;
        
        if ($networkRequests > 1000) { // More than 1000 requests from same /24 network
            return true;
        }

        Redis::incr("network:{$ipPrefix}:{$currentMinute}");
        Redis::expire("network:{$ipPrefix}:{$currentMinute}", 120);

        return false;
    }

    /**
     * Build rate limit response.
     */
    private function buildResponse(Request $request, string $message, int $status = 429)
    {
        if ($request->expectsJson()) {
            return response()->json([
                'error' => 'Rate limit exceeded',
                'message' => $message,
                'retry_after' => 60,
                'timestamp' => now()->toISOString()
            ], $status);
        }

        return response($message, $status);
    }

    /**
     * Add rate limit headers to response.
     */
    private function addRateLimitHeaders($response, string $key, int $maxAttempts, int $decayMinutes)
    {
        $remaining = $this->rateLimiter->retriesLeft($key . ':minute', $maxAttempts);
        $reset = $this->rateLimiter->availableIn($key . ':minute');

        $response->headers->set('X-RateLimit-Limit', $maxAttempts);
        $response->headers->set('X-RateLimit-Remaining', max(0, $remaining));
        $response->headers->set('X-RateLimit-Reset', $reset);
        $response->headers->set('X-RateLimit-Retry-After', $reset);
    }
}
