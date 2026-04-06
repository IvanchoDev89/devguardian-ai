<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-gray-900">
    <!-- Animated Background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative max-w-6xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="text-center mb-10">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-blue-500 rounded-2xl mb-4 shadow-lg shadow-purple-500/25">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
        </div>
        <h1 class="text-4xl font-bold text-white mb-3 bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
          Repository Scanner
        </h1>
        <p class="text-gray-400 text-lg max-w-2xl mx-auto">
          Scan entire GitHub, GitLab, or Bitbucket repositories for security vulnerabilities
        </p>
      </div>

      <!-- Provider Selection -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <button
          v-for="provider in providers"
          :key="provider.id"
          @click="selectProvider(provider.id)"
          class="p-6 rounded-2xl border-2 transition-all duration-300 flex flex-col items-center gap-3"
          :class="selectedProvider === provider.id 
            ? 'bg-purple-500/20 border-purple-500 shadow-lg shadow-purple-500/25' 
            : 'bg-gray-800/50 border-gray-700 hover:border-gray-600'"
        >
          <div class="w-12 h-12 rounded-xl flex items-center justify-center" :class="provider.bgClass">
            <svg v-if="provider.id === 'github'" class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            <svg v-else-if="provider.id === 'gitlab'" class="w-6 h-6 text-orange-500" fill="currentColor" viewBox="0 0 24 24">
              <path d="M22.65 14.39L12 22.13 1.35 14.39a.84.84 0 0 1-.3-.94l1.22-3.78 2.44-7.51A.42.42 0 0 1 4.82 2a.43.43 0 0 1 .58 0 .42.42 0 0 1 .11.18l2.44 7.49h8.1l2.44-7.51A.42.42 0 0 1 18.6 2a.43.43 0 0 1 .58 0 .42.42 0 0 1 .11.18l2.44 7.51L23 13.45a.84.84 0 0 1-.35.94z"/>
            </svg>
            <svg v-else class="w-6 h-6 text-blue-400" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm-1.653 17.996L5.5 13.747l1.702-3.958 4.145 9.207zm6.206-8.549l-4.145 9.207 4.847-.24-1.702-8.967zm-1.106 3.704l-3.447-7.358-3.447 7.358 6.894-.001z"/>
            </svg>
          </div>
          <span class="text-white font-semibold">{{ provider.name }}</span>
          <span class="text-gray-500 text-xs">{{ provider.urlPattern }}</span>
        </button>
      </div>

      <!-- URL Input -->
      <div class="bg-gray-800/80 backdrop-blur border border-gray-700/50 rounded-2xl p-6 mb-6">
        <div class="flex flex-col md:flex-row gap-4">
          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-300 mb-2">Repository URL</label>
            <div class="relative">
              <input
                v-model="repoUrl"
                type="text"
                class="w-full bg-gray-900/50 border border-gray-600/50 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="https://github.com/owner/repository"
                :disabled="isLoading"
              />
            </div>
          </div>
          <div class="w-full md:w-48">
            <label class="block text-sm font-medium text-gray-300 mb-2">Branch</label>
            <input
              v-model="branch"
              type="text"
              class="w-full bg-gray-900/50 border border-gray-600/50 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="main"
              :disabled="isLoading"
            />
          </div>
          <div class="flex items-end">
            <button
              @click="startScan"
              :disabled="isLoading || !repoUrl"
              class="w-full md:w-auto bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold py-3 px-8 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-purple-500/25"
            >
              <svg v-if="!isLoading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isLoading ? 'Scanning...' : 'Scan Repository' }}
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mt-4 flex items-center gap-3 px-4 py-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400">
          <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span class="text-sm">{{ error }}</span>
        </div>
      </div>

      <!-- Free Trial Banner -->
      <div v-if="!isAuthenticated" class="mb-6 bg-gradient-to-r from-amber-900/50 to-orange-900/50 border border-amber-500/30 rounded-2xl p-6">
        <div class="flex flex-col md:flex-row items-center justify-between gap-4">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-amber-500/20 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/>
              </svg>
            </div>
            <div>
              <h3 class="text-white font-semibold">Free Trial: 3 scans remaining</h3>
              <p class="text-gray-400 text-sm">Sign up to get 3 free repository scans, or login to use your plan quota.</p>
            </div>
          </div>
          <div class="flex gap-3">
            <router-link to="/signup" class="px-6 py-2 bg-amber-500 hover:bg-amber-600 text-white font-semibold rounded-xl transition-colors">
              Sign Up Free
            </router-link>
            <router-link to="/login" class="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-xl transition-colors">
              Login
            </router-link>
          </div>
        </div>
      </div>

      <!-- Results Section -->
      <div v-if="scanResult" class="space-y-6">
        <!-- Results Header -->
        <div class="bg-gray-800/80 backdrop-blur border border-gray-700/50 rounded-2xl p-6">
          <div class="flex flex-col md:flex-row items-center justify-between gap-4">
            <div>
              <h2 class="text-2xl font-bold text-white">{{ scanResult.repo_url }}</h2>
              <p class="text-gray-400">{{ scanResult.provider }} repository • Scan ID: {{ scanResult.scan_id }}</p>
            </div>
            <div class="flex items-center gap-6">
              <div class="text-center">
                <div class="text-4xl font-bold" :class="scoreClass">{{ scanResult.score }}</div>
                <div class="text-gray-400 text-sm">Security Score</div>
              </div>
              <div class="text-center">
                <div class="text-4xl font-bold text-white">{{ scanResult.total_files }}</div>
                <div class="text-gray-400 text-sm">Files Scanned</div>
              </div>
              <div class="text-center">
                <div class="text-4xl font-bold" :class="scanResult.total_vulnerabilities > 0 ? 'text-red-400' : 'text-green-400'">
                  {{ scanResult.total_vulnerabilities }}
                </div>
                <div class="text-gray-400 text-sm">Vulnerabilities</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Vulnerabilities Found -->
        <div v-if="vulnerabilities.length" class="bg-gray-800/80 backdrop-blur border border-gray-700/50 rounded-2xl overflow-hidden">
          <div class="px-6 py-4 bg-red-900/30 border-b border-gray-700/50">
            <h3 class="text-white font-semibold">Security Issues Found</h3>
          </div>
          <div class="divide-y divide-gray-700/30">
            <div 
              v-for="(vuln, index) in vulnerabilities" 
              :key="index"
              class="px-6 py-4 hover:bg-gray-700/20 transition-colors"
            >
              <div class="flex items-start gap-4">
                <div class="w-10 h-10 rounded-xl flex items-center justify-center" :class="severityBgClass(vuln.severity)">
                  <svg class="w-5 h-5" :class="severityIconClass(vuln.severity)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
                  </svg>
                </div>
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="px-2 py-0.5 rounded text-xs font-medium uppercase" :class="severityBadgeClass(vuln.severity)">
                      {{ vuln.severity }}
                    </span>
                    <span class="text-gray-500 text-xs">{{ vuln.type }}</span>
                  </div>
                  <p class="text-white font-medium">{{ vuln.title }}</p>
                  <p class="text-gray-400 text-sm mt-1">{{ vuln.description }}</p>
                  <p class="text-gray-500 text-xs mt-2 font-mono">{{ vuln.file }}:{{ vuln.line }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- No Vulnerabilities -->
        <div v-else class="bg-green-500/10 border border-green-500/30 rounded-2xl p-8 text-center">
          <div class="w-20 h-20 mx-auto mb-4 bg-green-500/20 rounded-2xl flex items-center justify-center">
            <svg class="w-10 h-10 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-white mb-2">Repository is Secure!</h3>
          <p class="text-gray-400">No vulnerabilities detected in this repository.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { scannerApi } from '../services/api_client'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const providers = [
  { 
    id: 'github', 
    name: 'GitHub', 
    urlPattern: 'github.com/owner/repo',
    bgClass: 'bg-gray-800'
  },
  { 
    id: 'gitlab', 
    name: 'GitLab', 
    urlPattern: 'gitlab.com/owner/repo',
    bgClass: 'bg-orange-500/20'
  },
  { 
    id: 'bitbucket', 
    name: 'Bitbucket', 
    urlPattern: 'bitbucket.org/owner/repo',
    bgClass: 'bg-blue-500/20'
  }
]

const selectedProvider = ref('github')
const repoUrl = ref('')
const branch = ref('main')
const isLoading = ref(false)
const error = ref('')
const scanResult = ref<any>(null)
const vulnerabilities = ref<any[]>([])

const isAuthenticated = computed(() => authStore.isAuthenticated)

const scoreClass = computed(() => {
  if (!scanResult.value) return 'text-gray-500'
  if (scanResult.value.score >= 80) return 'text-green-400'
  if (scanResult.value.score >= 50) return 'text-yellow-400'
  return 'text-red-400'
})

function selectProvider(id: string) {
  selectedProvider.value = id
}

function severityBadgeClass(severity: string) {
  const classes: Record<string, string> = {
    critical: 'bg-red-500/20 text-red-400',
    high: 'bg-orange-500/20 text-orange-400',
    medium: 'bg-yellow-500/20 text-yellow-400',
    low: 'bg-blue-500/20 text-blue-400'
  }
  return classes[severity] || classes.medium
}

function severityBgClass(severity: string) {
  const classes: Record<string, string> = {
    critical: 'bg-red-500/20',
    high: 'bg-orange-500/20',
    medium: 'bg-yellow-500/20',
    low: 'bg-blue-500/20'
  }
  return classes[severity] || classes.medium
}

function severityIconClass(severity: string) {
  const classes: Record<string, string> = {
    critical: 'text-red-400',
    high: 'text-orange-400',
    medium: 'text-yellow-400',
    low: 'text-blue-400'
  }
  return classes[severity] || classes.medium
}

async function startScan() {
  if (!repoUrl.value) {
    error.value = 'Please enter a repository URL'
    return
  }
  
  error.value = ''
  isLoading.value = true
  scanResult.value = null
  vulnerabilities.value = []
  
  try {
    const result = await scannerApi.scanRepo(repoUrl.value, selectedProvider.value, branch.value)
    scanResult.value = result
    
    // Fetch detailed results
    const details = await scannerApi.getRepoScanResults(result.scan_id)
    if (details.vulnerabilities) {
      vulnerabilities.value = details.vulnerabilities.map((v: any) => ({
        severity: v.severity?.toLowerCase() || 'medium',
        type: v.type,
        title: v.vulnerability_type || v.type,
        description: v.description,
        file: v.file,
        line: v.line_number || v.line
      }))
    }
  } catch (e: any) {
    error.value = e.message || 'Failed to scan repository'
  } finally {
    isLoading.value = false
  }
}
</script>
