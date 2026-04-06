<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-white">Security Scanner</h1>
        <p class="text-gray-400 mt-1">Comprehensive security analysis</p>
      </div>
      <div class="flex gap-2">
        <span v-for="tool in activeTools" :key="tool" 
              class="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full">
          {{ tool }}
        </span>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Scan Configuration -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-slate-800/50 rounded-xl border border-white/10 p-6">
          <h2 class="text-lg font-semibold text-white mb-4">New Scan</h2>
          
          <form @submit.prevent="startScan" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Scan Type</label>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                <button
                  v-for="type in scanTypes"
                  :key="type.value"
                  type="button"
                  @click="form.scan_type = type.value; updateActiveTools(type.value)"
                  :class="[
                    'p-3 rounded-lg border transition-all text-left',
                    form.scan_type === type.value
                      ? 'border-blue-500 bg-blue-500/10'
                      : 'border-white/10 hover:border-white/30'
                  ]"
                >
                  <div class="flex items-center gap-2">
                    <span class="text-xl">{{ type.icon }}</span>
                    <div>
                      <div class="text-sm font-medium text-white">{{ type.label }}</div>
                      <div class="text-xs text-gray-500">{{ type.tools }}</div>
                    </div>
                  </div>
                </button>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Target</label>
              <input
                v-model="form.target"
                type="text"
                required
                placeholder="GitHub URL, local path, or Docker image"
                class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div class="flex gap-3">
              <button
                type="submit"
                :disabled="loading"
                class="flex-1 py-3 px-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-700 disabled:opacity-50 transition-all"
              >
                <span v-if="loading" class="flex items-center justify-center gap-2">
                  <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                  </svg>
                  Scanning...
                </span>
                <span v-else>🚀 Start Scan</span>
              </button>
              <button
                type="button"
                @click="exportResults"
                :disabled="!lastResult"
                class="px-6 py-3 bg-white/10 text-white rounded-lg hover:bg-white/20 disabled:opacity-50"
              >
                📥 Export
              </button>
            </div>
          </form>

          <div v-if="error" class="mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
            <p class="text-red-400 text-sm">{{ error }}</p>
          </div>
        </div>

        <!-- Results -->
        <div v-if="lastResult" class="bg-slate-800/50 rounded-xl border border-white/10 p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-white">
              Scan Results
              <span class="ml-2 px-2 py-0.5 rounded-full text-sm" 
                    :class="lastResult.vulnerabilities_found > 0 ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'">
                {{ lastResult.vulnerabilities_found }} found
              </span>
            </h2>
            <button @click="lastResult = null" class="text-gray-400 hover:text-white">
              ✕
            </button>
          </div>

          <div class="mb-4 flex gap-2 flex-wrap">
            <button
              v-for="tool in Object.keys(lastResult.results || {})"
              :key="tool"
              @click="selectedTool = tool"
              :class="[
                'px-3 py-1 rounded-full text-sm transition-all',
                selectedTool === tool ? 'bg-blue-500 text-white' : 'bg-white/10 text-gray-400 hover:bg-white/20'
              ]"
            >
              {{ tool }}
              <span v-if="lastResult.results[tool]?.total" class="ml-1 opacity-70">
                ({{ lastResult.results[tool].total }})
              </span>
            </button>
          </div>

          <div v-if="selectedTool && lastResult.results?.[selectedTool]?.error" 
               class="p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
            <p class="text-yellow-400 text-sm">{{ lastResult.results[selectedTool].error }}</p>
          </div>

          <div v-else-if="vulnsToShow.length === 0" class="text-center py-8 text-gray-400">
            <span class="text-4xl">✅</span>
            <p class="mt-2">No vulnerabilities found!</p>
          </div>

          <div v-else class="space-y-3 max-h-96 overflow-y-auto">
            <div
              v-for="(vuln, index) in vulnsToShow"
              :key="index"
              class="p-4 bg-white/5 rounded-lg border-l-4"
              :class="severityBorder(vuln.severity)"
            >
              <div class="flex items-start justify-between gap-4">
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="px-2 py-0.5 rounded text-xs bg-white/10">{{ vuln.tool }}</span>
                    <h3 class="text-white font-medium">{{ vuln.title }}</h3>
                  </div>
                  <p class="text-gray-400 text-sm">{{ vuln.description }}</p>
                  <div class="flex items-center gap-4 mt-2 text-xs text-gray-500">
                    <span v-if="vuln.file_path" class="flex items-center gap-1">
                      📁 {{ vuln.file_path }}<span v-if="vuln.line_number">:{{ vuln.line_number }}</span>
                    </span>
                    <span v-if="vuln.cwe_id" class="px-2 py-0.5 bg-white/10 rounded">{{ vuln.cwe_id }}</span>
                  </div>
                  <div v-if="vuln.code_snippet" class="mt-2 p-2 bg-black/30 rounded font-mono text-xs text-gray-300 overflow-x-auto">
                    <code>{{ vuln.code_snippet }}</code>
                  </div>
                </div>
                <span :class="['px-2 py-1 text-xs rounded-full whitespace-nowrap', severityBadge(vuln.severity)]">
                  {{ vuln.severity }}
                </span>
              </div>
              <div v-if="vuln.fix_suggestion" class="mt-3 p-3 bg-green-500/10 border border-green-500/20 rounded-lg">
                <p class="text-xs text-green-400 font-medium">💡 Fix Suggestion:</p>
                <p class="text-sm text-green-300 mt-1">{{ vuln.fix_suggestion }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="space-y-6">
        <div class="bg-slate-800/50 rounded-xl border border-white/10 p-6">
          <h3 class="text-white font-semibold mb-4">📊 Scan History</h3>
          <div v-if="scans.length === 0" class="text-gray-400 text-sm text-center py-4">
            No scans yet
          </div>
          <div v-else class="space-y-2">
            <div
              v-for="scan in scans.slice(0, 5)"
              :key="scan.id"
              class="p-3 bg-white/5 rounded-lg"
            >
              <div class="flex items-center justify-between">
                <span class="text-white text-sm">{{ scan.name }}</span>
                <span :class="['text-xs px-2 py-0.5 rounded-full', statusClass(scan.status)]">
                  {{ scan.status }}
                </span>
              </div>
              <p class="text-gray-500 text-xs mt-1 truncate">{{ scan.target }}</p>
            </div>
          </div>
        </div>

        <div class="bg-slate-800/50 rounded-xl border border-white/10 p-6">
          <h3 class="text-white font-semibold mb-4">🛠️ Available Tools</h3>
          <div class="space-y-2 text-sm">
            <div v-for="tool in toolsList" :key="tool.name" class="flex items-center justify-between">
              <span class="text-gray-300">{{ tool.name }}</span>
              <span :class="tool.installed ? 'text-green-400' : 'text-gray-500'">
                {{ tool.installed ? '✅' : '❌' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { scansApi } from '../services/api_client'

const authStore = useAuthStore()

const form = ref({
  scan_type: 'all',
  target: ''
})

const loading = ref(false)
const error = ref('')
const scans = ref<any[]>([])
const lastResult = ref<any>(null)
const selectedTool = ref<string | null>(null)
const activeTools = ref<string[]>(['semgrep', 'bandit', 'gosec', 'gitleaks', 'pip-audit', 'npm-audit'])

const scanTypes = [
  { value: 'all', label: 'Full Scan', icon: '🔍', tools: 'All tools' },
  { value: 'python', label: 'Python', icon: '🐍', tools: 'Bandit, Semgrep' },
  { value: 'javascript', label: 'JavaScript', icon: '📦', tools: 'npm audit' },
  { value: 'go', label: 'Go', icon: '🔷', tools: 'gosec' },
  { value: 'secrets', label: 'Secrets', icon: '🔑', tools: 'Gitleaks' },
  { value: 'docker', label: 'Docker', icon: '🐳', tools: 'Trivy' },
  { value: 'dependencies', label: 'Dependencies', icon: '📋', tools: 'pip/npm audit' },
]

const toolsList = [
  { name: 'Semgrep', installed: true },
  { name: 'Bandit', installed: true },
  { name: 'Gosec', installed: true },
  { name: 'Gitleaks', installed: true },
  { name: 'pip-audit', installed: true },
  { name: 'npm audit', installed: true },
  { name: 'Trivy', installed: true },
]

const vulnsToShow = computed(() => {
  if (!lastResult.value?.results) return []
  
  if (selectedTool.value && lastResult.value.results[selectedTool.value]?.vulnerabilities) {
    return lastResult.value.results[selectedTool.value].vulnerabilities
  }
  
  const all: any[] = []
  for (const toolResults of Object.values(lastResult.value.results)) {
    if (toolResults?.vulnerabilities) {
      all.push(...toolResults.vulnerabilities)
    }
  }
  return all
})

function updateActiveTools(type: string) {
  const toolMap: Record<string, string[]> = {
    all: ['semgrep', 'bandit', 'gosec', 'gitleaks', 'pip-audit', 'npm-audit'],
    python: ['semgrep', 'bandit', 'gosec'],
    javascript: ['semgrep', 'npm-audit'],
    go: ['gosec', 'semgrep'],
    secrets: ['gitleaks'],
    docker: ['trivy'],
    dependencies: ['pip-audit', 'npm-audit']
  }
  activeTools.value = toolMap[type] || []
}

onMounted(async () => {
  if (authStore.token) {
    try {
      scans.value = await scansApi.list(authStore.token, { limit: 10 })
    } catch (e) {
      console.error('Failed to load scans:', e)
    }
  }
})

async function startScan() {
  loading.value = true
  error.value = ''
  lastResult.value = null
  selectedTool.value = null
  
  try {
    const result = await scansApi.run(authStore.token, {
      scan_type: form.value.scan_type,
      target: form.value.target,
      options: {
        gitleaks_path: '/tmp/gitleaks',
        trivy_path: '/tmp/trivy'
      }
    })
    
    lastResult.value = result
    await loadScans()
  } catch (e: any) {
    error.value = e.message || 'Scan failed'
  } finally {
    loading.value = false
  }
}

async function loadScans() {
  if (!authStore.token) return
  try {
    scans.value = await scansApi.list(authStore.token, { limit: 10 })
  } catch (e) {
    console.error('Failed to load scans:', e)
  }
}

function exportResults() {
  if (!lastResult.value) return
  
  const dataStr = JSON.stringify(lastResult.value, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `scan-results-${Date.now()}.json`
  link.click()
  URL.revokeObjectURL(url)
}

function severityBadge(severity: string) {
  const map: Record<string, string> = {
    critical: 'bg-red-500/20 text-red-400',
    high: 'bg-orange-500/20 text-orange-400',
    medium: 'bg-yellow-500/20 text-yellow-400',
    low: 'bg-blue-500/20 text-blue-400'
  }
  return map[severity] || 'bg-gray-500/20 text-gray-400'
}

function severityBorder(severity: string) {
  const map: Record<string, string> = {
    critical: 'border-l-red-500',
    high: 'border-l-orange-500',
    medium: 'border-l-yellow-500',
    low: 'border-l-blue-500'
  }
  return map[severity] || 'border-l-gray-500'
}

function statusClass(status: string) {
  const map: Record<string, string> = {
    pending: 'bg-gray-500/20 text-gray-400',
    running: 'bg-yellow-500/20 text-yellow-400',
    completed: 'bg-green-500/20 text-green-400',
    failed: 'bg-red-500/20 text-red-400'
  }
  return map[status] || 'bg-gray-500/20 text-gray-400'
}
</script>
