<template>
  <div class="flex h-screen bg-slate-900">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-800/50 backdrop-blur-sm border-r border-white/10 flex flex-col">
      <!-- Logo -->
      <div class="flex items-center h-16 px-6 border-b border-white/10">
        <router-link to="/" class="flex items-center">
          <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center mr-3">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <span class="text-lg font-bold text-white">DevGuardian</span>
        </router-link>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200"
          :class="[
            $route.path === item.path 
              ? 'bg-gradient-to-r from-blue-600/20 to-cyan-600/20 text-white border-l-2 border-cyan-400' 
              : 'text-gray-400 hover:text-white hover:bg-white/5'
          ]"
        >
          <component :is="item.icon" class="w-5 h-5 mr-3 flex-shrink-0" />
          {{ item.name }}
        </router-link>
      </nav>

      <!-- User Section -->
      <div class="p-4 border-t border-white/10">
        <div class="flex items-center">
          <img 
            :src="user?.avatar || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=32&h=32&fit=crop&crop=face'" 
            class="w-10 h-10 rounded-full border-2 border-white/20"
          />
          <div class="ml-3 flex-1 min-w-0">
            <p class="text-sm font-medium text-white truncate">{{ user?.name || 'User' }}</p>
            <p class="text-xs text-gray-400 truncate">{{ user?.email || '' }}</p>
          </div>
          <button 
            @click="handleLogout"
            class="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
            title="Logout"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Bar -->
      <header class="flex items-center h-16 px-6 bg-slate-900/50 backdrop-blur-sm border-b border-white/10">
        <h1 class="text-lg font-semibold text-white">Dashboard</h1>
        
        <div class="flex-1"></div>
        
        <button 
          @click="refreshData"
          :disabled="loading"
          class="flex items-center px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-sm font-medium text-white hover:bg-white/20 disabled:opacity-50 transition-all"
        >
          <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          Refresh
        </button>
      </header>

      <!-- Dashboard Content -->
      <main class="flex-1 overflow-y-auto p-6">
        <!-- Background Pattern -->
        <div class="absolute inset-0 bg-grid-white/5 bg-grid-16 pointer-events-none"></div>
        
        <!-- Error Alert -->
        <div v-if="error" class="mb-6 bg-red-500/10 backdrop-blur-sm rounded-lg p-4 border border-red-500/30">
          <div class="flex">
            <svg class="w-5 h-5 text-red-400 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            <div>
              <h3 class="text-sm font-medium text-red-400">Error Loading Data</h3>
              <p class="text-sm text-red-300 mt-1">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-400">Total Scans</p>
                <p class="text-3xl font-bold text-white mt-1">{{ stats.totalScans }}</p>
              </div>
              <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-400">Critical Vulnerabilities</p>
                <p class="text-3xl font-bold text-red-400 mt-1">{{ stats.criticalVulns }}</p>
              </div>
              <div class="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-400">Fixed Today</p>
                <p class="text-3xl font-bold text-green-400 mt-1">{{ stats.fixedToday }}</p>
              </div>
              <div class="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-400">Security Score</p>
                <p class="text-3xl font-bold text-cyan-400 mt-1">{{ stats.securityScore }}%</p>
              </div>
              <div class="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <router-link 
            to="/sql-injection-scanner"
            class="bg-gradient-to-r from-blue-600/20 to-cyan-600/20 border border-blue-500/30 rounded-xl p-6 hover:from-blue-600/30 hover:to-cyan-600/30 transition-all group"
          >
            <div class="flex items-center">
              <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-semibold text-white">Run New Scan</h3>
                <p class="text-sm text-gray-400">Analyze your code for vulnerabilities</p>
              </div>
            </div>
          </router-link>

          <router-link 
            to="/vulnerabilities"
            class="bg-white/5 border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all group"
          >
            <div class="flex items-center">
              <div class="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-semibold text-white">View Vulnerabilities</h3>
                <p class="text-sm text-gray-400">{{ vulnerabilities.length }} open issues</p>
              </div>
            </div>
          </router-link>

          <router-link 
            to="/ai-fixes"
            class="bg-white/5 border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all group"
          >
            <div class="flex items-center">
              <div class="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-semibold text-white">AI Fixes</h3>
                <p class="text-sm text-gray-400">Get AI-generated patches</p>
              </div>
            </div>
          </router-link>
        </div>

        <!-- Recent Scans & Vulnerabilities -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Recent Scans -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <h3 class="text-lg font-semibold text-white mb-4">Recent Scans</h3>
            <div class="space-y-3">
              <div 
                v-for="scan in recentScans" 
                :key="scan.id"
                class="flex items-center justify-between p-3 bg-white/5 rounded-lg"
              >
                <div class="flex items-center">
                  <div :class="['w-2 h-2 rounded-full mr-3', getStatusColor(scan.status)]"></div>
                  <div>
                    <p class="text-sm font-medium text-white">{{ scan.repository || scan.name || 'Unknown' }}</p>
                    <p class="text-xs text-gray-400">{{ scan.time || scan.created_at || 'Recently' }}</p>
                  </div>
                </div>
                <span :class="['px-2 py-1 text-xs rounded-full', getSeverityClass(scan.severity)]">
                  {{ scan.vulnerabilities || scan.severity || 'N/A' }}
                </span>
              </div>
              <div v-if="recentScans.length === 0" class="text-center py-8 text-gray-400">
                No scans yet. Start your first scan!
              </div>
            </div>
          </div>

          <!-- Recent Vulnerabilities -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <h3 class="text-lg font-semibold text-white mb-4">Recent Vulnerabilities</h3>
            <div class="space-y-3">
              <div 
                v-for="vuln in filteredVulnerabilities.slice(0, 5)" 
                :key="vuln.id"
                class="flex items-center justify-between p-3 bg-white/5 rounded-lg"
              >
                <div class="flex items-center">
                  <div :class="['w-2 h-2 rounded-full mr-3', getSeverityColor(vuln.severity)]"></div>
                  <div>
                    <p class="text-sm font-medium text-white">{{ vuln.title || vuln.type }}</p>
                    <p class="text-xs text-gray-400">{{ vuln.repository || vuln.file }}</p>
                  </div>
                </div>
                <span :class="['px-2 py-1 text-xs rounded-full', getSeverityClass(vuln.severity)]">
                  {{ vuln.severity }}
                </span>
              </div>
              <div v-if="vulnerabilities.length === 0" class="text-center py-8 text-gray-400">
                No vulnerabilities found. Great job!
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { dashboardService } from '../services/api'
import { useNotificationStore } from '../stores/notifications'
import { useAuthStore } from '../stores/auth'
import { 
  LayoutDashboard, 
  Search, 
  Shield, 
  Wrench, 
  Folder, 
  Pentagon, 
  Settings, 
  CreditCard, 
  ShieldAlert 
} from 'lucide-vue-next'

const router = useRouter()
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

const navItems = computed(() => {
  const items = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Scanner', path: '/sql-injection-scanner', icon: Search },
    { name: 'Repositories', path: '/repositories', icon: Folder },
    { name: 'Vulnerabilities', path: '/vulnerabilities', icon: Shield },
    { name: 'AI Fixes', path: '/ai-fixes', icon: Wrench },
    { name: 'Pentesting', path: '/pentesting', icon: Pentagon },
  ]
  
  if (authStore.isAdmin) {
    items.push({ name: 'Admin Panel', path: '/super-admin', icon: ShieldAlert })
  }
  
  items.push({ name: 'Enterprise Assets', path: '/enterprise-assets', icon: Folder })
  
  items.push(
    { name: 'Billing', path: '/billing', icon: CreditCard },
    { name: 'Settings', path: '/settings', icon: Settings }
  )
  
  return items
})

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

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  refreshData()
})
</script>
