<template>
  <div class="min-h-screen pt-16 bg-slate-900">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-white mb-8">Billing & API Keys</h1>

      <!-- Current Plan -->
      <div class="bg-slate-800/50 border border-slate-700 rounded-xl p-6 mb-8">
        <h2 class="text-xl font-semibold text-white mb-4">Current Plan</h2>
        <div class="flex items-center justify-between">
          <div>
            <p class="text-2xl font-bold text-cyan-400 capitalize">{{ currentPlan }}</p>
            <p class="text-gray-400">{{ scansUsed }} / {{ scansLimit }} scans this month</p>
          </div>
          <button 
            @click="router.push('/pricing')"
            class="bg-cyan-600 hover:bg-cyan-700 text-white px-6 py-2 rounded-lg"
          >
            Change Plan
          </button>
        </div>
        
        <!-- Usage Bar -->
        <div class="mt-4">
          <div class="bg-slate-700 rounded-full h-3">
            <div 
              class="bg-gradient-to-r from-cyan-500 to-blue-500 h-3 rounded-full transition-all"
              :style="{ width: Math.min(usagePercent, 100) + '%' }"
            ></div>
          </div>
          <p class="text-sm text-gray-400 mt-2">{{ usagePercent.toFixed(1) }}% used • {{ scansLimit - scansUsed }} scans remaining</p>
        </div>
      </div>

      <!-- API Keys -->
      <div class="bg-slate-800/50 border border-slate-700 rounded-xl p-6 mb-8">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold text-white">API Keys</h2>
          <button 
            @click="showCreateModal = true"
            class="bg-cyan-600 hover:bg-cyan-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Create Key
          </button>
        </div>

        <!-- API Keys List -->
        <div v-if="apiKeys.length > 0" class="space-y-4">
          <div 
            v-for="key in apiKeys" 
            :key="key.id"
            class="bg-slate-700/50 rounded-lg p-4 border border-slate-600"
          >
            <div class="flex items-center justify-between">
              <div>
                <p class="font-semibold text-white">{{ key.name }}</p>
                <p class="text-sm text-gray-400">
                  {{ key.plan }} plan • Created {{ formatDate(key.created_at) }}
                </p>
              </div>
              <div class="flex items-center gap-2">
                <span 
                  :class="[
                    'px-3 py-1 rounded-full text-sm',
                    key.is_active ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                  ]"
                >
                  {{ key.is_active ? 'Active' : 'Inactive' }}
                </span>
                <button 
                  @click="copyKey(key)"
                  class="text-gray-400 hover:text-white p-2"
                  title="Copy Key"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                  </svg>
                </button>
                <button 
                  @click="rotateKey(key)"
                  class="text-gray-400 hover:text-white p-2"
                  title="Rotate Key"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                  </svg>
                </button>
                <button 
                  @click="deleteKey(key)"
                  class="text-gray-400 hover:text-red-400 p-2"
                  title="Delete Key"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="mt-3 flex items-center gap-4 text-sm text-gray-400">
              <span>{{ key.scans_used_this_month }} / {{ key.monthly_scans_limit }} scans used</span>
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-8 text-gray-400">
          <p>No API keys yet. Create one to get started.</p>
        </div>
      </div>

      <!-- Usage History -->
      <div class="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
        <h2 class="text-xl font-semibold text-white mb-4">Usage History</h2>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="text-left text-gray-400 border-b border-slate-700">
                <th class="pb-3">Date</th>
                <th class="pb-3">Scans</th>
                <th class="pb-3">API Key</th>
                <th class="pb-3">Status</th>
              </tr>
            </thead>
            <tbody class="text-gray-300">
              <tr class="border-b border-slate-700/50">
                <td class="py-3">Feb 20, 2026</td>
                <td class="py-3">47</td>
                <td class="py-3">My First Key</td>
                <td class="py-3"><span class="text-green-400">Completed</span></td>
              </tr>
              <tr class="border-b border-slate-700/50">
                <td class="py-3">Feb 19, 2026</td>
                <td class="py-3">23</td>
                <td class="py-3">My First Key</td>
                <td class="py-3"><span class="text-green-400">Completed</span></td>
              </tr>
              <tr>
                <td class="py-3">Feb 18, 2026</td>
                <td class="py-3">30</td>
                <td class="py-3">My First Key</td>
                <td class="py-3"><span class="text-green-400">Completed</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Create Key Modal -->
      <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div class="bg-slate-800 rounded-xl p-6 w-full max-w-md border border-slate-700">
          <h3 class="text-xl font-bold text-white mb-4">Create API Key</h3>
          
          <div class="space-y-4">
            <div>
              <label class="block text-gray-400 text-sm mb-2">Key Name</label>
              <input 
                v-model="newKey.name"
                type="text" 
                placeholder="My API Key"
                class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white"
              />
            </div>
            
            <div>
              <label class="block text-gray-400 text-sm mb-2">Plan</label>
              <select 
                v-model="newKey.plan"
                class="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white"
              >
                <option value="free">Free (100 scans/mo)</option>
                <option value="pro">Pro (1,000 scans/mo - $29/mo)</option>
                <option value="enterprise">Enterprise (10,000 scans/mo - $199/mo)</option>
              </select>
            </div>
          </div>

          <div class="flex gap-3 mt-6">
            <button 
              @click="showCreateModal = false"
              class="flex-1 bg-slate-700 hover:bg-slate-600 text-white py-2 rounded-lg"
            >
              Cancel
            </button>
            <button 
              @click="createKey"
              :disabled="!newKey.name"
              class="flex-1 bg-cyan-600 hover:bg-cyan-700 text-white py-2 rounded-lg disabled:opacity-50"
            >
              Create
            </button>
          </div>
        </div>
      </div>

      <!-- Success Modal -->
      <div v-if="showSuccessModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div class="bg-slate-800 rounded-xl p-6 w-full max-w-md border border-slate-700">
          <h3 class="text-xl font-bold text-white mb-4">API Key Created</h3>
          <p class="text-gray-400 mb-4">
            Copy this key now. You won't be able to see it again!
          </p>
          <div class="bg-slate-900 p-3 rounded-lg font-mono text-sm text-green-400 break-all">
            {{ createdKey }}
          </div>
          <button 
            @click="showSuccessModal = false"
            class="w-full mt-4 bg-cyan-600 hover:bg-cyan-700 text-white py-2 rounded-lg"
          >
            I've Saved My Key
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiService } from '../services/api'

