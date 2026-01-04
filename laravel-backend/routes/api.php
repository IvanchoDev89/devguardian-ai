<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\OrganizationController;
use App\Http\Controllers\Api\RepositoryController;
use App\Http\Controllers\Api\VulnerabilityController;

Route::prefix('v1')->group(function () {
    // Organizations
    Route::apiResource('organizations', OrganizationController::class);
    
    // Repositories
    Route::apiResource('repositories', RepositoryController::class);
    Route::post('repositories/{repository}/scan', [RepositoryController::class, 'scan']);
    Route::get('repositories/{repository}/vulnerabilities', [RepositoryController::class, 'vulnerabilities']);
    
    // Vulnerabilities
    Route::apiResource('vulnerabilities', VulnerabilityController::class)->only(['index', 'show']);
    Route::post('vulnerabilities/{vulnerability}/generate-fix', [VulnerabilityController::class, 'generateFix']);
    Route::get('vulnerabilities/{vulnerability}/fixes', [VulnerabilityController::class, 'fixes']);
    Route::patch('vulnerabilities/{vulnerability}/status', [VulnerabilityController::class, 'updateStatus']);
});
