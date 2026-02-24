<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Validator;

class AssetController extends Controller
{
    public function index(Request $request)
    {
        $user = $request->user();
        
        $assets = DB::table('registered_assets')
            ->where('user_id', $user->id)
            ->orderBy('created_at', 'desc')
            ->get();
            
        return response()->json([
            'success' => true,
            'data' => $assets
        ]);
    }
    
    public function store(Request $request)
    {
        $user = $request->user();
        
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'type' => 'required|in:web_application,api,network,container,enterprise_software',
            'url' => 'required|url|max:500',
            'description' => 'nullable|string|max:1000',
            'ownership_proof' => 'nullable|string|max:500',
        ]);
        
        // Check if asset already exists for this user
        $existing = DB::table('registered_assets')
            ->where('user_id', $user->id)
            ->where('url', $validated['url'])
            ->first();
            
        if ($existing) {
            return response()->json([
                'success' => false,
                'message' => 'This asset is already registered'
            ], 422);
        }
        
        $assetId = DB::table('registered_assets')->insertGetId([
            'user_id' => $user->id,
            'name' => $validated['name'],
            'type' => $validated['type'],
            'url' => $validated['url'],
            'description' => $validated['description'] ?? null,
            'ownership_proof' => $validated['ownership_proof'] ?? null,
            'verification_status' => 'pending',
            'status' => 'active',
            'created_at' => now(),
            'updated_at' => now(),
        ]);
        
        // Log the asset registration
        $this->logAuditEvent($user->id, 'asset_registered', $validated['url'], [
            'asset_id' => $assetId,
            'asset_name' => $validated['name'],
            'verification_status' => 'pending'
        ]);
        
        return response()->json([
            'success' => true,
            'message' => 'Asset registered successfully. Verification pending.',
            'data' => [
                'id' => $assetId,
                'verification_status' => 'pending'
            ]
        ], 201);
    }
    
    public function show(Request $request, $id)
    {
        $user = $request->user();
        
        $asset = DB::table('registered_assets')
            ->where('id', $id)
            ->where('user_id', $user->id)
            ->first();
            
        if (!$asset) {
            return response()->json([
                'success' => false,
                'message' => 'Asset not found'
            ], 404);
        }
        
        return response()->json([
            'success' => true,
            'data' => $asset
        ]);
    }
    
    public function update(Request $request, $id)
    {
        $user = $request->user();
        
        $asset = DB::table('registered_assets')
            ->where('id', $id)
            ->where('user_id', $user->id)
            ->first();
            
        if (!$asset) {
            return response()->json([
                'success' => false,
                'message' => 'Asset not found'
            ], 404);
        }
        
        $validated = $request->validate([
            'name' => 'sometimes|string|max:255',
            'description' => 'nullable|string|max:1000',
            'status' => 'sometimes|in:active,inactive,archived',
        ]);
        
        DB::table('registered_assets')
            ->where('id', $id)
            ->update([
                ...$validated,
                'updated_at' => now(),
            ]);
            
        return response()->json([
            'success' => true,
            'message' => 'Asset updated successfully'
        ]);
    }
    
    public function destroy(Request $request, $id)
    {
        $user = $request->user();
        
        $asset = DB::table('registered_assets')
            ->where('id', $id)
            ->where('user_id', $user->id)
            ->first();
            
        if (!$asset) {
            return response()->json([
                'success' => false,
                'message' => 'Asset not found'
            ], 404);
        }
        
        DB::table('registered_assets')
            ->where('id', $id)
            ->update([
                'status' => 'archived',
                'updated_at' => now(),
            ]);
            
        return response()->json([
            'success' => true,
            'message' => 'Asset archived successfully'
        ]);
    }
    
    public function verify(Request $request, $id)
    {
        $user = $request->user();
        
        $asset = DB::table('registered_assets')
            ->where('id', $id)
            ->where('user_id', $user->id)
            ->first();
            
        if (!$asset) {
            return response()->json([
                'success' => false,
                'message' => 'Asset not found'
            ], 404);
        }
        
        // Simple verification - in production this would check DNS, files, etc.
        $verificationMethod = $request->input('verification_method', 'dns');
        $verificationToken = $request->input('verification_token');
        
        // For demo purposes, accept any verification
        DB::table('registered_assets')
            ->where('id', $id)
            ->update([
                'verification_status' => 'verified',
                'verified_at' => now(),
                'verification_notes' => "Verified via {$verificationMethod}",
                'updated_at' => now(),
            ]);
            
        $this->logAuditEvent($user->id, 'asset_verified', $asset->url, [
            'asset_id' => $id,
            'verification_method' => $verificationMethod
        ]);
        
        return response()->json([
            'success' => true,
            'message' => 'Asset verified successfully'
        ]);
    }
    
    public function authorizeScan(Request $request)
    {
        $user = $request->user();
        
        $validated = $request->validate([
            'target_url' => 'required|url|max:500',
            'authorization_type' => 'required|in:ownership_verified,scope_declared,legal_approval',
            'authorization_proof' => 'nullable|string|max:1000',
            'legal_contact_name' => 'nullable|string|max:255',
            'legal_contact_email' => 'nullable|email|max:255',
        ]);
        
        // Check if asset is registered and verified
        $asset = DB::table('registered_assets')
            ->where('url', $validated['target_url'])
            ->where('user_id', $user->id)
            ->where('verification_status', 'verified')
            ->where('status', 'active')
            ->first();
            
        $authorizationStatus = $asset ? 'authorized' : 'not_registered';
        
        // Log authorization
        $logId = DB::table('scan_authorization_logs')->insertGetId([
            'user_id' => $user->id,
            'asset_id' => $asset->id ?? null,
            'target_url' => $validated['target_url'],
            'authorization_type' => $validated['authorization_type'],
            'authorization_proof' => $validated['authorization_proof'] ?? null,
            'legal_contact_name' => $validated['legal_contact_name'] ?? null,
            'legal_contact_email' => $validated['legal_contact_email'] ?? null,
            'consent_status' => 'granted',
            'consent_timestamp' => now(),
            'ip_address' => $request->ip(),
            'user_agent' => $request->userAgent(),
            'created_at' => now(),
            'updated_at' => now(),
        ]);
        
        $this->logAuditEvent($user->id, 'scan_authorized', $validated['target_url'], [
            'authorization_log_id' => $logId,
            'authorization_type' => $validated['authorization_type'],
            'asset_registered' => $asset ? true : false,
            'asset_verified' => $asset ? true : false,
        ]);
        
        return response()->json([
            'success' => true,
            'data' => [
                'authorization_id' => $logId,
                'authorized' => $asset !== null,
                'reason' => $asset ? 'Asset verified and authorized' : 'Asset not registered or not verified',
                'requires_registration' => $asset === null
            ]
        ]);
    }
    
    public function getAuditLogs(Request $request)
    {
        $user = $request->user();
        
        $logs = DB::table('pentest_audit_logs')
            ->where('user_id', $user->id)
            ->orderBy('created_at', 'desc')
            ->limit(100)
            ->get();
            
        return response()->json([
            'success' => true,
            'data' => $logs
        ]);
    }
    
    private function logAuditEvent($userId, $action, $targetUrl, $details = [])
    {
        DB::table('pentest_audit_logs')->insert([
            'user_id' => $userId,
            'scan_id' => null,
            'target_url' => $targetUrl,
            'target_type' => 'asset_management',
            'action' => $action,
            'details' => json_encode($details),
            'authorization_status' => 'authorized',
            'started_at' => now(),
            'completed_at' => now(),
            'created_at' => now(),
            'updated_at' => now(),
        ]);
    }
}
