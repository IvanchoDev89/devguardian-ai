<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('organizations', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->string('name', 255);
            $table->string('slug', 255)->unique();
            $table->enum('billing_tier', ['free', 'starter', 'pro', 'enterprise'])->default('free');
            $table->jsonb('settings')->nullable();
            $table->string('encryption_key')->nullable();
            $table->timestamp('trial_ends_at')->nullable();
            $table->timestamps();
            
            $table->index(['billing_tier']);
            $table->index(['trial_ends_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('organizations');
    }
};
