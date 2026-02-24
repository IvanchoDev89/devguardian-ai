<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;

class AuthController extends Controller
{
    public function register(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|string|email|max:255|unique:users',
            'password' => 'required|string|min:8|confirmed',
        ]);

        $user = DB::table('users')->insert([
            'name' => $validated['name'],
            'email' => $validated['email'],
            'password' => Hash::make($validated['password']),
            'role' => 'member',
            'is_active' => true,
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        $token = $this->createToken($validated['email']);

        return response()->json([
            'success' => true,
            'message' => 'Registration successful',
            'data' => [
                'user' => [
                    'name' => $validated['name'],
                    'email' => $validated['email'],
                    'role' => 'member',
                ],
                'token' => $token,
            ]
        ], 201);
    }

    public function login(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        $user = DB::table('users')
            ->where('email', $validated['email'])
            ->first();

        if (!$user || !Hash::check($validated['password'], $user->password)) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid credentials'
            ], 401);
        }

        if (!$user->is_active) {
            return response()->json([
                'success' => false,
                'message' => 'Account is disabled'
            ], 403);
        }

        $token = $this->createToken($user->email);

        return response()->json([
            'success' => true,
            'message' => 'Login successful',
            'data' => [
                'user' => [
                    'id' => $user->id,
                    'name' => $user->name,
                    'email' => $user->email,
                    'role' => $user->role,
                ],
                'token' => $token,
            ]
        ]);
    }

    public function logout(Request $request): JsonResponse
    {
        // Get the token and delete it
        $token = $request->bearerToken();
        
        if ($token) {
            $hashedToken = hash('sha256', $token);
            DB::table('personal_access_tokens')
                ->where('token', $hashedToken)
                ->delete();
        }
        
        return response()->json([
            'success' => true,
            'message' => 'Logged out successfully'
        ]);
    }

    public function me(Request $request): JsonResponse
    {
        $userId = $this->getAuthenticatedUserId($request);
        
        $user = DB::table('users')
            ->where('id', $userId)
            ->first();

        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'User not found'
            ], 404);
        }

        return response()->json([
            'success' => true,
            'data' => [
                'id' => $user->id,
                'name' => $user->name,
                'email' => $user->email,
                'role' => $user->role,
            ]
        ]);
    }

    private function createToken(string $email): string
    {
        $token = bin2hex(random_bytes(32));
        
        // Get user
        $user = DB::table('users')->where('email', $email)->first();
        
        if ($user) {
            // Store token in personal_access_tokens table
            DB::table('personal_access_tokens')->insert([
                'tokenable_type' => 'App\\Models\\User',
                'tokenable_id' => $user->id,
                'name' => 'API Token',
                'token' => hash('sha256', $token),
                'abilities' => '["*"]',
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
        
        return $token;
    }
    
    private function getAuthenticatedUserId(Request $request): int
    {
        // Check for authentication token in header
        $token = $request->bearerToken();
        
        if (!$token) {
            throw new \Illuminate\Validation\UnauthorizedException('Authentication required');
        }
        
        // Validate token and get user
        $tokenRecord = DB::table('personal_access_tokens')
            ->where('token', hash('sha256', $token))
            ->first();
        
        if (!$tokenRecord) {
            throw new \Illuminate\Validation\UnauthorizedException('Invalid or expired token');
        }
        
        return $tokenRecord->tokenable_id;
    }
}
