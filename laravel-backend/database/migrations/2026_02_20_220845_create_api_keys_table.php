<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('api_keys', function (Blueprint $table) {
            $table->id();
            $table->uuid('key_id')->unique();
            $table->string('key_hash')->unique();
            $table->string('name');
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('plan')->default('free');
            $table->integer('monthly_scans_limit')->default(100);
            $table->integer('scans_used_this_month')->default(0);
            $table->timestamp('last_used_at')->nullable();
            $table->boolean('is_active')->default(true);
            $table->timestamps();
            
            $table->index(['user_id', 'is_active']);
            $table->index(['key_hash']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('api_keys');
    }
};
