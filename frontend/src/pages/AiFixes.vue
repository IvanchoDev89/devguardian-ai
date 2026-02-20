<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">AI Fixes</h1>
      <p class="text-gray-600">Review AI-generated security fixes</p>
    </div>
    
    <!-- Filters and Search -->
    <div class="mb-6 bg-white p-4 rounded-lg shadow-sm border">
      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search fixes..."
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div class="flex gap-2">
          <select
            v-model="statusFilter"
            class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
            <option value="applied">Applied</option>
          </select>
          <select
            v-model="severityFilter"
            class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Severity</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
      </div>
    </div>
    
    <!-- Stats Overview -->
    <div class="mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white p-4 rounded-lg shadow-sm border">
        <div class="text-2xl font-bold text-blue-600">{{ stats.total }}</div>
        <div class="text-sm text-gray-600">Total Fixes</div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm border">
        <div class="text-2xl font-bold text-green-600">{{ stats.applied }}</div>
        <div class="text-sm text-gray-600">Applied</div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm border">
        <div class="text-2xl font-bold text-yellow-600">{{ stats.pending }}</div>
        <div class="text-sm text-gray-600">Pending</div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm border">
        <div class="text-2xl font-bold text-red-600">{{ stats.critical }}</div>
        <div class="text-sm text-gray-600">Critical</div>
      </div>
    </div>
    
    <div class="card">
      <!-- Loading state -->
      <div v-if="loading" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="mt-2 text-gray-600">Loading AI fixes...</p>
      </div>
      
      <!-- Error state -->
      <div v-else-if="error" class="text-center py-8">
        <div class="text-red-600 mb-4">
          <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <p class="text-red-600">{{ error }}</p>
        <button @click="loadAiFixes" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          Retry
        </button>
      </div>
      
      <!-- Empty state -->
      <div v-else-if="filteredFixes.length === 0" class="border-4 border-dashed border-gray-200 rounded-lg h-64 flex items-center justify-center">
        <div class="text-center">
          <svg class="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <p class="text-gray-500 mt-2">
            {{ searchQuery || statusFilter || severityFilter ? 'No fixes found matching your criteria' : 'No AI fixes generated yet' }}
          </p>
          <p class="text-sm text-gray-400 mt-2">
            {{ searchQuery || statusFilter || severityFilter ? 'Try adjusting your filters' : 'AI fixes will appear here when vulnerabilities are detected' }}
          </p>
        </div>
      </div>
      
      <!-- AI fixes list -->
      <div v-else class="space-y-4">
        <div v-for="fix in paginatedFixes" :key="fix.id" class="border rounded-lg p-4 hover:shadow-md transition-shadow">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-2">
                <h3 class="font-semibold text-gray-900">{{ fix.title }}</h3>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getSeverityClass(fix.severity)">
                  {{ fix.severity }}
                </span>
              </div>
              <p class="text-sm text-gray-600 mb-3">{{ fix.description }}</p>
              <div class="flex items-center space-x-4 text-xs text-gray-500">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getStatusClass(fix.status)">
                  {{ fix.status }}
                </span>
                <span>{{ formatDate(fix.created_at) }}</span>
                <span>Confidence: {{ Math.round(fix.confidence * 100) }}%</span>
                <span v-if="fix.cwe_id">CWE-{{ fix.cwe_id }}</span>
              </div>
            </div>
            <div class="flex gap-2 ml-4">
              <button
                @click="viewFixDetails(fix)"
                class="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                View Details
              </button>
              <button
                v-if="fix.status === 'pending'"
                @click="approveFix(fix.id)"
                class="px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700"
              >
                Approve
              </button>
              <button
                v-if="fix.status === 'approved'"
                @click="applyFix(fix.id)"
                class="px-3 py-1 text-sm bg-purple-600 text-white rounded hover:bg-purple-700"
              >
                Apply
              </button>
              <button
                v-if="fix.status === 'pending'"
                @click="rejectFix(fix.id)"
                class="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700"
              >
                Reject
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Pagination -->
      <div v-if="filteredFixes.length > itemsPerPage" class="mt-6 flex justify-center">
        <nav class="flex items-center space-x-2">
          <button
            @click="currentPage > 1 && currentPage--"
            :disabled="currentPage === 1"
            class="px-3 py-1 border rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <span class="px-3 py-1">
            Page {{ currentPage }} of {{ totalPages }}
          </span>
          <button
            @click="currentPage < totalPages && currentPage++"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 border rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </nav>
      </div>
    </div>
    
    <!-- Fix Details Modal -->
    <div v-if="selectedFix" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg max-w-4xl max-h-[90vh] overflow-y-auto m-4">
        <div class="p-6">
          <div class="flex justify-between items-start mb-4">
            <h2 class="text-xl font-bold">{{ selectedFix.title }}</h2>
            <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          
          <div class="space-y-4">
            <div>
              <h3 class="font-semibold mb-2">Description</h3>
              <p class="text-gray-600">{{ selectedFix.description }}</p>
            </div>
            
            <div>
              <h3 class="font-semibold mb-2">Vulnerability Details</h3>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="font-medium">Type:</span> {{ selectedFix.vulnerability_type }}
                </div>
                <div>
                  <span class="font-medium">Severity:</span> 
                  <span class="ml-1 px-2 py-1 rounded text-xs" :class="getSeverityClass(selectedFix.severity)">
                    {{ selectedFix.severity }}
                  </span>
                </div>
                <div>
                  <span class="font-medium">Confidence:</span> {{ Math.round(selectedFix.confidence * 100) }}%
                </div>
                <div v-if="selectedFix.cwe_id">
                  <span class="font-medium">CWE ID:</span> {{ selectedFix.cwe_id }}
                </div>
                <div v-if="selectedFix.cvss_score">
                  <span class="font-medium">CVSS Score:</span> {{ selectedFix.cvss_score }}
                </div>
                <div>
                  <span class="font-medium">Status:</span> 
                  <span class="ml-1 px-2 py-1 rounded text-xs" :class="getStatusClass(selectedFix.status)">
                    {{ selectedFix.status }}
                  </span>
                </div>
              </div>
            </div>
            
            <div v-if="selectedFix.original_code">
              <h3 class="font-semibold mb-2">Original Code</h3>
              <pre class="bg-gray-100 p-3 rounded text-sm overflow-x-auto"><code>{{ selectedFix.original_code }}</code></pre>
            </div>
            
            <div v-if="selectedFix.fixed_code">
              <h3 class="font-semibold mb-2">Fixed Code</h3>
              <pre class="bg-green-50 p-3 rounded text-sm overflow-x-auto"><code>{{ selectedFix.fixed_code }}</code></pre>
            </div>
            
            <div v-if="selectedFix.explanation">
              <h3 class="font-semibold mb-2">Explanation</h3>
              <p class="text-gray-600">{{ selectedFix.explanation }}</p>
            </div>
            
            <div v-if="selectedFix.recommendations && selectedFix.recommendations.length > 0">
              <h3 class="font-semibold mb-2">Recommendations</h3>
              <ul class="list-disc list-inside text-gray-600">
                <li v-for="recommendation in selectedFix.recommendations" :key="recommendation">
                  {{ recommendation }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { aiFixApi } from '@/services/api'

interface AiFix {
  id: string
  title: string
  description: string
  status: 'pending' | 'approved' | 'rejected' | 'applied'
  severity: 'critical' | 'high' | 'medium' | 'low'
  confidence: number
  created_at: string
  vulnerability_type: string
  cwe_id?: string
  cvss_score?: number
  original_code?: string
  fixed_code?: string
  explanation?: string
  recommendations?: string[]
}

const loading = ref(false)
const error = ref('')
const aiFixes = ref<AiFix[]>([])
const searchQuery = ref('')
const statusFilter = ref('')
const severityFilter = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(10)
const selectedFix = ref<AiFix | null>(null)

// Computed properties
const filteredFixes = computed(() => {
  let filtered = aiFixes.value

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(fix => 
      fix.title.toLowerCase().includes(query) ||
      fix.description.toLowerCase().includes(query) ||
      fix.vulnerability_type.toLowerCase().includes(query)
    )
  }

  // Apply status filter
  if (statusFilter.value) {
    filtered = filtered.filter(fix => fix.status === statusFilter.value)
  }

  // Apply severity filter
  if (severityFilter.value) {
    filtered = filtered.filter(fix => fix.severity === severityFilter.value)
  }

  return filtered
})

