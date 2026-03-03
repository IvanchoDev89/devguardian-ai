<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
    <Navbar />
    
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-white">Admin Dashboard</h1>
          <p class="text-gray-400 mt-1">Manage your DevGuardian AI organization</p>
        </div>
        <div class="flex gap-3">
          <router-link 
            to="/scan"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
          >
            <span>🔍</span> New Scan
          </router-link>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <!-- Total Scans -->
        <div class="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Total Scans</p>
              <p class="text-3xl font-bold text-white mt-1">{{ stats.totalScans }}</p>
            </div>
            <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>
          <p class="text-green-400 text-sm mt-2">↑ Active</p>
        </div>

        <!-- Vulnerabilities Found -->
        <div class="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Vulnerabilities</p>
              <p class="text-3xl font-bold text-white mt-1">{{ stats.totalVulnerabilities }}</p>
            </div>
            <div class="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
              </svg>
            </div>
          </div>
          <p class="text-gray-400 text-sm mt-2">{{ Math.floor(stats.totalVulnerabilities * 0.3) }} critical</p>
        </div>

        <!-- Security Score -->
        <div class="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Security Score</p>
              <p class="text-3xl font-bold mt-1" :class="scoreColor">{{ stats.securityScore }}</p>
            </div>
            <div class="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
          </div>
          <p class="text-gray-400 text-sm mt-2">
            {{ stats.securityScore >= 80 ? 'Excellent' : stats.securityScore >= 50 ? 'Needs Work' : 'Critical' }}
          </p>
        </div>

        <!-- Account -->
        <div class="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Plan</p>
              <p class="text-3xl font-bold text-white mt-1 capitalize">{{ userPlan }}</p>
            </div>
            <div class="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
              </svg>
            </div>
          </div>
          <p class="text-gray-400 text-sm mt-2">{{ userRole }} access</p>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Recent Scans -->
        <div class="lg:col-span-2 bg-gray-800/50 border border-gray-700 rounded-xl">
          <div class="px-5 py-4 border-b border-gray-700 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-white">Recent Scans</h2>
            <button class="text-blue-400 text-sm hover:text-blue-300">View All</button>
          </div>
          <div class="divide-y divide-gray-700">
            <div 
              v-for="scan in recentScans" 
              :key="scan.id"
              class="px-5 py-4 hover:bg-gray-700/30 transition-colors"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center">
                    <span class="text-blue-400">🔍</span>
                  </div>
                  <div>
                    <p class="text-white font-medium">{{ scan.name }}</p>
                    <p class="text-gray-400 text-sm">{{ scan.language }} • {{ scan.date }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <span 
                    class="px-2 py-1 rounded text-xs font-medium"
                    :class="{
                      'bg-green-500/20 text-green-400': scan.score >= 80,
                      'bg-yellow-500/20 text-yellow-400': scan.score >= 50 && scan.score < 80,
                      'bg-red-500/20 text-red-400': scan.score < 50
                    }"
                  >
                    Score: {{ scan.score }}
                  </span>
                  <p class="text-gray-500 text-xs mt-1">{{ scan.issues }} issues</p>
                </div>
              </div>
            </div>
            
            <div v-if="!recentScans.length" class="px-5 py-8 text-center text-gray-400">
              <p class="mb-2">No scans yet.</p>
              <router-link to="/scan" class="text-blue-400 hover:text-blue-300">Run your first scan →</router-link>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Account Info -->
          <div class="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
            <h3 class="text-white font-semibold mb-4">Account</h3>
            <div class="space-y-3">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-white font-medium">
                  {{ userInitials }}
                </div>
                <div>
                  <p class="text-white font-medium">{{ userName }}</p>
                  <p class="text-gray-400 text-sm">{{ userEmail }}</p>
                </div>
              </div>
              <div class="pt-3 border-t border-gray-700">
                <span 
                  class="px-2 py-1 rounded text-xs font-medium"
                  :class="roleBadgeClass"
                >
                  {{ userRole }}
                </span>
              </div>
            </div>
          </div>

          <!-- Vulnerability Breakdown -->
          <div class="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
            <h3 class="text-white font-semibold mb-4">Vulnerability Types</h3>
            <div class="space-y-3">
              <div v-for="item in vulnBreakdown" :key="item.type" class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <span 
                    class="w-2 h-2 rounded-full"
                    :class="{
                      'bg-red-500': item.severity === 'critical',
                      'bg-orange-500': item.severity === 'high',
                      'bg-yellow-500': item.severity === 'medium',
                      'bg-blue-500': item.severity === 'low'
                    }"
                  ></span>
                  <span class="text-gray-300 text-sm">{{ item.type }}</span>
                </div>
                <span class="text-white font-medium">{{ item.count }}</span>
              </div>
              
              <div v-if="!vulnBreakdown.length" class="text-gray-400 text-sm text-center py-2">
                No data yet
              </div>
            </div>
          </div>

          <!-- System Status -->
          <div class="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
            <h3 class="text-white font-semibold mb-4">System Status</h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-gray-400 text-sm">AI Scanner</span>
                <span class="flex items-center gap-2 text-green-400 text-sm">
                  <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  Online
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400 text-sm">Last Scan</span>
                <span class="text-white text-sm">{{ lastScanTime }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-400 text-sm">API Status</span>
                <span class="text-green-400 text-sm">Ready</span>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="bg-gray-800/50 border border-gray-700 rounded-xl p-5">
            <h3 class="text-white font-semibold mb-4">Quick Actions</h3>
            <div class="space-y-2">
              <router-link 
                to="/scan"
                class="flex items-center gap-3 p-3 bg-gray-700/50 rounded-lg hover:bg-gray-700 transition-colors text-blue-400 hover:text-blue-300"
              >
                <span>🔍</span>
                <span class="text-sm">Run New Scan</span>
              </router-link>
              
              <router-link 
                to="/settings"
                class="flex items-center gap-3 p-3 bg-gray-700/50 rounded-lg hover:bg-gray-700 transition-colors text-gray-300 hover:text-white"
              >
                <span>⚙️</span>
                <span class="text-sm">Settings</span>
              </router-link>
              
              <router-link 
                to="/docs"
                class="flex items-center gap-3 p-3 bg-gray-700/50 rounded-lg hover:bg-gray-700 transition-colors text-gray-300 hover:text-white"
              >
                <span>📚</span>
                <span class="text-sm">Documentation</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'

const stats = ref({
  totalScans: 0,
  totalVulnerabilities: 0,
  securityScore: 100
})

const recentScans = ref<any[]>([])
const vulnBreakdown = ref<any[]>([])
const lastScanTime = ref('Never')

// User data
const userData = computed(() => {
  const stored = localStorage.getItem('user')
  if (stored) {
    try {
      return JSON.parse(stored)
    } catch {
      return null
    }
  }
  return null
})

const userName = computed(() => userData.value?.name || 'Admin User')
const userEmail = computed(() => userData.value?.email || 'admin@devguardian.ai')
const userRole = computed(() => userData.value?.role || 'super_admin')
const userPlan = computed(() => localStorage.getItem('plan') || 'enterprise')
const userInitials = computed(() => {
  const name = userName.value
  if (name && name.length > 0) {
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
  }
  return 'A'
})

const roleBadgeClass = computed(() => {
  const role = userRole.value
  if (role === 'super_admin') return 'bg-red-500/20 text-red-400'
  if (role === 'admin') return 'bg-orange-500/20 text-orange-400'
  return 'bg-gray-500/20 text-gray-400'
})

const scoreColor = computed(() => {
  if (stats.value.securityScore >= 80) return 'text-green-400'
  if (stats.value.securityScore >= 50) return 'text-yellow-400'
  return 'text-red-400'
})

onMounted(() => {
  // Load from localStorage
  stats.value.totalScans = parseInt(localStorage.getItem('scans_count') || '0')
  stats.value.totalVulnerabilities = parseInt(localStorage.getItem('vuln_count') || '0')
  
  // Calculate security score
  if (stats.value.totalScans > 0) {
    stats.value.securityScore = Math.max(0, 100 - (stats.value.totalVulnerabilities * 5))
  } else {
    stats.value.securityScore = 100
  }
  
  // Load recent scans
  const savedScans = localStorage.getItem('recent_scans')
  if (savedScans) {
    try {
      recentScans.value = JSON.parse(savedScans)
    } catch {
      recentScans.value = []
    }
  }
  
  // Set last scan time
  const lastScan = localStorage.getItem('last_scan_time')
  if (lastScan) {
    const date = new Date(lastScan)
    lastScanTime.value = date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
  }
  
  // Build vuln breakdown
  if (stats.value.totalVulnerabilities > 0) {
    vulnBreakdown.value = [
      { type: 'SQL Injection', severity: 'critical', count: Math.floor(stats.value.totalVulnerabilities * 0.3) },
      { type: 'Hardcoded Secrets', severity: 'critical', count: Math.floor(stats.value.totalVulnerabilities * 0.25) },
      { type: 'XSS', severity: 'high', count: Math.floor(stats.value.totalVulnerabilities * 0.2) },
      { type: 'Command Injection', severity: 'high', count: Math.floor(stats.value.totalVulnerabilities * 0.15) },
      { type: 'Other', severity: 'medium', count: Math.floor(stats.value.totalVulnerabilities * 0.1) }
    ].filter(x => x.count > 0)
  }
})
</script>
