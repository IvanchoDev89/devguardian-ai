<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class PlanController extends Controller
{
    public function index(): JsonResponse
    {
        $plans = [
            [
                'id' => 'free',
                'name' => 'Free',
                'price' => 0,
                'interval' => 'month',
                'features' => [
                    '100 scans per month',
                    'Basic vulnerability detection',
                    'Email support',
                    '1 user',
                    'Public repositories only',
                ],
                'limits' => [
                    'scans_per_month' => 100,
                    'repositories' => 3,
                    'users' => 1,
                    'ai_fixes' => false,
                    'api_access' => true,
                    'priority_support' => false,
                ]
            ],
            [
                'id' => 'pro',
                'name' => 'Pro',
                'price' => 29,
                'interval' => 'month',
                'popular' => true,
                'features' => [
                    '1,000 scans per month',
                    'AI-powered fix suggestions',
                    'Priority support',
                    '5 users',
                    'Private repositories',
                    'API access',
                    'Custom rules',
                    'Slack integration',
                ],
                'limits' => [
                    'scans_per_month' => 1000,
                    'repositories' => -1, // unlimited
                    'users' => 5,
                    'ai_fixes' => true,
                    'api_access' => true,
                    'priority_support' => true,
                ]
            ],
            [
                'id' => 'enterprise',
                'name' => 'Enterprise',
                'price' => 199,
                'interval' => 'month',
                'features' => [
                    '10,000 scans per month',
                    'Everything in Pro',
                    'Dedicated support',
                    'Unlimited users',
                    'On-premise deployment',
                    'SSO/SAML',
                    'Custom integrations',
                    'Audit logs',
                    'SLA guarantee',
                ],
                'limits' => [
                    'scans_per_month' => 10000,
                    'repositories' => -1,
                    'users' => -1,
                    'ai_fixes' => true,
                    'api_access' => true,
                    'priority_support' => true,
                    'sso' => true,
                    'on_premise' => true,
                ]
            ],
        ];

        return response()->json([
            'success' => true,
            'data' => $plans
        ]);
    }

    public function show(string $id): JsonResponse
    {
        $plans = [
            'free' => [
                'id' => 'free',
                'name' => 'Free',
                'price' => 0,
                'features' => [
                    '100 scans per month',
                    'Basic vulnerability detection',
                    'Email support',
                ]
            ],
            'pro' => [
                'id' => 'pro',
                'name' => 'Pro',
                'price' => 29,
                'features' => [
                    '1,000 scans per month',
                    'AI-powered fix suggestions',
                    'Priority support',
                    'API access',
                ]
            ],
            'enterprise' => [
                'id' => 'enterprise',
                'name' => 'Enterprise',
                'price' => 199,
                'features' => [
                    '10,000 scans per month',
                    'Dedicated support',
                    'On-premise deployment',
                    'SSO/SAML',
                ]
            ],
        ];

        if (!isset($plans[$id])) {
            return response()->json([
                'success' => false,
                'message' => 'Plan not found'
            ], 404);
        }

        return response()->json([
            'success' => true,
            'data' => $plans[$id]
        ]);
    }
}
