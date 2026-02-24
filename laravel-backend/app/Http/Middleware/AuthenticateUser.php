<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class AuthenticateUser
{
    public function handle(Request $request, Closure $next): Response
    {
        $token = $request->bearerToken();
        
        // Also check Authorization header without Bearer prefix
        if (!$token) {
            $authHeader = $request->header('Authorization');
            if ($authHeader && str_starts_with($authHeader, 'Bearer ')) {
                $token = substr($authHeader, 7);
            }
        }

        if (!$token) {
            return response()->json([
                'success' => false,
                'message' => 'Authentication required'
            ], 401);
        }

        // Try to find user by token in personal_access_tokens table
        $hashedToken = hash('sha256', $token);
        $tokenRecord = \Illuminate\Support\Facades\DB::table('personal_access_tokens')
            ->where('token', $hashedToken)
            ->first();

        if ($tokenRecord) {
            $user = \Illuminate\Support\Facades\DB::table('users')
                ->where('id', $tokenRecord->tokenable_id)
                ->first();

            if (!$user) {
                return response()->json([
                    'success' => false,
                    'message' => 'User not found'
                ], 401);
            }

            if (!$user->is_active) {
                return response()->json([
                    'success' => false,
                    'message' => 'Account is disabled'
                ], 403);
            }

            $request->setUserResolver(function () use ($user) {
                return $user;
            });

            return $next($request);
        }

        // Fallback: Try to decode old format tokens (base64 encoded email:timestamp:random)
        try {
            $decoded = base64_decode($token);
            if ($decoded) {
                $parts = explode(':', $decoded);
                if (count($parts) >= 2) {
                    $email = $parts[0];
                    
                    $user = \Illuminate\Support\Facades\DB::table('users')
                        ->where('email', $email)
                        ->first();

                    if ($user && $user->is_active) {
                        $request->setUserResolver(function () use ($user) {
                            return $user;
                        });

                        return $next($request);
                    }
                }
            }
        } catch (\Exception $e) {
            // Token decode failed
        }

        return response()->json([
            'success' => false,
            'message' => 'Invalid or expired token'
        ], 401);
    }
}
