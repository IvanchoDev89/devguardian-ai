<?php

declare(strict_types=1);

namespace App\Core\Application\Services;

use App\Core\Domain\Organizations\Organization;
use App\Core\Domain\Repositories\Repository;
use App\Core\Domain\Vulnerabilities\Vulnerability;
use App\Core\Domain\AiFixes\AiFix;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Carbon\Carbon;
use Carbon\CarbonPeriod;

final class SecurityMetricsService
{
    public function getOrganizationMetrics(Organization $organization, array $filters = []): array
    {
        $dateRange = $this->getDateRangeFromFilters($filters);
        
        return [
            'overview' => $this->getOverviewMetrics($organization, $dateRange),
            'vulnerability_trends' => $this->getVulnerabilityTrends($organization, $dateRange),
            'remediation_metrics' => $this->getRemediationMetrics($organization, $dateRange),
            'severity_breakdown' => $this->getSeverityBreakdown($organization),
            'repository_metrics' => $this->getRepositoryMetricsData($organization),
            'compliance_metrics' => $this->getComplianceMetrics($organization),
            'ai_fix_performance' => $this->getAiFixPerformanceMetrics($organization)
        ];
    }

    public function getRepositoryMetrics(Repository $repository, array $filters = []): array
    {
        $dateRange = $this->getDateRangeFromFilters($filters);
        
        return [
            'overview' => $this->getRepositoryOverview($repository, $dateRange),
            'vulnerability_history' => $this->getRepositoryVulnerabilityHistory($repository, $dateRange),
            'fix_success_rate' => $this->getRepositoryFixSuccessRate($repository),
            'scan_frequency' => $this->getRepositoryScanFrequency($repository),
            'security_score' => $this->calculateRepositorySecurityScore($repository)
        ];
    }

    public function getVulnerabilityMetrics(Vulnerability $vulnerability): array
    {
        return [
            'basic_info' => [
                'id' => $vulnerability->id,
                'title' => $vulnerability->title,
                'severity' => $vulnerability->severity->value,
                'cvss_score' => $vulnerability->cvss_score,
                'status' => $vulnerability->status->value,
                'detected_at' => $vulnerability->detected_at,
                'fixed_at' => $vulnerability->fixed_at
            ],
            'time_metrics' => [
                'time_to_remediation_hours' => $vulnerability->getTimeToRemediationInHours(),
                'age_in_days' => $vulnerability->detected_at->diffInDays(now()),
                'is_overdue' => $this->isVulnerabilityOverdue($vulnerability)
            ],
            'fix_attempts' => [
                'total_attempts' => $vulnerability->aiFixes()->count(),
                'successful_fixes' => $vulnerability->aiFixes()->successful()->count(),
                'failed_fixes' => $vulnerability->aiFixes()->failed()->count(),
                'average_confidence' => $vulnerability->aiFixes()->avg('confidence_score')
            ]
        ];
    }

    private function getOverviewMetrics(Organization $organization, array $dateRange): array
    {
        $query = $organization->repositories()->withCount('vulnerabilities');
        
        if (isset($dateRange['start'])) {
            $query->whereHas('vulnerabilities', function ($q) use ($dateRange) {
                $q->whereBetween('detected_at', [$dateRange['start'], $dateRange['end']]);
            });
        }

        $repositories = $query->get();
        
        $totalVulnerabilities = $repositories->sum('vulnerabilities_count');
        $criticalVulnerabilities = $this->getCriticalVulnerabilityCount($organization, $dateRange);
        $fixedVulnerabilities = $this->getFixedVulnerabilityCount($organization, $dateRange);
        
        return [
            'total_repositories' => $repositories->count(),
            'active_repositories' => $repositories->where('status', 'active')->count(),
            'total_vulnerabilities' => $totalVulnerabilities,
            'critical_vulnerabilities' => $criticalVulnerabilities,
            'high_vulnerabilities' => $this->getHighVulnerabilityCount($organization, $dateRange),
            'fixed_vulnerabilities' => $fixedVulnerabilities,
            'unfixed_vulnerabilities' => $totalVulnerabilities - $fixedVulnerabilities,
            'average_cvss_score' => $this->getAverageCVSSScore($organization, $dateRange),
            'security_score' => $this->calculateOrganizationSecurityScore($organization)
        ];
    }

