<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
    <Navbar />
    
    <div class="max-w-6xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-white mb-2">
          🔍 Vulnerability Scanner
        </h1>
        <p class="text-gray-400">Paste your code and discover security issues in seconds</p>
        
        <div class="mt-4 inline-flex items-center px-4 py-2 rounded-full bg-gray-800/50 border border-gray-700">
          <span 
            class="w-2 h-2 rounded-full mr-2"
            :class="serviceStatus.class === 'online' ? 'bg-green-500' : 'bg-red-500'"
          ></span>
          <span class="text-sm text-gray-300">{{ serviceStatus.text }}</span>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Input Panel -->
        <div class="lg:col-span-2 space-y-4">
          <!-- Language Selector -->
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-gray-300">Programming Language</label>
            <select 
              v-model="selectedLanguage"
              class="bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="typescript">TypeScript</option>
              <option value="java">Java</option>
              <option value="php">PHP</option>
              <option value="go">Go</option>
              <option value="rust">Rust</option>
              <option value="csharp">C#</option>
            </select>
          </div>

          <!-- Code Input -->
          <div class="relative">
            <textarea
              v-model="code"
              class="w-full h-80 bg-gray-800/50 border border-gray-700 rounded-xl p-4 text-gray-100 font-mono text-sm resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-500"
              :disabled="isLoading"
              placeholder="// Paste your code here...

