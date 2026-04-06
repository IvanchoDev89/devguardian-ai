<template>
  <div class="min-h-screen bg-gray-900">
    <main class="max-w-7xl mx-auto px-4 py-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center h-64">
        <div class="text-center">
          <div class="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p class="text-gray-400">Loading security dashboard...</p>
        </div>
      </div>

      <div v-else>
        <!-- Header Stats Row -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
          <!-- Total Scans -->
          <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-400 text-xs uppercase tracking-wider">Total Scans</span>
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <p class="text-2xl font-bold text-white">{{ stats.totalScans }}</p>
            <p class="text-xs text-green-400 mt-1">↑ {{ todayScans }} today</p>
          </div>

          <!-- Vulnerabilities -->
          <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-400 text-xs uppercase tracking-wider">Vulnerabilities</span>
              <svg class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
              </svg>
            </div>
            <p class="text-2xl font-bold text-white">{{ stats.totalVulnerabilities }}</p>
            <p class="text-xs text-red-400 mt-1">{{ stats.criticalVulns }} critical</p>
          </div>

          <!-- Open Issues -->
          <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-400 text-xs uppercase tracking-wider">Open Issues</span>
              <svg class="w-4 h-4 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <p class="text-2xl font-bold text-white">{{ stats.openVulns }}</p>
            <p class="text-xs text-gray-400 mt-1">{{ stats.fixedVulns }} fixed</p>
          </div>

          <!-- Users -->
          <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-400 text-xs uppercase tracking-wider">Users</span>
              <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
              </svg>
            </div>
            <p class="text-2xl font-bold text-white">{{ stats.totalUsers }}</p>
            <p class="text-xs text-green-400 mt-1">{{ stats.activeUsers }} active</p>
          </div>

          <!-- API Keys -->
          <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-400 text-xs uppercase tracking-wider">API Keys</span>
              <svg class="w-4 h-4 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
              </svg>
            </div>
            <p class="text-2xl font-bold text-white">{{ stats.totalApiKeys }}</p>
            <p class="text-xs text-green-400 mt-1">{{ stats.activeApiKeys }} active</p>
          </div>

          <!-- Security Score -->
          <div class="bg-gray-800 rounded-xl p-4 border border-gray-700">
            <div class="flex items-center justify-between mb-2">
              <span class="text-gray-400 text-xs uppercase tracking-wider">Avg Score</span>
              <svg class="w-4 h-4" :class="scoreColor" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <p class="text-2xl font-bold" :class="scoreColor">{{ stats.avgScore }}</p>
            <p class="text-xs text-gray-400 mt-1">{{ scoreLabel }}</p>
          </div>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <!-- Severity Breakdown -->
          <div class="bg-gray-800 rounded-xl p-5 border border-gray-700">
            <h3 class="text-white font-semibold mb-4">Severity Distribution</h3>
            <div class="space-y-3">
              <div v-for="(count, severity) in severityBreakdown" :key="severity">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-gray-400 text-sm capitalize">{{ severity }}</span>
                  <span class="text-white font-medium">{{ count }}</span>
                </div>
                <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                  <div 
                    class="h-full rounded-full transition-all duration-500"
                    :class="severityColor(severity)"
                    :style="{ width: getSeverityPercent(count) + '%' }"
                  ></div>
                </div>
              </div>
              <div v-if="Object.keys(severityBreakdown).length === 0" class="text-gray-500 text-sm text-center py-4">
                No vulnerabilities detected
              </div>
            </div>
          </div>

          <!-- Vulnerability Status -->
          <div class="bg-gray-800 rounded-xl p-5 border border-gray-700">
            <h3 class="text-white font-semibold mb-4">Issue Status</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-lg bg-red-500/20 flex items-center justify-center">
                    <span class="text-red-400">🔴</span>
                  </div>
                  <div>
                    <p class="text-white font-medium">Open</p>
                    <p class="text-gray-400 text-xs">Not yet addressed</p>
                  </div>
                </div>
                <span class="text-xl font-bold text-red-400">{{ vulnStatus.open }}</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center">
                    <span class="text-blue-400">🔵</span>
                  </div>
                  <div>
                    <p class="text-white font-medium">In Progress</p>
                    <p class="text-gray-400 text-xs">Being fixed</p>
                  </div>
                </div>
                <span class="text-xl font-bold text-blue-400">{{ vulnStatus.in_progress }}</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-lg bg-green-500/20 flex items-center justify-center">
                    <span class="text-green-400">✅</span>
                  </div>
                  <div>
                    <p class="text-white font-medium">Fixed</p>
                    <p class="text-gray-400 text-xs">Resolved</p>
                  </div>
                </div>
                <span class="text-xl font-bold text-green-400">{{ vulnStatus.fixed }}</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-lg bg-gray-500/20 flex items-center justify-center">
                    <span class="text-gray-400">⚪</span>
                  </div>
                  <div>
                    <p class="text-white font-medium">False Positive</p>
                    <p class="text-gray-400 text-xs">Marked as false</p>
                  </div>
                </div>
                <span class="text-xl font-bold text-gray-400">{{ vulnStatus.false_positive }}</span>
              </div>
            </div>
          </div>

          <!-- Top Vulnerabilities -->
          <div class="bg-gray-800 rounded-xl p-5 border border-gray-700">
            <h3 class="text-white font-semibold mb-4">Top Vulnerability Types</h3>
            <div class="space-y-3">
              <div v-for="(vuln, index) in topVulns" :key="index" class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <span 
                    class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold"
                    :class="index === 0 ? 'bg-red-500/20 text-red-400' : index === 1 ? 'bg-orange-500/20 text-orange-400' : 'bg-yellow-500/20 text-yellow-400'"
                  >
                    {{ index + 1 }}
                  </span>
                  <span class="text-gray-300 text-sm">{{ vuln.type }}</span>
                </div>
                <span class="text-white font-medium">{{ vuln.count }}</span>
              </div>
              <div v-if="topVulns.length === 0" class="text-gray-500 text-sm text-center py-4">
                No vulnerabilities detected
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Scans Table -->
        <div class="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden mb-6">
          <div class="px-5 py-4 border-b border-gray-700 flex items-center justify-between">
            <h3 class="text-white font-semibold">Recent Scans</h3>
            <div class="flex items-center gap-3">
              <span class="text-gray-400 text-sm">{{ stats.totalScans }} total scans</span>
              <button @click="refreshData" class="text-blue-400 hover:text-blue-300 text-sm flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                Refresh
              </button>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-700/50">
                <tr>
                  <th class="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Scan ID</th>
                  <th class="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">User</th>
                  <th class="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Language</th>
                  <th class="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Status</th>
                  <th class="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Score</th>
                  <th class="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Issues</th>
                  <th class="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Duration</th>
                  <th class="px-5 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Date</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-700">
                <tr v-for="scan in recentScans" :key="scan.scan_id" class="hover:bg-gray-700/30 transition-colors">
                  <td class="px-5 py-4">
                    <span class="text-blue-400 font-mono text-sm">{{ scan.scan_id?.slice(0, 12) }}</span>
                  </td>
                  <td class="px-5 py-4 text-gray-300 text-sm">{{ scan.user_id?.slice(0, 20) || 'Anonymous' }}</td>
                  <td class="px-5 py-4">
                    <span class="px-2 py-1 bg-gray-700 text-gray-300 rounded text-xs">{{ scan.language }}</span>
                  </td>
                  <td class="px-5 py-4">
                    <span 
                      class="px-2 py-1 rounded text-xs font-medium"
                      :class="{
                        'bg-green-500/20 text-green-400': scan.status === 'completed',
                        'bg-yellow-500/20 text-yellow-400': scan.status === 'pending',
                        'bg-red-500/20 text-red-400': scan.status === 'failed'
                      }"
                    >
                      {{ scan.status }}
                    </span>
                  </td>
                  <td class="px-5 py-4">
                    <span 
                      class="px-2 py-1 rounded text-xs font-medium"
                      :class="{
                        'bg-green-500/20 text-green-400': scan.score >= 80,
                        'bg-yellow-500/20 text-yellow-400': scan.score >= 50 && scan.score < 80,
                        'bg-red-500/20 text-red-400': scan.score < 50
                      }"
                    >
                      {{ scan.score }}
                    </span>
                  </td>
                  <td class="px-5 py-4">
                    <span 
                      class="text-sm font-medium"
                      :class="scan.total_vulnerabilities > 0 ? 'text-red-400' : 'text-green-400'"
                    >
                      {{ scan.total_vulnerabilities }}
                    </span>
                  </td>
                  <td class="px-5 py-4 text-gray-400 text-sm">
                    {{ scan.duration_ms ? scan.duration_ms + 'ms' : '-' }}
                  </td>
                  <td class="px-5 py-4 text-gray-400 text-sm">
                    {{ formatDate(scan.created_at) }}
                  </td>
                </tr>
                <tr v-if="recentScans.length === 0">
                  <td colspan="8" class="px-5 py-8 text-center text-gray-500">
                    No scans yet. Start scanning to see activity here.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- System Health -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- API Usage -->
          <div class="bg-gray-800 rounded-xl p-5 border border-gray-700">
            <h3 class="text-white font-semibold mb-4">API Keys Usage</h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between p-3 bg-gray-700/30 rounded-lg">
                <span class="text-gray-400">Total Keys</span>
                <span class="text-white font-medium">{{ stats.totalApiKeys }}</span>
              </div>
              <div class="flex items-center justify-between p-3 bg-gray-700/30 rounded-lg">
                <span class="text-gray-400">Active Keys</span>
                <span class="text-green-400 font-medium">{{ stats.activeApiKeys }}</span>
              </div>
              <div class="flex items-center justify-between p-3 bg-gray-700/30 rounded-lg">
                <span class="text-gray-400">Webhooks</span>
                <span class="text-white font-medium">{{ stats.totalWebhooks }}</span>
              </div>
            </div>
          </div>

          <!-- Activity -->
          <div class="bg-gray-800 rounded-xl p-5 border border-gray-700">
            <h3 class="text-white font-semibold mb-4">Daily Activity</h3>
            <div class="space-y-3">
              <div v-for="(count, date) in dailyScans" :key="date" class="flex items-center justify-between">
                <span class="text-gray-400 text-sm">{{ formatShortDate(date) }}</span>
                <div class="flex items-center gap-2">
                  <div class="w-32 h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div 
                      class="h-full bg-blue-500 rounded-full"
                      :style="{ width: getDailyPercent(count) + '%' }"
                    ></div>
                  </div>
                  <span class="text-white font-medium text-sm w-8 text-right">{{ count }}</span>
                </div>
              </div>
              <div v-if="Object.keys(dailyScans).length === 0" class="text-gray-500 text-sm text-center py-4">
                No activity data yet
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { adminApi } from '../services/api_client'

