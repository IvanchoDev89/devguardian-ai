<?php

declare(strict_types=1);

namespace App\Core\Application\Services;

use App\Core\Domain\Repositories\Repository;
use App\Core\Domain\Organizations\Organization;
use App\Core\Domain\AiFixes\AiFix;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\DB;
use Exception;

final class GitIntegrationService
{
    public function __construct(
        private readonly string $githubClientId,
        private readonly string $githubClientSecret,
        private readonly string $gitlabClientId,
        private readonly string $gitlabClientSecret
    ) {}

    public function getOAuthUrl(string $provider, string $redirectUri, string $state = null): string
    {
        return match ($provider) {
            'github' => $this->getGitHubOAuthUrl($redirectUri, $state),
            'gitlab' => $this->getGitLabOAuthUrl($redirectUri, $state),
            default => throw new Exception("Unsupported provider: {$provider}")
        };
    }

    public function exchangeCodeForToken(string $provider, string $code, string $redirectUri): array
    {
        return match ($provider) {
            'github' => $this->exchangeGitHubCodeForToken($code, $redirectUri),
            'gitlab' => $this->exchangeGitLabCodeForToken($code, $redirectUri),
            default => throw new Exception("Unsupported provider: {$provider}")
        };
    }

    public function getUserRepositories(string $provider, string $accessToken): array
    {
        return match ($provider) {
            'github' => $this->getGitHubRepositories($accessToken),
            'gitlab' => $this->getGitLabRepositories($accessToken),
            default => throw new Exception("Unsupported provider: {$provider}")
        };
    }

    public function createPullRequest(Repository $repository, AiFix $aiFix, array $options = []): array
    {
        $provider = $repository->provider->value;
        
        return match ($provider) {
            'github' => $this->createGitHubPullRequest($repository, $aiFix, $options),
            'gitlab' => $this->createGitLabMergeRequest($repository, $aiFix, $options),
            default => throw new Exception("Unsupported provider: {$provider}")
        };
    }

    public function commitFix(Repository $repository, AiFix $aiFix): array
    {
        $provider = $repository->provider->value;
        
        return match ($provider) {
            'github' => $this->commitGitHubFix($repository, $aiFix),
            'gitlab' => $this->commitGitLabFix($repository, $aiFix),
            default => throw new Exception("Unsupported provider: {$provider}")
        };
    }

    public function getRepositoryDetails(string $provider, string $owner, string $repo, string $accessToken): array
    {
        return match ($provider) {
            'github' => $this->getGitHubRepositoryDetails($owner, $repo, $accessToken),
            'gitlab' => $this->getGitLabRepositoryDetails($owner, $repo, $accessToken),
            default => throw new Exception("Unsupported provider: {$provider}")
        };
    }

    public function setupWebhook(Repository $repository, string $webhookUrl, string $secret): array
    {
        $provider = $repository->provider->value;
        $accessToken = $this->getAccessTokenForRepository($repository);
        
        return match ($provider) {
            'github' => $this->setupGitHubWebhook($repository, $webhookUrl, $secret, $accessToken),
            'gitlab' => $this->setupGitLabWebhook($repository, $webhookUrl, $secret, $accessToken),
            default => throw new Exception("Unsupported provider: {$provider}")
        };
    }

    private function getGitHubOAuthUrl(string $redirectUri, ?string $state): string
    {
        $params = [
            'client_id' => $this->githubClientId,
            'redirect_uri' => $redirectUri,
            'scope' => 'repo admin:repo_hook user:email',
            'state' => $state ?? bin2hex(random_bytes(16))
        ];

        return 'https://github.com/login/oauth/authorize?' . http_build_query($params);
    }

    private function getGitLabOAuthUrl(string $redirectUri, ?string $state): string
    {
        $params = [
            'client_id' => $this->gitlabClientId,
            'redirect_uri' => $redirectUri,
            'response_type' => 'code',
            'scope' => 'api read_repository write_repository',
            'state' => $state ?? bin2hex(random_bytes(16))
        ];

        return 'https://gitlab.com/oauth/authorize?' . http_build_query($params);
    }

