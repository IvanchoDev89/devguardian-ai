<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class ApiKeyController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $apiKeys = DB::table('api_keys')
            ->where('user_id', $request->user_id ?? 1)
            ->orderByDesc('created_at')
            ->get();

        return response()->json([
            'success' => true,
            'data' => $apiKeys->map(function ($key) {
                return [
                    'id' => $key->id,
                    'key_id' => $key->key_id,
                    'name' => $key->name,
                    'plan' => $key->plan,
                    'monthly_scans_limit' => $key->monthly_scans_limit,
                    'scans_used_this_month' => $key->scans_used_this_month,
                    'last_used_at' => $key->last_used_at,
                    'is_active' => $key->is_active,
                    'created_at' => $key->created_at,
                ];
            })
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'plan' => 'in:free,pro,enterprise',
        ]);

        $plan = $validated['plan'] ?? 'free';
        $limits = [
            'free' => 100,
            'pro' => 1000,
            'enterprise' => 10000,
        ];

        $keyId = Str::uuid()->toString();
        $secret = 'dg_' . Str::random(32);
        $keyHash = hash('sha256', $secret);

        DB::table('api_keys')->insert([
            'key_id' => $keyId,
            'key_hash' => $keyHash,
            'name' => $validated['name'],
            'user_id' => $request->user_id ?? 1,
            'plan' => $plan,
            'monthly_scans_limit' => $limits[$plan],
            'scans_used_this_month' => 0,
            'is_active' => true,
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        $fullKey = $keyId . '.' . $secret;

        return response()->json([
            'success' => true,
            'message' => 'API key created successfully',
            'data' => [
                'key_id' => $keyId,
                'key' => $fullKey,
                'name' => $validated['name'],
                'plan' => $plan,
                'monthly_scans_limit' => $limits[$plan],
                'warning' => 'Store this key securely. It will not be shown again.'
            ]
        ], 201);
    }

    public function show(Request $request, string $id): JsonResponse
    {
        $apiKey = DB::table('api_keys')
            ->where('key_id', $id)
            ->where('user_id', $request->user_id ?? 1)
            ->first();

        if (!$apiKey) {
            return response()->json([
                'success' => false,
                'message' => 'API key not found'
            ], 404);
        }

        return response()->json([
            'success' => true,
            'data' => [
                'id' => $apiKey->id,
                'key_id' => $apiKey->key_id,
                'name' => $apiKey->name,
                'plan' => $apiKey->plan,
                'monthly_scans_limit' => $apiKey->monthly_scans_limit,
                'scans_used_this_month' => $apiKey->scans_used_this_month,
                'last_used_at' => $apiKey->last_used_at,
                'is_active' => $apiKey->is_active,
                'created_at' => $apiKey->created_at,
            ]
        ]);
    }

    public function update(Request $request, string $id): JsonResponse
    {
        $validated = $request->validate([
            'name' => 'sometimes|string|max:255',
            'plan' => 'sometimes|in:free,pro,enterprise',
            'is_active' => 'sometimes|boolean',
        ]);

        $apiKey = DB::table('api_keys')
            ->where('key_id', $id)
            ->where('user_id', $request->user_id ?? 1)
            ->first();

        if (!$apiKey) {
            return response()->json([
                'success' => false,
                'message' => 'API key not found'
            ], 404);
        }

        $updates = $validated;
        
        if (isset($validated['plan'])) {
            $limits = [
                'free' => 100,
                'pro' => 1000,
                'enterprise' => 10000,
            ];
            $updates['monthly_scans_limit'] = $limits[$validated['plan']];
        }

        $updates['updated_at'] = now();

        DB::table('api_keys')
            ->where('key_id', $id)
            ->update($updates);

        return response()->json([
            'success' => true,
            'message' => 'API key updated successfully'
        ]);
    }

    public function destroy(Request $request, string $id): JsonResponse
    {
        $deleted = DB::table('api_keys')
            ->where('key_id', $id)
            ->where('user_id', $request->user_id ?? 1)
            ->delete();

        if (!$deleted) {
            return response()->json([
                'success' => false,
                'message' => 'API key not found'
            ], 404);
        }

        return response()->json([
            'success' => true,
            'message' => 'API key deleted successfully'
        ]);
    }

    public function rotate(Request $request, string $id): JsonResponse
    {
        $apiKey = DB::table('api_keys')
            ->where('key_id', $id)
            ->where('user_id', $request->user_id ?? 1)
            ->first();

        if (!$apiKey) {
            return response()->json([
                'success' => false,
                'message' => 'API key not found'
            ], 404);
        }

        $newSecret = 'dg_' . Str::random(32);
        $newKeyHash = hash('sha256', $newSecret);

        DB::table('api_keys')
            ->where('key_id', $id)
            ->update([
                'key_hash' => $newKeyHash,
                'updated_at' => now(),
            ]);

        $fullKey = $id . '.' . $newSecret;

        return response()->json([
            'success' => true,
            'message' => 'API key rotated successfully',
            'data' => [
                'key' => $fullKey,
                'warning' => 'Store this key securely. It will not be shown again.'
            ]
        ]);
    }

    public function usage(Request $request, string $id): JsonResponse
    {
        $apiKey = DB::table('api_keys')
            ->where('key_id', $id)
            ->first();

        if (!$apiKey) {
            return response()->json([
                'success' => false,
                'message' => 'API key not found'
            ], 404);
        }

        return response()->json([
            'success' => true,
            'data' => [
                'plan' => $apiKey->plan,
                'scans_used_this_month' => $apiKey->scans_used_this_month,
                'monthly_scans_limit' => $apiKey->monthly_scans_limit,
                'usage_percentage' => round(($apiKey->scans_used_this_month / $apiKey->monthly_scans_limit) * 100, 2),
                'remaining_scans' => max(0, $apiKey->monthly_scans_limit - $apiKey->scans_used_this_month),
            ]
        ]);
    }

    public function validateKey(string $key): ?array
    {
        $parts = explode('.', $key);
        if (count($parts) !== 2) {
            return null;
        }

        [$keyId, $secret] = $parts;
        $keyHash = hash('sha256', $secret);

        $apiKey = DB::table('api_keys')
            ->where('key_id', $keyId)
            ->where('key_hash', $keyHash)
            ->where('is_active', true)
            ->first();

        if (!$apiKey) {
            return null;
        }

        if ($apiKey->scans_used_this_month >= $apiKey->monthly_scans_limit) {
            return ['error' => 'Monthly scan limit exceeded', 'code' => 429];
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
}
