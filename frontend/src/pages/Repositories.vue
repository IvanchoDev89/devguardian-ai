<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <div class="px-4 py-6 sm:px-0">
      <!-- Header Section -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Repositories</h1>
            <p class="text-gray-600 mt-2">Manage and monitor your code repositories</p>
          </div>
          <button 
            @click="showAddRepositoryModal = true"
            class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
          >
            <svg class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Add Repository
          </button>
        </div>
      </div>

      <!-- Stats Overview -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Total Repositories</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.total }}</p>
            </div>
            <div class="bg-blue-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Active Scans</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.scanning }}</p>
            </div>
            <div class="bg-yellow-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Vulnerabilities Found</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.vulnerabilities }}</p>
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
              <p class="text-sm font-medium text-gray-600">Last Scan</p>
              <p class="text-sm font-medium text-gray-900 mt-1">{{ stats.lastScan }}</p>
            </div>
            <div class="bg-green-100 rounded-lg p-3">
              <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
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
                placeholder="Search repositories..."
                class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
          <div class="flex gap-2">
            <select v-model="filterStatus" class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="">All Status</option>
              <option value="healthy">Healthy</option>
              <option value="scanning">Scanning</option>
              <option value="error">Error</option>
            </select>
            <select v-model="sortBy" class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
              <option value="name">Name</option>
              <option value="lastScan">Last Scan</option>
              <option value="vulnerabilities">Vulnerabilities</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Repository List -->
      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="text-center">
          <svg class="animate-spin h-8 w-8 text-blue-600 mx-auto" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p class="mt-2 text-sm text-gray-600">Loading repositories...</p>
        </div>
      </div>

      <div v-else-if="filteredRepositories.length === 0" class="text-center py-12">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
          </svg>
          <h3 class="mt-4 text-lg font-medium text-gray-900">No repositories found</h3>
          <p class="mt-2 text-sm text-gray-500">
            {{ searchQuery ? 'Try adjusting your search terms' : 'Get started by connecting your first repository' }}
          </p>
          <button 
            v-if="!searchQuery"
            @click="showAddRepositoryModal = true"
            class="mt-4 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Add Your First Repository
          </button>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="repo in filteredRepositories" 
          :key="repo.id"
          class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center">
              <div class="bg-gray-100 rounded-lg p-2 mr-3">
                <svg class="h-5 w-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-medium text-gray-900">{{ repo.name }}</h3>
                <p class="text-sm text-gray-500">{{ repo.description }}</p>
              </div>
            </div>
            <div class="flex items-center">
              <span 
                :class="getStatusClass(repo.status)"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              >
                {{ repo.status }}
              </span>
            </div>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between text-sm">
              <span class="text-gray-600">Vulnerabilities</span>
              <span class="font-medium" :class="getVulnerabilityClass(repo.vulnerabilities)">
                {{ repo.vulnerabilities }}
              </span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-gray-600">Last Scan</span>
              <span class="font-medium text-gray-900">{{ repo.lastScan }}</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-gray-600">Language</span>
              <span class="font-medium text-gray-900">{{ repo.language }}</span>
            </div>
          </div>

          <div class="mt-4 pt-4 border-t border-gray-200">
            <div class="flex items-center justify-between">
              <button 
                @click="scanRepository(repo.id)"
                :disabled="repo.status === 'scanning'"
                class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg v-if="repo.status === 'scanning'" class="animate-spin -ml-1 mr-2 h-3 w-3 text-gray-700" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <svg v-else class="-ml-1 mr-2 h-3 w-3 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
                {{ repo.status === 'scanning' ? 'Scanning...' : 'Scan' }}
              </button>
              <div class="flex items-center space-x-2">
                <button 
                  @click="viewRepository(repo.id)"
                  class="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  View
                </button>
                <button 
                  @click="deleteRepository(repo.id)"
                  class="text-red-600 hover:text-red-800 text-sm font-medium"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Repository Modal -->
    <div v-if="showAddRepositoryModal" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                  Add New Repository
                </h3>
                <div class="space-y-4">
                  <div>
                    <label for="repo-url" class="block text-sm font-medium text-gray-700">Repository URL</label>
                    <input
                      id="repo-url"
                      v-model="newRepo.url"
                      type="url"
                      placeholder="https://github.com/user/repo"
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    />
                  </div>
                  <div>
                    <label for="repo-branch" class="block text-sm font-medium text-gray-700">Branch</label>
                    <input
                      id="repo-branch"
                      v-model="newRepo.branch"
                      type="text"
                      placeholder="main"
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              @click="addRepository"
              type="button"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Add Repository
            </button>
            <button
              @click="showAddRepositoryModal = false"
              type="button"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Repository {
  id: string
  name: string
  description: string
  url: string
  branch: string
  status: 'healthy' | 'scanning' | 'error'
  vulnerabilities: number
  lastScan: string
  language: string
}

