<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Concerns\HasUuids;

class AiFix extends Model
{
    use HasUuids;

    protected $fillable = [
        'id',
        'vulnerability_id',
        'fixed_code',
        'confidence',
        'explanation',
        'recommendations',
        'status',
        'created_at'
    ];

    protected $casts = [
        'confidence' => 'float',
        'recommendations' => 'array',
        'created_at' => 'datetime'
    ];

    public function vulnerability()
    {
        return $this->belongsTo(Vulnerability::class);
    }
}
