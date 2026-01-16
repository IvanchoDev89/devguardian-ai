<?php

use Illuminate\Support\Facades\Route;

// Vulnerability Management Web Routes
Route::prefix('vulnerabilities')->name('vulnerabilities.')->group(function () {
    Route::get('/scanner', [App\Http\Controllers\Api\VulnerabilityScannerController::class, 'scanner'])
        ->name('scanner');
});