const router = useRouter()

interface ApiKey {
  id: number
  key_id: string
  name: string
  plan: string
  monthly_scans_limit: number
  scans_used_this_month: number
  is_active: boolean
  created_at: string
}

const apiKeys = ref<ApiKey[]>([])
const currentPlan = ref('free')
const scansUsed = ref(0)
const scansLimit = ref(100)
const showCreateModal = ref(false)
const showSuccessModal = ref(false)
const createdKey = ref('')

const newKey = ref({
  name: '',
  plan: 'free'
})

const usagePercent = computed(() => {
  if (scansLimit.value === 0) return 0
  return (scansUsed.value / scansLimit.value) * 100
})

const loadApiKeys = async () => {
  try {
    const response = await apiService.get('/api-keys')
    if (response.success && response.data) {
      apiKeys.value = response.data
    }
  } catch (error) {
    console.error('Failed to load API keys:', error)
  }
}

const createKey = async () => {
  try {
    const response = await apiService.post('/api-keys', {
      name: newKey.value.name,
      plan: newKey.value.plan
    })
    
    if (response.success && response.data) {
      createdKey.value = response.data.key
      showCreateModal.value = false
      showSuccessModal.value = true
      loadApiKeys()
    }
  } catch (error) {
    console.error('Failed to create API key:', error)
  }
}

const copyKey = async (key: ApiKey) => {
  const fullKey = key.key_id + '.dg_xxxxx'
  await navigator.clipboard.writeText(fullKey)
  alert('API key copied to clipboard!')
}

const rotateKey = async (key: ApiKey) => {
  if (!confirm('Are you sure you want to rotate this key? The old key will stop working.')) return
  
  try {
    const response = await apiService.post(`/api-keys/${key.key_id}/rotate`)
    if (response.success && response.data) {
      createdKey.value = response.data.key
      showSuccessModal.value = true
    }
  } catch (error) {
    console.error('Failed to rotate key:', error)
  }
}

const deleteKey = async (key: ApiKey) => {
  if (!confirm('Are you sure you want to delete this key?')) return
  
  try {
    await apiService.delete(`/api-keys/${key.key_id}`)
    loadApiKeys()
  } catch (error) {
    console.error('Failed to delete key:', error)
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
}

onMounted(() => {
  loadApiKeys()
})
</script>
