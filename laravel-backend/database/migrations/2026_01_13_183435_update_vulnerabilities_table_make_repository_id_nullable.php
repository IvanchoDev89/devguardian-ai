<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::table('vulnerabilities', function (Blueprint $table) {
            $table->dropForeign(['repository_id']);
            $table->uuid('repository_id')->nullable()->change();
            $table->foreign('repository_id')->references('id')->on('repositories')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('vulnerabilities', function (Blueprint $table) {
            $table->dropForeign(['repository_id']);
            $table->uuid('repository_id')->nullable(false)->change();
            $table->foreign('repository_id')->references('id')->on('repositories')->onDelete('cascade');
        });
    }
};