    private function getVulnerabilityTrends(Organization $organization, array $dateRange): array
    {
        $period = CarbonPeriod::create($dateRange['start'], '1 week', $dateRange['end']);
        $trends = [];

        foreach ($period as $date) {
            $weekStart = $date->copy()->startOfWeek();
            $weekEnd = $date->copy()->endOfWeek();
            
            $detected = $organization->repositories()
                ->withCount(['vulnerabilities' => function ($q) use ($weekStart, $weekEnd) {
                    $q->whereBetween('detected_at', [$weekStart, $weekEnd]);
                }])
                ->get()
                ->sum('vulnerabilities_count');
            
            $fixed = $organization->repositories()
                ->withCount(['vulnerabilities' => function ($q) use ($weekStart, $weekEnd) {
                    $q->whereBetween('fixed_at', [$weekStart, $weekEnd]);
                }])
                ->get()
                ->sum('vulnerabilities_count');

            $trends[] = [
                'week' => $weekStart->format('Y-m-d'),
                'detected' => $detected,
                'fixed' => $fixed,
                'net_change' => $detected - $fixed
            ];
        }

        return $trends;
    }

    private function getRemediationMetrics(Organization $organization, array $dateRange): array
    {
        $vulnerabilities = $this->getVulnerabilitiesInDateRange($organization, $dateRange);
        
        $fixedVulnerabilities = $vulnerabilities->where('status', 'fixed');
        $mttrData = $fixedVulnerabilities
            ->map(fn($v) => $v->getTimeToRemediationInHours())
            ->filter()
            ->values();

        return [
            'mean_time_to_remediation_hours' => $mttrData->avg() ?? 0,
            'median_time_to_remediation_hours' => $this->calculateMedian($mttrData->toArray()),
            'remediation_rate_percentage' => $vulnerabilities->count() > 0 
                ? round(($fixedVulnerabilities->count() / $vulnerabilities->count()) * 100, 2)
                : 0,
            'total_fixed' => $fixedVulnerabilities->count(),
            'total_outstanding' => $vulnerabilities->whereNotIn('status', ['fixed', 'ignored', 'false_positive'])->count(),
            'sla_compliance_rate' => $this->calculateSLAComplianceRate($fixedVulnerabilities)
        ];
    }

    private function getSeverityBreakdown(Organization $organization): array
    {
        $vulnerabilities = $organization->repositories()
            ->with('vulnerabilities')
            ->get()
            ->flatMap(fn($repo) => $repo->vulnerabilities);

        return [
            'critical' => [
                'count' => $vulnerabilities->where('severity', 'critical')->count(),
                'percentage' => $this->calculatePercentage($vulnerabilities->count(), $vulnerabilities->where('severity', 'critical')->count())
            ],
            'high' => [
                'count' => $vulnerabilities->where('severity', 'high')->count(),
                'percentage' => $this->calculatePercentage($vulnerabilities->count(), $vulnerabilities->where('severity', 'high')->count())
            ],
            'medium' => [
                'count' => $vulnerabilities->where('severity', 'medium')->count(),
                'percentage' => $this->calculatePercentage($vulnerabilities->count(), $vulnerabilities->where('severity', 'medium')->count())
            ],
            'low' => [
                'count' => $vulnerabilities->where('severity', 'low')->count(),
                'percentage' => $this->calculatePercentage($vulnerabilities->count(), $vulnerabilities->where('severity', 'low')->count())
            ]
        ];
    }

    private function getRepositoryMetricsData(Organization $organization): array
    {
        $repositories = $organization->repositories()->with('vulnerabilities')->get();
        
        return $repositories->map(function ($repository) {
            $vulnerabilities = $repository->vulnerabilities;
            
            return [
                'id' => $repository->id,
                'name' => $repository->name,
                'full_name' => $repository->full_name,
                'provider' => $repository->provider->value,
                'vulnerability_count' => $vulnerabilities->count(),
                'critical_count' => $vulnerabilities->where('severity', 'critical')->count(),
                'high_count' => $vulnerabilities->where('severity', 'high')->count(),
                'fixed_count' => $vulnerabilities->where('status', 'fixed')->count(),
                'last_scanned_at' => $repository->last_scanned_at,
                'security_score' => $this->calculateRepositorySecurityScore($repository)
            ];
        })->toArray();
    }

    private function getComplianceMetrics(Organization $organization): array
    {
        return [
            'scan_coverage' => $this->calculateScanCoverage($organization),
            'critical_vulnerability_sla' => $this->calculateCriticalSLACompliance($organization),
            'documentation_coverage' => $this->calculateDocumentationCoverage($organization),
            'access_control_compliance' => $this->calculateAccessControlCompliance($organization),
            'overall_compliance_score' => $this->calculateOverallComplianceScore($organization)
        ];
    }

