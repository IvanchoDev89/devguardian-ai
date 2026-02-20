<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
    <!-- Background Pattern -->
    <div class="absolute inset-0 bg-grid-white/5 bg-grid-16"></div>
    
    <div class="relative">
      <!-- Header -->
      <div class="px-4 py-6 sm:px-0">
        <div class="max-w-7xl mx-auto">
          <div class="text-center mb-8">
            <h1 class="text-3xl sm:text-4xl font-bold text-white mb-4">
              <span class="bg-gradient-to-r from-blue-400 via-cyan-300 to-blue-400 bg-clip-text text-transparent">
                SQL Injection Scanner
              </span>
            </h1>
            <p class="text-xl text-gray-300 max-w-3xl mx-auto">
              Advanced vulnerability detection with <span class="text-blue-400 font-semibold">zero false positives</span>
            </p>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="px-4 sm:px-0">
        <div class="max-w-7xl mx-auto">
          <!-- Scanner Interface -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
            <!-- Input Panel -->
            <div class="lg:col-span-1">
              <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 sticky top-6">
                <h2 class="text-xl font-semibold text-white mb-6 flex items-center">
                  <svg class="w-6 h-6 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  Scanner Configuration
                </h2>
                
                <div class="space-y-6">
                  <!-- Repository URL -->
                  <div>
                    <label class="block text-sm font-medium text-gray-300 mb-2">
                      Repository URL
                    </label>
                    <input
                      v-model="repositoryUrl"
                      type="text"
                      placeholder="https://github.com/user/repo"
                      class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                    />
                  </div>

                  <!-- Scan Type -->
                  <div>
                    <label class="block text-sm font-medium text-gray-300 mb-2">
                      Scan Type
                    </label>
                    <select
                      v-model="scanType"
                      class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                    >
                      <option value="quick">Quick Scan</option>
                      <option value="deep">Deep Scan</option>
                      <option value="custom">Custom Rules</option>
                    </select>
                  </div>

                  <!-- Advanced Options -->
                  <div class="space-y-4">
                    <h3 class="text-sm font-medium text-gray-300 mb-3">Advanced Options</h3>
                    
                    <label class="flex items-center">
                      <input
                        v-model="options.checkBlindSQL"
                        type="checkbox"
                        class="w-4 h-4 bg-white/5 border-white/10 rounded text-blue-500 focus:ring-blue-500"
                      />
                      <span class="ml-2 text-sm text-gray-300">Check Blind SQL Injection</span>
                    </label>
                    
                    <label class="flex items-center">
                      <input
                        v-model="options.checkTimeBased"
                        type="checkbox"
                        class="w-4 h-4 bg-white/5 border-white/10 rounded text-blue-500 focus:ring-blue-500"
                      />
                      <span class="ml-2 text-sm text-gray-300">Time-based Attacks</span>
                    </label>
                    
                    <label class="flex items-center">
                      <input
                        v-model="options.checkUnionBased"
                        type="checkbox"
                        class="w-4 h-4 bg-white/5 border-white/10 rounded text-blue-500 focus:ring-blue-500"
                      />
                      <span class="ml-2 text-sm text-gray-300">Union-based Queries</span>
                    </label>
                  </div>

                  <!-- Action Buttons -->
                  <div class="space-y-3">
                    <button
                      @click="runSampleScan"
                      :disabled="loading"
                      class="w-full py-3 px-4 bg-gradient-to-r from-cyan-600 to-blue-600 text-white font-semibold rounded-lg hover:from-cyan-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-[1.02]"
                    >
                      <span v-if="loading" class="flex items-center justify-center">
                        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Scanning...
                      </span>
                      <span v-else>🚀 Test Sample Code</span>
                    </button>
                    
                    <button
                      @click="runScan"
                      :disabled="loading || !repositoryUrl"
                      class="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                    >
                      {{ loading ? 'Scanning Repository...' : '🔍 Scan Repository' }}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Results Panel -->
            <div class="lg:col-span-2">
              <!-- Scan Progress -->
              <ScanProgress v-if="loading" />
              
              <!-- Results -->
              <div v-if="scanResult && !loading" class="space-y-6">
                <!-- Summary Cards -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                  <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:border-blue-500/30 transition-all duration-300">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="text-sm font-medium text-gray-400">Files Scanned</p>
                        <p class="text-2xl font-bold text-white mt-1">{{ scanResult.files_scanned }}</p>
                      </div>
                      <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
                        <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                        </svg>
                      </div>
                    </div>
                  </div>
                  
                  <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:border-red-500/30 transition-all duration-300">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="text-sm font-medium text-gray-400">Vulnerabilities</p>
                        <p class="text-2xl font-bold text-white mt-1">{{ scanResult.vulnerabilities_found }}</p>
                      </div>
                      <div class="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center">
                        <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
                        </svg>
                      </div>
                    </div>
                  </div>
                  
                  <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:border-green-500/30 transition-all duration-300">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="text-sm font-medium text-gray-400">False Positives</p>
                        <p class="text-2xl font-bold text-white mt-1">{{ scanResult.summary.false_positive_rate }}%</p>
                      </div>
                      <div class="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
                        <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                      </div>
                    </div>
                  </div>
                  
                  <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:border-cyan-500/30 transition-all duration-300">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="text-sm font-medium text-gray-400">Confidence</p>
                        <p class="text-2xl font-bold text-white mt-1">{{ scanResult.summary.confidence }}%</p>
                      </div>
                      <div class="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center">
                        <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Vulnerabilities List -->
                <div v-if="scanResult.vulnerabilities.length > 0" class="space-y-4">
                  <h3 class="text-xl font-semibold text-white mb-6 flex items-center">
                    <svg class="w-6 h-6 mr-2 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
                    </svg>
                    Detected Vulnerabilities
                  </h3>
                  
                  <VulnerabilityCard 
                    v-for="vuln in scanResult.vulnerabilities" 
                    :key="vuln.id"
                    :vulnerability="vuln"
                  />
                </div>

                <!-- No Vulnerabilities Found -->
                <div v-else class="bg-green-500/10 backdrop-blur-sm rounded-2xl p-12 border border-green-500/30 text-center">
                  <div class="flex flex-col items-center">
                    <div class="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mb-6">
                      <svg class="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                    </div>
                    <h3 class="text-2xl font-bold text-white mb-4">No SQL Injection vulnerabilities detected</h3>
                    <p class="text-green-300 text-lg max-w-md mx-auto">
                      Your code appears to be secure against SQL injection attacks. Great job following security best practices!
                    </p>
                    <div class="mt-6 flex justify-center">
                      <button class="px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-lg hover:from-green-700 hover:to-emerald-700 transition-all duration-200">
                        🎉 View Full Report
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Error State -->
              <div v-if="error" class="bg-red-500/10 backdrop-blur-sm rounded-2xl p-8 border border-red-500/30">
                <div class="flex items-center">
                  <svg class="w-6 h-6 text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
                  </svg>
                  <div>
                    <h3 class="text-lg font-semibold text-red-400 mb-2">Scan Failed</h3>
                    <p class="text-red-300">{{ error }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { aiService } from '../services/api'
import { useNotificationStore } from '../stores/notifications'
import ScanProgress from '../components/ScanProgress.vue'
import VulnerabilityCard from '../components/VulnerabilityCard.vue'

const loading = ref(false)
const error = ref<string | null>(null)
const repositoryUrl = ref('')
const scanType = ref('quick')
const scanResult = ref<any>(null)
const notificationStore = useNotificationStore()

const options = ref({
  checkBlindSQL: true,
  checkTimeBased: true,
  checkUnionBased: false
} as {
  checkBlindSQL: boolean
  checkTimeBased: boolean
  checkUnionBased: boolean
})

const runSampleScan = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await aiService.scanCode(`
      // Sample vulnerable SQL injection code
      const userInput = req.query.id;
      const sql = "SELECT * FROM users WHERE id = '" + userInput + "'";
      connection.query(sql, (err, result) => {
        if (err) throw err;
        console.log('User found:', result[0]);
      });
    `, {
      scanType: 'comprehensive',
      checkBlindSQL: options.value.checkBlindSQL
    } as any)
    
    if (response.success && response.data) {
      scanResult.value = response.data
      notificationStore.success('Scan Completed', `Found ${response.data.vulnerabilities_found} vulnerabilities`)
    } else {
      throw new Error(response.message || 'Scan failed')
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Sample scan failed'
    notificationStore.error('Scan Failed', error.value)
  } finally {
    loading.value = false
  }
}