const loading = ref(true)
const todayScans = ref(0)

const stats = ref({
  totalScans: 0,
  totalVulnerabilities: 0,
  openVulns: 0,
  fixedVulns: 0,
  totalUsers: 0,
  activeUsers: 0,
  totalApiKeys: 0,
  activeApiKeys: 0,
  totalWebhooks: 0,
  avgScore: 0,
  criticalVulns: 0
})

const severityBreakdown = ref<Record<string, number>>({})
const vulnStatus = ref({ open: 0, in_progress: 0, fixed: 0, false_positive: 0 })
const topVulns = ref<{type: string, count: number}[]>([])
const recentScans = ref<any[]>([])
const dailyScans = ref<Record<string, number>>({})

const scoreColor = computed(() => {
  if (stats.value.avgScore >= 80) return 'text-green-400'
  if (stats.value.avgScore >= 50) return 'text-yellow-400'
  return 'text-red-400'
})

const scoreLabel = computed(() => {
  if (stats.value.avgScore >= 80) return 'Excellent'
  if (stats.value.avgScore >= 50) return 'Needs Work'
  return 'Critical'
})

function severityColor(severity: string): string {
  const colors: Record<string, string> = {
    critical: 'bg-red-500',
    high: 'bg-orange-500',
    medium: 'bg-yellow-500',
    low: 'bg-blue-500',
    info: 'bg-gray-500'
  }
  return colors[severity] || 'bg-gray-500'
}