Example:
password = 'my_password'
query = f'SELECT * FROM users WHERE id = {user_id}'"
              spellcheck="false"
            ></textarea>
            
            <div v-if="code" class="absolute bottom-4 right-4 text-xs text-gray-500">
              {{ code.length }} characters
            </div>
          </div>

          <!-- Actions -->
          <div class="flex gap-3">
            <button 
              class="flex-1 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-blue-700 hover:to-cyan-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center gap-2"
              :disabled="isLoading || !code.trim()"
              @click="handleAnalyze"
            >
              <span v-if="isLoading" class="animate-spin">⏳</span>
              <span v-else>🔍</span>
              {{ isLoading ? 'Analyzing...' : 'Scan Code' }}
            </button>
            <button 
              class="px-6 py-3 bg-gray-800 border border-gray-700 text-gray-300 rounded-xl hover:bg-gray-700 transition-colors"
              @click="clearCode"
            >
              Clear
            </button>
          </div>

          <!-- Error -->
          <div v-if="error" class="bg-red-500/10 border border-red-500/20 rounded-xl p-4 flex items-center gap-3">
            <span class="text-red-400">⚠️</span>
            <p class="text-red-400 text-sm">{{ error }}</p>
          </div>
        </div>

        <!-- Results Panel -->
        <div class="space-y-4">
          <!-- Score Card -->
          <div v-if="analysisResult" class="bg-gray-800/50 border border-gray-700 rounded-xl p-6">
            <div class="text-center">
              <div 
                class="text-5xl font-bold mb-2"
                :class="{
                  'text-green-400': analysisResult.score >= 80,
                  'text-yellow-400': analysisResult.score >= 50 && analysisResult.score < 80,
                  'text-red-400': analysisResult.score < 50
                }"
              >
                {{ analysisResult.score }}
              </div>
              <div class="text-gray-400 text-sm">Security Score</div>
              
              <div class="mt-4 flex justify-center gap-2">
                <span 
                  v-if="analysisResult.total_vulnerabilities > 0"
                  class="px-3 py-1 bg-red-500/20 text-red-400 rounded-full text-xs"
                >
                  {{ analysisResult.total_vulnerabilities }} Issues
                </span>
                <span 
                  v-else
                  class="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-xs"
                >
                  No Issues
                </span>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="bg-gray-800/50 border border-gray-700 rounded-xl p-6 text-center">
            <div class="text-4xl mb-3">🛡️</div>
            <p class="text-gray-400 text-sm">Enter code and click Scan to analyze</p>
          </div>

          <!-- AI Fix Button -->
          <button 
            v-if="analysisResult?.vulnerabilities?.length"
            class="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all duration-200 flex items-center justify-center gap-2"
            :disabled="isAnalyzing"
            @click="analyzeWithLLM"
          >
            <span v-if="isAnalyzing">⏳</span>
            <span v-else>🤖</span>
            {{ isAnalyzing ? 'Analyzing...' : 'AI Fix Suggestions' }}
          </button>

          <!-- Vulnerabilities List -->
          <div v-if="analysisResult?.vulnerabilities?.length" class="bg-gray-800/50 border border-gray-700 rounded-xl overflow-hidden">
            <div class="px-4 py-3 border-b border-gray-700 bg-gray-800/80">
              <h3 class="text-white font-semibold">Vulnerabilities Found</h3>
            </div>
            <div class="max-h-96 overflow-y-auto">
              <div 
                v-for="(vuln, index) in analysisResult.vulnerabilities" 
                :key="index"
                class="px-4 py-3 border-b border-gray-700/50 hover:bg-gray-700/30"
              >
                <div class="flex items-start gap-3">
                  <span 
                    class="px-2 py-0.5 rounded text-xs font-medium"
                    :class="{
                      'bg-red-500/20 text-red-400': vuln.severity === 'critical',
                      'bg-orange-500/20 text-orange-400': vuln.severity === 'high',
                      'bg-yellow-500/20 text-yellow-400': vuln.severity === 'medium',
                      'bg-blue-500/20 text-blue-400': vuln.severity === 'low'
                    }"
                  >
                    {{ vuln.severity }}
                  </span>
                  <div class="flex-1 min-w-0">
                    <p class="text-white text-sm font-medium">{{ vuln.vulnerability_type }}</p>
                    <p class="text-gray-400 text-xs mt-1">{{ vuln.description }}</p>
                    <p v-if="vuln.line_number" class="text-gray-500 text-xs mt-1">Line {{ vuln.line_number }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- AI Results -->
          <div v-if="llmResults.length" class="bg-gray-800/50 border border-gray-700 rounded-xl overflow-hidden">
            <div class="px-4 py-3 border-b border-gray-700 bg-purple-800/30">
              <h3 class="text-white font-semibold">🤖 AI Analysis</h3>
            </div>
            <div class="p-4 space-y-3">
              <div 
                v-for="(result, index) in llmResults" 
                :key="index"
                class="bg-purple-500/10 border border-purple-500/20 rounded-lg p-3"
              >
                <p class="text-gray-200 text-sm">{{ result.explanation }}</p>
                <pre v-if="result.suggested_fix" class="mt-2 bg-gray-900/50 rounded p-2 text-xs text-green-400 overflow-x-auto">{{ result.suggested_fix }}</pre>
              </div>
            </div>
          </div>

          <!-- No Vulnerabilities -->
          <div v-if="analysisResult && !analysisResult.vulnerabilities.length" class="bg-green-500/10 border border-green-500/20 rounded-xl p-6 text-center">
            <div class="text-4xl mb-3">✅</div>
            <p class="text-green-400 font-semibold">Code is Secure!</p>
            <p class="text-gray-400 text-sm mt-1">No vulnerabilities detected</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { vulnerabilityScannerApi, llmAnalyzerApi } from '../services/api'
import Navbar from '../components/Navbar.vue'

const code = ref('')
const selectedLanguage = ref('python')
const isLoading = ref(false)
const isAnalyzing = ref(false)
const error = ref('')
const analysisResult = ref<any>(null)
const llmResults = ref<any[]>([])
const serviceStatus = ref({ text: 'Checking...', class: '' })

onMounted(async () => {
  try {
    const h = await vulnerabilityScannerApi.checkHealth()
    serviceStatus.value = { 
      text: h.status === 'ok' ? 'Scanner Online' : 'Scanner Offline', 
      class: h.status === 'ok' ? 'online' : 'offline' 
    }
  } catch { 
    serviceStatus.value = { text: 'Scanner Error', class: 'offline' } 
  }
})

const scoreClass = computed(() => {
  if (!analysisResult.value) return ''
  if (analysisResult.value.score >= 80) return 'good'
  if (analysisResult.value.score >= 50) return 'medium'
  return 'poor'
})

async function handleAnalyze() {
  error.value = ''
  llmResults.value = []
  if (!code.value.trim()) { error.value = 'Please enter code'; return }
  
  isLoading.value = true
  try {
    analysisResult.value = await vulnerabilityScannerApi.analyzeCode(code.value, selectedLanguage.value)
    
    // Save scan count
    const count = parseInt(localStorage.getItem('scans_count') || '0')
    localStorage.setItem('scans_count', String(count + 1))
    
    // Save vuln count
    const vulnCount = parseInt(localStorage.getItem('vuln_count') || '0')
    localStorage.setItem('vuln_count', String(vulnCount + (analysisResult.value.total_vulnerabilities || 0)))
  } catch (e) { 
    error.value = String(e) 
  }
  finally { 
    isLoading.value = false 
  }
}

function clearCode() {
  code.value = ''
  analysisResult.value = null
  llmResults.value = []
  error.value = ''
}

async function analyzeWithLLM() {
  if (!analysisResult.value?.vulnerabilities?.length) return
  
  isAnalyzing.value = true
  error.value = ''
  llmResults.value = []
  
  try {
    for (const vuln of analysisResult.value.vulnerabilities) {
      const result = await llmAnalyzerApi.analyzeVulnerability(
        {
          type: vuln.vulnerability_type || vuln.type || 'unknown',
          severity: vuln.severity || 'medium',
          message: vuln.description || vuln.message || '',
          line_content: vuln.line_content
        },
        code.value,
        selectedLanguage.value,
        true
      )
      
      if (result) {
        llmResults.value.push(result)
      }
    }
  } catch (e) { 
    console.error('AI analysis error:', e)
    error.value = 'AI analysis failed. Try again.'
  }
  finally { 
    isAnalyzing.value = false 
  }
}
</script>