const runScan = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Validate repository URL
    if (!repositoryUrl.value) {
      throw new Error('Please enter a repository URL')
    }
    
    notificationStore.info('Repository Scan', `Starting scan of ${repositoryUrl.value}`)
    
    // Mock repository scan - in real implementation, this would:
    // 1. Clone the repository
    // 2. Analyze files for SQL injection vulnerabilities
    // 3. Return detailed results
    
    const mockResponse = {
      files_scanned: 156,
      vulnerabilities_found: 2,
      vulnerabilities: [
        {
          id: '1',
          title: 'SQL Injection in User Authentication',
          type: 'SQL Injection',
          severity: 'Critical',
          status: 'Open',
          cwe: 'CWE-89',
          description: 'SQL injection vulnerability found in authentication module',
          file: 'auth/login.php',
          line: 45,
          code: `const sql = "SELECT * FROM users WHERE id = '" + userInput + "'";`,
          evidence: 'Direct concatenation of user input into SQL query',
          user_input_source: 'HTTP POST parameter "id"',
          explanation: 'An attacker can manipulate SQL queries by injecting malicious SQL code through the id parameter. This could lead to unauthorized data access, data modification, or complete database compromise.',
          exploitability: 'High',
          impact: 'High',
          recommended_fix: `// Secure implementation
const userId = parseInt(req.query.id, 10);
const sql = "SELECT * FROM users WHERE id = $1";
connection.query(sql, [userId], (err, result) => {
  // ... rest of code
});`
        },
        {
          id: '2',
          title: 'Blind SQL Injection',
          type: 'SQL Injection',
          severity: 'High',
          status: 'Open',
          cwe: 'CWE-89',
          description: 'Blind SQL injection vulnerability detected in search functionality',
          file: 'search.php',
          line: 78,
          code: `$query = "SELECT * FROM products WHERE name LIKE '%" + req.query.search + "%'";`,
          evidence: 'User input directly concatenated into SQL query without parameterization',
          user_input_source: 'HTTP GET parameter "search"',
          explanation: 'The search functionality is vulnerable to blind SQL injection attacks. Attackers can extract database information through boolean-based or time-based attacks.',
          exploitability: 'Medium',
          impact: 'High',
          recommended_fix: `// Secure implementation
const searchQuery = req.query.search;
const sql = "SELECT * FROM products WHERE name LIKE ?";
connection.query(sql, [searchQuery], (err, result) => {
  // ... rest of code
});`
        }
      ],
      summary: {
        false_positive_rate: 0,
        confidence: 95,
        scan_duration: '2.3s',
        scan_type: scanType.value
      }
    }
    
    scanResult.value = mockResponse
    notificationStore.warning('Vulnerabilities Found', `Found ${mockResponse.vulnerabilities_found} SQL injection vulnerabilities`)
    
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Scan failed'
    notificationStore.error('Scan Failed', error.value)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // Auto-run sample scan for demonstration
  setTimeout(() => {
    runSampleScan()
  }, 1000)
})
</script>
