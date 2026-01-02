<?php

declare(strict_types=1);

namespace App\Core\Domain\ValueObjects;

final readonly class CVSSScore
{
    public function __construct(
        public float $score,
        public ?string $vector = null,
        public ?string $version = null
    ) {
        $this->validateScore();
    }

    private function validateScore(): void
    {
        if ($this->score < 0.0 || $this->score > 10.0) {
            throw new \InvalidArgumentException('CVSS score must be between 0.0 and 10.0');
        }
    }

    public function getSeverity(): string
    {
        return match (true) {
            $this->score >= 9.0 => 'critical',
            $this->score >= 7.0 => 'high',
            $this->score >= 4.0 => 'medium',
            $this->score > 0.0 => 'low',
            default => 'none'
        };
    }

    public function isCritical(): bool
    {
        return $this->score >= 9.0;
    }

    public function toArray(): array
    {
        return [
            'score' => $this->score,
            'vector' => $this->vector,
            'version' => $this->version,
            'severity' => $this->getSeverity()
        ];
    }
}
