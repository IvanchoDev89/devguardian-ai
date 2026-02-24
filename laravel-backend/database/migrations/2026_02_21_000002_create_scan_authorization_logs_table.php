<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('scan_authorization_logs', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('user_id');
            $table->unsignedBigInteger('asset_id')->nullable();
            $table->string('target_url');
            $table->string('authorization_type'); // ownership_verified, scope_declared, legal_approval
            $table->text('authorization_proof')->nullable(); // Legal document reference, etc.
            $table->string('legal_contact_name')->nullable();
            $table->string('legal_contact_email')->nullable();
            $table->enum('consent_status', ['granted', 'denied', 'pending'])->default('granted');
            $table->timestamp('consent_timestamp')->nullable();
            $table->string('ip_address')->nullable();
            $table->string('user_agent')->nullable();
            $table->timestamps();
            
            $table->foreign('user_id')->references('id')->on('users')->onDelete('cascade');
            $table->foreign('asset_id')->references('id')->on('registered_assets')->onDelete('set null');
            $table->index('user_id');
            $table->index('target_url');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('scan_authorization_logs');
    }
};
