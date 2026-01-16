<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Third Party Services
    |--------------------------------------------------------------------------
    |
    | This file is for storing the credentials for third party services such
    | as Mailgun, Postmark, AWS and more. This file provides the de facto
    | location for this type of information, allowing packages to have
    | a conventional file to locate the various service credentials.
    |
    */

    'postmark' => [
        'key' => env('POSTMARK_API_KEY'),
    ],

    'resend' => [
        'key' => env('RESEND_API_KEY'),
    ],

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    ],

    'slack' => [
        'notifications' => [
            'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
            'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
        ],
    ],

    // AI Service Configuration
    'ai_service' => [
        'url' => env('AI_SERVICE_URL', 'http://localhost:8003'),
        'timeout' => env('AI_SERVICE_TIMEOUT', 30),
        'secret_key' => env('AI_SERVICE_SECRET_KEY'),
        'endpoints' => [
            'scan' => '/api/security/scan',
            'batch_scan' => '/api/security/scan/batch',
            'generate_fix' => '/api/ai-fix/generate-fix',
            'health' => '/health'
        ]
    ],

    // OAuth Configuration
    'oauth' => [
        'github' => [
            'client_id' => env('GITHUB_CLIENT_ID'),
            'client_secret' => env('GITHUB_CLIENT_SECRET'),
            'redirect' => env('GITHUB_REDIRECT_URI'),
            'scope' => 'repo user:email',
        ],
        'gitlab' => [
            'client_id' => env('GITLAB_CLIENT_ID'),
            'client_secret' => env('GITLAB_CLIENT_SECRET'),
            'redirect' => env('GITLAB_REDIRECT_URI'),
            'scope' => 'read_repository read_user profile email',
        ],
        'bitbucket' => [
            'client_id' => env('BITBUCKET_CLIENT_ID'),
            'client_secret' => env('BITBUCKET_CLIENT_SECRET'),
            'redirect' => env('BITBUCKET_REDIRECT_URI'),
            'scope' => 'repository:write account',
        ],
    ],

];
