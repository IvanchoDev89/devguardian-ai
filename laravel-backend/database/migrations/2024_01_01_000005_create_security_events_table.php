<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('security_events', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->uuid('organization_id');
            $table->uuid('repository_id')->nullable();
            $table->uuid('vulnerability_id')->nullable();
            $table->string('event_type', 100);
            $table->json('event_data')->nullable();
            $table->string('severity', 20)->nullable();
            $table->timestamp('timestamp');
            $table->json('metadata')->nullable();
            $table->timestamps();
            
            $table->index(['organization_id']);
            $table->index(['repository_id']);
            $table->index(['vulnerability_id']);
            $table->index(['event_type']);
            $table->index(['timestamp']);
            $table->index(['severity']);
        });
        
        // Add foreign key constraints only if using PostgreSQL
        if (config('database.default') === 'pgsql') {
            DB::statement('ALTER TABLE security_events ADD CONSTRAINT fk_security_events_organization_id FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE CASCADE');
            DB::statement('ALTER TABLE security_events ADD CONSTRAINT fk_security_events_repository_id FOREIGN KEY (repository_id) REFERENCES repositories (id) ON DELETE CASCADE');
            DB::statement('ALTER TABLE security_events ADD CONSTRAINT fk_security_events_vulnerability_id FOREIGN KEY (vulnerability_id) REFERENCES vulnerabilities (id) ON DELETE CASCADE');
            
            // Convert to TimescaleDB hypertable if TimescaleDB extension is available
            try {
                DB::statement("SELECT create_hypertable('security_events', 'timestamp', chunk_time_interval => INTERVAL '1 day')");
            } catch (\Exception $e) {
                // TimescaleDB not available, continue with regular table
            }
        }
    }

    public function down(): void
    {
        Schema::dropIfExists('security_events');
    }
};
