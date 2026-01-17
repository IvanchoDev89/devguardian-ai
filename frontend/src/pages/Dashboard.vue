<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- Header Section -->
    <div class="px-4 py-6 sm:px-0">
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 flex items-center gap-3">
              <span class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Security Dashboard
              </span>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Live
              </span>
            </h1>
            <p class="text-gray-600 mt-2">Monitor your security posture and AI-powered fixes</p>
          </div>
          <div class="flex items-center gap-3">
            <button 
              @click="refreshData"
              :disabled="loading"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-700" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="-ml-1 mr-2 h-4 w-4 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              Refresh
            </button>
          </div>
        </div>
      </div>

      <!-- Stats Overview -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Total Vulnerabilities</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.totalVulnerabilities }}</p>
              <div class="flex items-center mt-2">
                <span class="text-sm text-red-600 font-medium">{{ stats.criticalVulnerabilities }} critical</span>
                <span class="text-gray-400 mx-2">•</span>
                <span class="text-sm text-gray-500">{{ stats.newThisWeek }} this week</span>
              </div>
            </div>
            <div class="bg-red-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Repositories</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.totalRepositories }}</p>
              <div class="flex items-center mt-2">
                <span class="text-sm text-green-600 font-medium">{{ stats.scanningRepositories }} scanning</span>
                <span class="text-gray-400 mx-2">•</span>
                <span class="text-sm text-gray-500">{{ stats.healthyRepositories }} healthy</span>
              </div>
            </div>
            <div class="bg-blue-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">AI Fixes Generated</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.aiFixesGenerated }}</p>
              <div class="flex items-center mt-2">
                <span class="text-sm text-green-600 font-medium">{{ stats.successRate }}% success</span>
                <span class="text-gray-400 mx-2">•</span>
                <span class="text-sm text-gray-500">{{ stats.pendingFixes }} pending</span>
              </div>
            </div>
            <div class="bg-green-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Security Score</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.securityScore }}</p>
              <div class="flex items-center mt-2">
                <span class="text-sm font-medium" :class="getScoreColor(stats.securityScore)">
                  {{ getScoreLabel(stats.securityScore) }}
                </span>
                <span class="text-gray-400 mx-2">•</span>
                <span class="text-sm text-gray-500">+{{ stats.scoreChange }} this month</span>
              </div>
            </div>
            <div class="bg-purple-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Vulnerability Trends -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Vulnerability Trends</h3>
            <select class="text-sm border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500">
              <option>Last 7 days</option>
              <option>Last 30 days</option>
              <option>Last 3 months</option>
            </select>
          </div>
          <div class="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
            <div class="text-center">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
              <p class="mt-2 text-sm text-gray-500">Chart visualization coming soon</p>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Recent Activity</h3>
            <router-link to="/ai-fixes" class="text-sm text-blue-600 hover:text-blue-800 font-medium">
              View all
            </router-link>
          </div>
          <div class="space-y-4">
            <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start space-x-3">
              <div class="flex-shrink-0">
                <div :class="getActivityIconClass(activity.type)" class="rounded-full p-2">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getActivityIcon(activity.type)"></path>
                  </svg>
                </div>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm text-gray-900">{{ activity.title }}</p>
                <p class="text-xs text-gray-500">{{ activity.time }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button class="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <div class="bg-blue-100 rounded-lg p-2 mr-3">
              <svg class="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
            </div>
            <div class="text-left">
              <p class="text-sm font-medium text-gray-900">Add Repository</p>
              <p class="text-xs text-gray-500">Connect a new repository</p>
            </div>
          </button>

          <button class="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <div class="bg-green-100 rounded-lg p-2 mr-3">
              <svg class="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="text-left">
              <p class="text-sm font-medium text-gray-900">Run Scan</p>
              <p class="text-xs text-gray-500">Start security scan</p>
            </div>
          </button>

          <button class="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <div class="bg-purple-100 rounded-lg p-2 mr-3">
              <svg class="h-5 w-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
            <div class="text-left">
              <p class="text-sm font-medium text-gray-900">Generate Fix</p>
              <p class="text-xs text-gray-500">AI-powered fixes</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Activity {
  id: string
  type: 'vulnerability' | 'fix' | 'scan' | 'repository'
  title: string
  time: string
}

interface Stats {
  totalVulnerabilities: number
  criticalVulnerabilities: number
  newThisWeek: number
  totalRepositories: number
  scanningRepositories: number
  healthyRepositories: number
  aiFixesGenerated: number
  successRate: number
  pendingFixes: number
  securityScore: number
  scoreChange: number
}

const loading = ref(false)
const stats = ref<Stats>({
  totalVulnerabilities: 24,
  criticalVulnerabilities: 3,
  newThisWeek: 7,
  totalRepositories: 12,
  scanningRepositories: 2,
  healthyRepositories: 10,
  aiFixesGenerated: 18,
  successRate: 94,
  pendingFixes: 4,
  securityScore: 87,
  scoreChange: 5
})

const recentActivity = ref<Activity[]>([
  {
    id: '1',
    type: 'vulnerability',
    title: 'Critical SQL injection found in auth module',
    time: '2 minutes ago'
  },
  {
    id: '2',
    type: 'fix',
    title: 'AI fix applied to payment service',
    time: '15 minutes ago'
  },
  {
    id: '3',
    type: 'scan',
    title: 'Security scan completed for user-service',
    time: '1 hour ago'
  },
  {
    id: '4',
    type: 'repository',
    title: 'New repository connected: frontend-app',
    time: '3 hours ago'
  }
])

const getScoreColor = (score: number): string => {
  if (score >= 90) return 'text-green-600'
  if (score >= 70) return 'text-yellow-600'
  return 'text-red-600'
}

const getScoreLabel = (score: number): string => {
  if (score >= 90) return 'Excellent'
  if (score >= 70) return 'Good'
  return 'Needs Improvement'
}

const getActivityIconClass = (type: string): string => {
  const classes: Record<string, string> = {
    vulnerability: 'bg-red-100 text-red-600',
    fix: 'bg-green-100 text-green-600',
    scan: 'bg-blue-100 text-blue-600',
    repository: 'bg-purple-100 text-purple-600'
  }
  return classes[type] || 'bg-gray-100 text-gray-600'
}

const getActivityIcon = (type: string): string => {
  const icons: Record<string, string> = {
    vulnerability: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z',
    fix: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
    scan: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
    repository: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4'
  }
  return icons[type] || 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
}

const refreshData = async () => {
  loading.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    // Update stats with new data
  } catch (error) {
    console.error('Failed to refresh dashboard data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // Initialize dashboard data
})
</script>
