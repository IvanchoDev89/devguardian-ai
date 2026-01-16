<?php

namespace App\Core\Domain\Repositories;

use App\Models\AiFix;
use Illuminate\Support\Collection;

class AiFixRepository
{
    public function all(): Collection
    {
        return AiFix::all();
    }

    public function findById(string $id): ?AiFix
    {
        return AiFix::find($id);
    }

    public function create(array $data): AiFix
    {
        return AiFix::create($data);
    }

    public function update(string $id, array $data): ?AiFix
    {
        $fix = AiFix::find($id);
        if ($fix) {
            $fix->update($data);
        }
        return $fix;
    }

    public function delete(string $id): bool
    {
        $fix = AiFix::find($id);
        if ($fix) {
            return $fix->delete();
        }
        return false;
    }

    public function findByVulnerabilityId(string $vulnerabilityId): Collection
    {
        return AiFix::where('vulnerability_id', $vulnerabilityId)->get();
    }

    public function findByStatus(string $status): Collection
    {
        return AiFix::where('status', $status)->get();
    }
}
