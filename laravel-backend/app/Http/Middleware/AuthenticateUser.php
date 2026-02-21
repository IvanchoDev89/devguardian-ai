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

        // Decode the token (simple base64 encoded format from AuthController)
        try {
            $decoded = base64_decode($token);
            if (!$decoded) {
                return response()->json([
                    'success' => false,
                    'message' => 'Invalid token'
                ], 401);
            }
            
            $parts = explode(':', $decoded);
            if (count($parts) < 2) {
                return response()->json([
                    'success' => false,
                    'message' => 'Invalid token format'
                ], 401);
            }

            $email = $parts[0];
            
            // Find user by email
            $user = \Illuminate\Support\Facades\DB::table('users')
                ->where('email', $email)
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

            // Set user on request
            $request->setUserResolver(function () use ($user) {
                return $user;
            });

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid token: ' . $e->getMessage()
            ], 401);
        }

        return $next($request);
    }
}
