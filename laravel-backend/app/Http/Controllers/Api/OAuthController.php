<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

class OAuthController extends Controller
{
    private $githubClientId;
    private $githubClientSecret;

    public function __construct()
    {
        $this->githubClientId = config('services.github.client_id');
        $this->githubClientSecret = config('services.github.client_secret');
    }

    public function githubRedirect(): JsonResponse
    {
        $state = Str::random(40);
        session(['github_oauth_state' => $state]);

        $redirectUri = config('app.url') . '/api/auth/github/callback';
        
        $url = 'https://github.com/login/oauth/authorize?' . http_build_query([
            'client_id' => $this->githubClientId,
            'redirect_uri' => $redirectUri,
            'scope' => 'user:email,repo',
            'state' => $state,
        ]);

        // Return the URL so frontend can redirect
        return response()->json([
            'success' => true,
            'data' => [
                'url' => $url
            ]
        ]);
    }

    public function githubCallback(Request $request): JsonResponse
    {
        $code = $request->get('code');
        $state = $request->get('state');

        if (!$code || !$state) {
            return response()->json([
                'success' => false,
                'message' => 'Missing code or state parameter'
            ], 400);
        }

        $savedState = session('github_oauth_state');
        if ($state !== $savedState) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid state parameter'
            ], 400);
        }

        try {
            $accessToken = $this->exchangeCodeForToken($code);
            $githubUser = $this->getGithubUser($accessToken);
            $githubEmail = $this->getGithubEmail($accessToken);

            $user = $this->findOrCreateUser($githubUser, $githubEmail);

            $token = $this->createToken($user->email);

            return response()->json([
                'success' => true,
                'message' => 'Login successful',
                'data' => [
                    'user' => [
                        'id' => $user->id,
                        'name' => $user->name,
                        'email' => $user->email,
                        'role' => $user->role,
                        'avatar' => $githubUser['avatar_url'] ?? null,
                    ],
                    'token' => $token,
                    'provider' => 'github'
                ]
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'GitHub authentication failed: ' . $e->getMessage()
            ], 500);
        }
    }

    private function exchangeCodeForToken(string $code): string
    {
        $response = \Illuminate\Support\Facades\Http::post('https://github.com/login/oauth/access_token', [
            'client_id' => $this->githubClientId,
            'client_secret' => $this->githubClientSecret,
            'code' => $code,
        ]);

        parse_str($response->body(), $data);
        return $data['access_token'] ?? '';
    }

    private function getGithubUser(string $token): array
    {
        $response = \Illuminate\Support\Facades\Http::withHeaders([
            'Authorization' => 'Bearer ' . $token,
            'Accept' => 'application/vnd.github.v3+json',
        ])->get('https://api.github.com/user');

        return $response->json() ?? [];
    }

    private function getGithubEmail(string $token): ?string
    {
        $response = \Illuminate\Support\Facades\Http::withHeaders([
            'Authorization' => 'Bearer ' . $token,
            'Accept' => 'application/vnd.github.v3+json',
        ])->get('https://api.github.com/user/emails');

        $emails = $response->json() ?? [];
        
        foreach ($emails as $email) {
            if ($email['primary'] ?? false) {
                return $email['email'];
            }
        }

        return $emails[0]['email'] ?? null;
    }

    private function findOrCreateUser(array $githubUser, ?string $email): \stdClass
    {
        if (!$email) {
            $email = $githubUser['login'] . '@github.local';
        }

        $user = DB::table('users')->where('email', $email)->first();

        if (!$user) {
            $userId = DB::table('users')->insertGetId([
                'name' => $githubUser['name'] ?? $githubUser['login'],
                'email' => $email,
                'password' => Hash::make(Str::random(32)),
                'role' => 'member',
                'is_active' => true,
                'created_at' => now(),
                'updated_at' => now(),
            ]);

            $user = (object) [
                'id' => $userId,
                'name' => $githubUser['name'] ?? $githubUser['login'],
                'email' => $email,
                'role' => 'member',
            ];
        }

        DB::table('users')->where('id', $user->id)->update([
            'github_id' => $githubUser['id'],
            'avatar' => $githubUser['avatar_url'],
            'updated_at' => now(),
        ]);

        return $user;
    }

    private function createToken(string $email): string
    {
        return base64_encode($email . ':' . time() . ':' . rand(1000, 9999));
    }
}
