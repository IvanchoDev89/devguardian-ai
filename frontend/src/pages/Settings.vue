<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
    <div class="max-w-7xl mx-auto px-4 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-white">Settings</h1>
        <p class="text-gray-400 mt-2">Manage your account and integrations</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Sidebar Navigation -->
        <div class="lg:col-span-1">
          <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-4">
            <nav class="space-y-1">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                @click="activeTab = tab.id"
                class="w-full flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200"
                :class="activeTab === tab.id 
                  ? 'bg-gradient-to-r from-blue-600/20 to-cyan-600/20 text-white border-l-2 border-cyan-400' 
                  : 'text-gray-400 hover:text-white hover:bg-white/5'"
              >
                <component :is="tab.icon" class="w-5 h-5 mr-3" />
                {{ tab.name }}
              </button>
            </nav>
          </div>
        </div>

        <!-- Content -->
        <div class="lg:col-span-3 space-y-6">
          <!-- Profile Tab -->
          <div v-if="activeTab === 'profile'" class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6">
            <h2 class="text-xl font-semibold text-white mb-6">Profile Settings</h2>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Name</label>
                <input
                  v-model="profile.name"
                  type="text"
                  class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Email</label>
                <input
                  v-model="profile.email"
                  type="email"
                  class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Plan</label>
                <div class="flex items-center gap-3 px-4 py-3 bg-white/5 border border-white/10 rounded-lg">
                  <span class="px-3 py-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-sm font-medium rounded-full capitalize">
                    {{ authStore.plan }}
                  </span>
                  <span class="text-gray-400 text-sm">{{ authStore.scansUsed }} / {{ authStore.scansQuota }} scans used</span>
                </div>
              </div>
              
              <button
                @click="saveProfile"
                class="mt-4 px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all"
              >
                Save Changes
              </button>
            </div>
          </div>

          <!-- API Keys Tab -->
          <div v-if="activeTab === 'apikeys'" class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6">
            <div class="flex items-center justify-between mb-6">
              <div>
                <h2 class="text-xl font-semibold text-white">API Keys</h2>
                <p class="text-gray-400 text-sm mt-1">Manage your API keys for programmatic access</p>
              </div>
              <button
                @click="showCreateKeyModal = true"
                class="px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white text-sm font-medium rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all"
              >
                + Create Key
              </button>
            </div>

            <!-- Usage Stats -->
            <div class="grid grid-cols-3 gap-4 mb-6">
              <div class="bg-white/5 rounded-lg p-4 border border-white/10">
                <p class="text-gray-400 text-sm">Plan</p>
                <p class="text-2xl font-bold text-white capitalize">{{ usageStats?.plan || 'free' }}</p>
              </div>
              <div class="bg-white/5 rounded-lg p-4 border border-white/10">
                <p class="text-gray-400 text-sm">Scans Used</p>
                <p class="text-2xl font-bold text-white">{{ usageStats?.scans_used || 0 }}</p>
              </div>
              <div class="bg-white/5 rounded-lg p-4 border border-white/10">
                <p class="text-gray-400 text-sm">Remaining</p>
                <p class="text-2xl font-bold text-green-400">{{ usageStats?.remaining || 0 }}</p>
              </div>
            </div>

            <!-- Keys List -->
            <div class="space-y-3">
              <div
                v-for="key in apiKeys"
                :key="key.key_id"
                class="bg-white/5 rounded-lg p-4 border border-white/10 flex items-center justify-between"
              >
                <div>
                  <p class="text-white font-medium">{{ key.name }}</p>
                  <p class="text-gray-400 text-sm font-mono">{{ key.key_prefix || '****' }}... </p>
                  <p class="text-gray-500 text-xs mt-1">Created: {{ formatDate(key.created_at) }}</p>
                </div>
                <div class="flex items-center gap-2">
                  <span 
                    class="px-2 py-1 rounded text-xs font-medium"
                    :class="key.is_active ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'"
                  >
                    {{ key.is_active ? 'Active' : 'Inactive' }}
                  </span>
                  <button
                    @click="deleteApiKey(key.key_id)"
                    class="p-2 text-gray-400 hover:text-red-400 transition-colors"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </div>

              <div v-if="apiKeys.length === 0" class="text-center py-8 text-gray-400">
                <svg class="w-12 h-12 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                </svg>
                <p>No API keys yet</p>
                <p class="text-sm">Create an API key to start integrating</p>
              </div>
            </div>
          </div>

          <!-- Webhooks Tab -->
          <div v-if="activeTab === 'webhooks'" class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6">
            <div class="flex items-center justify-between mb-6">
              <div>
                <h2 class="text-xl font-semibold text-white">Webhooks</h2>
                <p class="text-gray-400 text-sm mt-1">Receive notifications when scans complete</p>
              </div>
              <button
                @click="showCreateWebhookModal = true"
                class="px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white text-sm font-medium rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all"
              >
                + Add Webhook
              </button>
            </div>

            <div class="space-y-3">
              <div
                v-for="webhook in webhooks"
                :key="webhook.webhook_id"
                class="bg-white/5 rounded-lg p-4 border border-white/10 flex items-center justify-between"
              >
                <div>
                  <p class="text-white font-medium">{{ webhook.name }}</p>
                  <p class="text-gray-400 text-sm font-mono">{{ webhook.url }}</p>
                  <p class="text-gray-500 text-xs mt-1">Events: {{ webhook.events?.join(', ') }}</p>
                </div>
                <div class="flex items-center gap-2">
                  <button
                    @click="testWebhook(webhook.webhook_id)"
                    class="px-3 py-1 text-sm text-gray-400 hover:text-white border border-white/10 rounded hover:bg-white/5 transition-colors"
                  >
                    Test
                  </button>
                  <button
                    @click="deleteWebhook(webhook.webhook_id)"
                    class="p-2 text-gray-400 hover:text-red-400 transition-colors"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </div>

              <div v-if="webhooks.length === 0" class="text-center py-8 text-gray-400">
                <p>No webhooks configured</p>
              </div>
            </div>
          </div>

          <!-- Teams Tab -->
          <div v-if="activeTab === 'teams'" class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6">
            <div class="flex items-center justify-between mb-6">
              <div>
                <h2 class="text-xl font-semibold text-white">Teams</h2>
                <p class="text-gray-400 text-sm mt-1">Manage your organization and team members</p>
              </div>
              <button
                @click="createTeam"
                class="px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white text-sm font-medium rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all"
              >
                + Create Team
              </button>
            </div>

            <div class="space-y-3">
              <div
                v-for="team in teams"
                :key="team.team_id"
                class="bg-white/5 rounded-lg p-4 border border-white/10"
              >
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-white font-medium">{{ team.name }}</p>
                    <p class="text-gray-400 text-sm">{{ team.member_count || 1 }} members</p>
                  </div>
                  <span class="px-3 py-1 bg-purple-500/20 text-purple-400 text-sm rounded-full capitalize">
                    {{ team.plan }}
                  </span>
                </div>
              </div>

              <div v-if="teams.length === 0" class="text-center py-8 text-gray-400">
                <p>No teams yet</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create API Key Modal -->
    <div v-if="showCreateKeyModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-slate-800 rounded-xl border border-white/10 p-6 w-full max-w-md">
        <h3 class="text-xl font-semibold text-white mb-4">Create API Key</h3>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Key Name</label>
            <input
              v-model="newKey.name"
              type="text"
              placeholder="My API Key"
              class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Plan</label>
            <select
              v-model="newKey.plan"
              class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="free">Free (50 scans/month)</option>
              <option value="pro">Pro (500 scans/month)</option>
              <option value="enterprise">Enterprise (unlimited)</option>
            </select>
          </div>
        </div>

        <div class="flex gap-3 mt-6">
          <button
            @click="showCreateKeyModal = false"
            class="flex-1 px-4 py-3 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="createApiKey"
            class="flex-1 px-4 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all"
          >
            Create
          </button>
        </div>
      </div>
    </div>

    <!-- Create Webhook Modal -->
    <div v-if="showCreateWebhookModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-slate-800 rounded-xl border border-white/10 p-6 w-full max-w-md">
        <h3 class="text-xl font-semibold text-white mb-4">Add Webhook</h3>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Name</label>
            <input
              v-model="newWebhook.name"
              type="text"
              placeholder="My Webhook"
              class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">URL</label>
            <input
              v-model="newWebhook.url"
              type="url"
              placeholder="https://your-server.com/webhook"
              class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Events</label>
            <div class="space-y-2">
              <label class="flex items-center text-gray-300">
                <input type="checkbox" v-model="newWebhook.events" value="scan.completed" class="mr-2" />
                Scan Completed
              </label>
              <label class="flex items-center text-gray-300">
                <input type="checkbox" v-model="newWebhook.events" value="scan.failed" class="mr-2" />
                Scan Failed
              </label>
            </div>
          </div>
        </div>

        <div class="flex gap-3 mt-6">
          <button
            @click="showCreateWebhookModal = false"
            class="flex-1 px-4 py-3 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="createWebhook"
            class="flex-1 px-4 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all"
          >
            Create
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import { useAuthStore } from '../stores/auth_new'
import { apiKeysApi, webhooksApi, teamsApi } from '../services/api_new'

