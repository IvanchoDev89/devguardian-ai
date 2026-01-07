<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            // Add new columns if they don't exist
            if (!Schema::hasColumn('users', 'organization_id')) {
                $table->uuid('organization_id')->nullable()->after('id');
            }
            if (!Schema::hasColumn('users', 'role')) {
                $table->enum('role', ['admin', 'member', 'viewer'])->default('member')->after('password');
            }
            if (!Schema::hasColumn('users', 'is_active')) {
                $table->boolean('is_active')->default(true)->after('role');
            }
            if (!Schema::hasColumn('users', 'preferences')) {
                $table->json('preferences')->nullable()->after('is_active');
            }
            
            // Add indexes (SQLite will ignore if they already exist)
            $table->index(['organization_id', 'role']);
            $table->index(['email']);
        });
        
        // Add foreign key only for PostgreSQL
        if (config('database.default') === 'pgsql') {
            Schema::table('users', function (Blueprint $table) {
                $table->foreign('organization_id')->references('id')->on('organizations')->onDelete('set null');
            });
        }
    }

    public function down(): void
    {
        Schema::dropIfExists('users');
    }
};