    private function exchangeGitHubCodeForToken(string $code, string $redirectUri): array
    {
        $response = Http::asForm()->post('https://github.com/login/oauth/access_token', [
            'client_id' => $this->githubClientId,
            'client_secret' => $this->githubClientSecret,
            'code' => $code,
            'redirect_uri' => $redirectUri
        ]);

        if (!$response->successful()) {
            throw new Exception('GitHub token exchange failed: ' . $response->status());
        }

        parse_str($response->body(), $data);
        
        return [
            'access_token' => $data['access_token'],
            'token_type' => $data['token_type'],
            'scope' => $data['scope'] ?? null
        ];
    }

    private function exchangeGitLabCodeForToken(string $code, string $redirectUri): array
    {
        $response = Http::asForm()->post('https://gitlab.com/oauth/token', [
            'client_id' => $this->gitlabClientId,
            'client_secret' => $this->gitlabClientSecret,
            'code' => $code,
            'redirect_uri' => $redirectUri,
            'grant_type' => 'authorization_code'
        ]);

        if (!$response->successful()) {
            throw new Exception('GitLab token exchange failed: ' . $response->status());
        }

        $data = $response->json();
        
        return [
            'access_token' => $data['access_token'],
            'token_type' => $data['token_type'],
            'expires_in' => $data['expires_in'] ?? null,
            'refresh_token' => $data['refresh_token'] ?? null
        ];
    }

    private function getGitHubRepositories(string $accessToken): array
    {
        $response = Http::withToken($accessToken)
            ->get('https://api.github.com/user/repos', [
                'type' => 'owner',
                'per_page' => 100
            ]);

        if (!$response->successful()) {
            throw new Exception('Failed to fetch GitHub repositories: ' . $response->status());
        }

        return $response->json();
    }

    private function getGitLabRepositories(string $accessToken): array
    {
        $response = Http::withToken($accessToken)
            ->get('https://gitlab.com/api/v4/projects', [
                'owned' => true,
                'per_page' => 100
            ]);

        if (!$response->successful()) {
            throw new Exception('Failed to fetch GitLab repositories: ' . $response->status());
        }

        return $response->json();
    }

    private function createGitHubPullRequest(Repository $repository, AiFix $aiFix, array $options = []): array
    {
        $accessToken = $this->getAccessTokenForRepository($repository);
        $gitUrl = $repository->getGitRepositoryUrl();
        
        // Create a new branch for the fix
        $branchName = $this->generateBranchName($aiFix);
        $this->createGitHubBranch($gitUrl, $branchName, $accessToken);
        
        // Commit the fix
        $commitData = $this->commitGitHubFix($repository, $aiFix, $branchName);
        
        // Create pull request
        $prData = [
            'title' => $options['title'] ?? "Fix: {$aiFix->vulnerability->title}",
            'body' => $this->generatePRDescription($aiFix),
            'head' => $branchName,
            'base' => $repository->branch,
            'draft' => $options['draft'] ?? false
        ];

        $response = Http::withToken($accessToken)
            ->post($gitUrl->getApiUrl() . '/pulls', $prData);

        if (!$response->successful()) {
            throw new Exception('Failed to create GitHub pull request: ' . $response->status());
        }

        $pr = $response->json();
        
        // Update AI fix with PR information
        $aiFix->update([
            'metadata' => array_merge($aiFix->metadata ?? [], [
                'pull_request_url' => $pr['html_url'],
                'pull_request_number' => $pr['number'],
                'branch_name' => $branchName,
                'commit_sha' => $commitData['sha']
            ])
        ]);

        return $pr;
    }

    private function createGitLabMergeRequest(Repository $repository, AiFix $aiFix, array $options = []): array
    {
        $accessToken = $this->getAccessTokenForRepository($repository);
        $gitUrl = $repository->getGitRepositoryUrl();
        
        // Create a new branch for the fix
        $branchName = $this->generateBranchName($aiFix);
        $this->createGitLabBranch($gitUrl, $branchName, $accessToken);
        
        // Commit the fix
        $commitData = $this->commitGitLabFix($repository, $aiFix, $branchName);
        
        // Create merge request
        $mrData = [
            'title' => $options['title'] ?? "Fix: {$aiFix->vulnerability->title}",
            'description' => $this->generatePRDescription($aiFix),
            'source_branch' => $branchName,
            'target_branch' => $repository->branch,
            'draft' => $options['draft'] ?? false
        ];

        $response = Http::withToken($accessToken)
            ->post($gitUrl->getApiUrl() . '/merge_requests', $mrData);

        if (!$response->successful()) {
            throw new Exception('Failed to create GitLab merge request: ' . $response->status());
        }

        $mr = $response->json();
        
        // Update AI fix with MR information
        $aiFix->update([
            'metadata' => array_merge($aiFix->metadata ?? [], [
                'merge_request_url' => $mr['web_url'],
                'merge_request_iid' => $mr['iid'],
                'branch_name' => $branchName,
                'commit_sha' => $commitData['id']
            ])
        ]);

        return $mr;
    }

