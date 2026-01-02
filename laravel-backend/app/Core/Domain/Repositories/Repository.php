<?php

declare(strict_types=1);

namespace App\Core\Domain\Repositories;

use App\Core\Domain\Organizations\Organization;
use App\Core\Domain\ValueObjects\GitRepositoryUrl;
use App\Core\Domain\Vulnerabilities\Vulnerability;
use App\Core\Domain\AiFixes\AiFix;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

enum RepositoryStatus: string
{
    case ACTIVE = 'active';
    case INACTIVE = 'inactive';
    case ARCHIVED = 'archived';
}

enum RepositoryProvider: string
{
    case GITHUB = 'github';
    case GITLAB = 'gitlab';
    case BITBUCKET = 'bitbucket';
}

final class Repository extends Model
{
    use HasFactory;

    protected $fillable = [
        'organization_id',
        'name',
        'full_name',
        'provider',
        'external_id',
        'url',
        'branch',
        'status',
        'scan_config',
        'provider_config',
        'last_scanned_at'
    ];

    protected $casts = [
        'id' => 'string',
        'organization_id' => 'string',
        'provider' => RepositoryProvider::class,
        'status' => RepositoryStatus::class,
        'scan_config' => 'array',
        'provider_config' => 'array',
        'last_scanned_at' => 'datetime'
    ];

    public function organization(): BelongsTo
    {
        return $this->belongsTo(Organization::class);
    }

    public function vulnerabilities(): HasMany
    {
        return $this->hasMany(Vulnerability::class);
    }

    public function aiFixes(): HasMany
    {
        return $this->hasMany(AiFix::class);
    }

    public function getGitRepositoryUrl(): GitRepositoryUrl
    {
        return GitRepositoryUrl::fromUrl($this->url);
    }

    public function isActive(): bool
    {
        return $this->status === RepositoryStatus::ACTIVE;
    }

    public function isArchived(): bool
    {
        return $this->status === RepositoryStatus::ARCHIVED;
    }

    public function activate(): void
    {
        $this->status = RepositoryStatus::ACTIVE;
        $this->save();
    }

    public function deactivate(): void
    {
        $this->status = RepositoryStatus::INACTIVE;
        $this->save();
    }

    public function archive(): void
    {
        $this->status = RepositoryStatus::ARCHIVED;
        $this->save();
    }

    public function getScanSetting(string $key, mixed $default = null): mixed
    {
        return data_get($this->scan_config, $key, $default);
    }

    public function setScanSetting(string $key, mixed $value): void
    {
        $this->scan_config = array_merge($this->scan_config ?? [], [$key => $value]);
    }

    public function getProviderSetting(string $key, mixed $default = null): mixed
    {
        return data_get($this->provider_config, $key, $default);
    }

    public function setProviderSetting(string $key, mixed $value): void
    {
        $this->provider_config = array_merge($this->provider_config ?? [], [$key => $value]);
    }

    public function needsScanning(): bool
    {
        if (!$this->isActive()) {
            return false;
        }

        $scanInterval = $this->getScanSetting('interval_hours', 24);
        
        if (!$this->last_scanned_at) {
            return true;
        }

        return $this->last_scanned_at->lt(now()->subHours($scanInterval));
    }

    public function getVulnerabilityStats(): array
    {
        $vulnerabilities = $this->vulnerabilities;
        
        return [
            'total' => $vulnerabilities->count(),
            'critical' => $vulnerabilities->where('cvss_score', '>=', 9.0)->count(),
            'high' => $vulnerabilities->whereBetween('cvss_score', [7.0, 8.9])->count(),
            'medium' => $vulnerabilities->whereBetween('cvss_score', [4.0, 6.9])->count(),
            'low' => $vulnerabilities->whereBetween('cvss_score', [0.1, 3.9])->count(),
            'fixed' => $vulnerabilities->where('status', 'fixed')->count(),
            'in_progress' => $vulnerabilities->whereIn('status', ['analyzing', 'fixing'])->count()
        ];
    }

    public function getAverageCVSSScore(): float
    {
        return $this->vulnerabilities()->avg('cvss_score') ?? 0.0;
    }

    public function getLatestVulnerabilities(int $limit = 10): \Illuminate\Database\Eloquent\Collection
    {
        return $this->vulnerabilities()
            ->latest('detected_at')
            ->limit($limit)
            ->get();
    }

    public function scopeActive($query)
    {
        return $query->where('status', RepositoryStatus::ACTIVE);
    }

    public function scopeByProvider($query, RepositoryProvider $provider)
    {
        return $query->where('provider', $provider);
    }

    public function scopeNeedingScan($query)
    {
        return $query->where('status', RepositoryStatus::ACTIVE)
            ->where(function ($q) {
                $q->whereNull('last_scanned_at')
                  ->orWhere('last_scanned_at', '<', now()->subHours(24));
            });
    }
}
