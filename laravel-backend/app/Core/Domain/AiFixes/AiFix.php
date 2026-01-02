<?php

declare(strict_types=1);

namespace App\Core\Domain\AiFixes;

use App\Core\Domain\Repositories\Repository;
use App\Core\Domain\Vulnerabilities\Vulnerability;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

enum AiFixStatus: string
{
    case GENERATED = 'generated';
    case VALIDATING = 'validating';
    case VALIDATED = 'validated';
    case FAILED = 'failed';
    case APPLIED = 'applied';
}

final class AiFix extends Model
{
    use HasFactory;

    protected $fillable = [
        'vulnerability_id',
        'repository_id',
        'diff_content',
        'confidence_score',
        'status',
        'validation_results',
        'error_message',
        'retry_count',
        'test_results'
    ];

    protected $casts = [
        'id' => 'string',
        'vulnerability_id' => 'string',
        'repository_id' => 'string',
        'confidence_score' => 'decimal:2',
        'status' => AiFixStatus::class,
        'validation_results' => 'array',
        'test_results' => 'array'
    ];

    public function vulnerability(): BelongsTo
    {
        return $this->belongsTo(Vulnerability::class);
    }

    public function repository(): BelongsTo
    {
        return $this->belongsTo(Repository::class);
    }

    public function isHighConfidence(): bool
    {
        return $this->confidence_score >= 0.8;
    }

    public function isMediumConfidence(): bool
    {
        return $this->confidence_score >= 0.6 && $this->confidence_score < 0.8;
    }

    public function isLowConfidence(): bool
    {
        return $this->confidence_score < 0.6;
    }

    public function isSuccessful(): bool
    {
        return in_array($this->status, [AiFixStatus::VALIDATED, AiFixStatus::APPLIED]);
    }

    public function hasFailed(): bool
    {
        return $this->status === AiFixStatus::FAILED;
    }

    public function canRetry(): bool
    {
        return $this->hasFailed() && $this->retry_count < 3;
    }

    public function markAsValidating(): void
    {
        $this->status = AiFixStatus::VALIDATING;
        $this->save();
    }

    public function markAsValidated(array $validationResults = []): void
    {
        $this->status = AiFixStatus::VALIDATED;
        $this->validation_results = $validationResults;
        $this->save();
    }

    public function markAsFailed(string $errorMessage): void
    {
        $this->status = AiFixStatus::FAILED;
        $this->error_message = $errorMessage;
        $this->retry_count++;
        $this->save();
    }

    public function markAsApplied(): void
    {
        $this->status = AiFixStatus::APPLIED;
        $this->save();
    }

    public function incrementRetry(): void
    {
        $this->retry_count++;
        $this->save();
    }

    public function getDiffStats(): array
    {
        $lines = explode("\n", $this->diff_content);
        
        $additions = 0;
        $deletions = 0;
        
        foreach ($lines as $line) {
            if (str_starts_with($line, '+') && !str_starts_with($line, '+++')) {
                $additions++;
            } elseif (str_starts_with($line, '-') && !str_starts_with($line, '---')) {
                $deletions++;
            }
        }
        
        return [
            'additions' => $additions,
            'deletions' => $deletions,
            'total_changes' => $additions + $deletions
        ];
    }

    public function getValidationSummary(): array
    {
        if (!$this->validation_results) {
            return [];
        }

        return [
            'syntax_valid' => $this->validation_results['syntax_valid'] ?? false,
            'tests_passed' => $this->validation_results['tests_passed'] ?? false,
            'security_validated' => $this->validation_results['security_validated'] ?? false,
            'performance_impact' => $this->validation_results['performance_impact'] ?? 'unknown',
            'compatibility_score' => $this->validation_results['compatibility_score'] ?? 0.0
        ];
    }

    public function getTestSummary(): array
    {
        if (!$this->test_results) {
            return [];
        }

        return [
            'total_tests' => $this->test_results['total_tests'] ?? 0,
            'passed_tests' => $this->test_results['passed_tests'] ?? 0,
            'failed_tests' => $this->test_results['failed_tests'] ?? 0,
            'skipped_tests' => $this->test_results['skipped_tests'] ?? 0,
            'coverage_percentage' => $this->test_results['coverage_percentage'] ?? 0.0
        ];
    }

    public function scopeSuccessful($query)
    {
        return $query->whereIn('status', [AiFixStatus::VALIDATED, AiFixStatus::APPLIED]);
    }

    public function scopeFailed($query)
    {
        return $query->where('status', AiFixStatus::FAILED);
    }

    public function scopeHighConfidence($query)
    {
        return $query->where('confidence_score', '>=', 0.8);
    }

    public function scopeByVulnerability($query, string $vulnerabilityId)
    {
        return $query->where('vulnerability_id', $vulnerabilityId);
    }
}
