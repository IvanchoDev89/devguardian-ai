<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    public function run(): void
    {
        User::create([
            'name' => 'Super Admin',
            'email' => 'superadmin@devguardian.ai',
            'password' => Hash::make('superadmin123'),
            'role' => 'admin',
            'is_active' => true,
        ]);

        User::create([
            'name' => 'Admin User',
            'email' => 'admin@devguardian.ai',
            'password' => Hash::make('admin123'),
            'role' => 'admin',
            'is_active' => true,
        ]);

        User::create([
            'name' => 'Regular User',
            'email' => 'user@devguardian.ai',
            'password' => Hash::make('user123'),
            'role' => 'member',
            'is_active' => true,
        ]);
    }
}
