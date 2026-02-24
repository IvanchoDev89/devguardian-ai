<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    public function up(): void
    {
        // SQLite doesn't support modifying enum, so we need to recreate the table
        // For simplicity, we'll just change the column to string
        DB::statement("ALTER TABLE users RENAME TO users_old");
        DB::statement("CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            email_verified_at TIMESTAMP NULL,
            password VARCHAR(255) NOT NULL,
            organization_id VARCHAR(36) NULL,
            role VARCHAR(50) DEFAULT 'member',
            is_active BOOLEAN DEFAULT 1,
            preferences JSON NULL,
            remember_token VARCHAR(100) NULL,
            created_at TIMESTAMP NULL,
            updated_at TIMESTAMP NULL
        )");
        
        // Copy data from old table
        DB::statement("INSERT INTO users (id, name, email, email_verified_at, password, organization_id, role, is_active, preferences, remember_token, created_at, updated_at)
            SELECT id, name, email, email_verified_at, password, organization_id, role, is_active, preferences, remember_token, created_at, updated_at
            FROM users_old");
        
        DB::statement("DROP TABLE users_old");
    }

    public function down(): void
    {
        // Reverse the process
        DB::statement("ALTER TABLE users RENAME TO users_old");
        DB::statement("CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            email_verified_at TIMESTAMP NULL,
            password VARCHAR(255) NOT NULL,
            organization_id VARCHAR(36) NULL,
            role VARCHAR(50) DEFAULT 'member',
            is_active BOOLEAN DEFAULT 1,
            preferences JSON NULL,
            remember_token VARCHAR(100) NULL,
            created_at TIMESTAMP NULL,
            updated_at TIMESTAMP NULL
        )");
        
        DB::statement("INSERT INTO users (id, name, email, email_verified_at, password, organization_id, role, is_active, preferences, remember_token, created_at, updated_at)
            SELECT id, name, email, email_verified_at, password, organization_id, 
            CASE WHEN role = 'super_admin' THEN 'admin' ELSE role END,
            is_active, preferences, remember_token, created_at, updated_at
            FROM users_old");
        
        DB::statement("DROP TABLE users_old");
    }
};
