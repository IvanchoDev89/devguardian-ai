<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class BillingController extends Controller
{
    private $stripeKey;
    private $stripeSecret;

    public function __construct()
    {
        $this->stripeKey = config('services.stripe.key');
        $this->stripeSecret = config('services.stripe.secret');
    }

    public function getSubscription(Request $request): JsonResponse
    {
        $userId = $request->user_id ?? 1;

        $subscription = DB::table('subscriptions')
            ->where('user_id', $userId)
            ->first();

        if (!$subscription) {
            $subscription = [
                'plan_id' => 'free',
                'status' => 'active',
                'amount' => 0,
            ];
        }

        return response()->json([
            'success' => true,
            'data' => $subscription
        ]);
    }

    public function createCheckoutSession(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'plan_id' => 'required|in:pro,enterprise',
        ]);

        $plans = [
            'pro' => [
                'name' => 'DevGuardian Pro',
                'price' => 2900,
                'scans' => 1000,
            ],
            'enterprise' => [
                'name' => 'DevGuardian Enterprise',
                'price' => 19900,
                'scans' => 10000,
            ],
        ];

        $plan = $plans[$validated['plan_id']];

        $checkoutId = 'checkout_' . Str::random(32);

        return response()->json([
            'success' => true,
            'data' => [
                'checkout_id' => $checkoutId,
                'url' => 'https://checkout.stripe.com/pay/' . $checkoutId,
                'plan' => $validated['plan_id'],
                'amount' => $plan['price'],
                'currency' => 'usd',
                'description' => $plan['name'] . ' - Monthly Subscription',
            ]
        ]);
    }

    public function createCustomer(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'email' => 'required|email',
            'name' => 'required|string',
        ]);

        $customerId = 'cus_' . Str::random(32);

        DB::table('subscriptions')->updateOrInsert(
            ['user_id' => $request->user_id ?? 1],
            [
                'stripe_customer_id' => $customerId,
                'plan_id' => 'free',
                'status' => 'active',
                'created_at' => now(),
                'updated_at' => now(),
            ]
        );

        return response()->json([
            'success' => true,
            'data' => [
                'customer_id' => $customerId,
            ]
        ]);
    }

    public function changePlan(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'plan_id' => 'required|in:free,pro,enterprise',
        ]);

        $plans = [
            'free' => ['scans' => 100, 'price' => 0],
            'pro' => ['scans' => 1000, 'price' => 29],
            'enterprise' => ['scans' => 10000, 'price' => 199],
        ];

        $plan = $plans[$validated['plan_id']];

        DB::table('subscriptions')
            ->where('user_id', $request->user_id ?? 1)
            ->update([
                'plan_id' => $validated['plan_id'],
                'status' => $validated['plan_id'] === 'free' ? 'active' : 'pending',
                'amount' => $plan['price'],
                'updated_at' => now(),
            ]);

        DB::table('api_keys')
            ->where('user_id', $request->user_id ?? 1)
            ->update([
                'plan' => $validated['plan_id'],
                'monthly_scans_limit' => $plan['scans'],
                'updated_at' => now(),
            ]);

        return response()->json([
            'success' => true,
            'message' => 'Plan changed to ' . $validated['plan_id'],
            'data' => [
                'plan_id' => $validated['plan_id'],
                'scans_included' => $plan['scans'],
                'price' => $plan['price'],
            ]
        ]);
    }

    public function cancelSubscription(Request $request): JsonResponse
    {
        DB::table('subscriptions')
            ->where('user_id', $request->user_id ?? 1)
            ->update([
                'status' => 'canceled',
                'canceled_at' => now(),
                'updated_at' => now(),
            ]);

        return response()->json([
            'success' => true,
            'message' => 'Subscription canceled'
        ]);
    }

    public function getInvoices(Request $request): JsonResponse
    {
        $invoices = DB::table('payments')
            ->where('user_id', $request->user_id ?? 1)
            ->orderByDesc('created_at')
            ->limit(20)
            ->get();

        return response()->json([
            'success' => true,
            'data' => $invoices
        ]);
    }

    public function webhook(Request $request): JsonResponse
    {
        $payload = $request->all();
        $eventType = $payload['type'] ?? '';

        switch ($eventType) {
            case 'checkout.session.completed':
                $this->handleCheckoutComplete($payload);
                break;
            case 'invoice.paid':
                $this->handleInvoicePaid($payload);
                break;
            case 'customer.subscription.deleted':
                $this->handleSubscriptionCanceled($payload);
                break;
        }

        return response()->json(['success' => true]);
    }

    private function handleCheckoutComplete(array $payload): void
    {
        $data = $payload['data']['object'] ?? [];
        $customerId = $data['customer'] ?? null;
        $subscriptionId = $data['subscription'] ?? null;

        if ($customerId) {
            DB::table('subscriptions')
                ->where('stripe_customer_id', $customerId)
                ->update([
                    'stripe_subscription_id' => $subscriptionId,
                    'status' => 'active',
                    'current_period_start' => now(),
                    'current_period_end' => now()->addMonth(),
                    'updated_at' => now(),
                ]);
        }
    }

    private function handleInvoicePaid(array $payload): void
    {
        $data = $payload['data']['object'] ?? [];
        
        DB::table('payments')->insert([
            'user_id' => 1,
            'stripe_invoice_id' => $data['id'] ?? null,
            'stripe_payment_intent_id' => $data['payment_intent'] ?? null,
            'amount' => ($data['amount_paid'] ?? 0) / 100,
            'currency' => $data['currency'] ?? 'usd',
            'status' => 'paid',
            'paid_at' => now(),
            'created_at' => now(),
            'updated_at' => now(),
        ]);
    }

    private function handleSubscriptionCanceled(array $payload): void
    {
        $data = $payload['data']['object'] ?? [];
        $subscriptionId = $data['id'] ?? null;

        DB::table('subscriptions')
            ->where('stripe_subscription_id', $subscriptionId)
            ->update([
                'status' => 'canceled',
                'canceled_at' => now(),
                'updated_at' => now(),
            ]);
    }

    public function getPaymentMethods(Request $request): JsonResponse
    {
        return response()->json([
            'success' => true,
            'data' => []
        ]);
    }

    public function addPaymentMethod(Request $request): JsonResponse
    {
        return response()->json([
            'success' => true,
            'message' => 'Payment method added (demo mode)',
            'data' => [
                'id' => 'pm_' . Str::random(32),
                'brand' => 'visa',
                'last4' => '4242',
                'exp_month' => 12,
                'exp_year' => 2027,
            ]
        ]);
    }
}