interface Stats {
  total: number
  scanning: number
  vulnerabilities: number
  lastScan: string
}

const loading = ref(false)
const searchQuery = ref('')
const filterStatus = ref('')
const sortBy = ref('name')
const showAddRepositoryModal = ref(false)

const newRepo = ref({
  url: '',
  branch: 'main'
})

const stats = ref<Stats>({
  total: 0,
  scanning: 0,
  vulnerabilities: 0,
  lastScan: 'Never'
})

const repositories = ref<Repository[]>([
  {
    id: '1',
    name: 'frontend-app',
    description: 'React frontend application',
    url: 'https://github.com/example/frontend-app',
    branch: 'main',
    status: 'healthy',
    vulnerabilities: 3,
    lastScan: '2 hours ago',
    language: 'JavaScript'
  },
  {
    id: '2',
    name: 'backend-api',
    description: 'Laravel REST API',
    url: 'https://github.com/example/backend-api',
    branch: 'main',
    status: 'scanning',
    vulnerabilities: 0,
    lastScan: 'Scanning...',
    language: 'PHP'
  },
  {
    id: '3',
    name: 'mobile-app',
    description: 'React Native mobile application',
    url: 'https://github.com/example/mobile-app',
    branch: 'main',
    status: 'error',
    vulnerabilities: 7,
    lastScan: '1 day ago',
    language: 'TypeScript'
  }
])

const filteredRepositories = computed(() => {
  let filtered = repositories.value

  // Filter by search query
  if (searchQuery.value) {
    filtered = filtered.filter(repo => 
      repo.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      repo.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  // Filter by status
  if (filterStatus.value) {
    filtered = filtered.filter(repo => repo.status === filterStatus.value)
  }

  // Sort
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        return a.name.localeCompare(b.name)
      case 'lastScan':
        return a.lastScan.localeCompare(b.lastScan)
      case 'vulnerabilities':
        return b.vulnerabilities - a.vulnerabilities
      default:
        return 0
    }
  })

  return filtered
})

const getStatusClass = (status: string): string => {
  const classes: Record<string, string> = {
    healthy: 'bg-green-100 text-green-800',
    scanning: 'bg-yellow-100 text-yellow-800',
    error: 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getVulnerabilityClass = (count: number): string => {
  if (count === 0) return 'text-green-600'
  if (count <= 3) return 'text-yellow-600'
  return 'text-red-600'
}

const scanRepository = async (id: string) => {
  const repo = repositories.value.find(r => r.id === id)
  if (repo) {
    repo.status = 'scanning'
    // Simulate scan
    setTimeout(() => {
      repo.status = 'healthy'
      repo.vulnerabilities = Math.floor(Math.random() * 10)
      repo.lastScan = 'Just now'
    }, 3000)
  }
}

const viewRepository = (id: string) => {
  console.log('View repository:', id)
  // Navigate to repository details
}

const deleteRepository = (id: string) => {
  if (confirm('Are you sure you want to delete this repository?')) {
    repositories.value = repositories.value.filter(r => r.id !== id)
  }
}

const addRepository = () => {
  if (newRepo.value.url) {
    const repo: Repository = {
      id: Date.now().toString(),
      name: newRepo.value.url.split('/').pop() || 'New Repository',
      description: 'New repository',
      url: newRepo.value.url,
      branch: newRepo.value.branch,
      status: 'healthy',
      vulnerabilities: 0,
      lastScan: 'Never',
      language: 'Unknown'
    }
    repositories.value.push(repo)
    showAddRepositoryModal.value = false
    newRepo.value = { url: '', branch: 'main' }
  }
}

onMounted(() => {
  // Update stats
  stats.value.total = repositories.value.length
  stats.value.scanning = repositories.value.filter(r => r.status === 'scanning').length
  stats.value.vulnerabilities = repositories.value.reduce((sum, r) => sum + r.vulnerabilities, 0)
})
</script>
