<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <div class="px-4 py-6 sm:px-0">
      <!-- Header Section -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Security Vulnerabilities</h1>
            <p class="text-gray-600 mt-2">View and manage security vulnerabilities across all repositories</p>
          </div>
          <button 
            @click="runScan"
            :disabled="scanning"
            class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <svg v-if="scanning" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="-ml-1 mr-2 h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            {{ scanning ? 'Scanning...' : 'Run Scan' }}
          </button>
        </div>
      </div>

      <!-- Stats Overview -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Total Vulnerabilities</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.total }}</p>
            </div>
            <div class="bg-red-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Critical</p>
              <p class="text-2xl font-bold text-red-600 mt-1">{{ stats.critical }}</p>
            </div>
            <div class="bg-red-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">High</p>
              <p class="text-2xl font-bold text-orange-600 mt-1">{{ stats.high }}</p>
            </div>
            <div class="bg-orange-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Fixed</p>
              <p class="text-2xl font-bold text-green-600 mt-1">{{ stats.fixed }}</p>
            </div>
            <div class="bg-green-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters and Search -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
        <div class="flex flex-col sm:flex-row gap-4">
          <div class="flex-1">
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search vulnerabilities..."
                class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
          <div class="flex gap-2">
            <select v-model="filterSeverity" class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">All Severities</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
            <select v-model="filterStatus" class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">All Status</option>
              <option value="open">Open</option>
              <option value="fixing">Fixing</option>
              <option value="fixed">Fixed</option>
            </select>
            <select v-model="sortBy" class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="severity">Severity</option>
              <option value="date">Date</option>
              <option value="repository">Repository</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Vulnerability List -->
      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="text-center">
          <svg class="animate-spin h-8 w-8 text-blue-600 mx-auto" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p class="mt-2 text-sm text-gray-600">Scanning for vulnerabilities...</p>
        </div>
      </div>

      <div v-else-if="filteredVulnerabilities.length === 0" class="text-center py-12">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <h3 class="mt-4 text-lg font-medium text-gray-900">No vulnerabilities found</h3>
          <p class="mt-2 text-sm text-gray-500">
            {{ searchQuery ? 'Try adjusting your search terms' : 'Great! No vulnerabilities detected in your repositories' }}
          </p>
        </div>
      </div>

      <div v-else class="space-y-4">
        <div 
          v-for="vulnerability in filteredVulnerabilities" 
          :key="vulnerability.id"
          class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center">
              <div :class="getSeverityIconClass(vulnerability.severity)" class="rounded-lg p-2 mr-3">
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-medium text-gray-900">{{ vulnerability.title }}</h3>
                <p class="text-sm text-gray-500">{{ vulnerability.description }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <span 
                :class="getSeverityClass(vulnerability.severity)"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              >
                {{ vulnerability.severity }}
              </span>
              <span 
                :class="getStatusClass(vulnerability.status)"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              >
                {{ vulnerability.status }}
              </span>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span class="text-gray-600">Repository:</span>
              <span class="font-medium text-gray-900">{{ vulnerability.repository }}</span>
            </div>
            <div>
              <span class="text-gray-600">File:</span>
              <span class="font-medium text-gray-900">{{ vulnerability.file }}</span>
            </div>
            <div>
              <span class="text-gray-600">CWE ID:</span>
              <span class="font-medium text-gray-900">{{ vulnerability.cweId }}</span>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-gray-200">
            <div class="flex items-center justify-between">
              <div class="text-sm text-gray-500">
                Detected {{ vulnerability.detectedAt }}
              </div>
              <div class="flex items-center space-x-2">
                <button 
                  @click="generateFix(vulnerability.id)"
                  :disabled="vulnerability.status === 'fixing'"
                  class="inline-flex items-center px-3 py-1.5 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg class="-ml-1 mr-2 h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                  </svg>
                  {{ vulnerability.status === 'fixing' ? 'Generating...' : 'Generate Fix' }}
                </button>
                <button 
                  @click="viewDetails(vulnerability.id)"
                  class="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  View Details
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { vulnerabilityService } from '../services/api'

interface Vulnerability {
  id: string
  title: string
  description: string
  severity: 'critical' | 'high' | 'medium' | 'low'
  status: 'open' | 'in_progress' | 'fixing' | 'resolved' | 'fixed'
  repository: string
  file: string
  cweId: string
  cvss_score?: number
  detectedAt: string
}

interface Stats {
  total: number
  critical: number
  high: number
  fixed: number
}

const loading = ref(false)
const scanning = ref(false)
const searchQuery = ref('')
const filterSeverity = ref('')
const filterStatus = ref('')
const sortBy = ref('severity')

const stats = ref<Stats>({
  total: 0,
  critical: 0,
  high: 0,
  fixed: 0
})

const vulnerabilities = ref<Vulnerability[]>([])

const loadVulnerabilities = async () => {
  loading.value = true
  try {
    const response = await vulnerabilityService.getVulnerabilities()
    if (response.success && response.data) {
      vulnerabilities.value = (Array.isArray(response.data) ? response.data : []).map((v: any) => ({
        id: v.id?.toString() || '0',
        title: v.title || 'Unknown Vulnerability',
        description: v.description || '',
        severity: v.severity || 'medium',
        status: v.status === 'open' ? 'open' : v.status === 'in_progress' ? 'fixing' : v.status === 'resolved' ? 'resolved' : 'open',
        repository: v.repository || 'unknown',
        file: v.file || v.repository || '',
        cweId: v.cwe_id || v.cweId || '',
        cvss_score: v.cvss_score,
        detectedAt: v.detected_at || v.created_at || new Date().toISOString()
      }))
    }
  } catch (error) {
    console.error('Failed to load vulnerabilities:', error)
  } finally {
    loading.value = false
    updateStats()
  }
}

const updateStats = () => {
  stats.value.total = vulnerabilities.value.length
  stats.value.critical = vulnerabilities.value.filter(v => v.severity === 'critical').length
  stats.value.high = vulnerabilities.value.filter(v => v.severity === 'high').length
  stats.value.fixed = vulnerabilities.value.filter(v => v.status === 'resolved' || v.status === 'fixed').length
}

const filteredVulnerabilities = computed(() => {
  let filtered = vulnerabilities.value

  // Filter by search query
  if (searchQuery.value) {
    filtered = filtered.filter(vuln => 
      vuln.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      vuln.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  // Filter by severity
  if (filterSeverity.value) {
    filtered = filtered.filter(vuln => vuln.severity === filterSeverity.value)
  }

  // Filter by status
  if (filterStatus.value) {
    filtered = filtered.filter(vuln => vuln.status === filterStatus.value)
  }

  // Sort
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'severity':
        const severityOrder = { critical: 4, high: 3, medium: 2, low: 1 }
        return severityOrder[b.severity] - severityOrder[a.severity]
      case 'date':
        return b.detectedAt.localeCompare(a.detectedAt)
      case 'repository':
        return a.repository.localeCompare(b.repository)
      default:
        return 0
    }
  })

  return filtered
})

