-- Initialize TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create database user with proper permissions
CREATE USER devguardian WITH PASSWORD 'devguardian_password';
GRANT ALL PRIVILEGES ON DATABASE devguardian TO devguardian;

-- Set up proper permissions for TimescaleDB
GRANT ALL ON SCHEMA public TO devguardian;
