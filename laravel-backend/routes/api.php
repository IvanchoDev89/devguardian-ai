<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\OrganizationController;
use App\Http\Controllers\Api\RepositoryController;
use App\Http\Controllers\Api\VulnerabilityController;
use App\Http\Controllers\Api\VulnerabilityScannerController;
use App\Http\Controllers\Api\SuperAdminController;

Route::prefix('v1')->middleware(['throttle:60,1'])->group(function () {
    // Organizations
    Route::apiResource('organizations', OrganizationController::class);
    
    // Repositories
    Route::apiResource('repositories', RepositoryController::class);
    Route::post('repositories/{repository}/scan', [RepositoryController::class, 'scan']);
    Route::get('repositories/{repository}/vulnerabilities', [RepositoryController::class, 'vulnerabilities']);
    
    // Vulnerabilities - Enhanced scanner routes
    Route::prefix('vulnerabilities')->name('vulnerabilities.')->group(function () {
        // Scanner routes
        Route::post('/scan-repository', [VulnerabilityScannerController::class, 'scanRepository'])
            ->name('scan.repository');
        
        Route::post('/scan-files', [VulnerabilityScannerController::class, 'scanFiles'])
            ->name('scan.files');
        
        // Management routes
        Route::get('/', [VulnerabilityController::class, 'index'])
            ->name('index');
        
        Route::get('/statistics', [VulnerabilityScannerController::class, 'statistics'])
            ->name('statistics');
        
        Route::get('/{id}', [VulnerabilityController::class, 'show'])
            ->name('show');
        
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
    });
});

// Super Admin Routes - Public for development
Route::prefix('v1/admin')->group(function () {
    Route::get('/dashboard', [SuperAdminController::class, 'dashboard']);
    Route::post('/system-scan', [SuperAdminController::class, 'runSystemScan']);
    Route::get('/audit-logs', [SuperAdminController::class, 'auditLogs']);
    Route::post('/users', [SuperAdminController::class, 'manageUsers']);
    Route::post('/generate-report', [SuperAdminController::class, 'generateReport']);
    Route::get('/stats', [SuperAdminController::class, 'stats']);
});
