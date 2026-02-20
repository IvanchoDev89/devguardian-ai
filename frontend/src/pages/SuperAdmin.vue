<template>
  <div class="min-h-screen pt-16">
    <!-- Loading Overlay -->
    <div v-if="loading" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-slate-800 p-8 rounded-xl flex flex-col items-center">
        <div class="animate-spin w-12 h-12 border-4 border-cyan-500 border-t-transparent rounded-full mb-4"></div>
        <p class="text-white">Loading dashboard data...</p>
      </div>
    </div>

    <!-- Error Banner -->
    <div v-if="error" class="bg-red-500/20 border border-red-500 text-red-400 px-4 py-2 mb-4">
      {{ error }}
    </div>
    
    <div class="container mx-auto px-4 py-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-white flex items-center gap-3">
              <svg class="w-10 h-10 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
              Super Admin Dashboard
            </h1>
            <p class="text-gray-400 mt-2">Enterprise-wide security monitoring and analytics</p>
          </div>
          <div class="flex items-center gap-4">
            <select v-model="timeRange" class="bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white">
              <option value="24h">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
            </select>
            <button @click="refreshData" class="bg-cyan-600 hover:bg-cyan-700 text-white px-4 py-2 rounded-lg flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              Refresh
            </button>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div v-for="stat in quickStats" :key="stat.label" class="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">{{ stat.label }}</p>
              <p class="text-3xl font-bold text-white mt-1">{{ stat.value }}</p>
              <p :class="stat.trend > 0 ? 'text-green-400' : 'text-red-400'" class="text-sm mt-1">
                {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}% {{ stat.period }}
              </p>
            </div>
            <div :class="`w-14 h-14 rounded-xl flex items-center justify-center ${stat.bgColor}`">
              <component :is="stat.icon" class="w-8 h-8" />
            </div>
          </div>
        </div>
      </div>

      <!-- Main Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- Real-time Activity -->
        <div class="lg:col-span-2 bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            Real-time System Activity
          </h2>
          <div class="h-64" ref="activityChartRef">
            <canvas id="activityChart"></canvas>
          </div>
        </div>

        <!-- System Health -->
        <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            System Health
          </h2>
          <div class="space-y-4">
            <div v-for="service in systemServices" :key="service.name" class="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
              <div class="flex items-center gap-3">
                <div :class="`w-3 h-3 rounded-full ${service.status === 'healthy' ? 'bg-green-500' : service.status === 'warning' ? 'bg-yellow-500' : 'bg-red-500'}`"></div>
                <span class="text-white">{{ service.name }}</span>
              </div>
              <span :class="`text-sm ${service.status === 'healthy' ? 'text-green-400' : service.status === 'warning' ? 'text-yellow-400' : 'text-red-400'}`">
                {{ service.uptime }}%
              </span>
            </div>
          </div>

          <!-- Resource Usage -->
          <div class="mt-6">
            <h3 class="text-white font-semibold mb-3">Resource Usage</h3>
            <div class="space-y-3">
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-400">CPU</span>
                  <span class="text-cyan-400">{{ resources.cpu }}%</span>
                </div>
                <div class="w-full bg-slate-700 rounded-full h-2">
                  <div class="bg-cyan-500 h-2 rounded-full" :style="{ width: resources.cpu + '%' }"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-400">Memory</span>
                  <span class="text-purple-400">{{ resources.memory }}%</span>
                </div>
                <div class="w-full bg-slate-700 rounded-full h-2">
                  <div class="bg-purple-500 h-2 rounded-full" :style="{ width: resources.memory + '%' }"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-400">Storage</span>
                  <span class="text-orange-400">{{ resources.storage }}%</span>
                </div>
                <div class="w-full bg-slate-700 rounded-full h-2">
                  <div class="bg-orange-500 h-2 rounded-full" :style="{ width: resources.storage + '%' }"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-400">Network I/O</span>
                  <span class="text-blue-400">{{ resources.network }} MB/s</span>
                </div>
                <div class="w-full bg-slate-700 rounded-full h-2">
                  <div class="bg-blue-500 h-2 rounded-full" :style="{ width: (resources.network / 100) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Second Row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Top Users -->
        <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            Top Active Users
          </h2>
          <div class="space-y-3">
            <div v-for="(user, index) in topUsers" :key="user.email" class="flex items-center gap-4 p-3 bg-slate-700/50 rounded-lg">
              <div class="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center text-white font-bold">
                {{ index + 1 }}
              </div>
              <div class="flex-1">
                <p class="text-white font-medium">{{ user.name }}</p>
                <p class="text-gray-400 text-sm">{{ user.email }}</p>
              </div>
              <div class="text-right">
                <p class="text-white font-bold">{{ user.scans }}</p>
                <p class="text-gray-400 text-xs">scans</p>
              </div>
              <div class="text-right">
                <p class="text-white font-bold">{{ user.apiCalls }}</p>
                <p class="text-gray-400 text-xs">API calls</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Security Alerts -->
        <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            Security Alerts
          </h2>
          <div class="space-y-3 max-h-80 overflow-y-auto">
            <div v-for="alert in securityAlerts" :key="alert.id" :class="`p-3 rounded-lg border-l-4 ${getAlertClass(alert.severity)}`">
              <div class="flex items-start justify-between">
                <div>
                  <p class="text-white font-medium">{{ alert.title }}</p>
                  <p class="text-gray-400 text-sm">{{ alert.message }}</p>
                </div>
                <span :class="`px-2 py-1 rounded text-xs font-bold ${getSeverityBadge(alert.severity)}`">
                  {{ alert.severity }}
                </span>
              </div>
              <p class="text-gray-500 text-xs mt-2">{{ alert.time }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Third Row -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- Vulnerability Distribution -->
        <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            Vulnerability Distribution
          </h2>
          <div class="h-48 flex items-center justify-center">
            <canvas id="vulnChart"></canvas>
          </div>
          <div class="mt-4 grid grid-cols-2 gap-2">
            <div v-for="vuln in vulnDistribution" :key="vuln.type" class="flex items-center justify-between text-sm">
              <div class="flex items-center gap-2">
                <div :class="`w-3 h-3 rounded-full ${vuln.color}`"></div>
                <span class="text-gray-400">{{ vuln.type }}</span>
              </div>
              <span class="text-white font-bold">{{ vuln.count }}</span>
            </div>
          </div>
        </div>

        <!-- AI Service Metrics -->
        <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            AI Service Metrics
          </h2>
          <div class="space-y-4">
            <div class="p-3 bg-slate-700/50 rounded-lg">
              <div class="flex justify-between items-center">
                <span class="text-gray-400">Total Requests</span>
                <span class="text-white font-bold">{{ aiMetrics.totalRequests.toLocaleString() }}</span>
              </div>
            </div>
            <div class="p-3 bg-slate-700/50 rounded-lg">
              <div class="flex justify-between items-center">
                <span class="text-gray-400">Avg Response Time</span>
                <span class="text-white font-bold">{{ aiMetrics.avgResponseTime }}ms</span>
              </div>
            </div>
            <div class="p-3 bg-slate-700/50 rounded-lg">
              <div class="flex justify-between items-center">
                <span class="text-gray-400">Success Rate</span>
                <span class="text-green-400 font-bold">{{ aiMetrics.successRate }}%</span>
              </div>
            </div>
            <div class="p-3 bg-slate-700/50 rounded-lg">
              <div class="flex justify-between items-center">
                <span class="text-gray-400">Tokens Used</span>
                <span class="text-white font-bold">{{ aiMetrics.tokensUsed.toLocaleString() }}</span>
              </div>
            </div>
            <div class="p-3 bg-slate-700/50 rounded-lg">
              <div class="flex justify-between items-center">
                <span class="text-gray-400">API Cost</span>
                <span class="text-yellow-400 font-bold">${{ aiMetrics.apiCost }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <svg class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            Quick Actions
          </h2>
          <div class="space-y-3">
            <button @click="runSystemScan" class="w-full bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700 text-white py-3 px-4 rounded-lg font-medium flex items-center justify-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              Run Full System Scan
            </button>
            <button @click="generateReport" class="w-full bg-slate-700 hover:bg-slate-600 text-white py-3 px-4 rounded-lg font-medium flex items-center justify-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              Generate Report
            </button>
            <button @click="viewAuditLogs" class="w-full bg-slate-700 hover:bg-slate-600 text-white py-3 px-4 rounded-lg font-medium flex items-center justify-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              View Audit Logs
            </button>
            <button @click="manageUsers" class="w-full bg-slate-700 hover:bg-slate-600 text-white py-3 px-4 rounded-lg font-medium flex items-center justify-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              Manage Users
            </button>
          </div>
        </div>
      </div>

      <!-- Database & API Tables -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Recent Scans -->
        <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <h2 class="text-xl font-bold text-white mb-4">Recent Scans</h2>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="text-left text-gray-400 text-sm border-b border-slate-700">
                  <th class="pb-3">Repository</th>
                  <th class="pb-3">Type</th>
                  <th class="pb-3">Vulns</th>
                  <th class="pb-3">Status</th>
                  <th class="pb-3">Time</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="scan in recentScans" :key="scan.id" class="border-b border-slate-700/50">
                  <td class="py-3 text-white">{{ scan.repository }}</td>
                  <td class="py-3 text-gray-400">{{ scan.type }}</td>
                  <td class="py-3">
                    <span :class="`px-2 py-1 rounded text-xs font-bold ${getVulnClass(scan.vulns)}`">
                      {{ scan.vulns }}
                    </span>
                  </td>
                  <td class="py-3">
                    <span :class="`px-2 py-1 rounded text-xs font-bold ${getStatusClass(scan.status)}`">
                      {{ scan.status }}
                    </span>
                  </td>
                  <td class="py-3 text-gray-400 text-sm">{{ scan.time }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- API Usage -->
        <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
          <h2 class="text-xl font-bold text-white mb-4">API Usage by Endpoint</h2>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="text-left text-gray-400 text-sm border-b border-slate-700">
                  <th class="pb-3">Endpoint</th>
                  <th class="pb-3">Requests</th>
                  <th class="pb-3">Errors</th>
                  <th class="pb-3">Avg Latency</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="api in apiUsage" :key="api.endpoint" class="border-b border-slate-700/50">
                  <td class="py-3 text-white font-mono text-sm">{{ api.endpoint }}</td>
                  <td class="py-3 text-gray-400">{{ api.requests.toLocaleString() }}</td>
                  <td class="py-3">
                    <span :class="api.errors > 0 ? 'text-red-400' : 'text-green-400'">
                      {{ api.errors }}
                    </span>
                  </td>
                  <td class="py-3 text-gray-400">{{ api.latency }}ms</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { superAdminApi } from '../services/api'

const timeRange = ref('24h')
const activityChartRef = ref<HTMLElement | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

// Quick Stats
const quickStats = ref([
  {
    label: 'Total Users',
    value: '0',
    trend: 0,
    period: 'this month',
    icon: null as any,
    bgColor: 'bg-blue-500/20'
  },
  {
    label: 'Active Scans',
    value: '0',
    trend: 0,
    period: 'today',
    icon: null as any,
    bgColor: 'bg-cyan-500/20'
  },
  {
    label: 'Vulnerabilities Found',
    value: '0',
    trend: 0,
    period: 'this week',
    icon: null as any,
    bgColor: 'bg-red-500/20'
  },
  {
    label: 'API Requests',
    value: '0',
    trend: 0,
    period: 'this month',
    icon: null as any,
    bgColor: 'bg-purple-500/20'
  }
])

// System Services
const systemServices = ref([
  { name: 'API Server', status: 'healthy', uptime: 0 },
  { name: 'AI Service', status: 'healthy', uptime: 0 },
  { name: 'Database', status: 'healthy', uptime: 0 },
  { name: 'Cache Layer', status: 'healthy', uptime: 0 },
  { name: 'ML Engine', status: 'healthy', uptime: 0 },
  { name: 'Scanner Service', status: 'healthy', uptime: 0 }
])

// Resources
const resources = ref({
  cpu: 0,
  memory: 0,
  storage: 0,
  network: 0
})

// Top Users
const topUsers = ref<any[]>([])

// Security Alerts
const securityAlerts = ref<any[]>([])

// Vulnerability Distribution
const vulnDistribution = ref([
  { type: 'Critical', count: 0, color: 'bg-red-500' },
  { type: 'High', count: 0, color: 'bg-orange-500' },
  { type: 'Medium', count: 0, color: 'bg-yellow-500' },
  { type: 'Low', count: 0, color: 'bg-blue-500' }
])

// AI Metrics
const aiMetrics = ref({
  totalRequests: 0,
  avgResponseTime: 0,
  successRate: 0,
  tokensUsed: 0,
  apiCost: 0
})

// Recent Scans
const recentScans = ref<any[]>([])

// API Usage
const apiUsage = ref<any[]>([])

// Fetch dashboard data
const fetchDashboardData = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await superAdminApi.getDashboard(timeRange.value)
    
    if (response.success && response.data) {
      const data = response.data
      
      // Update quick stats
      if (data.stats) {
        quickStats.value[0].value = (data.stats.total_users || 0).toLocaleString()
        quickStats.value[1].value = (data.stats.active_scans || 0).toLocaleString()
        quickStats.value[2].value = (data.stats.vulnerabilities_found || 0).toLocaleString()
        quickStats.value[3].value = formatNumber(data.stats.api_requests || 0)
      }
      
      // Update system health
      if (data.system_health) {
        systemServices.value = Object.entries(data.system_health).map(([name, info]: [string, any]) => ({
          name: name.charAt(0).toUpperCase() + name.slice(1).replace('_', ' '),
          status: info.status || 'healthy',
          uptime: info.uptime || 0
        }))
      }
      
      // Update resources
      if (data.resources) {
        resources.value = data.resources
      }
      
      // Update top users
      if (data.top_users) {
        topUsers.value = data.top_users.map((user: any, index: number) => ({
          name: user.name,
          email: user.email,
          scans: user.repo_count || 0,
          apiCalls: user.vuln_count || 0
        }))
      }
      
      // Update security alerts
      if (data.security_alerts) {
        securityAlerts.value = data.security_alerts
      }
      
      // Update vulnerability distribution
      if (data.vulnerability_distribution) {
        vulnDistribution.value = data.vulnerability_distribution.map((v: any) => ({
          type: v.type,
          count: v.count,
          color: v.type === 'Critical' ? 'bg-red-500' : 
                 v.type === 'High' ? 'bg-orange-500' : 
                 v.type === 'Medium' ? 'bg-yellow-500' : 'bg-blue-500'
        }))
      }
      
      // Update AI metrics
      if (data.ai_metrics) {
        aiMetrics.value = data.ai_metrics
      }
      
      // Update recent scans
      if (data.recent_scans) {
        recentScans.value = data.recent_scans.map((scan: any) => ({
          id: scan.id,
          repository: scan.repository_name || 'Unknown',
          type: scan.scan_type || 'Full Scan',
          vulns: scan.vulnerabilities_found || 0,
          status: scan.status || 'unknown',
          time: formatTimeAgo(scan.created_at)
        }))
      }
      
      // Update API usage
      if (data.api_usage) {
        apiUsage.value = data.api_usage
      }
    }
  } catch (err: any) {
    console.error('Failed to fetch dashboard data:', err)
    error.value = err.message || 'Failed to load dashboard data'
    loadMockData() // Fallback to mock data on error
  } finally {
    loading.value = false
  }
}

// Helper functions
const formatNumber = (num: number): string => {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
  return num.toString()
}

const formatTimeAgo = (dateString: string): string => {
  if (!dateString) return 'Unknown'
  const date = new Date(dateString)
  const now = new Date()
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000)
  
  if (seconds < 60) return 'Just now'
  if (seconds < 3600) return `${Math.floor(seconds / 60)} min ago`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`
  return `${Math.floor(seconds / 86400)} days ago`
}

// Load mock data as fallback
const loadMockData = () => {
  quickStats.value[0].value = '2,847'
  quickStats.value[1].value = '156'
  quickStats.value[2].value = '1,423'
  quickStats.value[3].value = '1.2M'
  
  systemServices.value = [
    { name: 'API Server', status: 'healthy', uptime: 99.99 },
    { name: 'AI Service', status: 'healthy', uptime: 99.87 },
    { name: 'Database', status: 'healthy', uptime: 99.95 },
    { name: 'Cache Layer', status: 'healthy', uptime: 99.99 },
    { name: 'ML Engine', status: 'warning', uptime: 98.45 },
    { name: 'Scanner Service', status: 'healthy', uptime: 99.78 }
  ]
  
  resources.value = { cpu: 45, memory: 62, storage: 38, network: 78 }
  
  topUsers.value = [
    { name: 'John Smith', email: 'john@enterprise.com', scans: 234, apiCalls: 4521 },
    { name: 'Sarah Johnson', email: 'sarah@techcorp.io', scans: 189, apiCalls: 3892 },
    { name: 'Michael Chen', email: 'm.chen@devteam.com', scans: 156, apiCalls: 2934 },
    { name: 'Emily Davis', email: 'emily@startup.co', scans: 134, apiCalls: 2456 },
    { name: 'Robert Wilson', email: 'r.wilson@bigcorp.net', scans: 98, apiCalls: 1823 }
  ]
  
  securityAlerts.value = [
    { id: 1, title: 'Failed Login Attempt', message: 'Multiple failed login attempts from IP 192.168.1.105', severity: 'high', time: '2 minutes ago' },
    { id: 2, title: 'New Admin User', message: 'New administrator account created', severity: 'medium', time: '15 minutes ago' },
    { id: 3, title: 'API Rate Limit Exceeded', message: 'User exceeded rate limit (5000 req/min)', severity: 'low', time: '32 minutes ago' },
    { id: 4, title: 'Critical Vulnerability Found', message: 'SQL Injection in repository api-service', severity: 'critical', time: '1 hour ago' },
    { id: 5, title: 'SSL Certificate Expiring', message: 'Certificate expires in 7 days', severity: 'medium', time: '2 hours ago' }
  ]
  
  vulnDistribution.value = [
    { type: 'Critical', count: 45, color: 'bg-red-500' },
    { type: 'High', count: 128, color: 'bg-orange-500' },
    { type: 'Medium', count: 342, color: 'bg-yellow-500' },
    { type: 'Low', count: 908, color: 'bg-blue-500' }
  ]
  
  aiMetrics.value = {
    totalRequests: 156789,
    avgResponseTime: 342,
    successRate: 99.7,
    tokensUsed: 4567234,
    apiCost: 234.56
  }
  
  recentScans.value = [
    { id: 1, repository: 'api-gateway', type: 'Full Scan', vulns: 12, status: 'completed', time: '5 min ago' },
    { id: 2, repository: 'user-service', type: 'Incremental', vulns: 3, status: 'completed', time: '12 min ago' },
    { id: 3, repository: 'payment-module', type: 'Full Scan', vulns: 28, status: 'completed', time: '25 min ago' },
    { id: 4, repository: 'auth-service', type: 'Full Scan', vulns: 0, status: 'completed', time: '1 hour ago' },
    { id: 5, repository: 'data-pipeline', type: 'Incremental', vulns: 7, status: 'running', time: '2 hours ago' }
  ]
  
  apiUsage.value = [
    { endpoint: '/api/v1/scan', requests: 45234, errors: 12, latency: 145 },
    { endpoint: '/api/v1/vulnerabilities', requests: 38921, errors: 5, latency: 89 },
    { endpoint: '/api/v1/ai-fix/generate', requests: 23456, errors: 23, latency: 2340 },
    { endpoint: '/api/v1/repositories', requests: 18234, errors: 2, latency: 67 },
    { endpoint: '/api/v1/users', requests: 12345, errors: 0, latency: 45 }
  ]
}

const getAlertClass = (severity: string) => {
  switch (severity) {
    case 'critical': return 'bg-red-900/30 border-red-500'
    case 'high': return 'bg-orange-900/30 border-orange-500'
    case 'medium': return 'bg-yellow-900/30 border-yellow-500'
    default: return 'bg-blue-900/30 border-blue-500'
  }
}

const getSeverityBadge = (severity: string) => {
  switch (severity) {
    case 'critical': return 'bg-red-500 text-white'
    case 'high': return 'bg-orange-500 text-white'
    case 'medium': return 'bg-yellow-500 text-black'
    default: return 'bg-blue-500 text-white'
  }
}

const getVulnClass = (count: number) => {
  if (count === 0) return 'bg-green-500/20 text-green-400'
  if (count < 5) return 'bg-yellow-500/20 text-yellow-400'
  if (count < 15) return 'bg-orange-500/20 text-orange-400'
  return 'bg-red-500/20 text-red-400'
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'completed': return 'bg-green-500/20 text-green-400'
    case 'running': return 'bg-blue-500/20 text-blue-400'
    case 'failed': return 'bg-red-500/20 text-red-400'
    default: return 'bg-gray-500/20 text-gray-400'
  }
}

const refreshData = () => {
  fetchDashboardData()
}

const runSystemScan = async () => {
  try {
    const response = await superAdminApi.runSystemScan('full', 'all')
    if (response.success) {
      console.log('System scan initiated:', response.data)
    }
  } catch (err) {
    console.error('Failed to run system scan:', err)
  }
}

const generateReport = async () => {
  try {
    const now = new Date()
    const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)
    const response = await superAdminApi.generateReport(
      'detailed',
      monthAgo.toISOString(),
      now.toISOString(),
      'pdf'
    )
    if (response.success) {
      console.log('Report generated:', response.data)
    }
  } catch (err) {
    console.error('Failed to generate report:', err)
  }
}

const viewAuditLogs = async () => {
  try {
    const response = await superAdminApi.getAuditLogs(100, 0)
    if (response.success) {
      console.log('Audit logs:', response.data)
    }
  } catch (err) {
    console.error('Failed to fetch audit logs:', err)
  }
}

const manageUsers = async () => {
  try {
    const response = await superAdminApi.manageUsers('list', { per_page: 10 })
    if (response.success) {
      console.log('Users:', response.data)
    }
  } catch (err) {
    console.error('Failed to fetch users:', err)
  }
}

// Watch for time range changes
watch(timeRange, () => {
  fetchDashboardData()
})

onMounted(() => {
  fetchDashboardData()
})
</script>
