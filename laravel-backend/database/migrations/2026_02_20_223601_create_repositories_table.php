<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        if (!Schema::hasTable('scan_jobs')) {
            Schema::create('scan_jobs', function (Blueprint $table) {
                $table->uuid('id')->primary();
                $table->foreignId('user_id')->constrained()->onDelete('cascade');
                $table->foreignId('repository_id')->nullable()->constrained()->onDelete('set null');
                $table->string('scan_type');
                $table->string('status')->default('pending');
                $table->json('config')->nullable();
                $table->json('results')->nullable();
                $table->timestamp('started_at')->nullable();
                $table->timestamp('completed_at')->nullable();
                $table->timestamps();
                
                $table->index(['user_id', 'status']);
                $table->index(['repository_id', 'status']);
            });
        }
    }

    public function down(): void
    {
        Schema::dropIfExists('scan_jobs');
    }
};
