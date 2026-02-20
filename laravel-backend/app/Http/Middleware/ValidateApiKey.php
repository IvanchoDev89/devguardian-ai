<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Symfony\Component\HttpFoundation\Response;

class ValidateApiKey
{
    public function handle(Request $request, Closure $next): Response
    {
        $apiKey = $request->bearerToken() ?? $request->header('X-API-Key');

        if (!$apiKey) {
            return response()->json([
                'success' => false,
                'error' => 'API key required',
                'message' => 'Provide API key via Authorization header or X-API-Key header'
            ], 401);
        }

        $validationResult = $this->validateKey($apiKey);

        if (isset($validationResult['error'])) {
            return response()->json([
                'success' => false,
                'error' => $validationResult['error'],
                'code' => $validationResult['code'] ?? 401
            ], $validationResult['code'] ?? 401);
        }

        $request->merge(['api_key_id' => $validationResult['id']]);
        $request->merge(['api_user_id' => $validationResult['user_id']]);
        $request->merge(['api_plan' => $validationResult['plan']]);

        return $next($request);
    }

    private function validateKey(string $key): ?array
    {
        $parts = explode('.', $key);
        if (count($parts) !== 2) {
            return ['error' => 'Invalid API key format', 'code' => 401];
        }

        [$keyId, $secret] = $parts;
        $keyHash = hash('sha256', $secret);

        $apiKey = DB::table('api_keys')
            ->where('key_id', $keyId)
            ->where('key_hash', $keyHash)
            ->where('is_active', true)
            ->first();

        if (!$apiKey) {
            return ['error' => 'Invalid API key', 'code' => 401];
        }

        if ($apiKey->scans_used_this_month >= $apiKey->monthly_scans_limit) {
            return [
                'error' => 'Monthly scan limit exceeded. Upgrade your plan.',
                'code' => 429,
                'retry_after' => $this->getSecondsUntilNextMonth()
            ];
        }

        DB::table('api_keys')
            ->where('id', $apiKey->id)
            ->update([
                'scans_used_this_month' => $apiKey->scans_used_this_month + 1,
                'last_used_at' => now(),
            ]);

        return [
            'id' => $apiKey->id,
            'user_id' => $apiKey->user_id,
            'plan' => $apiKey->plan,
            'remaining' => $apiKey->monthly_scans_limit - $apiKey->scans_used_this_month - 1,
        ];
    }

    private function getSecondsUntilNextMonth(): int
    {
        $now = now();
        $nextMonth = $now->copy()->startOfMonth()->addMonth();
        return $nextMonth->diffInSeconds($now);
    }
}
