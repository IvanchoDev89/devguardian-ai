<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Core\Domain\Repositories\OrganizationRepository;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class OrganizationController extends Controller
{
    public function __construct(
        private OrganizationRepository $organizationRepository
    ) {}

    public function index(): JsonResponse
    {
        $organizations = $this->organizationRepository->all();
        return response()->json($organizations);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'description' => 'nullable|string',
            'settings' => 'nullable|array'
        ]);

        $organization = $this->organizationRepository->create($validated);
        return response()->json($organization, 201);
    }

    public function show(string $id): JsonResponse
    {
        $organization = $this->organizationRepository->findById($id);
        
        if (!$organization) {
            return response()->json(['error' => 'Organization not found'], 404);
        }

        return response()->json($organization);
    }

    public function update(Request $request, string $id): JsonResponse
    {
        $validated = $request->validate([
            'name' => 'sometimes|string|max:255',
            'description' => 'sometimes|nullable|string',
            'settings' => 'sometimes|array'
        ]);

        $organization = $this->organizationRepository->update($id, $validated);
        
        if (!$organization) {
            return response()->json(['error' => 'Organization not found'], 404);
        }

        return response()->json($organization);
    }

    public function destroy(string $id): JsonResponse
    {
        $deleted = $this->organizationRepository->delete($id);
        
        if (!$deleted) {
            return response()->json(['error' => 'Organization not found'], 404);
        }

        return response()->json(null, 204);
    }
}
