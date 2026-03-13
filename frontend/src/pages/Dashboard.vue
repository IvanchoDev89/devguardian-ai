<template>
  <div>
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-white">Dashboard</h1>
      <p class="text-gray-400 mt-1">Welcome back, {{ userName }}</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div class="bg-slate-800/50 rounded-xl p-5 border border-white/10">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <div>
            <p class="text-gray-400 text-sm">Total Scans</p>
            <p class="text-2xl font-bold text-white">{{ stats.totalScans }}</p>
          </div>
        </div>
      </div>

      <div class="bg-slate-800/50 rounded-xl p-5 border border-white/10">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-red-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
          <div>
            <p class="text-gray-400 text-sm">Critical</p>
            <p class="text-2xl font-bold text-red-400">{{ stats.critical }}</p>
          </div>
        </div>
      </div>

      <div class="bg-slate-800/50 rounded-xl p-5 border border-white/10">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-green-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div>
            <p class="text-gray-400 text-sm">Fixed</p>
            <p class="text-2xl font-bold text-green-400">{{ stats.fixed }}</p>
          </div>
        </div>
      </div>

      <div class="bg-slate-800/50 rounded-xl p-5 border border-white/10">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-cyan-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <div>
            <p class="text-gray-400 text-sm">Score</p>
            <p class="text-2xl font-bold text-cyan-400">{{ stats.score }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Vulnerabilities -->
    <div class="bg-slate-800/50 rounded-xl border border-white/10 p-5">
      <h2 class="text-lg font-semibold text-white mb-4">Recent Vulnerabilities</h2>
      <div v-if="vulnerabilities.length === 0" class="text-gray-400 text-center py-8">
        No vulnerabilities found
      </div>
      <div v-else class="space-y-3">
        <div v-for="vuln in vulnerabilities.slice(0, 5)" :key="vuln.id" 
             class="flex items-center justify-between p-3 bg-slate-900/50 rounded-lg">
          <div class="flex items-center gap-3">
            <div :class="['w-2 h-2 rounded-full', severityColor(vuln.severity)]"></div>
            <div>
              <p class="text-white text-sm">{{ vuln.title }}</p>
              <p class="text-gray-500 text-xs">{{ vuln.file }} • {{ vuln.cwe_id }}</p>
            </div>
          </div>
          <span :class="['px-2 py-1 text-xs rounded-full', severityBadge(vuln.severity)]">
            {{ vuln.severity }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const userName = computed(() => authStore.user?.name || 'User')

const stats = ref({
  totalScans: 0,
  critical: 0,
  fixed: 0,
  score: 0
})

const vulnerabilities = ref<any[]>([])

const severityColor = (severity: string) => {
  const colors: Record<string, string> = {
    critical: 'bg-red-500',
    high: 'bg-orange-500',
    medium: 'bg-yellow-500',
    low: 'bg-blue-500'
  }
  return colors[severity] || 'bg-gray-500'
}

const severityBadge = (severity: string) => {
  const badges: Record<string, string> = {
    critical: 'bg-red-500/20 text-red-400',
    high: 'bg-orange-500/20 text-orange-400',
    medium: 'bg-yellow-500/20 text-yellow-400',
    low: 'bg-blue-500/20 text-blue-400'
  }
  return badges[severity] || 'bg-gray-500/20 text-gray-400'
}

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8003/api/v1/vulnerabilities')
    const data = await res.json()
    vulnerabilities.value = data || []
    
    stats.value.totalScans = 156
    stats.value.critical = data.filter((v: any) => v.severity === 'critical').length
    stats.value.fixed = 23
    stats.value.score = Math.max(0, 100 - (stats.value.critical * 15))
  } catch (e) {
    console.error('Failed to load data:', e)
  }
})
</script>
