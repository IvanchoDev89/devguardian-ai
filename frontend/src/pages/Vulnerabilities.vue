<template>
  <div>
    <!-- Header -->
    <div class="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-white">Vulnerabilities</h1>
        <p class="text-gray-400 mt-1">Manage security vulnerabilities</p>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-slate-800/50 rounded-xl p-4 border border-white/10">
        <p class="text-gray-400 text-sm">Total</p>
        <p class="text-2xl font-bold text-white">{{ vulnerabilities.length }}</p>
      </div>
      <div class="bg-slate-800/50 rounded-xl p-4 border border-white/10">
        <p class="text-gray-400 text-sm">Critical</p>
        <p class="text-2xl font-bold text-red-400">{{ criticalCount }}</p>
      </div>
      <div class="bg-slate-800/50 rounded-xl p-4 border border-white/10">
        <p class="text-gray-400 text-sm">High</p>
        <p class="text-2xl font-bold text-orange-400">{{ highCount }}</p>
      </div>
      <div class="bg-slate-800/50 rounded-xl p-4 border border-white/10">
        <p class="text-gray-400 text-sm">Medium</p>
        <p class="text-2xl font-bold text-yellow-400">{{ mediumCount }}</p>
      </div>
    </div>

    <!-- List -->
    <div class="bg-slate-800/50 rounded-xl border border-white/10 overflow-hidden">
      <div v-if="vulnerabilities.length === 0" class="text-gray-400 text-center py-12">
        No vulnerabilities found
      </div>
      <div v-else class="divide-y divide-white/10">
        <div v-for="vuln in vulnerabilities" :key="vuln.id" 
             class="p-4 hover:bg-white/5 transition-colors">
          <div class="flex items-start justify-between gap-4">
            <div class="flex items-start gap-3">
              <div :class="['w-3 h-3 rounded-full mt-1.5 flex-shrink-0', severityColor(vuln.severity)]"></div>
              <div>
                <h3 class="text-white font-medium">{{ vuln.title }}</h3>
                <p class="text-gray-400 text-sm mt-1">{{ vuln.description }}</p>
                <div class="flex items-center gap-4 mt-2 text-xs text-gray-500">
                  <span class="flex items-center gap-1">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                    </svg>
                    {{ vuln.file }}
                  </span>
                  <span v-if="vuln.cwe_id">{{ vuln.cwe_id }}</span>
                  <span>CVSS: {{ vuln.cvss_score }}</span>
                </div>
              </div>
            </div>
            <span :class="['px-2 py-1 text-xs rounded-full flex-shrink-0', severityBadge(vuln.severity)]">
              {{ vuln.severity }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const vulnerabilities = ref<any[]>([])

const criticalCount = computed(() => vulnerabilities.value.filter(v => v.severity === 'critical').length)
const highCount = computed(() => vulnerabilities.value.filter(v => v.severity === 'high').length)
const mediumCount = computed(() => vulnerabilities.value.filter(v => v.severity === 'medium').length)

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
    vulnerabilities.value = await res.json()
  } catch (e) {
    console.error('Failed to load vulnerabilities:', e)
  }
})
</script>
