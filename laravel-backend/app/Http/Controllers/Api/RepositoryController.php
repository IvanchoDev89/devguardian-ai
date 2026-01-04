<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Core\Domain\Repositories\RepositoryRepository;
use App\Core\Domain\Repositories\VulnerabilityRepository;
use App\Jobs\ScanRepositoryJob;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class RepositoryController extends Controller
{
    public function __construct(
        private RepositoryRepository $repositoryRepository,
        private VulnerabilityRepository $vulnerabilityRepository
    ) {}

    public function index(): JsonResponse
    {
        $repositories = $this->repositoryRepository->all();
        return response()->json($repositories);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'url' => 'required|url',
            'organization_id' => 'required|uuid|exists:organizations,id',
            'settings' => 'nullable|array'
        ]);

        $repository = $this->repositoryRepository->create($validated);
        return response()->json($repository, 201);
    }

    public function show(string $id): JsonResponse
    {
        $repository = $this->repositoryRepository->findById($id);
        
        if (!$repository) {
            return response()->json(['error' => 'Repository not found'], 404);
        }

        return response()->json($repository);
    }

    public function scan(string $id): JsonResponse
    {
        $repository = $this->repositoryRepository->findById($id);
        
        if (!$repository) {
            return response()->json(['error' => 'Repository not found'], 404);
        }

        ScanRepositoryJob::dispatch($repository->id);
        
        return response()->json(['message' => 'Repository scan started'], 202);
    }

    public function vulnerabilities(string $id): JsonResponse
    {
        $repository = $this->repositoryRepository->findById($id);
        
        if (!$repository) {
            return response()->json(['error' => 'Repository not found'], 404);
        }

        $vulnerabilities = $this->vulnerabilityRepository->findByRepositoryId($id);
        return response()->json($vulnerabilities);
    }

    public function destroy(string $id): JsonResponse
    {
        $deleted = $this->repositoryRepository->delete($id);
        
        if (!$deleted) {
            return response()->json(['error' => 'Repository not found'], 404);
        }

        return response()->json(null, 204);
    }
}
