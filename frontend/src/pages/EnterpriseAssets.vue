<template>
  <div class="min-h-screen bg-slate-900">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-white">Enterprise Asset Management</h1>
        <p class="text-gray-400 mt-1">Register and manage your authorized scanning targets</p>
      </div>

      <!-- Add Asset Button -->
      <div class="mb-6 flex justify-end">
        <button 
          @click="showAddModal = true"
          class="px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg font-medium hover:from-blue-500 hover:to-cyan-500 transition-all"
        >
          + Register New Asset
        </button>
      </div>

      <!-- Assets Grid -->
      <div v-if="loading" class="text-center py-12 text-gray-400">
        Loading assets...
      </div>
      
      <div v-else-if="assets.length === 0" class="text-center py-12">
        <svg class="w-16 h-16 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/>
        </svg>
        <p class="text-gray-400 mb-4">No assets registered yet</p>
        <p class="text-sm text-gray-500">Register your web applications and APIs to enable authorized pentesting</p>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="asset in assets" 
          :key="asset.id"
          class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center">
              <div :class="`w-10 h-10 rounded-lg flex items-center justify-center mr-3 ${
                asset.type === 'web_application' ? 'bg-blue-500/20' :
                asset.type === 'api' ? 'bg-purple-500/20' : 'bg-green-500/20'
              }`">
                <svg v-if="asset.type === 'web_application'" class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/>
                </svg>
                <svg v-else-if="asset.type === 'api'" class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                <svg v-else class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2"/>
                </svg>
              </div>
              <div>
                <h3 class="text-white font-medium">{{ asset.name }}</h3>
                <p class="text-xs text-gray-400">{{ formatType(asset.type) }}</p>
              </div>
            </div>
            <span :class="`px-2 py-1 text-xs rounded-full ${
              asset.verification_status === 'verified' ? 'bg-green-500/20 text-green-400' :
              asset.verification_status === 'pending' ? 'bg-yellow-500/20 text-yellow-400' :
              'bg-red-500/20 text-red-400'
            }`">
              {{ asset.verification_status }}
            </span>
          </div>
          
          <p class="text-sm text-gray-400 mb-4 truncate">{{ asset.url }}</p>
          
          <p v-if="asset.description" class="text-xs text-gray-500 mb-4 line-clamp-2">
            {{ asset.description }}
          </p>
          
          <div class="flex items-center justify-between pt-4 border-t border-white/10">
            <button 
              v-if="asset.verification_status !== 'verified'"
              @click="verifyAsset(asset.id)"
              class="text-sm text-blue-400 hover:text-blue-300"
            >
              Verify Now
            </button>
            <span v-else class="text-xs text-green-400">
              ✓ Verified {{ formatDate(asset.verified_at) }}
            </span>
            
            <button 
              @click="deleteAsset(asset.id)"
              class="text-sm text-red-400 hover:text-red-300"
            >
              Remove
            </button>
          </div>
        </div>
      </div>

      <!-- Add Asset Modal -->
      <div v-if="showAddModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showAddModal = false">
        <div class="bg-slate-800 rounded-xl p-6 w-full max-w-md border border-white/10">
          <h2 class="text-xl font-bold text-white mb-4">Register New Asset</h2>
          
          <form @submit.prevent="addAsset" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Asset Name</label>
              <input 
                v-model="newAsset.name"
                type="text"
                required
                class="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="My Web Application"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Asset Type</label>
              <select 
                v-model="newAsset.type"
                required
                class="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="web_application">Web Application</option>
                <option value="api">REST API</option>
                <option value="network">Network Infrastructure</option>
                <option value="container">Container Image</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">URL</label>
              <input 
                v-model="newAsset.url"
                type="url"
                required
                class="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="https://app.example.com"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Description (Optional)</label>
              <textarea 
                v-model="newAsset.description"
                rows="2"
                class="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Brief description of the asset"
              ></textarea>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Ownership Proof</label>
              <input 
                v-model="newAsset.ownership_proof"
                type="text"
                class="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="DNS record, file upload, etc."
              />
            </div>
            
            <div class="flex gap-3 pt-4">
              <button 
                type="button"
                @click="showAddModal = false"
                class="flex-1 px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white hover:bg-white/20"
              >
                Cancel
              </button>
              <button 
                type="submit"
                :disabled="adding"
                class="flex-1 px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg font-medium hover:from-blue-500 hover:to-cyan-500 disabled:opacity-50"
              >
                {{ adding ? 'Registering...' : 'Register Asset' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { assetService } from '../services/api'

interface Asset {
  id: number
  name: string
  type: string
  url: string
  description: string
  verification_status: string
  status: string
  verified_at: string
  created_at: string
}

const assets = ref<Asset[]>([])
const loading = ref(false)
const showAddModal = ref(false)
const adding = ref(false)

const newAsset = ref({
  name: '',
  type: 'web_application',
  url: '',
  description: '',
  ownership_proof: ''
})

onMounted(async () => {
  await loadAssets()
})

const loadAssets = async () => {
  loading.value = true
  try {
    const response = await assetService.getAssets()
    if (response.success && response.data) {
      assets.value = response.data
    }
  } catch (error) {
    console.error('Error loading assets:', error)
  } finally {
    loading.value = false
  }
}

const addAsset = async () => {
  adding.value = true
  try {
    const response = await assetService.createAsset(newAsset.value)
    if (response.success) {
      showAddModal.value = false
      newAsset.value = { name: '', type: 'web_application', url: '', description: '', ownership_proof: '' }
      await loadAssets()
    }
  } catch (error) {
    console.error('Error adding asset:', error)
  } finally {
    adding.value = false
  }
}

const verifyAsset = async (id: number) => {
  try {
    await assetService.verifyAsset(id, 'dns')
    await loadAssets()
  } catch (error) {
    console.error('Error verifying asset:', error)
  }
}

const deleteAsset = async (id: number) => {
  if (!confirm('Are you sure you want to remove this asset?')) return
  
  try {
    await assetService.deleteAsset(id)
    await loadAssets()
  } catch (error) {
    console.error('Error deleting asset:', error)
  }
}

const formatType = (type: string) => {
  const types: Record<string, string> = {
    'web_application': 'Web Application',
    'api': 'REST API',
    'network': 'Network',
    'container': 'Container',
    'enterprise_software': 'Enterprise Software'
  }
  return types[type] || type
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString()
}
</script>
