<?php

declare(strict_types=1);

namespace App\Core\Domain\ValueObjects;

final readonly class GitRepositoryUrl
{
    public function __construct(
        public string $url,
        public string $provider,
        public string $owner,
        public string $repository
    ) {
        $this->validate();
    }

    private function validate(): void
    {
        if (empty($this->url)) {
            throw new \InvalidArgumentException('Repository URL cannot be empty');
        }

        if (!in_array($this->provider, ['github', 'gitlab', 'bitbucket'])) {
            throw new \InvalidArgumentException('Invalid provider: ' . $this->provider);
        }

        if (empty($this->owner) || empty($this->repository)) {
            throw new \InvalidArgumentException('Owner and repository name cannot be empty');
        }
    }

    public static function fromUrl(string $url): self
    {
        $patterns = [
            'github' => '/^https?:\/\/(?:www\.)?github\.com\/([^\/]+)\/([^\/\?]+)(?:\.git)?\/?$/',
            'gitlab' => '/^https?:\/\/(?:www\.)?gitlab\.com\/([^\/]+)\/([^\/\?]+)(?:\.git)?\/?$/',
            'bitbucket' => '/^https?:\/\/(?:www\.)?bitbucket\.org\/([^\/]+)\/([^\/\?]+)(?:\.git)?\/?$/'
        ];

        foreach ($patterns as $provider => $pattern) {
            if (preg_match($pattern, $url, $matches)) {
                return new self($url, $provider, $matches[1], rtrim($matches[2], '.git'));
            }
        }

        throw new \InvalidArgumentException('Invalid repository URL format');
    }

    public function getFullName(): string
    {
        return $this->owner . '/' . $this->repository;
    }

    public function getApiUrl(): string
    {
        return match ($this->provider) {
            'github' => "https://api.github.com/repos/{$this->owner}/{$this->repository}",
            'gitlab' => "https://gitlab.com/api/v4/projects/{$this->owner}%2F{$this->repository}",
            'bitbucket' => "https://api.bitbucket.org/2.0/repositories/{$this->owner}/{$this->repository}",
            default => throw new \InvalidArgumentException('Unsupported provider')
        };
    }

    public function getCloneUrl(string $token = null): string
    {
        $baseUrl = match ($this->provider) {
            'github' => "https://github.com/{$this->owner}/{$this->repository}.git",
            'gitlab' => "https://gitlab.com/{$this->owner}/{$this->repository}.git",
            'bitbucket' => "https://bitbucket.org/{$this->owner}/{$this->repository}.git",
            default => throw new \InvalidArgumentException('Unsupported provider')
        };

        if ($token) {
            return str_replace('https://', "https://{$token}@", $baseUrl);
        }

        return $baseUrl;
    }

    public function toArray(): array
    {
        return [
            'url' => $this->url,
            'provider' => $this->provider,
            'owner' => $this->owner,
            'repository' => $this->repository,
            'full_name' => $this->getFullName(),
            'api_url' => $this->getApiUrl()
        ];
    }
}
