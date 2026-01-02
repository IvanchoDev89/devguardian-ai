<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    public function up(): void
    {
        // Create TimescaleDB hypertable for security events
        DB::statement("
            CREATE TABLE security_events (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                organization_id UUID NOT NULL,
                repository_id UUID,
                vulnerability_id UUID,
                event_type VARCHAR(100) NOT NULL,
                event_data JSONB,
                severity VARCHAR(20),
                timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                metadata JSONB,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            )
        ");
        
        // Create indexes
        DB::statement('CREATE INDEX idx_security_events_organization_id ON security_events (organization_id)');
        DB::statement('CREATE INDEX idx_security_events_repository_id ON security_events (repository_id)');
        DB::statement('CREATE INDEX idx_security_events_vulnerability_id ON security_events (vulnerability_id)');
        DB::statement('CREATE INDEX idx_security_events_type ON security_events (event_type)');
        DB::statement('CREATE INDEX idx_security_events_timestamp ON security_events (timestamp)');
        DB::statement('CREATE INDEX idx_security_events_severity ON security_events (severity)');
        
        // Convert to TimescaleDB hypertable
        DB::statement("SELECT create_hypertable('security_events', 'timestamp', chunk_time_interval => INTERVAL '1 day')");
        
        // Create foreign key constraints
        DB::statement('ALTER TABLE security_events ADD CONSTRAINT fk_security_events_organization_id FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE CASCADE');
        DB::statement('ALTER TABLE security_events ADD CONSTRAINT fk_security_events_repository_id FOREIGN KEY (repository_id) REFERENCES repositories (id) ON DELETE CASCADE');
        DB::statement('ALTER TABLE security_events ADD CONSTRAINT fk_security_events_vulnerability_id FOREIGN KEY (vulnerability_id) REFERENCES vulnerabilities (id) ON DELETE CASCADE');
    }

    public function down(): void
    {
        Schema::dropIfExists('security_events');
    }
};