    private function getAiFixPerformanceMetrics(Organization $organization): array
    {
        $aiFixes = $organization->repositories()
            ->with('aiFixes')
            ->get()
            ->flatMap(fn($repo) => $repo->aiFixes);

        return [
            'total_fixes_generated' => $aiFixes->count(),
            'successful_fixes' => $aiFixes->successful()->count(),
            'failed_fixes' => $aiFixes->failed()->count(),
            'success_rate_percentage' => $aiFixes->count() > 0 
                ? round(($aiFixes->successful()->count() / $aiFixes->count()) * 100, 2)
                : 0,
            'average_confidence_score' => $aiFixes->avg('confidence_score'),
            'average_generation_time_ms' => $aiFixes->avg('metadata.generation_time_ms'),
            'high_confidence_fixes' => $aiFixes->where('confidence_score', '>=', 0.8)->count(),
            'retry_rate' => $this->calculateRetryRate($aiFixes)
        ];
    }

    private function calculateOrganizationSecurityScore(Organization $organization): float
    {
        $vulnerabilities = $organization->repositories()
            ->with('vulnerabilities')
            ->get()
            ->flatMap(fn($repo) => $repo->vulnerabilities);

        if ($vulnerabilities->count() === 0) {
            return 100.0;
        }

        $criticalWeight = 0.4;
        $highWeight = 0.3;
        $mediumWeight = 0.2;
        $lowWeight = 0.1;

        $total = $vulnerabilities->count();
        $critical = $vulnerabilities->where('severity', 'critical')->count();
        $high = $vulnerabilities->where('severity', 'high')->count();
        $medium = $vulnerabilities->where('severity', 'medium')->count();
        $low = $vulnerabilities->where('severity', 'low')->count();

        $riskScore = (
            ($critical / $total) * $criticalWeight +
            ($high / $total) * $highWeight +
            ($medium / $total) * $mediumWeight +
            ($low / $total) * $lowWeight
        ) * 100;

        return max(0, 100 - $riskScore);
    }

    private function calculateRepositorySecurityScore(Repository $repository): float
    {
        $vulnerabilities = $repository->vulnerabilities;

        if ($vulnerabilities->count() === 0) {
            return 100.0;
        }

        $criticalWeight = 0.4;
        $highWeight = 0.3;
        $mediumWeight = 0.2;
        $lowWeight = 0.1;

        $total = $vulnerabilities->count();
        $critical = $vulnerabilities->where('severity', 'critical')->count();
        $high = $vulnerabilities->where('severity', 'high')->count();
        $medium = $vulnerabilities->where('severity', 'medium')->count();
        $low = $vulnerabilities->where('severity', 'low')->count();

        $riskScore = (
            ($critical / $total) * $criticalWeight +
            ($high / $total) * $highWeight +
            ($medium / $total) * $mediumWeight +
            ($low / $total) * $lowWeight
        ) * 100;

        return max(0, 100 - $riskScore);
    }

    private function isVulnerabilityOverdue(Vulnerability $vulnerability): bool
    {
        $slaHours = match ($vulnerability->severity) {
            'critical' => 24,
            'high' => 72,
            'medium' => 168, // 1 week
            'low' => 720,    // 30 days
            default => 720
        };

        return $vulnerability->detected_at->lt(now()->subHours($slaHours)) && !$vulnerability->isFixed();
    }

    private function getDateRangeFromFilters(array $filters): array
    {
        $defaultDays = 30;
        $days = $filters['days'] ?? $defaultDays;
        
        return [
            'start' => now()->subDays($days)->startOfDay(),
            'end' => now()->endOfDay()
        ];
    }

    private function getVulnerabilitiesInDateRange(Organization $organization, array $dateRange)
    {
        return $organization->repositories()
            ->with('vulnerabilities')
            ->get()
            ->flatMap(fn($repo) => $repo->vulnerabilities)
            ->filter(fn($vuln) => 
                $vuln->detected_at->between($dateRange['start'], $dateRange['end'])
            );
    }

    private function calculateMedian(array $values): float
    {
        sort($values);
        $count = count($values);
        
        if ($count === 0) return 0;
        
        $middle = floor($count / 2);
        
        if ($count % 2 === 0) {
            return ($values[$middle - 1] + $values[$middle]) / 2;
        }
        
        return $values[$middle];
    }

    private function calculatePercentage(int $total, int $count): float
    {
        return $total > 0 ? round(($count / $total) * 100, 2) : 0;
    }

