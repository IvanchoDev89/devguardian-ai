<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class EmailService
{
    private $apiKey;
    private $fromEmail;
    private $fromName;

    public function __construct()
    {
        $this->apiKey = config('services.resend.api_key', 're_123456789');
        $this->fromEmail = config('services.resand.from_email', 'DevGuardian AI <security@devguardian.ai>');
        $this->fromName = 'DevGuardian AI';
    }

    public function send(array $to, string $subject, string $html, string $text = null): bool
    {
        try {
            $response = Http::withHeaders([
                'Authorization' => 'Bearer ' . $this->apiKey,
                'Content-Type' => 'application/json',
            ])->post('https://api.resend.com/emails', [
                'from' => $this->fromEmail,
                'to' => $to,
                'subject' => $subject,
                'html' => $html,
                'text' => $text ?? strip_tags($html),
            ]);

            if ($response->successful()) {
                Log::info('Email sent successfully', ['to' => $to, 'subject' => $subject]);
                return true;
            }

            Log::error('Failed to send email', [
                'to' => $to,
                'subject' => $subject,
                'response' => $response->json()
            ]);
            return false;
        } catch (\Exception $e) {
            Log::error('Email service exception', ['error' => $e->getMessage()]);
            return false;
        }
    }

    public function sendWelcome(string $email, string $name): bool
    {
        $subject = 'Welcome to DevGuardian AI';
        $html = $this->getWelcomeTemplate($name);
        return $this->send([$email], $subject, $html);
    }

    public function sendScanComplete(string $email, string $repoName, int $vulnCount): bool
    {
        $subject = "Security Scan Complete: {$repoName}";
        $html = $this->getScanCompleteTemplate($repoName, $vulnCount);
        return $this->send([$email], $subject, $html);
    }

    public function sendVulnerabilityAlert(string $email, string $vulnTitle, string $severity): bool
    {
        $subject = "Critical Vulnerability Alert: {$vulnTitle}";
        $html = $this->getVulnerabilityAlertTemplate($vulnTitle, $severity);
        return $this->send([$email], $subject, $html);
    }

    public function sendPlanUpgrade(string $email, string $planName): bool
    {
        $subject = "You've Upgraded to {$planName}";
        $html = $this->getPlanUpgradeTemplate($planName);
        return $this->send([$email], $subject, $html);
    }

    public function sendPaymentReceipt(string $email, float $amount, string $invoiceId): bool
    {
        $subject = "Payment Receipt - DevGuardian AI";
        $html = $this->getPaymentReceiptTemplate($amount, $invoiceId);
        return $this->send([$email], $subject, $html);
    }

    private function getWelcomeTemplate(string $name): string
    {
        return <<<HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #e2e8f0; padding: 40px 20px;">
    <div style="max-width: 600px; margin: 0 auto; background: #1e293b; border-radius: 16px; padding: 40px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #06b6d4; margin: 0;">🛡️ DevGuardian AI</h1>
        </div>
        <h2 style="color: #fff; margin-top: 0;">Welcome, {$name}!</h2>
        <p style="color: #94a3b8; line-height: 1.6;">
            Thank you for joining DevGuardian AI. We're excited to help you secure your code.
        </p>
        <div style="margin: 30px 0;">
            <a href="https://devguardian.ai/dashboard" style="display: inline-block; background: linear-gradient(135deg, #06b6d4, #3b82f6); color: white; padding: 14px 28px; border-radius: 8px; text-decoration: none; font-weight: 600;">
                Go to Dashboard
            </a>
        </div>
        <p style="color: #64748b; font-size: 14px;">
            Need help? Reply to this email or contact our support team.
        </p>
    </div>
</body>
</html>
HTML;
    }

    private function getScanCompleteTemplate(string $repoName, int $vulnCount): string
    {
        $severityColor = $vulnCount > 0 ? '#ef4444' : '#22c55e';
        $severityText = $vulnCount > 0 ? 'Action Required' : 'All Clear';
        
        return <<<HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #e2e8f0; padding: 40px 20px;">
    <div style="max-width: 600px; margin: 0 auto; background: #1e293b; border-radius: 16px; padding: 40px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #06b6d4; margin: 0;">🛡️ DevGuardian AI</h1>
            <p style="color: #64748b; margin-top: 8px;">Security Scan Complete</p>
        </div>
        <h2 style="color: #fff; margin-top: 0;">Scan Finished: {$repoName}</h2>
        <div style="background: #0f172a; border-radius: 12px; padding: 24px; margin: 20px 0; text-align: center;">
            <p style="color: #94a3b8; margin: 0 0 8px 0; font-size: 14px;">Vulnerabilities Found</p>
            <p style="color: {$severityColor}; font-size: 48px; font-weight: 700; margin: 0;">{$vulnCount}</p>
            <p style="color: {$severityColor}; font-size: 14px; margin: 8px 0 0 0;">{$severityText}</p>
        </div>
        <div style="margin: 30px 0;">
            <a href="https://devguardian.ai/vulnerabilities" style="display: inline-block; background: linear-gradient(135deg, #06b6d4, #3b82f6); color: white; padding: 14px 28px; border-radius: 8px; text-decoration: none; font-weight: 600;">
                View Results
            </a>
        </div>
    </div>
</body>
</html>
HTML;
    }

    private function getVulnerabilityAlertTemplate(string $vulnTitle, string $severity): string
    {
        $color = match($severity) {
            'critical' => '#dc2626',
            'high' => '#ea580c',
            'medium' => '#ca8a04',
            default => '#64748b'
        };
        
        return <<<HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #e2e8f0; padding: 40px 20px;">
    <div style="max-width: 600px; margin: 0 auto; background: #1e293b; border-radius: 16px; padding: 40px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: {$color}; margin: 0;">⚠️ Vulnerability Alert</h1>
        </div>
        <h2 style="color: #fff; margin-top: 0;">{$vulnTitle}</h2>
        <div style="background: {$color}20; border: 1px solid {$color}; border-radius: 8px; padding: 16px; margin: 20px 0;">
            <p style="color: {$color}; font-weight: 600; margin: 0;">Severity: {$severity}</p>
        </div>
        <p style="color: #94a3b8; line-height: 1.6;">
            A new vulnerability was detected in your repository that requires immediate attention.
        </p>
        <div style="margin: 30px 0;">
            <a href="https://devguardian.ai/vulnerabilities" style="display: inline-block; background: {$color}; color: white; padding: 14px 28px; border-radius: 8px; text-decoration: none; font-weight: 600;">
                View Vulnerability
            </a>
        </div>
    </div>
</body>
</html>
HTML;
    }

    private function getPlanUpgradeTemplate(string $planName): string
    {
        return <<<HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #e2e8f0; padding: 40px 20px;">
    <div style="max-width: 600px; margin: 0 auto; background: #1e293b; border-radius: 16px; padding: 40px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #22c55e; margin: 0;">🎉 Plan Upgraded!</h1>
        </div>
        <h2 style="color: #fff; margin-top: 0;">You're now on {$planName}</h2>
        <p style="color: #94a3b8; line-height: 1.6;">
            Thank you for upgrading! You now have access to all the features of the {$planName} plan.
        </p>
        <div style="margin: 30px 0;">
            <a href="https://devguardian.ai/billing" style="display: inline-block; background: linear-gradient(135deg, #22c55e, #16a34a); color: white; padding: 14px 28px; border-radius: 8px; text-decoration: none; font-weight: 600;">
                View Your Plan
            </a>
        </div>
    </div>
</body>
</html>
HTML;
    }

    private function getPaymentReceiptTemplate(float $amount, string $invoiceId): string
    {
        return <<<HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #e2e8f0; padding: 40px 20px;">
    <div style="max-width: 600px; margin: 0 auto; background: #1e293b; border-radius: 16px; padding: 40px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #06b6d4; margin: 0;">💳 Payment Receipt</h1>
        </div>
        <div style="background: #0f172a; border-radius: 12px; padding: 24px; margin: 20px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                <span style="color: #94a3b8;">Amount</span>
                <span style="color: #fff; font-weight: 600;">\$ {$amount}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #94a3b8;">Invoice ID</span>
                <span style="color: #fff; font-family: monospace;">{$invoiceId}</span>
            </div>
        </div>
        <p style="color: #64748b; font-size: 14px;">
            Thank you for your payment. Your subscription is now active.
        </p>
    </div>
</body>
</html>
HTML;
    }
}
