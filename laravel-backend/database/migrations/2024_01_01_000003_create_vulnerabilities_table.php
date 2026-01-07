<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('vulnerabilities', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->uuid('repository_id');
            $table->string('cve_id', 50)->nullable();
            $table->string('identifier', 255);
            $table->string('title', 500);
            $table->text('description');
            $table->string('severity', 20);
            $table->decimal('cvss_score', 3, 1)->nullable();
            $table->string('cvss_vector', 200)->nullable();
            $table->jsonb('location');
            $table->enum('status', ['detected', 'analyzing', 'fixing', 'fixed', 'ignored', 'false_positive'])->default('detected');
            $table->jsonb('metadata')->nullable();
            $table->timestamp('detected_at');
            $table->timestamp('fixed_at')->nullable();
            $table->timestamps();
            
            $table->foreign('repository_id')->references('id')->on('repositories')->onDelete('cascade');
            $table->index(['repository_id', 'status']);
            $table->index(['severity']);
            $table->index(['cvss_score']);
            $table->index(['detected_at']);
        });
        
        // Create partitioned table function for monthly partitions (PostgreSQL only)
        if (config('database.default') === 'pgsql') {
            DB::statement('CREATE TABLE IF NOT EXISTS vulnerabilities_partitioned (LIKE public.vulnerabilities INCLUDING ALL)');
            DB::statement('ALTER TABLE vulnerabilities_partitioned ADD COLUMN IF NOT EXISTS partition_month DATE GENERATED ALWAYS AS (date_trunc(\'month\', created_at)) STORED');
            DB::statement('ALTER TABLE vulnerabilities_partitioned PARTITION BY RANGE (partition_month)');
        }
    }

    public function down(): void
    {
        Schema::dropIfExists('vulnerabilities');
    }
};