    private function calculateSLAComplianceRate($fixedVulnerabilities): float
    {
        if ($fixedVulnerabilities->count() === 0) {
            return 100.0;
        }

        $compliant = $fixedVulnerabilities->filter(function ($vuln) {
            $slaHours = match ($vuln->severity) {
                'critical' => 24,
                'high' => 72,
                'medium' => 168,
                'low' => 720,
                default => 720
            };

            return $vuln->getTimeToRemediationInHours() <= $slaHours;
        });

        return $this->calculatePercentage($fixedVulnerabilities->count(), $compliant->count());
    }

    private function calculateScanCoverage(Organization $organization): float
    {
        $totalRepos = $organization->repositories()->count();
        $scannedRepos = $organization->repositories()
            ->whereNotNull('last_scanned_at')
            ->where('last_scanned_at', '>', now()->subDays(7))
            ->count();

        return $this->calculatePercentage($totalRepos, $scannedRepos);
    }

    private function calculateCriticalSLACompliance(Organization $organization): float
    {
        $criticalVulns = $organization->repositories()
            ->with('vulnerabilities')
            ->get()
            ->flatMap(fn($repo) => $repo->vulnerabilities)
            ->where('severity', 'critical')
            ->where('status', 'fixed');

        return $this->calculateSLAComplianceRate($criticalVulns);
    }

    private function calculateDocumentationCoverage(Organization $organization): float
    {
        // Placeholder implementation
        return 85.0;
    }

    private function calculateAccessControlCompliance(Organization $organization): float
    {
        // Placeholder implementation
        return 90.0;
    }

    private function calculateOverallComplianceScore(Organization $organization): float
    {
        $metrics = [
            $this->calculateScanCoverage($organization) * 0.3,
            $this->calculateCriticalSLACompliance($organization) * 0.4,
            $this->calculateDocumentationCoverage($organization) * 0.15,
            $this->calculateAccessControlCompliance($organization) * 0.15
        ];

        return array_sum($metrics);
    }

    private function calculateRetryRate($aiFixes): float
    {
        $totalFixes = $aiFixes->count();
        $retriedFixes = $aiFixes->where('retry_count', '>', 0)->count();

        return $totalFixes > 0 ? $this->calculatePercentage($totalFixes, $retriedFixes) : 0;
    }

    // Helper methods for counts
    private function getCriticalVulnerabilityCount(Organization $organization, array $dateRange): int
    {
        return $this->getVulnerabilitiesInDateRange($organization, $dateRange)
            ->where('severity', 'critical')
            ->count();
    }

    private function getHighVulnerabilityCount(Organization $organization, array $dateRange): int
    {
        return $this->getVulnerabilitiesInDateRange($organization, $dateRange)
            ->where('severity', 'high')
            ->count();
    }

    private function getFixedVulnerabilityCount(Organization $organization, array $dateRange): int
    {
        return $this->getVulnerabilitiesInDateRange($organization, $dateRange)
            ->where('status', 'fixed')
            ->count();
    }

    private function getAverageCVSSScore(Organization $organization, array $dateRange): float
    {
        return $this->getVulnerabilitiesInDateRange($organization, $dateRange)
            ->whereNotNull('cvss_score')
            ->avg('cvss_score') ?? 0.0;
    }

    // Additional repository-specific methods
    private function getRepositoryOverview(Repository $repository, array $dateRange): array
    {
        $vulnerabilities = $repository->vulnerabilities()
            ->whereBetween('detected_at', [$dateRange['start'], $dateRange['end']])
            ->get();

        return [
            'total_vulnerabilities' => $vulnerabilities->count(),
            'critical_vulnerabilities' => $vulnerabilities->where('severity', 'critical')->count(),
            'high_vulnerabilities' => $vulnerabilities->where('severity', 'high')->count(),
            'fixed_vulnerabilities' => $vulnerabilities->where('status', 'fixed')->count(),
            'last_scan_date' => $repository->last_scanned_at
        ];
    }

    private function getRepositoryVulnerabilityHistory(Repository $repository, array $dateRange): array
    {
        // Implementation for historical vulnerability data
        return [];
    }

    private function getRepositoryFixSuccessRate(Repository $repository): float
    {
        $totalFixes = $repository->aiFixes()->count();
        $successfulFixes = $repository->aiFixes()->successful()->count();

        return $totalFixes > 0 ? $this->calculatePercentage($totalFixes, $successfulFixes) : 0;
    }

    private function getRepositoryScanFrequency(Repository $repository): array
    {
        return [
            'interval_hours' => $repository->getScanSetting('interval_hours', 24),
            'last_scan' => $repository->last_scanned_at,
            'next_scan_due' => $repository->last_scanned_at 
                ? $repository->last_scanned_at->addHours($repository->getScanSetting('interval_hours', 24))
                : now()
        ];
    }
}
