<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('vulnerabilities', function (Blueprint $table) {
            $table->string('source', 50)->default('manual')->after('repository_id');
            $table->string('rule_id', 255)->nullable()->after('source');
            $table->decimal('confidence_score', 3, 2)->nullable()->after('rule_id');
            $table->text('fix_suggestion')->nullable()->after('confidence_score');
            $table->boolean('is_false_positive')->default(false)->after('fix_suggestion');
            $table->text('false_positive_reason')->nullable()->after('is_false_positive');
            $table->string('scan_id', 64)->nullable()->after('false_positive_reason');
            
            $table->index('source');
            $table->index('scan_id');
        });
    }

    public function down(): void
    {
        Schema::table('vulnerabilities', function (Blueprint $table) {
            $table->dropIndex(['source']);
            $table->dropIndex(['scan_id']);
            $table->dropColumn([
                'source',
                'rule_id', 
                'confidence_score',
                'fix_suggestion',
                'is_false_positive',
                'false_positive_reason',
                'scan_id'
            ]);
        });
    }
};
