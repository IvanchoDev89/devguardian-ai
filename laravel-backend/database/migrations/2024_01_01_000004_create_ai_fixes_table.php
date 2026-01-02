<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('ai_fixes', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->uuid('vulnerability_id');
            $table->uuid('repository_id');
            $table->text('diff_content');
            $table->decimal('confidence_score', 3, 2);
            $table->enum('status', ['generated', 'validating', 'validated', 'failed', 'applied'])->default('generated');
            $table->jsonb('validation_results')->nullable();
            $table->text('error_message')->nullable();
            $table->integer('retry_count')->default(0);
            $table->text('test_results')->nullable();
            $table->jsonb('metadata')->nullable();
            $table->timestamps();
            
            $table->foreign('vulnerability_id')->references('id')->on('vulnerabilities')->onDelete('cascade');
            $table->foreign('repository_id')->references('id')->on('repositories')->onDelete('cascade');
            $table->index(['vulnerability_id', 'status']);
            $table->index(['confidence_score']);
            $table->index(['created_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('ai_fixes');
    }
};