const authStore = useAuthStore()

const activeTab = ref('profile')
const apiKeys = ref<any[]>([])
const webhooks = ref<any[]>([])
const teams = ref<any[]>([])
const usageStats = ref<any>(null)

const showCreateKeyModal = ref(false)
const showCreateWebhookModal = ref(false)

const profile = ref({
  name: '',
  email: ''
})

const newKey = ref({ name: '', plan: 'free' })
const newWebhook = ref({ name: '', url: '', events: [] as string[] })

const UserIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' })
])

const KeyIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z' })
])

const WebhookIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1' })
])

const TeamIcon = () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' })
])

const tabs = [
  { id: 'profile', name: 'Profile', icon: UserIcon },
  { id: 'apikeys', name: 'API Keys', icon: KeyIcon },
  { id: 'webhooks', name: 'Webhooks', icon: WebhookIcon },
  { id: 'teams', name: 'Teams', icon: TeamIcon }
]

onMounted(async () => {
  profile.value = {
    name: authStore.user?.name || '',
    email: authStore.user?.email || ''
  }
  await loadData()
})

async function loadData() {
  try {
    apiKeys.value = await apiKeysApi.list()
    webhooks.value = await webhooksApi.list()
    teams.value = await teamsApi.list()
    usageStats.value = await apiKeysApi.getUsage()
  } catch (e) {
    console.error('Failed to load data:', e)
  }
}

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString()
}

