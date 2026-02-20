<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class GitHubService
{
    private $token;
    private $baseUrl = 'https://api.github.com';

    public function __construct(?string $token = null)
    {
        $this->token = $token ?? config('services.github.token');
    }

    public function setToken(string $token): self
    {
        $this->token = $token;
        return $this;
    }

    public function getUser(): ?array
    {
        $response = $this->request('GET', '/user');
        return $response['data'] ?? null;
    }

    public function getRepositories(): array
    {
        $repos = [];
        $page = 1;
        
        do {
            $response = $this->request('GET', '/user/repos', [
                'per_page' => 100,
                'page' => $page,
                'sort' => 'updated',
            ]);
            
            if (empty($response['data'])) {
                break;
            }
            
            $repos = array_merge($repos, $response['data']);
            $page++;
            
        } while (count($response['data']) === 100);
        
        return $repos;
    }

    public function getRepository(string $owner, string $repo): ?array
    {
        $response = $this->request('GET', "/repos/{$owner}/{$repo}");
        return $response['data'] ?? null;
    }

    public function getRepositoryContents(string $owner, string $repo, string $path = ''): array
    {
        $endpoint = "/repos/{$owner}/{$repo}/contents/{$path}";
        $response = $this->request('GET', $endpoint);
        return $response['data'] ?? [];
    }

    public function getFileContent(string $owner, string $repo, string $path): ?string
    {
        $endpoint = "/repos/{$owner}/{$repo}/contents/{$path}";
        $response = $this->request('GET', $endpoint);
        
        if (isset($response['data']['content'])) {
            return base64_decode($response['data']['content']);
        }
        
        return null;
    }

    public function getDefaultBranch(string $owner, string $repo): string
    {
        $repo = $this->getRepository($owner, $repo);
        return $repo['default_branch'] ?? 'main';
    }

    public function getBranch(string $owner, string $repo, string $branch): ?array
    {
        $response = $this->request('GET', "/repos/{$owner}/{$repo}/branches/{$branch}");
        return $response['data'] ?? null;
    }

    public function getCommits(string $owner, string $repo, int $perPage = 30): array
    {
        $response = $this->request('GET', "/repos/{$owner}/{$repo}/commits", [
            'per_page' => $perPage,
        ]);
        return $response['data'] ?? [];
    }

    public function getCommit(string $owner, string $repo, string $sha): ?array
    {
        $response = $this->request('GET', "/repos/{$owner}/{$repo}/commits/{$sha}");
        return $response['data'] ?? null;
    }

    public function downloadRepository(string $owner, string $repo): ?string
    {
        $zipball = $this->request('GET', "/repos/{$owner}/{$repo}/zipball");
        
        if (isset($zipball['headers']['location'])) {
            return $zipball['headers']['location'];
        }
        
        return null;
    }

    public function isCollaborator(string $owner, string $repo, string $username): bool
    {
        $response = $this->request('GET', "/repos/{$owner}/{$repo}/collaborators/{$username}");
        return $response['status'] === 204;
    }

    public function getRepositoryLanguages(string $owner, string $repo): array
    {
        $response = $this->request('GET', "/repos/{$owner}/{$repo}/languages");
        return $response['data'] ?? [];
    }

    public function searchRepositories(string $query, int $perPage = 30): array
    {
        $response = $this->request('GET', '/search/repositories', [
            'q' => $query,
            'per_page' => $perPage,
        ]);
        return $response['data']['items'] ?? [];
    }

    public function getWebhooks(string $owner, string $repo): array
    {
        $response = $this->request('GET', "/repos/{$owner}/{$repo}/hooks");
        return $response['data'] ?? [];
    }

    public function createWebhook(string $owner, string $repo, array $config): ?array
    {
        $response = $this->request('POST', "/repos/{$owner}/{$repo}/hooks", [
            'config' => $config,
            'events' => ['push'],
            'active' => true,
        ]);
        
        return $response['data'] ?? null;
    }

    public function parseGitUrl(string $url): ?array
    {
        // Handle various GitHub URL formats
        $patterns = [
            '/github\.com\/([^\/]+)\/([^\/]+?)(?:\.git)?$/i',
            '/github\.com\/([^\/]+)\/([^\/]+)\/tree\/([^\/]+)\/(.+)/i',
            '/git@github\.com:([^\/]+)\/([^\/]+?)(?:\.git)?$/i',
        ];
        
        foreach ($patterns as $pattern) {
            if (preg_match($pattern, $url, $matches)) {
                return [
                    'owner' => $matches[1],
                    'repo' => $matches[2],
                    'branch' => $matches[3] ?? null,
                    'path' => $matches[4] ?? null,
                ];
            }
        }
        
        return null;
    }

    private function request(string $method, string $endpoint, array $params = []): array
    {
        $headers = [
            'Accept' => 'application/vnd.github.v3+json',
            'User-Agent' => 'DevGuardian-AI/1.0',
        ];
        
        if ($this->token) {
            $headers['Authorization'] = 'Bearer ' . $this->token;
        }
        
        try {
            $response = Http::withHeaders($headers)
                ->timeout(30)
                ->retry(3, 1000);
            
            if (in_array($method, ['GET', 'HEAD']) && !empty($params)) {
                $response = $response->get($this->baseUrl . $endpoint, $params);
            } else {
                $response = $response->$method($this->baseUrl . $endpoint, $params);
            }
            
            $status = $response->status();
            $data = $response->json() ?? [];
            
            return [
                'status' => $status,
                'data' => $data,
                'headers' => $response->headers(),
            ];
            
        } catch (\Exception $e) {
            Log::error('GitHub API error', [
                'method' => $method,
                'endpoint' => $endpoint,
                'error' => $e->getMessage(),
            ]);
            
            return [
                'status' => 500,
                'data' => ['error' => $e->getMessage()],
                'headers' => [],
            ];
        }
    }
}
