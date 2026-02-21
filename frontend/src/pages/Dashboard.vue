<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
    <!-- Background Pattern -->
    <div class="absolute inset-0 bg-grid-white/5 bg-grid-16"></div>
    
    <div class="relative">
      <!-- Header Section -->
      <div class="px-4 py-6 sm:px-0">
        <div class="max-w-7xl mx-auto">
          <div class="flex items-center justify-between mb-8">
            <div>
              <h1 class="text-3xl font-bold text-white flex items-center gap-3">
                <span class="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                  DevGuardian AI Dashboard
                </span>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-500/20 text-green-400 border border-green-500/30">
                  <span class="w-2 h-2 bg-green-400 rounded-full mr-1 animate-pulse"></span>
                  Live
                </span>
              </h1>
              <p class="text-gray-400 mt-2">Real-time security monitoring with zero-noise detection</p>
            </div>
            <div class="flex items-center gap-3">
              <button 
                @click="refreshData"
                :disabled="loading"
                class="inline-flex items-center px-4 py-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-sm font-medium text-white hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
              >
                <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <svg v-else class="-ml-1 mr-2 h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                Refresh
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Alert -->
      <div v-if="error" class="mb-6 bg-red-500/10 backdrop-blur-sm rounded-lg p-4 border border-red-500/30">
        <div class="flex">
          <svg class="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
          </svg>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-400">Error Loading Data</h3>
            <div class="mt-2 text-sm text-red-300">
              <p>{{ error }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:border-blue-500/30 transition-all duration-300">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-400">Total Scans</p>
              <p class="text-2xl font-bold text-white mt-1">{{ stats.totalScans }}</p>
              <p class="text-xs text-green-400 mt-2">+12% from last week</p>
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
              <p class="text-sm font-medium text-gray-400">Critical Vulnerabilities</p>
              <p class="text-2xl font-bold text-white mt-1">{{ stats.criticalVulns }}</p>
              <p class="text-xs text-red-400 mt-2">Requires immediate action</p>
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
              <p class="text-sm font-medium text-gray-400">Fixed Today</p>
              <p class="text-2xl font-bold text-white mt-1">{{ stats.fixedToday }}</p>
              <p class="text-xs text-green-400 mt-2">Great progress!</p>
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
              <p class="text-sm font-medium text-gray-400">Security Score</p>
              <p class="text-2xl font-bold text-white mt-1">{{ stats.securityScore }}%</p>
              <p class="text-xs text-cyan-400 mt-2">Above average</p>
            </div>
            <div class="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-11h-7z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Vulnerability Trends -->
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
          <h3 class="text-lg font-semibold text-white mb-4 flex items-center">
            <svg class="w-5 h-5 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002 2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 00-2 2H5a2 2 0 00-2 2v10a2 2 0 002 2h2a2 2 0 002 2zm-6 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 00-2 2H5a2 2 0 00-2 2v10a2 2 0 002 2h2a2 2 0 002 2z"/>
            </svg>
            Vulnerability Trends
          </h3>
          <div class="h-64 flex items-center justify-center text-gray-400">
            <div class="text-center">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002 2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 00-2 2H5a2 2 0 00-2 2v10a2 2 0 002 2h2a2 2 0 002 2zm-6 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 00-2 2H5a2 2 0 00-2 2v10a2 2 0 002 2h2a2 2 0 002 2z"/>
              </svg>
              <p>Chart visualization coming soon</p>
              <p class="text-sm text-gray-500 mt-2">Integration with Chart.js</p>
            </div>
          </div>
        </div>

        <!-- Recent Scans -->
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
          <h3 class="text-lg font-semibold text-white mb-4 flex items-center">
            <svg class="w-5 h-5 mr-2 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3v4l3-3m-9 6V3m9 6h9"/>
            </svg>
            Recent Scans
          </h3>
          <div class="space-y-3">
            <div 
              v-for="scan in recentScans" 
              :key="scan.id" 
              class="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10 hover:border-blue-500/30 transition-all duration-200"
            >
              <div class="flex items-center">
                <div class="w-2 h-2 rounded-full mr-3" :class="getStatusColor(scan.status)"></div>
                <div>
                  <p class="text-sm font-medium text-white">{{ scan.repository }}</p>
                  <p class="text-xs text-gray-400">{{ scan.time }}</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-sm font-medium" :class="getVulnerabilityColor(scan.vulnerabilities)">{{ scan.vulnerabilities }}</p>
                <p class="text-xs text-gray-400">vulnerabilities</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Vulnerabilities Table -->
      <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 overflow-hidden">
        <div class="px-6 py-4 border-b border-white/10">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-white">Active Vulnerabilities</h3>
            <div class="flex items-center space-x-2">
              <select v-model="filterSeverity" class="bg-white/10 border border-white/20 rounded-lg text-sm text-white px-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">All Severities</option>
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
              <select v-model="filterStatus" class="bg-white/10 border border-white/20 rounded-lg text-sm text-white px-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">All Status</option>
                <option value="open">Open</option>
                <option value="in_progress">In Progress</option>
                <option value="fixed">Fixed</option>
              </select>
            </div>
          </div>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-white/5">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Repository</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Type</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Severity</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/10">
              <tr v-for="vuln in filteredVulnerabilities" :key="vuln.id" class="hover:bg-white/5 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-white">{{ vuln.repository }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{{ vuln.type }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 py-1 text-xs font-medium rounded-full" :class="getSeverityClass(vuln.severity)">
                    {{ vuln.severity }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 py-1 text-xs font-medium rounded-full" :class="getStatusClass(vuln.status)">
                    {{ vuln.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                  <button @click="viewVulnerability(vuln)" class="text-blue-400 hover:text-blue-300 mr-3">View</button>
                  <button @click="fixVulnerability(vuln)" class="text-green-400 hover:text-green-300">Fix</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { dashboardService } from '../services/api'
import { useNotificationStore } from '../stores/notifications'

const filterSeverity = ref('')
const filterStatus = ref('')

const loading = ref(false)
const error = ref('')

// Data from API
const stats = ref({
  totalScans: 0,
  criticalVulns: 0,
  fixedToday: 0,
  securityScore: 0
})

const recentScans = ref<any[]>([])
const vulnerabilities = ref<any[]>([])

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
    // Fetch stats from API
    const statsResponse = await dashboardService.getStats()
    if (statsResponse.success && statsResponse.data) {
      stats.value = {
        totalScans: statsResponse.data.total_scans || 0,
        criticalVulns: statsResponse.data.vulnerabilities?.critical || 0,
        fixedToday: statsResponse.data.vulnerabilities?.fixed || 0,
        securityScore: Math.max(0, 100 - (statsResponse.data.vulnerabilities?.critical * 10 || 0) - (statsResponse.data.vulnerabilities?.high * 5 || 0))
      }
    }
    
    // Fetch recent scans from API
    const scansResponse = await dashboardService.getRecentScans()
    if (scansResponse.success && scansResponse.data) {
      recentScans.value = scansResponse.data
    }
    
    // Fetch vulnerabilities from API
    const vulnsResponse = await dashboardService.getVulnerabilities()
    if (vulnsResponse.success && vulnsResponse.data) {
      vulnerabilities.value = vulnsResponse.data
    }
    
    const notificationStore = useNotificationStore()
    notificationStore.success('Data Refreshed', 'Dashboard data has been updated successfully')
  } catch (err: any) {
    error.value = err.message || 'Failed to refresh data'
    const notificationStore = useNotificationStore()
    notificationStore.error('Refresh Failed', error.value)
  } finally {
    loading.value = false
  }
}

// Helper functions
const getStatusColor = (status: string) => {
  switch (status) {
    case 'completed': return 'bg-green-400'
    case 'running': return 'bg-blue-400 animate-pulse'
    case 'failed': return 'bg-red-400'
    default: return 'bg-gray-400'
  }
}

const getVulnerabilityColor = (count: number) => {
  if (count === 0) return 'text-green-400'
  if (count <= 2) return 'text-yellow-400'
  return 'text-red-400'
}

const getSeverityClass = (severity: string) => {
  switch (severity) {
    case 'Critical': return 'bg-red-500/20 text-red-400 border border-red-500/30'
    case 'High': return 'bg-orange-500/20 text-orange-400 border border-orange-500/30'
    case 'Medium': return 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
    case 'Low': return 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
    default: return 'bg-gray-500/20 text-gray-400 border border-gray-500/30'
  }
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'Open': return 'bg-red-500/20 text-red-400 border border-red-500/30'
    case 'In Progress': return 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
    case 'Fixed': return 'bg-green-500/20 text-green-400 border border-green-500/30'
    default: return 'bg-gray-500/20 text-gray-400 border border-gray-500/30'
  }
}

const viewVulnerability = (vuln: any) => {
  const notificationStore = useNotificationStore()
  notificationStore.info('Vulnerability Details', `Viewing ${vuln.type} in ${vuln.repository}`)
}

const fixVulnerability = (vuln: any) => {
  const notificationStore = useNotificationStore()
  notificationStore.success('Fix Initiated', `AI fix started for ${vuln.type} vulnerability`)
}

onMounted(() => {
  refreshData()
})
</script>
