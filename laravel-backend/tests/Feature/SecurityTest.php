<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Illuminate\Support\Facades\Redis;
use App\Core\Application\Services\SecurityLogger;

class SecurityTest extends TestCase
{
    use RefreshDatabase, WithFaker;

    protected function setUp(): void
    {
        parent::setUp();
        
        // Clear Redis before each test
        Redis::flushall();
    }

    /**
     * Test SQL injection prevention.
     */
    public function test_sql_injection_prevention()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        // Attempt SQL injection through API endpoint
        $maliciousInput = "1' OR '1'='1";
        
        $response = $this->postJson('/api/v1/vulnerabilities/scan', [
            'code' => "SELECT * FROM users WHERE id = {$maliciousInput}",
            'language' => 'php'
        ]);

        // Should not return 500 (internal server error)
        $response->assertStatus(200);
        
        // Should detect the SQL injection vulnerability
        $data = $response->json();
        $this->assertArrayHasKey('vulnerabilities', $data);
        
        $sqlInjectionFound = false;
        foreach ($data['vulnerabilities'] as $vulnerability) {
            if ($vulnerability['type'] === 'sql_injection') {
                $sqlInjectionFound = true;
                break;
            }
        }
        
        $this->assertTrue($sqlInjectionFound, 'SQL injection should be detected');
    }

    /**
     * Test XSS prevention.
     */
    public function test_xss_prevention()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        $xssPayload = '<script>alert("XSS")</script>';
        
        $response = $this->postJson('/api/v1/vulnerabilities/scan', [
            'code' => "echo '{$xssPayload}';",
            'language' => 'php'
        ]);

        $response->assertStatus(200);
        
        $data = $response->json();
        $xssFound = false;
        foreach ($data['vulnerabilities'] as $vulnerability) {
            if ($vulnerability['type'] === 'xss') {
                $xssFound = true;
                break;
            }
        }
        
        $this->assertTrue($xssFound, 'XSS should be detected');
    }

    /**
     * Test command injection prevention.
     */
    public function test_command_injection_prevention()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        $commandInjection = '; rm -rf /';
        
        $response = $this->postJson('/api/v1/vulnerabilities/scan', [
            'code' => "exec('ls {$commandInjection}')",
            'language' => 'php'
        ]);

        $response->assertStatus(200);
        
        $data = $response->json();
        $commandInjectionFound = false;
        foreach ($data['vulnerabilities'] as $vulnerability) {
            if ($vulnerability['type'] === 'command_injection') {
                $commandInjectionFound = true;
                break;
            }
        }
        
        $this->assertTrue($commandInjectionFound, 'Command injection should be detected');
    }

    /**
     * Test path traversal prevention.
     */
    public function test_path_traversal_prevention()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        $pathTraversal = '../../../etc/passwd';
        
        $response = $this->postJson('/api/v1/vulnerabilities/scan', [
            'code' => "include('/path/to/file/{$pathTraversal}')",
            'language' => 'php'
        ]);

        $response->assertStatus(200);
        
        $data = $response->json();
        $pathTraversalFound = false;
        foreach ($data['vulnerabilities'] as $vulnerability) {
            if ($vulnerability['type'] === 'path_traversal') {
                $pathTraversalFound = true;
                break;
            }
        }
        
        $this->assertTrue($pathTraversalFound, 'Path traversal should be detected');
    }

    /**
     * Test rate limiting functionality.
     */
    public function test_rate_limiting()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        // Make multiple requests rapidly
        $responses = [];
        for ($i = 0; $i < 65; $i++) { // More than the rate limit
            $responses[] = $this->postJson('/api/v1/vulnerabilities/scan', [
                'code' => 'echo "test";',
                'language' => 'php'
            ]);
        }

        // At least one request should be rate limited
        $rateLimited = false;
        foreach ($responses as $response) {
            if ($response->status() === 429) {
                $rateLimited = true;
                break;
            }
        }

        $this->assertTrue($rateLimited, 'Rate limiting should be enforced');
    }

    /**
     * Test authentication requirements.
     */
    public function test_authentication_required()
    {
        // Test without authentication
        $response = $this->postJson('/api/v1/vulnerabilities/scan', [
            'code' => 'echo "test";',
            'language' => 'php'
        ]);

        $response->assertStatus(401);
    }

    /**
     * Test input validation.
     */
    public function test_input_validation()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        // Test with missing required fields
        $response = $this->postJson('/api/v1/vulnerabilities/scan', [
            // Missing 'code' field
            'language' => 'php'
        ]);

        $response->assertStatus(422);
        
        // Test with invalid language
        $response = $this->postJson('/api/v1/vulnerabilities/scan', [
            'code' => 'echo "test";',
            'language' => 'invalid_language'
        ]);

        $response->assertStatus(422);
    }

    /**
     * Test file upload security.
     */
    public function test_file_upload_security()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        // Test with malicious file content
        $maliciousContent = '<?php system($_GET["cmd"]); ?>';
        
        $response = $this->postJson('/api/v1/vulnerabilities/scan-files', [
            'file' => base64_encode($maliciousContent),
            'filename' => 'malicious.php'
        ]);

        $response->assertStatus(200);
        
        $data = $response->json();
        $maliciousCodeFound = false;
        foreach ($data['vulnerabilities'] as $vulnerability) {
            if (in_array($vulnerability['type'], ['xss', 'command_injection', 'backdoor'])) {
                $maliciousCodeFound = true;
                break;
            }
        }
        
        $this->assertTrue($maliciousCodeFound, 'Malicious file content should be detected');
    }

    /**
     * Test CSRF protection.
     */
    public function test_csrf_protection()
    {
        // Test without CSRF token (web routes)
        $response = $this->post('/vulnerabilities/scan', [
            'code' => 'echo "test";',
            'language' => 'php'
        ]);

        // Should redirect or show CSRF error
        $this->assertContains($response->status(), [419, 302]);
    }

    /**
     * Test security headers.
     */
    public function test_security_headers()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        $response = $this->getJson('/api/v1/vulnerabilities');
        
        // Check for security headers
        $this->assertNotNull($response->headers->get('X-Content-Type-Options'));
        $this->assertNotNull($response->headers->get('X-Frame-Options'));
        $this->assertNotNull($response->headers->get('X-XSS-Protection'));
    }

    /**
     * Test API key validation.
     */
    public function test_api_key_validation()
    {
        $user = User::factory()->create();
        
        // Test with invalid API key
        $response = $this->withHeaders([
            'Authorization' => 'Bearer invalid_token'
        ])->postJson('/api/v1/vulnerabilities/scan', [
            'code' => 'echo "test";',
            'language' => 'php'
        ]);

        $response->assertStatus(401);
    }

    /**
     * Test data sanitization in responses.
     */
    public function test_data_sanitization()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        $xssPayload = '<script>alert("XSS")</script>';
        
        $response = $this->postJson('/api/v1/vulnerabilities/scan', [
            'code' => "echo '{$xssPayload}';",
            'language' => 'php'
        ]);

        $response->assertStatus(200);
        
        // Response should not contain unescaped script tags
        $content = $response->getContent();
        $this->assertStringNotContainsString($content, '<script>');
        $this->assertStringNotContainsString($content, 'alert(');
    }

    /**
     * Test logging of security events.
     */
    public function test_security_logging()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        // Make a request that should trigger security logging
        $this->postJson('/api/v1/vulnerabilities/scan', [
            'code' => 'SELECT * FROM users WHERE id = 1\' OR \'1\'=\'1',
            'language' => 'php'
        ]);

        // Check if security event was logged
        $this->assertTrue(Redis::exists('security_events:' . date('Ymd')));
    }

    /**
     * Test concurrent request handling.
     */
    public function test_concurrent_request_handling()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        // Simulate concurrent requests
        $responses = [];
        for ($i = 0; $i < 10; $i++) {
            $responses[] = $this->postJson('/api/v1/vulnerabilities/scan', [
                'code' => 'echo "test ' . $i . '";',
                'language' => 'php'
            ]);
        }

        // All requests should succeed without race conditions
        foreach ($responses as $response) {
            $response->assertStatus(200);
        }
    }

    /**
     * Test memory usage limits.
     */
    public function test_memory_usage_limits()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        // Test with large input
        $largeInput = str_repeat('A', 1000000); // 1MB string
        
        $response = $this->postJson('/api/v1/vulnerabilities/scan', [
            'code' => $largeInput,
            'language' => 'php'
        ]);

        // Should handle large input gracefully
        $this->assertContains($response->status(), [200, 422]);
    }

    /**
     * Test timeout handling.
     */
    public function test_timeout_handling()
    {
        $user = User::factory()->create();
        $this->actingAs($user);

        // Test with complex code that might take time
        $complexCode = str_repeat('for($i=0;$i<1000;$i++) { echo $i; }', 100);
        
        $response = $this->postJson('/api/v1/vulnerabilities/scan', [
            'code' => $complexCode,
            'language' => 'php'
        ]);

        // Should handle timeout gracefully
        $this->assertContains($response->status(), [200, 408, 422]);
    }
}
