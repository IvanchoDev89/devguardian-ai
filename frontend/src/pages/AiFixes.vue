<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">AI Fixes</h1>
      <p class="text-gray-600">Review AI-generated security fixes</p>
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
      <div v-else-if="!aiFixes || aiFixes.length === 0" class="border-4 border-dashed border-gray-200 rounded-lg h-64 flex items-center justify-center">
        <div class="text-center">
          <p class="text-gray-500">No AI fixes generated yet</p>
          <p class="text-sm text-gray-400 mt-2">AI fixes will appear here when vulnerabilities are detected</p>
        </div>
      </div>
      
      <!-- AI fixes list -->
      <div v-else class="space-y-4">
        <div v-for="fix in aiFixes" :key="fix.id" class="border rounded-lg p-4">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="font-semibold text-gray-900">{{ fix.title }}</h3>
              <p class="text-sm text-gray-600 mt-1">{{ fix.description }}</p>
              <div class="mt-2 flex items-center space-x-2">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getStatusClass(fix.status)">
                  {{ fix.status }}
                </span>
                <span class="text-xs text-gray-500">{{ formatDate(fix.created_at) }}</span>
              </div>
            </div>
            <div class="flex space-x-2">
              <button @click="viewFixDetails(fix)" 
                      class="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700">
                View Details
              </button>
              <button v-if="fix.status === 'pending'" 
                      @click="applyFix(fix.id)"
                      class="px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700">
                Apply Fix
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { aiFixApi } from '../services/api'

interface AiFix {
  id: string
  title: string
  description: string
  status: 'pending' | 'applied' | 'failed'
  created_at: string
  vulnerability_id: string
}

const aiFixes = ref<AiFix[]>([])
const loading = ref(false)
const error = ref('')

const loadAiFixes = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await aiFixApi.getAiFixes()
    if (response.error) {
      error.value = response.error
    } else {
      aiFixes.value = response.data || []
    }
  } catch (err) {
    error.value = 'Failed to load AI fixes'
  } finally {
    loading.value = false
  }
}

const applyFix = async (fixId: string) => {
  try {
    const response = await aiFixApi.applyAiFix(fixId)
    if (response.error) {
      error.value = response.error
    } else {
      // Refresh the list
      await loadAiFixes()
    }
  } catch (err) {
    error.value = 'Failed to apply fix'
  }
}

const viewFixDetails = (fix: AiFix) => {
  // TODO: Implement fix details modal or navigation
  console.log('View fix details:', fix)
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800'
    case 'applied':
      return 'bg-green-100 text-green-800'
    case 'failed':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  loadAiFixes()
})
</script>
