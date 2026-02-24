<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class SanitizeInput
{
    /**
     * Handle an incoming request.
     * Sanitizes all input data to prevent XSS and injection attacks.
     */
    public function handle(Request $request, Closure $next): Response
    {
        // Skip for safe methods
        if (in_array($request->method(), ['GET', 'HEAD', 'OPTIONS'])) {
            return $next($request);
        }

        $input = $request->all();
        
        if (is_array($input) && !empty($input)) {
            $sanitized = $this->sanitize($input);
            $request->merge($sanitized);
        }

        return $next($request);
    }

    /**
     * Recursively sanitize input data
     */
    protected function sanitize(mixed $data): mixed
    {
        if (is_array($data)) {
            return array_map([$this, 'sanitize'], $data);
        }

        if (is_string($data)) {
            // Remove null bytes
            $data = str_replace("\0", '', $data);
            
            // Encode HTML entities
            $data = htmlspecialchars($data, ENT_QUOTES | ENT_HTML5, 'UTF-8');
            
            // Remove common XSS vectors
            $data = $this->removeXssVectors($data);
            
            return $data;
        }

        return $data;
    }

    /**
     * Remove common XSS attack vectors
     */
    protected function removeXssVectors(string $data): string
    {
        // Remove javascript: URLs
        $data = preg_replace('/javascript\s*:/i', '', $data);
        
        // Remove data: URLs (potential XSS)
        $data = preg_replace('/data\s*:/i', '', $data);
        
        // Remove vbscript: URLs
        $data = preg_replace('/vbscript\s*:/i', '', $data);
        
        return $data;
    }
}
