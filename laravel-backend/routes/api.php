<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\OrganizationController;
use App\Http\Controllers\Api\RepositoryController;
use App\Http\Controllers\Api\VulnerabilityController;
use App\Http\Controllers\Api\VulnerabilityScannerController;
use App\Http\Controllers\Api\SuperAdminController;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\ApiKeyController;
use App\Http\Controllers\Api\PlanController;
use App\Http\Controllers\Api\BillingController;
use App\Http\Controllers\Api\OAuthController;
use App\Http\Controllers\Api\DashboardController;
use App\Http\Controllers\Api\SettingsController;
use App\Http\Controllers\Api\MessageController;
use App\Http\Controllers\Api\NotificationController;
use App\Http\Controllers\Api\EmailQueueController;
use App\Http\Middleware\AuthenticateUser;

// Register middleware aliases
Route::aliasMiddleware('auth.user', AuthenticateUser::class);

// Auth Routes (public)
Route::prefix('auth')->group(function () {
    Route::post('/register', [AuthController::class, 'register']);
    Route::post('/login', [AuthController::class, 'login']);
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/me', [AuthController::class, 'me']);
    
    // GitHub OAuth
    Route::get('/github', [OAuthController::class, 'githubRedirect']);
    Route::get('/github/callback', [OAuthController::class, 'githubCallback']);
});

// Plans/Pricing (public)
Route::prefix('plans')->group(function () {
    Route::get('/', [PlanController::class, 'index']);
    Route::get('/{id}', [PlanController::class, 'show']);
});

// Billing & Subscription
Route::prefix('billing')->group(function () {
    Route::get('/subscription', [BillingController::class, 'getSubscription']);
    Route::post('/checkout', [BillingController::class, 'createCheckoutSession']);
    Route::post('/customer', [BillingController::class, 'createCustomer']);
    Route::post('/change-plan', [BillingController::class, 'changePlan']);
    Route::post('/cancel', [BillingController::class, 'cancelSubscription']);
    Route::get('/invoices', [BillingController::class, 'getInvoices']);
    Route::get('/payment-methods', [BillingController::class, 'getPaymentMethods']);
    Route::post('/payment-methods', [BillingController::class, 'addPaymentMethod']);
});

// Stripe Webhook
Route::post('/webhooks/stripe', [BillingController::class, 'webhook']);

// API Keys Management
Route::prefix('api-keys')->group(function () {
    Route::get('/', [ApiKeyController::class, 'index']);
    Route::post('/', [ApiKeyController::class, 'store']);
    Route::get('/{id}', [ApiKeyController::class, 'show']);
    Route::put('/{id}', [ApiKeyController::class, 'update']);
    Route::delete('/{id}', [ApiKeyController::class, 'destroy']);
    Route::post('/{id}/rotate', [ApiKeyController::class, 'rotate']);
    Route::get('/{id}/usage', [ApiKeyController::class, 'usage']);
});

Route::prefix('v1')->middleware(['throttle:60,1'])->group(function () {
    // Protected routes - require user authentication
    Route::middleware(['auth.user'])->group(function () {
        // Dashboard
        Route::get('/dashboard/stats', [DashboardController::class, 'stats']);
        Route::get('/dashboard/recent-scans', [DashboardController::class, 'recentScans']);
        Route::get('/dashboard/vulnerabilities', [DashboardController::class, 'vulnerabilities']);
        
        // Settings
        Route::get('/settings', [SettingsController::class, 'show']);
        Route::put('/settings', [SettingsController::class, 'update']);
        Route::post('/settings/password', [SettingsController::class, 'updatePassword']);
        Route::delete('/settings', [SettingsController::class, 'delete']);
        
        // Vulnerabilities
        Route::get('/vulnerabilities', [VulnerabilityController::class, 'index']);
        Route::get('/vulnerabilities/{id}', [VulnerabilityController::class, 'show']);
        Route::put('/vulnerabilities/{id}', [VulnerabilityController::class, 'update']);
        Route::delete('/vulnerabilities/{id}', [VulnerabilityController::class, 'destroy']);
        
        // Repositories
        Route::apiResource('repositories', RepositoryController::class);
        Route::post('repositories/{repository}/scan', [RepositoryController::class, 'scan']);
        Route::post('repositories/{repository}/refresh', [RepositoryController::class, 'refresh']);
        Route::get('repositories/{repository}/vulnerabilities', [RepositoryController::class, 'vulnerabilities']);
        
        // Messages
        Route::get('/messages', [MessageController::class, 'index']);
        Route::post('/messages', [MessageController::class, 'send']);
        Route::post('/messages/{id}/read', [MessageController::class, 'markAsRead']);
        Route::get('/messages/unread', [MessageController::class, 'unreadCount']);
        
        // Notifications
        Route::get('/notifications', [NotificationController::class, 'index']);
        Route::post('/notifications/{id}/read', [NotificationController::class, 'markAsRead']);
        Route::post('/notifications/read-all', [NotificationController::class, 'markAllAsRead']);
        Route::get('/notifications/unread', [NotificationController::class, 'unreadCount']);
        
        // Email Queue
        Route::get('/emails', [EmailQueueController::class, 'index']);
        Route::post('/emails/send', [EmailQueueController::class, 'send']);
        Route::post('/emails/send-bulk', [EmailQueueController::class, 'sendBulk']);
    });
    
    // Scanner routes - require user authentication
    Route::middleware(['auth.user'])->group(function () {
        Route::post('/vulnerabilities/scan-repository', [VulnerabilityScannerController::class, 'scanRepository']);
        Route::post('/vulnerabilities/scan-files', [VulnerabilityScannerController::class, 'scanFiles']);
        Route::get('/vulnerabilities/statistics', [VulnerabilityScannerController::class, 'statistics']);
    });
    
    // Organizations - require user authentication  
    Route::middleware(['auth.user'])->group(function () {
        Route::apiResource('organizations', OrganizationController::class);
    });
    
    // GitHub Integration - require user authentication
    Route::middleware(['auth.user'])->group(function () {
        Route::post('github/connect', [RepositoryController::class, 'connect']);
        Route::get('github/repositories', [RepositoryController::class, 'listGitHub']);
    });
    
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

// Super Admin Routes - Protected by auth and admin check
Route::prefix('v1/admin')->middleware(['auth:api'])->group(function () {
    Route::get('/dashboard', [SuperAdminController::class, 'dashboard']);
    Route::post('/system-scan', [SuperAdminController::class, 'runSystemScan']);
    Route::get('/audit-logs', [SuperAdminController::class, 'auditLogs']);
    Route::post('/users', [SuperAdminController::class, 'manageUsers']);
    Route::post('/generate-report', [SuperAdminController::class, 'generateReport']);
    Route::get('/stats', [SuperAdminController::class, 'stats']);
});