function getSeverityPercent(count: number): number {
  const total = Object.values(severityBreakdown.value).reduce((a, b) => a + b, 0)
  return total > 0 ? (count / total) * 100 : 0
}

function getDailyPercent(count: number): number {
  const max = Math.max(...Object.values(dailyScans.value), 1)
  return (count / max) * 100
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

function formatShortDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

async function loadData() {
  try {
    loading.value = true
    const data = await scannerApi.getAdminStats()
    
    const overview = data.overview || {}
    stats.value = {
      totalScans: overview.total_scans || 0,
      totalVulnerabilities: overview.total_vulnerabilities || 0,
      openVulns: data.vuln_status?.open || 0,
      fixedVulns: data.vuln_status?.fixed || 0,
      totalUsers: overview.total_users || 0,
      activeUsers: overview.total_users || 0,
      totalApiKeys: overview.total_api_keys || 0,
      activeApiKeys: overview.active_api_keys || 0,
      totalWebhooks: overview.total_webhooks || 0,
      avgScore: overview.avg_security_score || 0,
      criticalVulns: data.severity_breakdown?.critical || 0
    }
    
    severityBreakdown.value = data.severity_breakdown || {}
    vulnStatus.value = data.vuln_status || { open: 0, in_progress: 0, fixed: 0, false_positive: 0 }
    topVulns.value = data.top_vulnerabilities || []
    recentScans.value = data.recent_scans || []
    dailyScans.value = data.daily_scans || {}
    
    const today = new Date().toISOString().split('T')[0]
    todayScans.value = dailyScans.value[today] || 0
    
  } catch (error) {
    console.error('Failed to load admin stats:', error)
  } finally {
    loading.value = false
  }
}

function refreshData() {
  loadData()
}

onMounted(() => {
  loadData()
})
</script>
