<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Concerns\HasUuids;

class Repository extends Model
{
    use HasUuids;

    protected $fillable = [
        'id',
        'name',
        'url',
        'branch',
        'description',
        'owner_id',
        'last_scanned_at',
        'scan_settings'
    ];

    protected $casts = [
        'scan_settings' => 'array',
        'last_scanned_at' => 'datetime'
    ];

    public function vulnerabilities()
    {
        return $this->hasMany(Vulnerability::class);
    }

    public function owner()
    {
        return $this->belongsTo(User::class);
    }
}
