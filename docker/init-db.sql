-- Initialize TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create database user with proper permissions (skip if exists)
-- Note: Password will be set via environment variable
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'devguardian') THEN
      CREATE USER devguardian WITH PASSWORD '';
   END IF;
END
$$;

-- Grant privileges (ignore if already granted)
GRANT ALL PRIVILEGES ON DATABASE devguardian TO devguardian;

-- Set up proper permissions for TimescaleDB
GRANT ALL ON SCHEMA public TO devguardian;
