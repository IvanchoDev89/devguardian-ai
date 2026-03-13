<template>
  <div>
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-white">Security Tools</h1>
      <p class="text-gray-400 mt-1">Advanced security scanning and compliance</p>
    </div>

    <!-- Tool Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Secrets Scanner -->
      <div class="bg-slate-800/50 rounded-xl border border-white/10 p-5 hover:border-white/20 transition-colors">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 rounded-lg bg-red-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
            </svg>
          </div>
          <h3 class="text-white font-semibold">Secrets Scanner</h3>
        </div>
        <p class="text-gray-400 text-sm mb-4">Detect exposed API keys, tokens and credentials</p>
        <button @click="activeTool = 'secrets'" class="w-full py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded-lg transition-colors">
          Open Scanner
        </button>
      </div>

      <!-- Cloud Scanner -->
      <div class="bg-slate-800/50 rounded-xl border border-white/10 p-5 hover:border-white/20 transition-colors">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/>
            </svg>
          </div>
          <h3 class="text-white font-semibold">Cloud Scanner</h3>
        </div>
        <p class="text-gray-400 text-sm mb-4">Scan AWS, Azure, GCP, K8s, Docker configs</p>
        <button @click="testCloudScanner" class="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors">
          Open Scanner
        </button>
      </div>

      <!-- Security Posture -->
      <div class="bg-slate-800/50 rounded-xl border border-white/10 p-5 hover:border-white/20 transition-colors">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 rounded-lg bg-green-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
          </div>
          <h3 class="text-white font-semibold">Security Posture</h3>
        </div>
        <p class="text-gray-400 text-sm mb-4">Track security trends over time</p>
        <button @click="loadPosture" class="w-full py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors">
          View Trends
        </button>
      </div>

      <!-- Custom Rules -->
      <div class="bg-slate-800/50 rounded-xl border border-white/10 p-5 hover:border-white/20 transition-colors">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </div>
          <h3 class="text-white font-semibold">Custom Rules</h3>
        </div>
        <p class="text-gray-400 text-sm mb-4">Define your own security rules</p>
        <button @click="loadRules" class="w-full py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg transition-colors">
          Manage Rules
        </button>
      </div>

      <!-- Compliance -->
      <div class="bg-slate-800/50 rounded-xl border border-white/10 p-5 hover:border-white/20 transition-colors">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 rounded-lg bg-yellow-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 class="text-white font-semibold">Compliance</h3>
        </div>
        <p class="text-gray-400 text-sm mb-4">SOC2, ISO27001, HIPAA, PCI-DSS</p>
        <button class="w-full py-2 bg-yellow-600 hover:bg-yellow-700 text-white text-sm font-medium rounded-lg transition-colors">
          Generate Report
        </button>
      </div>

      <!-- Auto Remediation -->
      <div class="bg-slate-800/50 rounded-xl border border-white/10 p-5 hover:border-white/20 transition-colors">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 rounded-lg bg-cyan-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </div>
          <h3 class="text-white font-semibold">Auto Remediation</h3>
        </div>
        <p class="text-gray-400 text-sm mb-4">Automated vulnerability fixes</p>
        <button class="w-full py-2 bg-cyan-600 hover:bg-cyan-700 text-white text-sm font-medium rounded-lg transition-colors">
          View Fixes
        </button>
      </div>
    </div>

    <!-- Results Section -->
    <div v-if="results.length" class="mt-6 bg-slate-800/50 rounded-xl border border-white/10 p-5">
      <h3 class="text-white font-semibold mb-4">Scan Results</h3>
      <div class="space-y-3">
        <div v-for="(result, idx) in results" :key="idx" 
             class="p-3 bg-slate-900/50 rounded-lg">
          <div class="flex items-center justify-between">
            <span class="text-white">{{ result.issue || result.rule_name || result.title }}</span>
            <span :class="['px-2 py-1 text-xs rounded-full', getSeverityClass(result.severity)]">
              {{ result.severity || 'medium' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeTool = ref('')
const results = ref<any[]>([])

const getSeverityClass = (severity?: string) => {
  const s = severity?.toLowerCase() || 'medium'
  if (s === 'critical') return 'bg-red-500/20 text-red-400'
  if (s === 'high') return 'bg-orange-500/20 text-orange-400'
  if (s === 'medium') return 'bg-yellow-500/20 text-yellow-400'
  return 'bg-blue-500/20 text-blue-400'
}

const testCloudScanner = async () => {
  try {
    const res = await fetch('http://localhost:8003/api/v1/cloud/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ config: 'resource "aws_s3_bucket" "test" { acl = "public" }', provider: 'aws' })
    })
    const data = await res.json()
    results.value = data.findings || []
  } catch (e) {
    console.error('Cloud scan failed:', e)
  }
}

const loadPosture = async () => {
  try {
    const res = await fetch('http://localhost:8003/api/v1/posture/trend')
    const data = await res.json()
    results.value = [{ title: 'Security Trend', severity: data.trend || 'stable' }]
  } catch (e) {
    console.error('Failed to load posture:', e)
  }
}

const loadRules = async () => {
  try {
    const res = await fetch('http://localhost:8003/api/v1/rules/')
    const data = await res.json()
    results.value = data.map((r: any) => ({ title: r.name, severity: r.severity }))
  } catch (e) {
    console.error('Failed to load rules:', e)
  }
}
</script>