    private function commitGitHubFix(Repository $repository, AiFix $aiFix, ?string $branch = null): array
    {
        $accessToken = $this->getAccessTokenForRepository($repository);
        $gitUrl = $repository->getGitRepositoryUrl();
        
        // Get the vulnerable file path from the vulnerability location
        $vulnerability = $aiFix->vulnerability;
        $location = $vulnerability->location;
        $filePath = $location['file_path'] ?? '';
        
        if (empty($filePath)) {
            throw new Exception('Unable to determine file path for fix');
        }

        // Prepare commit data
        $commitData = [
            'message' => "Fix security vulnerability: {$vulnerability->title}",
            'content' => $aiFix->diff_content,
            'branch' => $branch ?? $repository->branch
        ];

        // Get current file to create proper diff
        $currentFileResponse = Http::withToken($accessToken)
            ->get($gitUrl->getApiUrl() . '/contents/' . $filePath);

        if ($currentFileResponse->successful()) {
            $commitData['sha'] = $currentFileResponse->json()['sha'];
        }

        $response = Http::withToken($accessToken)
            ->put($gitUrl->getApiUrl() . '/contents/' . $filePath, $commitData);

        if (!$response->successful()) {
            throw new Exception('Failed to commit fix to GitHub: ' . $response->status());
        }

        return $response->json();
    }

    private function commitGitLabFix(Repository $repository, AiFix $aiFix, ?string $branch = null): array
    {
        $accessToken = $this->getAccessTokenForRepository($repository);
        $gitUrl = $repository->getGitRepositoryUrl();
        
        $vulnerability = $aiFix->vulnerability;
        $location = $vulnerability->location;
        $filePath = $location['file_path'] ?? '';
        
        if (empty($filePath)) {
            throw new Exception('Unable to determine file path for fix');
        }

        // Create commit using GitLab API
        $commitData = [
            'branch' => $branch ?? $repository->branch,
            'commit_message' => "Fix security vulnerability: {$vulnerability->title}",
            'actions' => [
                [
                    'action' => 'update',
                    'file_path' => $filePath,
                    'content' => $aiFix->diff_content
                ]
            ]
        ];

        $response = Http::withToken($accessToken)
            ->post($gitUrl->getApiUrl() . '/repository/commits', $commitData);

        if (!$response->successful()) {
            throw new Exception('Failed to commit fix to GitLab: ' . $response->status());
        }

        return $response->json();
    }

    private function generateBranchName(AiFix $aiFix): string
    {
        $vulnerability = $aiFix->vulnerability;
        $prefix = 'fix/security-';
        $identifier = strtolower($vulnerability->identifier);
        
        // Clean up identifier for branch name
        $identifier = preg_replace('/[^a-z0-9-]/', '-', $identifier);
        $identifier = preg_replace('/-+/', '-', $identifier);
        $identifier = trim($identifier, '-');
        
        return $prefix . substr($identifier, 0, 50) . '-' . time();
    }