const paginatedFixes = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredFixes.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredFixes.value.length / itemsPerPage.value)
})

const stats = computed(() => {
  const total = aiFixes.value.length
  const applied = aiFixes.value.filter(fix => fix.status === 'applied').length
  const pending = aiFixes.value.filter(fix => fix.status === 'pending').length
  const critical = aiFixes.value.filter(fix => fix.severity === 'critical').length

  return { total, applied, pending, critical }
})

// Methods
const loadAiFixes = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await aiFixApi.getAiFixes()
    aiFixes.value = response.data || []
  } catch (err: any) {
    error.value = 'Failed to load AI fixes: ' + (err.response?.data?.message || err.message)
    console.error('Error loading AI fixes:', err)
  } finally {
    loading.value = false
  }
}

const viewFixDetails = (fix: AiFix) => {
  selectedFix.value = fix
}

const closeModal = () => {
  selectedFix.value = null
}

const approveFix = async (fixId: string) => {
  try {
    await aiFixApi.approveFix(fixId, true)
    // Update fix in local array
    const fix = aiFixes.value.find(f => f.id === fixId)
    if (fix) {
      fix.status = 'approved'
    }
  } catch (err: any) {
    error.value = 'Failed to approve fix: ' + (err.response?.data?.message || err.message)
  }
}

const applyFix = async (fixId: string) => {
  try {
    await aiFixApi.applyFix(fixId)
    // Update fix in local array
    const fix = aiFixes.value.find(f => f.id === fixId)
    if (fix) {
      fix.status = 'applied'
    }
  } catch (err: any) {
    error.value = 'Failed to apply fix: ' + (err.response?.data?.message || err.message)
  }
}

const rejectFix = async (fixId: string) => {
  try {
    await aiFixApi.rejectFix(fixId, false)
    // Update fix in local array
    const fix = aiFixes.value.find(f => f.id === fixId)
    if (fix) {
      fix.status = 'rejected'
    }
  } catch (err: any) {
    error.value = 'Failed to reject fix: ' + (err.response?.data?.message || err.message)
  }
}

const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    approved: 'bg-blue-100 text-blue-800',
    rejected: 'bg-red-100 text-red-800',
    applied: 'bg-green-100 text-green-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getSeverityClass = (severity: string) => {
  const classes: Record<string, string> = {
    critical: 'bg-red-100 text-red-800',
    high: 'bg-orange-100 text-orange-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800'
  }
  return classes[severity] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Lifecycle
onMounted(() => {
  loadAiFixes()
})
</script>
