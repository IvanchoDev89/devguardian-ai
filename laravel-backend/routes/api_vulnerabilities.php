<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Http\Request;
use App\Http\Controllers\Api\VulnerabilityScannerController;
use App\Http\Controllers\Api\VulnerabilityController;

// Vulnerability Management Routes
Route::prefix('vulnerabilities')->name('vulnerabilities.')->group(function () {
    // Scanner routes
    Route::post('/scan-repository', [VulnerabilityScannerController::class, 'scanRepository'])
        ->name('scan.repository');
    
    Route::post('/scan-files', [VulnerabilityScannerController::class, 'scanFiles'])
        ->name('scan.files');
    
    // Semgrep routes
    Route::post('/scan-semgrep', [VulnerabilityScannerController::class, 'scanWithSemgrep'])
        ->name('scan.semgrep');
    
    Route::post('/analyze-finding', [VulnerabilityScannerController::class, 'analyzeFindingWithClaude'])
        ->name('analyze-finding');
    
    // Management routes
    Route::get('/', [VulnerabilityController::class, 'index'])
        ->name('index');
    
    Route::get('/{id}', [VulnerabilityController::class, 'show'])
        ->name('show');
    
    Route::get('/statistics', [VulnerabilityScannerController::class, 'statistics'])
        ->name('statistics');
    
    // Fix management routes
    Route::post('/{id}/generate-fix', [VulnerabilityScannerController::class, 'generateFix'])
        ->name('generate-fix');
    
    Route::post('/{id}/apply-fix', [VulnerabilityScannerController::class, 'applyFix'])
        ->name('apply-fix');
    
    Route::get('/{id}/fixes', [VulnerabilityController::class, 'fixes'])
        ->name('fixes');
    
    Route::patch('/{id}/status', [VulnerabilityController::class, 'updateStatus'])
        ->name('update-status');
});

// AI Service Integration Routes
Route::prefix('ai')->name('ai.')->group(function () {
    Route::post('/scan-code', function () {
        // Forward to AI service for code scanning
        $response = \Illuminate\Support\Facades\Http::post(
            config('services.ai_service.url') . '/api/security/scan',
            request()->all()
        );
        
        return response()->json($response->json());
    })->name('scan-code');
    
    Route::post('/generate-fix', function () {
        // Forward to AI service for fix generation
        $response = \Illuminate\Support\Facades\Http::post(
            config('services.ai_service.url') . '/api/ai-fix/generate-fix',
            request()->all()
        );
        
        return response()->json($response->json());
    })->name('generate-fix');
    
    // Semgrep Integration Routes
    Route::post('/semgrep/scan', function (Request $request) {
        $validated = $request->validate([
            'repository_url' => 'required|url',
            'branch' => 'nullable|string',
            'github_token' => 'nullable|string',
            'rules' => 'nullable|string',
            'analyze_false_positives' => 'nullable|boolean'
        ]);
        
        $response = \Illuminate\Support\Facades\Http::timeout(600)->post(
            config('services.ai_service.url') . '/api/semgrep/scan',
            $validated
        );
        
        if (!$response->successful()) {
            return response()->json([
                'error' => 'Semgrep scan failed',
                'message' => $response->body()
            ], $response->status());
        }
        
        return response()->json($response->json());
    })->name('semgrep.scan');
    
    Route::post('/semgrep/analyze-finding', function (Request $request) {
        $validated = $request->validate([
            'code_snippet' => 'required|string',
            'finding_type' => 'required|string',
            'file_path' => 'required|string',
            'line_number' => 'required|integer'
        ]);
        
        $response = \Illuminate\Support\Facades\Http::timeout(60)->post(
            config('services.ai_service.url') . '/api/semgrep/analyze-finding',
            $validated
        );
        
        if (!$response->successful()) {
            return response()->json([
                'error' => 'Analysis failed',
                'message' => $response->body()
            ], $response->status());
        }
        
        return response()->json($response->json());
    })->name('semgrep.analyze');
});
