<template>
  <div class="min-h-screen bg-gray-900 text-gray-100">
    <Navbar />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-white mb-4">API Documentation</h1>
        <p class="text-xl text-gray-400 max-w-3xl mx-auto">
          Integrate DevGuardian AI into your applications with our powerful REST API
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Sidebar -->
        <div class="lg:col-span-1">
          <nav class="sticky top-24 space-y-2">
            <a v-for="section in sections" :key="section.id" 
               :href="`#${section.id}`"
               class="block px-4 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
               :class="{ 'text-cyan-400 bg-white/10': activeSection === section.id }"
               @click="activeSection = section.id"
            >
              {{ section.title }}
            </a>
          </nav>
        </div>

        <!-- Content -->
        <div class="lg:col-span-3 space-y-12">
          <!-- Authentication -->
          <section id="authentication">
            <h2 class="text-3xl font-bold text-white mb-4">Authentication</h2>
            <p class="text-gray-400 mb-6">
              All API requests require authentication using an API key. Include your key in the request header.
            </p>
            
            <div class="bg-gray-800 rounded-xl p-6 border border-white/10">
              <h3 class="text-lg font-semibold text-white mb-4">Request Headers</h3>
              <pre class="bg-gray-900 rounded-lg p-4 overflow-x-auto text-sm text-cyan-400 font-mono">Authorization: Bearer YOUR_API_KEY