function saveProfile() {
  // In a real app, this would call the API
  alert('Profile saved!')
}

async function createApiKey() {
  try {
    await apiKeysApi.create(newKey.value.name, newKey.value.plan)
    showCreateKeyModal.value = false
    newKey.value = { name: '', plan: 'free' }
    await loadData()
  } catch (e: any) {
    alert(e.message || 'Failed to create API key')
  }
}

async function deleteApiKey(keyId: string) {
  if (confirm('Are you sure you want to delete this API key?')) {
    try {
      await apiKeysApi.delete(keyId)
      await loadData()
    } catch (e: any) {
      alert(e.message || 'Failed to delete API key')
    }
  }
}

async function createWebhook() {
  try {
    await webhooksApi.create(newWebhook.value.url, newWebhook.value.events, newWebhook.value.name)
    showCreateWebhookModal.value = false
    newWebhook.value = { name: '', url: '', events: [] }
    await loadData()
  } catch (e: any) {
    alert(e.message || 'Failed to create webhook')
  }
}

async function deleteWebhook(webhookId: string) {
  if (confirm('Are you sure you want to delete this webhook?')) {
    try {
      await webhooksApi.delete(webhookId)
      await loadData()
    } catch (e: any) {
      alert(e.message || 'Failed to delete webhook')
    }
  }
}

async function testWebhook(webhookId: string) {
  try {
    await webhooksApi.test(webhookId)
    alert('Test webhook sent!')
  } catch (e: any) {
    alert(e.message || 'Failed to send test webhook')
  }
}

async function createTeam() {
  const name = prompt('Team name:')
  if (name) {
    try {
      await teamsApi.create(name)
      await loadData()
    } catch (e: any) {
      alert(e.message || 'Failed to create team')
    }
  }
}
</script>