    private function generatePRDescription(AiFix $aiFix): string
    {
        $vulnerability = $aiFix->vulnerability;
        
        $description = "## Security Fix\n\n";
        $description .= "**Vulnerability:** {$vulnerability->title}\n\n";
        $description .= "**Severity:** {$vulnerability->severity->value}\n\n";
        
        if ($vulnerability->cvss_score) {
            $description .= "**CVSS Score:** {$vulnerability->cvss_score}\n\n";
        }
        
        $description .= "**Description:** {$vulnerability->description}\n\n";
        
        $description .= "## AI-Generated Fix\n\n";
        $description .= "**Confidence Score:** " . round($aiFix->confidence_score * 100, 1) . "%\n\n";
        
        if (isset($aiFix->metadata['explanation'])) {
            $description .= "**Explanation:** {$aiFix->metadata['explanation']}\n\n";
        }
        
        if (!empty($aiFix->metadata['potential_side_effects'])) {
            $description .= "## Potential Side Effects\n\n";
            foreach ($aiFix->metadata['potential_side_effects'] as $sideEffect) {
                $description .= "- {$sideEffect}\n";
            }
            $description .= "\n";
        }
        
        $description .= "---\n\n";
        $description .= "*This fix was automatically generated by DevGuardian AI. Please review carefully before merging.*";
        
        return $description;
    }

    private function getAccessTokenForRepository(Repository $repository): string
    {
        // In a real implementation, this would retrieve the stored access token
        // for the repository's organization from the database
        $organization = $repository->organization;
        
        // For now, return a placeholder
        return $organization->getSetting("{$repository->provider}_access_token", '');
    }

    private function getGitHubRepositoryDetails(string $owner, string $repo, string $accessToken): array
    {
        $response = Http::withToken($accessToken)
            ->get("https://api.github.com/repos/{$owner}/{$repo}");

        if (!$response->successful()) {
            throw new Exception('Failed to fetch GitHub repository details: ' . $response->status());
        }

        return $response->json();
    }

    private function getGitLabRepositoryDetails(string $owner, string $repo, string $accessToken): array
    {
        $encodedPath = urlencode("{$owner}/{$repo}");
        $response = Http::withToken($accessToken)
            ->get("https://gitlab.com/api/v4/projects/{$encodedPath}");

        if (!$response->successful()) {
            throw new Exception('Failed to fetch GitLab repository details: ' . $response->status());
        }

        return $response->json();
    }

    private function setupGitHubWebhook(Repository $repository, string $webhookUrl, string $secret, string $accessToken): array
    {
        $gitUrl = $repository->getGitRepositoryUrl();
        
        $webhookData = [
            'name' => 'web',
            'active' => true,
            'events' => ['push', 'pull_request', 'release'],
            'config' => [
                'url' => $webhookUrl,
                'content_type' => 'json',
                'secret' => $secret
            ]
        ];

        $response = Http::withToken($accessToken)
            ->post($gitUrl->getApiUrl() . '/hooks', $webhookData);

        if (!$response->successful()) {
            throw new Exception('Failed to create GitHub webhook: ' . $response->status());
        }

        return $response->json();
    }

    private function setupGitLabWebhook(Repository $repository, string $webhookUrl, string $secret, string $accessToken): array
    {
        $gitUrl = $repository->getGitRepositoryUrl();
        
        $webhookData = [
            'url' => $webhookUrl,
            'push_events' => true,
            'merge_requests_events' => true,
            'tag_push_events' => true,
            'token' => $secret
        ];

        $response = Http::withToken($accessToken)
            ->post($gitUrl->getApiUrl() . '/hooks', $webhookData);

        if (!$response->successful()) {
            throw new Exception('Failed to create GitLab webhook: ' . $response->status());
        }

        return $response->json();
    }

    // Additional helper methods for branch creation, etc.
    private function createGitHubBranch($gitUrl, string $branchName, string $accessToken): void
    {
        // Get base branch reference
        $response = Http::withToken($accessToken)
            ->get($gitUrl->getApiUrl() . '/git/refs/heads/' . $gitUrl->repository);

        if (!$response->successful()) {
            throw new Exception('Failed to get base branch reference: ' . $response->status());
        }

        $baseRef = $response->json();
        $sha = $baseRef['object']['sha'];

        // Create new branch
        $branchData = [
            'ref' => "refs/heads/{$branchName}",
            'sha' => $sha
        ];

        $response = Http::withToken($accessToken)
            ->post($gitUrl->getApiUrl() . '/git/refs', $branchData);

        if (!$response->successful()) {
            throw new Exception('Failed to create GitHub branch: ' . $response->status());
        }
    }

    private function createGitLabBranch($gitUrl, string $branchName, string $accessToken): void
    {
        // GitLab creates branches automatically when committing to a new branch
        // So we don't need to explicitly create it
    }
}
