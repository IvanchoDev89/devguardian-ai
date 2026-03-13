<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-white">Code Scanner</h1>
      <p class="text-gray-400 mt-1">Scan your code for security vulnerabilities</p>
    </div>

    <div class="bg-slate-800/50 rounded-xl border border-white/10 p-5 mb-6">
      <textarea 
        v-model="code" 
        placeholder="Paste your code here..."
        class="w-full h-64 bg-slate-900/50 border border-white/10 rounded-lg p-4 text-white font-mono text-sm focus:outline-none focus:border-cyan-500"
      ></textarea>
      
      <div class="flex gap-3 mt-4">
        <button 
          @click="scanCode" 
          :disabled="loading || !code"
          class="px-6 py-2 bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-600 text-white font-medium rounded-lg transition-colors"
        >
          {{ loading ? 'Scanning...' : 'Scan Code' }}
        </button>
        <button @click="code = ''" class="px-6 py-2 bg-white/10 hover:bg-white/20 text-white font-medium rounded-lg">
          Clear
        </button>
      </div>
    </div>

    <div v-if="results.length" class="bg-slate-800/50 rounded-xl border border-white/10 p-5">
      <h2 class="text-lg font-semibold text-white mb-4">Findings ({{ results.length }})</h2>
      <div class="space-y-3">
        <div v-for="(finding, idx) in results" :key="idx" class="p-4 bg-slate-900/50 rounded-lg">
          <div class="flex items-center justify-between mb-2">
            <span :class="['px-2 py-1 text-xs rounded-full', severityClass(finding.severity)]">
              {{ finding.severity }}
            </span>
            <span class="text-gray-500 text-sm">Line {{ finding.line_number || 'N/A' }}</span>
          </div>
          <p class="text-white">{{ finding.description || finding.title }}</p>
          <p v-if="finding.remediation" class="text-gray-400 text-sm mt-2">Fix: {{ finding.remediation }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const code = ref('')
const loading = ref(false)
const results = ref<any[]>([])

const severityClass = (severity?: string) => {
  const s = severity?.toLowerCase() || 'medium'
  if (s === 'critical') return 'bg-red-500/20 text-red-400'
  if (s === 'high') return 'bg-orange-500/20 text-orange-400'
  if (s === 'medium') return 'bg-yellow-500/20 text-yellow-400'
  return 'bg-blue-500/20 text-blue-400'
}

const scanCode = async () => {
  if (!code.value) return
  loading.value = true
  try {
    const res = await fetch('http://localhost:8003/api/v1/secrets/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: code.value })
    })
    const data = await res.json()
    results.value = data.findings || []
  } catch (e) {
    console.error('Scan failed:', e)
  } finally {
    loading.value = false
  }
}
</script>
