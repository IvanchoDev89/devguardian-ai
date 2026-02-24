<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\GitHubService;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class RepositoryController extends Controller
{
    private $github;

    public function __construct()
    {
        $this->github = new GitHubService();
    }

    public function index(Request $request): JsonResponse
    {
        $userId = $this->getAuthenticatedUserId($request);
        
        $repositories = DB::table('repositories')
            ->where('user_id', $userId)
            ->orderByDesc('last_scan_at')
            ->limit(50)
            ->get();

        return response()->json([
            'success' => true,
            'data' => $repositories
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'url' => 'required|url',
            'name' => 'nullable|string|max:255',
        ]);

        $parsed = $this->github->parseGitUrl($validated['url']);
        
        if (!$parsed) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid GitHub repository URL'
            ], 400);
        }

        $userId = $this->getAuthenticatedUserId($request);
        
        $repoId = DB::table('repositories')->insertGetId([
            'user_id' => $userId,
            'name' => $validated['name'] ?? $parsed['repo'],
            'url' => $validated['url'],
            'owner' => $parsed['owner'],
            'repo' => $parsed['repo'],
            'default_branch' => 'main',
            'is_private' => true,
            'last_scan_at' => null,
            'vulnerability_count' => 0,
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        $repository = DB::table('repositories')->find($repoId);

        return response()->json([
            'success' => true,
            'message' => 'Repository added successfully',
            'data' => $repository
        ], 201);
    }

    public function show(Request $request, string $id): JsonResponse
    {
        $repository = DB::table('repositories')
            ->where('id', $id)
            ->first();

        if (!$repository) {
            return response()->json([
                'success' => false,
                'message' => 'Repository not found'
            ], 404);
        }

        return response()->json([
            'success' => true,
            'data' => $repository
        ]);
    }

    public function destroy(Request $request, string $id): JsonResponse
    {
        $deleted = DB::table('repositories')
            ->where('id', $id)
            ->delete();

        if (!$deleted) {
            return response()->json([
                'success' => false,
                'message' => 'Repository not found'
            ], 404);
        }

        return response()->json([
            'success' => true,
            'message' => 'Repository deleted successfully'
        ]);
    }

    public function scan(Request $request, string $id): JsonResponse
    {
        $repository = DB::table('repositories')
            ->where('id', $id)
            ->first();

        if (!$repository) {
            return response()->json([
                'success' => false,
                'message' => 'Repository not found'
            ], 404);
        }

        $scanId = Str::uuid()->toString();
        
        DB::table('scan_jobs')->insert([
            'id' => $scanId,
            'user_id' => $repository->user_id,
            'repository_id' => $id,
            'scan_type' => 'full',
            'status' => 'pending',
            'config' => json_encode([
                'target' => $repository->url,
                'target_type' => 'source_code',
            ]),
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        return response()->json([
            'success' => true,
            'message' => 'Scan initiated successfully',
            'data' => [
                'scan_id' => $scanId,
                'repository_id' => $id,
                'status' => 'pending'
            ]
        ], 202);
    }

    public function vulnerabilities(Request $request, string $id): JsonResponse
    {
        $vulnerabilities = DB::table('vulnerabilities')
            ->where('repository_id', $id)
            ->orderByDesc('created_at')
            ->limit(100)
            ->get();

        return response()->json([
            'success' => true,
            'data' => $vulnerabilities
        ]);
    }

    public function refresh(Request $request, string $id): JsonResponse
    {
        $repository = DB::table('repositories')
            ->where('id', $id)
            ->first();

        if (!$repository) {
            return response()->json([
                'success' => false,
                'message' => 'Repository not found'
            ], 404);
        }

        $github = new GitHubService($request->bearerToken());
        $repoData = $github->getRepository($repository->owner, $repository->repo);

        if (!$repoData) {
            return response()->json([
                'success' => false,
                'message' => 'Failed to fetch repository from GitHub'
            ], 400);
        }

        DB::table('repositories')
            ->where('id', $id)
            ->update([
                'name' => $repoData['name'],
                'default_branch' => $repoData['default_branch'] ?? 'main',
                'is_private' => $repoData['private'] ?? true,
                'language' => $repoData['language'] ?? null,
                'updated_at' => now(),
            ]);

        return response()->json([
            'success' => true,
            'message' => 'Repository refreshed successfully'
        ]);
    }

    public function connect(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'github_token' => 'required|string',
        ]);

        $github = new GitHubService($validated['github_token']);
        $user = $github->getUser();

        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid GitHub token'
            ], 401);
        }

        DB::table('users')
            ->where('id', $request->user_id ?? 1)
            ->update([
                'github_token' => $validated['github_token'],
                'github_id' => $user['id'],
                'updated_at' => now(),
            ]);

        $repositories = $github->getRepositories();

        return response()->json([
            'success' => true,
            'message' => 'GitHub connected successfully',
            'data' => [
                'user' => [
                    'id' => $user['id'],
                    'login' => $user['login'],
                    'name' => $user['name'],
                    'avatar' => $user['avatar_url'],
                ],
                'repositories_count' => count($repositories)
            ]
        ]);
    }

    public function listGitHub(Request $request): JsonResponse
    {
        $github = new GitHubService($request->bearerToken());
        $repos = $github->getRepositories();

        $formatted = array_map(function ($repo) {
            return [
                'id' => $repo['id'],
                'name' => $repo['name'],
                'full_name' => $repo['full_name'],
                'private' => $repo['private'],
                'language' => $repo['language'],
                'updated_at' => $repo['updated_at'],
                'url' => $repo['html_url'],
            ];
        }, $repos);

        return response()->json([
            'success' => true,
            'data' => $formatted
        ]);
    }
    
    private function getAuthenticatedUserId(Request $request): int
    {
        $token = $request->bearerToken();
        
        if (!$token) {
            throw new \Illuminate\Validation\UnauthorizedException('Authentication required');
        }
        
        $tokenRecord = DB::table('personal_access_tokens')
            ->where('token', hash('sha256', $token))
            ->first();
        
        if (!$tokenRecord) {
            throw new \Illuminate\Validation\UnauthorizedException('Invalid or expired token');
        }
        
        return $tokenRecord->tokenable_id;
    }
}
