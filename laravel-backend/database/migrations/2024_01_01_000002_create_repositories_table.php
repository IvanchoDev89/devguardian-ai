<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('repositories', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->uuid('organization_id');
            $table->string('name', 255);
            $table->string('full_name', 255);
            $table->enum('provider', ['github', 'gitlab', 'bitbucket']);
            $table->string('external_id', 255);
            $table->string('url', 2048);
            $table->string('branch', 255)->default('main');
            $table->enum('status', ['active', 'inactive', 'archived'])->default('active');
            $table->jsonb('scan_config')->nullable();
            $table->jsonb('provider_config')->nullable();
            $table->timestamp('last_scanned_at')->nullable();
            $table->timestamps();
            
            $table->foreign('organization_id')->references('id')->on('organizations')->onDelete('cascade');
            $table->unique(['provider', 'external_id']);
            $table->index(['organization_id', 'status']);
            $table->index(['last_scanned_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('repositories');
    }
};
