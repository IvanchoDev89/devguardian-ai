<?php

declare(strict_types=1);

namespace App\Core\Domain\Organizations;

use App\Core\Domain\ValueObjects\CVSSScore;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Str;

final class Organization extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'slug',
        'billing_tier',
        'settings',
        'encryption_key',
        'trial_ends_at'
    ];

    protected $casts = [
        'id' => 'string',
        'settings' => 'array',
        'trial_ends_at' => 'datetime'
    ];

    protected $hidden = [
        'encryption_key'
    ];

    public function repositories(): HasMany
    {
        return $this->hasMany(Repository::class);
    }

    public function users(): HasMany
    {
        return $this->hasMany(\App\Models\User::class);
    }

    public function getRouteKeyName(): string
    {
        return 'slug';
    }

    protected static function boot(): void
    {
        parent::boot();

        static::creating(function (Organization $organization) {
            if (empty($organization->slug)) {
                $organization->slug = Str::slug($organization->name);
            }
            
            if (empty($organization->encryption_key)) {
                $organization->encryption_key = encrypt(random_bytes(32));
            }
        });

        static::updating(function (Organization $organization) {
            if ($organization->isDirty('name') && empty($organization->slug)) {
                $organization->slug = Str::slug($organization->name);
            }
        });
    }

    public function isOnTrial(): bool
    {
        return $this->trial_ends_at && $this->trial_ends_at->isFuture();
    }

    public function hasFeature(string $feature): bool
    {
        $features = [
            'free' => ['basic_scanning', '5_repositories'],
            'starter' => ['basic_scanning', 'ai_fixes', '50_repositories', 'api_access'],
            'pro' => ['advanced_scanning', 'ai_fixes', 'unlimited_repositories', 'api_access', 'priority_support', 'custom_integrations'],
            'enterprise' => ['advanced_scanning', 'ai_fixes', 'unlimited_repositories', 'api_access', 'priority_support', 'custom_integrations', 'sso', 'audit_logs', 'dedicated_support']
        ];

        return in_array($feature, $features[$this->billing_tier] ?? []);
    }

    public function getMaxRepositories(): int
    {
        return match ($this->billing_tier) {
            'free' => 5,
            'starter' => 50,
            default => -1 // unlimited
        };
    }

    public function canAddRepository(): bool
    {
        if ($this->getMaxRepositories() === -1) {
            return true;
        }

        return $this->repositories()->count() < $this->getMaxRepositories();
    }

    public function getSetting(string $key, mixed $default = null): mixed
    {
        return data_get($this->settings, $key, $default);
    }

    public function setSetting(string $key, mixed $value): void
    {
        $this->settings = array_merge($this->settings ?? [], [$key => $value]);
    }

    public function getAverageCVSSScore(): float
    {
        return $this->repositories()
            ->with('vulnerabilities')
            ->get()
            ->flatMap(fn($repo) => $repo->vulnerabilities)
            ->avg('cvss_score') ?? 0.0;
    }

    public function getTotalVulnerabilities(): int
    {
        return $this->repositories()
            ->withCount('vulnerabilities')
            ->sum('vulnerabilities_count');
    }

    public function getCriticalVulnerabilities(): int
    {
        return $this->repositories()
            ->whereHas('vulnerabilities', fn($q) => $q->where('cvss_score', '>=', 9.0))
            ->withCount(['vulnerabilities' => fn($q) => $q->where('cvss_score', '>=', 9.0)])
            ->sum('vulnerabilities_count');
    }
}
