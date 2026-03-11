<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-gray-900">
    <!-- Animated Background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative max-w-7xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="text-center mb-10">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl mb-4 shadow-lg shadow-blue-500/25">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
        </div>
        <h1 class="text-4xl font-bold text-white mb-3 bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
          Vulnerability Scanner
        </h1>
        <p class="text-gray-400 text-lg max-w-2xl mx-auto">
          AI-powered security analysis. Paste your code and discover vulnerabilities in seconds.
        </p>
        
        <!-- Status Bar -->
        <div class="mt-6 flex flex-wrap justify-center gap-3">
          <div class="flex items-center gap-2 px-4 py-2 rounded-full bg-gray-800/60 backdrop-blur border border-gray-700/50">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75" :class="serviceOnline ? 'bg-green-400' : 'bg-red-400'"></span>
              <span class="relative inline-flex rounded-full h-2 w-2" :class="serviceOnline ? 'bg-green-500' : 'bg-red-500'"></span>
            </span>
            <span class="text-sm" :class="serviceOnline ? 'text-green-400' : 'text-red-400'">
              {{ serviceOnline ? 'Scanner Online' : 'Scanner Offline' }}
            </span>
          </div>
          
          <div class="flex items-center gap-2 px-4 py-2 rounded-full bg-gray-800/60 backdrop-blur border border-gray-700/50">
            <svg class="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            <span class="text-sm text-gray-300">
              <span class="text-cyan-400 font-semibold">{{ scansUsed }}</span> / {{ scansQuota }} scans
            </span>
          </div>

          <div v-if="lastScanTime" class="flex items-center gap-2 px-4 py-2 rounded-full bg-gray-800/60 backdrop-blur border border-gray-700/50">
            <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span class="text-sm text-gray-400">Last: {{ lastScanTime }}</span>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <!-- Left Panel - Code Input -->
        <div class="lg:col-span-7 space-y-4">
          <!-- Language Selector -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <label class="text-sm font-medium text-gray-300">Language</label>
              <div class="relative">
                <select 
                  v-model="selectedLanguage"
                  class="appearance-none bg-gray-800/80 border border-gray-600/50 rounded-xl px-4 py-2.5 pr-10 text-white text-sm font-medium focus:ring-2 focus:ring-blue-500 focus:border-transparent cursor-pointer backdrop-blur"
                >
                  <option value="python">🐍 Python</option>
                  <option value="javascript">📜 JavaScript</option>
                  <option value="typescript">💎 TypeScript</option>
                  <option value="java">☕ Java</option>
                  <option value="php">🐘 PHP</option>
                  <option value="go">🔵 Go</option>
                  <option value="rust">🦀 Rust</option>
                  <option value="csharp">🔷 C#</option>
                  <option value="ruby">💎 Ruby</option>
                  <option value="cpp">⚡ C++</option>
                </select>
                <svg class="w-4 h-4 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </div>
            </div>
            <div v-if="code" class="text-sm text-gray-500">
              {{ code.length.toLocaleString() }} characters
            </div>
          </div>

          <!-- Code Editor -->
          <div class="relative group">
            <div class="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="relative bg-gray-800/80 backdrop-blur border border-gray-700/50 rounded-2xl overflow-hidden">
              <!-- Editor Header -->
              <div class="flex items-center justify-between px-4 py-3 bg-gray-900/50 border-b border-gray-700/50">
                <div class="flex items-center gap-2">
                  <div class="flex gap-1.5">
                    <span class="w-3 h-3 rounded-full bg-red-500/80"></span>
                    <span class="w-3 h-3 rounded-full bg-yellow-500/80"></span>
                    <span class="w-3 h-3 rounded-full bg-green-500/80"></span>
                  </div>
                  <span class="text-xs text-gray-500 ml-2">code.{{ languageExtensions[selectedLanguage] }}</span>
                </div>
                <button 
                  v-if="code" 
                  @click="clearCode"
                  class="text-xs text-gray-500 hover:text-red-400 transition-colors"
                >
                  Clear ✕
                </button>
              </div>
              
              <!-- Code Textarea -->
              <textarea
                v-model="code"
                class="w-full h-96 bg-transparent text-gray-100 font-mono text-sm p-4 resize-none focus:outline-none"
                :disabled="isLoading"
                :class="{'opacity-50': isLoading}"
                placeholder="Paste your code here to analyze for security vulnerabilities...

