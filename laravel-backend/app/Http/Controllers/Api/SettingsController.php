<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

class SettingsController extends Controller
{
    public function show(Request $request)
    {
        $user = $request->user();
        
        return response()->json([
            'success' => true,
            'data' => [
                'name' => $user->name,
                'email' => $user->email,
                'avatar' => $user->avatar,
                'two_factor_enabled' => !empty($user->two_factor_secret),
                'notifications' => $user->preferences['notifications'] ?? [
                    'email_vulnerabilities' => true,
                    'email_scans' => true,
                    'email_marketing' => false
                ],
                'security' => $user->preferences['security'] ?? [
                    'session_timeout' => 30,
                    'require_2fa' => false
                ]
            ]
        ]);
    }
    
    public function update(Request $request)
    {
        $user = $request->user();
        
        $validated = $request->validate([
            'name' => 'sometimes|string|max:255',
            'email' => 'sometimes|email|unique:users,email,' . $user->id,
            'avatar' => 'sometimes|string|nullable',
            'notifications' => 'sometimes|array',
            'security' => 'sometimes|array'
        ]);
        
        $preferences = $user->preferences ?? [];
        
        if (isset($validated['notifications'])) {
            $preferences['notifications'] = $validated['notifications'];
        }
        
        if (isset($validated['security'])) {
            $preferences['security'] = $validated['security'];
        }
        
        DB::table('users')
            ->where('id', $user->id)
            ->update([
                'name' => $validated['name'] ?? $user->name,
                'email' => $validated['email'] ?? $user->email,
                'avatar' => $validated['avatar'] ?? $user->avatar,
                'preferences' => json_encode($preferences),
                'updated_at' => now()
            ]);
        
        return response()->json([
            'success' => true,
            'message' => 'Settings updated successfully'
        ]);
    }
    
    public function updatePassword(Request $request)
    {
        $user = $request->user();
        
        $validated = $request->validate([
            'current_password' => 'required|string',
            'new_password' => 'required|string|min:8|confirmed'
        ]);
        
        if (!Hash::check($validated['current_password'], $user->password)) {
            return response()->json([
                'success' => false,
                'message' => 'Current password is incorrect'
            ], 422);
        }
        
        DB::table('users')
            ->where('id', $user->id)
            ->update([
                'password' => Hash::make($validated['new_password']),
                'updated_at' => now()
            ]);
        
        return response()->json([
            'success' => true,
            'message' => 'Password updated successfully'
        ]);
    }
    
    public function delete(Request $request)
    {
        $user = $request->user();
        
        DB::table('users')->where('id', $user->id)->delete();
        
        return response()->json([
            'success' => true,
            'message' => 'Account deleted successfully'
        ]);
    }
}
