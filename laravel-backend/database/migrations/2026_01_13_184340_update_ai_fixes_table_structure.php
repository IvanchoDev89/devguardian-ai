<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        try {
            Schema::table('ai_fixes', function (Blueprint $table) {
                // Drop existing foreign keys if they exist
                try {
                    $table->dropForeign(['vulnerability_id']);
                } catch (\Exception $e) {
                    // Foreign key doesn't exist, continue
                }
                
                try {
                    $table->dropForeign(['repository_id']);
                } catch (\Exception $e) {
                    // Foreign key doesn't exist, continue
                }
                
                // Add new columns
                $table->longText('fixed_code')->nullable();
                $table->text('explanation')->nullable();
                $table->json('recommendations')->nullable();
                
                // Make repository_id nullable
                $table->uuid('repository_id')->nullable()->change();
                
                // Re-add foreign keys
                $table->foreign('vulnerability_id')->references('id')->on('vulnerabilities')->onDelete('cascade');
                $table->foreign('repository_id')->references('id')->on('repositories')->onDelete('cascade');
            });
        } catch (\Exception $e) {
            // Log error but don't fail the migration
            \Log::error('Migration failed: ' . $e->getMessage());
            throw $e;
        }
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        try {
            Schema::table('ai_fixes', function (Blueprint $table) {
                // Drop foreign keys if they exist
                try {
                    $table->dropForeign(['vulnerability_id']);
                } catch (\Exception $e) {
                    // Foreign key doesn't exist, continue
                }
                
                try {
                    $table->dropForeign(['repository_id']);
                } catch (\Exception $e) {
                    // Foreign key doesn't exist, continue
                }
                
                // Drop new columns
                $table->dropColumn(['fixed_code', 'explanation', 'recommendations']);
                
                // Make repository_id not nullable
                $table->uuid('repository_id')->nullable(false)->change();
                
                // Re-add foreign keys
                $table->foreign('vulnerability_id')->references('id')->on('vulnerabilities')->onDelete('cascade');
                $table->foreign('repository_id')->references('id')->on('repositories')->onDelete('cascade');
            });
        } catch (\Exception $e) {
            // Log error but don't fail the migration
            \Log::error('Migration rollback failed: ' . $e->getMessage());
            throw $e;
        }
    }
};