Content-Type: application/json</pre>
            </div>

            <div class="mt-6 bg-blue-900/20 border border-blue-500/30 rounded-xl p-6">
              <div class="flex items-start">
                <svg class="w-6 h-6 text-blue-400 mr-3 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <div>
                  <h4 class="font-semibold text-blue-400">API Key Security</h4>
                  <p class="text-gray-400 text-sm mt-1">
                    Keep your API keys secure. Never expose them in client-side code or public repositories.
                  </p>
                </div>
              </div>
            </div>
          </section>

          <!-- Endpoints -->
          <section id="endpoints">
            <h2 class="text-3xl font-bold text-white mb-4">API Endpoints</h2>
            
            <!-- Scan Code -->
            <div class="bg-gray-800 rounded-xl p-6 border border-white/10 mb-6">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                  <span class="bg-green-600 text-white text-xs font-bold px-2 py-1 rounded mr-3">POST</span>
                  <h3 class="text-lg font-semibold text-white">/api/v1/scan</h3>
                </div>
                <span class="text-gray-500 text-sm">Scan code for vulnerabilities</span>
              </div>
              
              <p class="text-gray-400 mb-4">Submit code for security analysis</p>
              
              <h4 class="text-sm font-semibold text-gray-300 mb-2">Request Body</h4>
              <pre class="bg-gray-900 rounded-lg p-4 overflow-x-auto text-sm text-cyan-400 font-mono mb-4">{
  "code": "SELECT * FROM users WHERE id = " + userId,
  "language": "python",
  "scan_type": "sql_injection"
}</pre>

              <h4 class="text-sm font-semibold text-gray-300 mb-2">Response</h4>
              <pre class="bg-gray-900 rounded-lg p-4 overflow-x-auto text-sm text-cyan-400 font-mono">{
  "success": true,
  "vulnerabilities": [
    {
      "type": "sql_injection",
      "severity": "high",
      "line": 1,
      "message": "Potential SQL injection vulnerability",
      "fix": "Use parameterized queries"
    }
  ],
  "credits_used": 1
}</pre>
            </div>

            <!-- Get Scan Results -->
            <div class="bg-gray-800 rounded-xl p-6 border border-white/10 mb-6">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                  <span class="bg-blue-600 text-white text-xs font-bold px-2 py-1 rounded mr-3">GET</span>
                  <h3 class="text-lg font-semibold text-white">/api/v1/scans/{id}</h3>
                </div>
                <span class="text-gray-500 text-sm">Get scan results</span>
              </div>
              
              <h4 class="text-sm font-semibold text-gray-300 mb-2">Response</h4>
              <pre class="bg-gray-900 rounded-lg p-4 overflow-x-auto text-sm text-cyan-400 font-mono">{
  "id": "scan_123",
  "status": "completed",
  "vulnerabilities": [...],
  "created_at": "2024-01-15T10:30:00Z"
}</pre>
            </div>

            <!-- Get Credits -->
            <div class="bg-gray-800 rounded-xl p-6 border border-white/10 mb-6">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                  <span class="bg-blue-600 text-white text-xs font-bold px-2 py-1 rounded mr-3">GET</span>
                  <h3 class="text-lg font-semibold text-white">/api/v1/credits</h3>
                </div>
                <span class="text-gray-500 text-sm">Check remaining credits</span>
              </div>
              
              <h4 class="text-sm font-semibold text-gray-300 mb-2">Response</h4>
              <pre class="bg-gray-900 rounded-lg p-4 overflow-x-auto text-sm text-cyan-400 font-mono">{
  "credits": 950,
  "total_used": 50,
  "subscription_tier": "pro"
}</pre>
            </div>

            <!-- GitHub Integration -->
            <div class="bg-gray-800 rounded-xl p-6 border border-white/10 mb-6">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                  <span class="bg-purple-600 text-white text-xs font-bold px-2 py-1 rounded mr-3">POST</span>
                  <h3 class="text-lg font-semibold text-white">/api/v1/github/scan</h3>
                </div>
                <span class="text-gray-500 text-sm">Scan GitHub repository</span>
              </div>
              
              <h4 class="text-sm font-semibold text-gray-300 mb-2">Request Body</h4>
              <pre class="bg-gray-900 rounded-lg p-4 overflow-x-auto text-sm text-cyan-400 font-mono mb-4">{
  "repository": "owner/repo-name",
  "branch": "main",
  "scan_types": ["sql_injection", "xss", "secrets"]
}</pre>
            </div>
          </section>

          <!-- Rate Limits -->
          <section id="rate-limits">
            <h2 class="text-3xl font-bold text-white mb-4">Rate Limits</h2>
            <p class="text-gray-400 mb-6">
              API requests are rate-limited based on your subscription tier.
            </p>
            
            <div class="overflow-x-auto">
              <table class="w-full text-left">
                <thead>
                  <tr class="border-b border-white/10">
                    <th class="py-3 px-4 text-gray-400 font-semibold">Tier</th>
                    <th class="py-3 px-4 text-gray-400 font-semibold">Requests/min</th>
                    <th class="py-3 px-4 text-gray-400 font-semibold">Daily Credits</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-white/10">
                  <tr>
                    <td class="py-3 px-4 text-white">Free</td>
                    <td class="py-3 px-4 text-gray-400">10</td>
                    <td class="py-3 px-4 text-gray-400">50</td>
                  </tr>
                  <tr>
                    <td class="py-3 px-4 text-white">Pro</td>
                    <td class="py-3 px-4 text-gray-400">60</td>
                    <td class="py-3 px-4 text-gray-400">1,000</td>
                  </tr>
                  <tr>
                    <td class="py-3 px-4 text-white">Enterprise</td>
                    <td class="py-3 px-4 text-gray-400">300</td>
                    <td class="py-3 px-4 text-gray-400">Unlimited</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- Error Codes -->
          <section id="errors">
            <h2 class="text-3xl font-bold text-white mb-4">Error Codes</h2>
            
            <div class="overflow-x-auto">
              <table class="w-full text-left">
                <thead>
                  <tr class="border-b border-white/10">
                    <th class="py-3 px-4 text-gray-400 font-semibold">Code</th>
                    <th class="py-3 px-4 text-gray-400 font-semibold">Message</th>
                    <th class="py-3 px-4 text-gray-400 font-semibold">Description</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-white/10">
                  <tr>
                    <td class="py-3 px-4 text-red-400 font-mono">401</td>
                    <td class="py-3 px-4 text-white">Unauthorized</td>
                    <td class="py-3 px-4 text-gray-400">Invalid or missing API key</td>
                  </tr>
                  <tr>
                    <td class="py-3 px-4 text-red-400 font-mono">403</td>
                    <td class="py-3 px-4 text-white">Forbidden</td>
                    <td class="py-3 px-4 text-gray-400">Insufficient credits or permissions</td>
                  </tr>
                  <tr>
                    <td class="py-3 px-4 text-red-400 font-mono">429</td>
                    <td class="py-3 px-4 text-white">Too Many Requests</td>
                    <td class="py-3 px-4 text-gray-400">Rate limit exceeded</td>
                  </tr>
                  <tr>
                    <td class="py-3 px-4 text-red-400 font-mono">500</td>
                    <td class="py-3 px-4 text-white">Server Error</td>
                    <td class="py-3 px-4 text-gray-400">Internal server error</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- SDKs -->
          <section id="sdks">
            <h2 class="text-3xl font-bold text-white mb-4">SDKs & Libraries</h2>
            <p class="text-gray-400 mb-6">
              Official SDKs for easy integration
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-gray-800 rounded-xl p-6 border border-white/10">
                <div class="flex items-center mb-3">
                  <svg class="w-8 h-8 text-yellow-400 mr-3" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm-2.917 16.083c-2.258 0-4.083-1.825-4.083-4.083s1.825-4.083 4.083-4.083c1.103 0 2.024.402 2.735 1.067l-1.107 1.068c-.304-.292-.834-.63-1.628-.63-1.394 0-2.531 1.155-2.531 2.579 0 1.424 1.138 2.579 2.531 2.579 1.616 0 2.224-1.162 2.316-1.762h-2.316v-1.4h3.855c.036.204.064.408.064.677.001 2.332-1.563 3.988-3.919 3.988zm4.155-1.151c-.322.522-.773.869-1.31 1.018v1.035h-1.988v-1.035c-.829-.22-1.595-.776-1.875-1.711h3.551c-.028.45-.378.693-.751.693zm.378-2.115h-2.533v1.262h2.305c.538.001.938-.38.938-.631-.001-.251-.401-.631-.71-.631z"/>
                  </svg>
                  <h3 class="text-lg font-semibold text-white">Python</h3>
                </div>
                <code class="text-sm text-gray-400">pip install devguardian-sdk</code>
              </div>
              
              <div class="bg-gray-800 rounded-xl p-6 border border-white/10">
                <div class="flex items-center mb-3">
                  <svg class="w-8 h-8 text-blue-400 mr-3" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                  </svg>
                  <h3 class="text-lg font-semibold text-white">JavaScript / Node.js</h3>
                </div>
                <code class="text-sm text-gray-400">npm install @devguardian/sdk</code>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>

    <!-- CTA -->
    <div class="bg-gradient-to-r from-cyan-600 to-blue-600 py-16 mt-12">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold text-white mb-4">Ready to get started?</h2>
        <p class="text-xl text-white/80 mb-8">
          Start securing your code today with our powerful API
        </p>
        <div class="flex justify-center gap-4">
          <router-link to="/signup" class="bg-white text-cyan-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
            Get API Key
          </router-link>
          <router-link to="/pricing" class="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white/10 transition-colors">
            View Pricing
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Navbar from '../components/Navbar.vue'

const activeSection = ref('authentication')

const sections = [
  { id: 'authentication', title: 'Authentication' },
  { id: 'endpoints', title: 'API Endpoints' },
  { id: 'rate-limits', title: 'Rate Limits' },
  { id: 'errors', title: 'Error Codes' },
  { id: 'sdks', title: 'SDKs & Libraries' }
]
</script>