const getSeverityClass = (severity: string): string => {
  const classes: Record<string, string> = {
    critical: 'bg-red-100 text-red-800',
    high: 'bg-orange-100 text-orange-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-blue-100 text-blue-800'
  }
  return classes[severity] || 'bg-gray-100 text-gray-800'
}

const getStatusClass = (status: string): string => {
  const classes: Record<string, string> = {
    open: 'bg-red-100 text-red-800',
    fixing: 'bg-yellow-100 text-yellow-800',
    fixed: 'bg-green-100 text-green-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getSeverityIconClass = (severity: string): string => {
  const classes: Record<string, string> = {
    critical: 'bg-red-100 text-red-600',
    high: 'bg-orange-100 text-orange-600',
    medium: 'bg-yellow-100 text-yellow-600',
    low: 'bg-blue-100 text-blue-600'
  }
  return classes[severity] || 'bg-gray-100 text-gray-600'
}

const runScan = async () => {
  scanning.value = true
  loading.value = true
  try {
    // Simulate scan
    await new Promise(resolve => setTimeout(resolve, 3000))
    // Add new vulnerabilities
    const newVuln: Vulnerability = {
      id: Date.now().toString(),
      title: 'New vulnerability detected',
      description: 'Simulated vulnerability from scan',
      severity: 'medium',
      status: 'open',
      repository: 'backend-api',
      file: 'app/Models/User.php',
      cweId: 'CWE-20',
      detectedAt: 'Just now'
    }
    vulnerabilities.value.push(newVuln)
  } catch (error) {
    console.error('Scan failed:', error)
  } finally {
    scanning.value = false
    loading.value = false
  }
}

const generateFix = (id: string) => {
  const vulnerability = vulnerabilities.value.find(v => v.id === id)
  if (vulnerability) {
    vulnerability.status = 'fixing'
    // Simulate AI fix generation
    setTimeout(() => {
      vulnerability.status = 'fixed'
    }, 5000)
  }
}

const viewDetails = (id: string) => {
  console.log('View vulnerability details:', id)
  // Navigate to vulnerability details
}

onMounted(() => {
  loadVulnerabilities()
})
</script>
