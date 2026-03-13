<template>
  <div class="p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-white">Dashboard</h1>
        <p class="text-gray-400 text-sm">Welcome back, {{ user?.name || 'User' }}</p>
      </div>
      <button 
        @click="refreshData"
        :disabled="loading"
        class="flex items-center px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-sm font-medium text-white hover:bg-white/20 disabled:opacity-50"
      >
        <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        Refresh
      </button>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="mb-6 bg-red-500/10 rounded-lg p-4 border border-red-500/30">
      <p class="text-red-400 text-sm">{{ error }}</p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white/5 rounded-xl p-6 border border-white/10">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-400 text-sm">Total Scans</p>
            <p class="text-3xl font-bold text-white mt-1">{{ stats.totalScans }}</p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white/5 rounded-xl p-6 border border-white/10">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-400 text-sm">Critical Vulnerabilities</p>
            <p class="text-3xl font-bold text-red-400 mt-1">{{ stats.criticalVulns }}</p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-red-500/20 flex items-center justify-center">
            <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white/5 rounded-xl p-6 border border-white/10">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-400 text-sm">Fixed Today</p>
            <p class="text-3xl font-bold text-green-400 mt-1">{{ stats.fixedToday }}</p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-green-500/20 flex items-center justify-center">
            <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white/5 rounded-xl p-6 border border-white/10">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-400 text-sm">Security Score</p>
            <p class="text-3xl font-bold text-cyan-400 mt-1">{{ stats.securityScore }}</p>
          </div>
          <div class="w-12 h-12 rounded-xl bg-cyan-500/20 flex items-center justify-center">
            <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Scans -->
    <div class="bg-white/5 rounded-xl border border-white/10 p-6 mb-6">
      <h2 class="text-lg font-semibold text-white mb-4">Recent Scans</h2>
      <div v-if="recentScans.length === 0" class="text-center py-8 text-gray-400">
        No scans yet. Start your first scan!
      </div>
      <div v-else class="space-y-3">
        <div v-for="scan in recentScans.slice(0, 5)" :key="scan.scan_id" class="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg">
          <div class="flex items-center gap-3">
            <div :class="['w-2 h-2 rounded-full', getStatusColor(scan.status)]"></div>
            <div>
              <p class="text-white text-sm">{{ scan.file_name || 'Unknown' }}</p>
              <p class="text-gray-500 text-xs">{{ scan.language }} • {{ new Date(scan.created_at).toLocaleDateString() }}</p>
            </div>
          </div>
          <span class="text-gray-400 text-sm">Score: {{ scan.score || 0 }}</span>
        </div>
      </div>
    </div>

    <!-- Vulnerabilities -->
    <div class="bg-white/5 rounded-xl border border-white/10 p-6">
      <h2 class="text-lg font-semibold text-white mb-4">Recent Vulnerabilities</h2>
      <div v-if="vulnerabilities.length === 0" class="text-center py-8 text-gray-400">
        No vulnerabilities found. Great job!
      </div>
      <div v-else class="space-y-3">
        <div v-for="vuln in vulnerabilities.slice(0, 5)" :key="vuln.id" class="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg">
          <div class="flex items-center gap-3">
            <div :class="['w-2 h-2 rounded-full', getSeverityColor(vuln.severity)]"></div>
            <div>
              <p class="text-white text-sm">{{ vuln.vulnerability_type }}</p>
              <p class="text-gray-500 text-xs">Line {{ vuln.line_number }}</p>
            </div>
          </div>
          <span :class="['px-2 py-1 text-xs rounded-full', getSeverityClass(vuln.severity)]">{{ vuln.severity }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { dashboardService } from '../services/api'
import { useNotificationStore } from '../stores/notifications'
import { useAuthStore } from '../stores/auth'

const notificationStore = useNotificationStore()
const authStore = useAuthStore()

const user = computed(() => authStore.user)

const loading = ref(false)
const error = ref('')

const stats = ref({
  totalScans: 0,
  criticalVulns: 0,
  fixedToday: 0,
  securityScore: 0
})

const recentScans = ref<any[]>([])
const vulnerabilities = ref<any[]>([])

const filterSeverity = ref('')
const filterStatus = ref('')

const filteredVulnerabilities = computed(() => {
  return vulnerabilities.value.filter(vuln => {
    const matchesSeverity = !filterSeverity.value || vuln.severity === filterSeverity.value
    const matchesStatus = !filterStatus.value || vuln.status === filterStatus.value
    return matchesSeverity && matchesStatus
  })
})

const refreshData = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const statsResponse = await dashboardService.getStats()
    if (statsResponse.success && statsResponse.data) {
      stats.value = {
        totalScans: statsResponse.data.total_scans || 0,
        criticalVulns: statsResponse.data.vulnerabilities?.critical || 0,
        fixedToday: statsResponse.data.vulnerabilities?.fixed || 0,
        securityScore: Math.max(0, 100 - (statsResponse.data.vulnerabilities?.critical * 10 || 0) - (statsResponse.data.vulnerabilities?.high * 5 || 0))
      }
    }
    
    const scansResponse = await dashboardService.getRecentScans()
    if (scansResponse.success && scansResponse.data) {
      recentScans.value = scansResponse.data
    }
    
    const vulnsResponse = await dashboardService.getVulnerabilities()
    if (vulnsResponse.success && vulnsResponse.data) {
      vulnerabilities.value = vulnsResponse.data
    }
    
    notificationStore.success('Data Refreshed', 'Dashboard data has been updated successfully')
  } catch (err: any) {
    error.value = err.message || 'Failed to refresh data'
    notificationStore.error('Refresh Failed', error.value)
  } finally {
    loading.value = false
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'completed': return 'bg-green-400'
    case 'running': return 'bg-blue-400 animate-pulse'
    case 'failed': return 'bg-red-400'
    default: return 'bg-gray-400'
  }
}

const getSeverityColor = (severity: string) => {
  switch (severity?.toLowerCase()) {
    case 'critical': return 'bg-red-500'
    case 'high': return 'bg-orange-500'
    case 'medium': return 'bg-yellow-500'
    case 'low': return 'bg-blue-500'
    default: return 'bg-gray-500'
  }
}

const getSeverityClass = (severity: string) => {
  switch (severity?.toLowerCase()) {
    case 'critical': return 'bg-red-500/20 text-red-400'
    case 'high': return 'bg-orange-500/20 text-orange-400'
    case 'medium': return 'bg-yellow-500/20 text-yellow-400'
    case 'low': return 'bg-blue-500/20 text-blue-400'
    default: return 'bg-gray-500/20 text-gray-400'
  }
}

onMounted(() => {
  refreshData()
})
</script>