Example:
import os
password = 'admin123'  # Hardcoded password
os.system('rm -rf ' + user_input)  # Command injection
eval(user_input)  # Code injection"
                spellcheck="false"
              ></textarea>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3">
            <button 
              class="flex-1 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40"
              :disabled="isLoading || !code.trim()"
              @click="handleAnalyze"
            >
              <svg v-if="!isLoading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isLoading ? 'Analyzing Code...' : 'Start Security Scan' }}
            </button>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="flex items-center gap-3 px-4 py-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400">
            <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span class="text-sm">{{ error }}</span>
          </div>
        </div>

        <!-- Right Panel - Results -->
        <div class="lg:col-span-5 space-y-4">
          <!-- Loading State -->
          <div v-if="isLoading" class="bg-gray-800/80 backdrop-blur border border-gray-700/50 rounded-2xl p-8 text-center">
            <div class="relative w-24 h-24 mx-auto mb-4">
              <div class="absolute inset-0 border-4 border-blue-500/20 rounded-full"></div>
              <div class="absolute inset-0 border-4 border-transparent border-t-blue-500 rounded-full animate-spin"></div>
              <div class="absolute inset-2 flex items-center justify-center">
                <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
              </div>
            </div>
            <h3 class="text-white font-semibold text-lg mb-2">Analyzing Code</h3>
            <p class="text-gray-400 text-sm">Our AI is scanning for security vulnerabilities...</p>
            <div class="mt-4 flex justify-center gap-1">
              <span class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
              <span class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
              <span class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else-if="!analysisResult" class="bg-gray-800/80 backdrop-blur border border-gray-700/50 rounded-2xl p-8 text-center">
            <div class="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-gray-700 to-gray-600 rounded-2xl flex items-center justify-center">
              <svg class="w-10 h-10 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <h3 class="text-white font-semibold text-lg mb-2">Ready to Scan</h3>
            <p class="text-gray-400 text-sm">Paste your code and click scan to analyze for vulnerabilities</p>
          </div>

          <!-- Results - Score Card -->
          <div v-else class="bg-gray-800/80 backdrop-blur border border-gray-700/50 rounded-2xl overflow-hidden">
            <div class="p-6 text-center" :class="scoreBgClass">
              <div class="relative inline-block mb-4">
                <svg class="w-32 h-32 transform -rotate-90">
                  <circle cx="64" cy="64" r="56" stroke="currentColor" stroke-width="8" fill="none" class="text-gray-700"/>
                  <circle 
                    cx="64" cy="64" r="56" 
                    stroke="currentColor" 
                    stroke-width="8" 
                    fill="none" 
                    class="transition-all duration-1000"
                    :stroke-dasharray="circumference"
                    :stroke-dashoffset="dashOffset"
                    :class="scoreColorClass"
                  />
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                  <span class="text-4xl font-bold" :class="scoreTextClass">
                    {{ analysisResult.score }}
                  </span>
                </div>
              </div>
              <div class="text-lg font-semibold" :class="scoreLabelClass">
                {{ scoreLabel }}
              </div>
              <div class="mt-3 flex justify-center gap-2">
                <span 
                  class="px-3 py-1 rounded-full text-xs font-medium"
                  :class="analysisResult.total_vulnerabilities > 0 ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'"
                >
                  {{ analysisResult.total_vulnerabilities }} {{ analysisResult.total_vulnerabilities === 1 ? 'Issue' : 'Issues' }}
                </span>
              </div>
            </div>
          </div>

          <!-- AI Fix Button -->
          <button 
            v-if="analysisResult?.vulnerabilities?.length && !isAnalyzing"
            class="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 flex items-center justify-center gap-2 shadow-lg shadow-purple-500/25"
            @click="analyzeWithLLM"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
            </svg>
            Get AI Fix Suggestions
          </button>

          <!-- Vulnerabilities List -->
          <div v-if="analysisResult?.vulnerabilities?.length" class="bg-gray-800/80 backdrop-blur border border-gray-700/50 rounded-2xl overflow-hidden">
            <div class="px-4 py-3 bg-gray-900/50 border-b border-gray-700/50 flex items-center justify-between">
              <h3 class="text-white font-semibold">Vulnerabilities</h3>
              <span class="text-xs text-gray-500">{{ analysisResult.vulnerabilities.length }} found</span>
            </div>
            <div class="max-h-96 overflow-y-auto">
              <div 
                v-for="(vuln, index) in analysisResult.vulnerabilities" 
                :key="index"
                class="px-4 py-4 border-b border-gray-700/30 hover:bg-gray-700/20 transition-colors"
              >
                <div class="flex items-start gap-3">
                  <div 
                    class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                    :class="severityBgClass(vuln.severity)"
                  >
                    <svg class="w-4 h-4" :class="severityIconClass(vuln.severity)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
                    </svg>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 mb-1">
                      <span 
                        class="px-2 py-0.5 rounded text-xs font-medium uppercase"
                        :class="severityBadgeClass(vuln.severity)"
                      >
                        {{ vuln.severity }}
                      </span>
                      <span class="text-gray-500 text-xs">Line {{ vuln.line_number }}</span>
                    </div>
                    <p class="text-white font-medium text-sm">{{ vuln.vulnerability_type }}</p>
                    <p class="text-gray-400 text-xs mt-1 line-clamp-2">{{ vuln.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- AI Results -->
          <div v-if="llmResults.length" class="bg-gradient-to-br from-purple-900/50 to-pink-900/50 border border-purple-500/30 rounded-2xl overflow-hidden">
            <div class="px-4 py-3 bg-purple-900/30 border-b border-purple-500/30">
              <h3 class="text-white font-semibold flex items-center gap-2">
                <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                </svg>
                AI Analysis & Fixes
              </h3>
            </div>
            <div class="p-4 space-y-4 max-h-96 overflow-y-auto">
              <div 
                v-for="(result, index) in llmResults" 
                :key="index"
                class="bg-gray-900/50 rounded-xl p-4"
              >
                <p class="text-gray-200 text-sm">{{ result.explanation }}</p>
                <div v-if="result.suggested_fix" class="mt-3">
                  <p class="text-xs text-green-400 mb-2">Suggested Fix:</p>
                  <pre class="bg-gray-950/80 rounded-lg p-3 text-xs text-green-300 overflow-x-auto whitespace-pre-wrap font-mono">{{ result.suggested_fix }}</pre>
                </div>
              </div>
            </div>
          </div>

          <!-- Success State -->
          <div v-if="analysisResult && !analysisResult.vulnerabilities.length" class="bg-gradient-to-br from-green-900/50 to-emerald-900/50 border border-green-500/30 rounded-2xl p-8 text-center">
            <div class="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h3 class="text-white font-semibold text-xl mb-2">Code is Secure!</h3>
            <p class="text-gray-400">No vulnerabilities detected in your code</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { scannerApi } from '../services/api_new'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const code = ref('')
const selectedLanguage = ref('python')
const isLoading = ref(false)
const isAnalyzing = ref(false)
const error = ref('')
const analysisResult = ref<any>(null)
const llmResults = ref<any[]>([])
const serviceOnline = ref(true)
const lastScanTime = ref('')

const languageExtensions: Record<string, string> = {
  python: 'py',
  javascript: 'js',
  typescript: 'ts',
  java: 'java',
  php: 'php',
  go: 'go',
  rust: 'rs',
  csharp: 'cs',
  ruby: 'rb',
  cpp: 'cpp'
}

const circumference = 2 * Math.PI * 56

const dashOffset = computed(() => {
  if (!analysisResult.value) return circumference
  return circumference - (analysisResult.value.score / 100) * circumference
})

const scoreBgClass = computed(() => {
  if (!analysisResult.value) return 'bg-gray-800'
  if (analysisResult.value.score >= 80) return 'bg-gradient-to-b from-green-900/50 to-gray-800'
  if (analysisResult.value.score >= 50) return 'bg-gradient-to-b from-yellow-900/50 to-gray-800'
  return 'bg-gradient-to-b from-red-900/50 to-gray-800'
})

const scoreColorClass = computed(() => {
  if (!analysisResult.value) return 'text-gray-500'
  if (analysisResult.value.score >= 80) return 'text-green-500'
  if (analysisResult.value.score >= 50) return 'text-yellow-500'
  return 'text-red-500'
})

const scoreTextClass = computed(() => {
  if (!analysisResult.value) return 'text-gray-500'
  if (analysisResult.value.score >= 80) return 'text-green-400'
  if (analysisResult.value.score >= 50) return 'text-yellow-400'
  return 'text-red-400'
})

const scoreLabelClass = computed(() => {
  if (!analysisResult.value) return 'text-gray-500'
  if (analysisResult.value.score >= 80) return 'text-green-400'
  if (analysisResult.value.score >= 50) return 'text-yellow-400'
  return 'text-red-400'
})

const scoreLabel = computed(() => {
  if (!analysisResult.value) return 'Waiting...'
  if (analysisResult.value.score >= 80) return 'Excellent Security'
  if (analysisResult.value.score >= 50) return 'Needs Improvement'
  return 'Critical Issues'
})

const scansUsed = computed(() => authStore.scansUsed)
const scansQuota = computed(() => authStore.scansQuota)

function severityBadgeClass(severity: string) {
  const classes: Record<string, string> = {
    critical: 'bg-red-500/20 text-red-400',
    high: 'bg-orange-500/20 text-orange-400',
    medium: 'bg-yellow-500/20 text-yellow-400',
    low: 'bg-blue-500/20 text-blue-400',
    info: 'bg-gray-500/20 text-gray-400'
  }
  return classes[severity] || classes.info
}

function severityBgClass(severity: string) {
  const classes: Record<string, string> = {
    critical: 'bg-red-500/20',
    high: 'bg-orange-500/20',
    medium: 'bg-yellow-500/20',
    low: 'bg-blue-500/20',
    info: 'bg-gray-500/20'
  }
  return classes[severity] || classes.info
}

function severityIconClass(severity: string) {
  const classes: Record<string, string> = {
    critical: 'text-red-400',
    high: 'text-orange-400',
    medium: 'text-yellow-400',
    low: 'text-blue-400',
    info: 'text-gray-400'
  }
  return classes[severity] || classes.info
}

onMounted(async () => {
  await authStore.refreshUsage()
  
  const lastScan = localStorage.getItem('last_scan_time')
  if (lastScan) {
    const date = new Date(lastScan)
    lastScanTime.value = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  }
  
  try {
    const h = await scannerApi.health()
    serviceOnline.value = h.status === 'ok'
  } catch {
    serviceOnline.value = false
  }
})

async function handleAnalyze() {
  error.value = ''
  llmResults.value = []
  if (!code.value.trim()) { 
    error.value = 'Please enter code to analyze' 
    return 
  }
  
  isLoading.value = true
  try {
    analysisResult.value = await scannerApi.analyze(code.value, selectedLanguage.value)
    
    const count = parseInt(localStorage.getItem('scans_count') || '0')
    localStorage.setItem('scans_count', String(count + 1))
    
    const vulnCount = parseInt(localStorage.getItem('vuln_count') || '0')
    localStorage.setItem('vuln_count', String(vulnCount + (analysisResult.value.total_vulnerabilities || 0)))
    
    localStorage.setItem('last_scan_time', new Date().toISOString())
    lastScanTime.value = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    
    await authStore.refreshUsage()
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
    for (const vuln of analysisResult.value.vulnerabilities.slice(0, 3)) {
      try {
        const result = await scannerApi.analyze(vuln, code.value, selectedLanguage.value)
        if (result) {
          llmResults.value.push(result)
        }
      } catch {
        // Skip failed analyses
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
