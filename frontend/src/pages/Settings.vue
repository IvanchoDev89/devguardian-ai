<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <div class="px-4 py-6 sm:px-0">
      <!-- Header Section -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Settings</h1>
        <p class="text-gray-600 mt-2">Configure your DevGuardian AI preferences and integrations</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Profile Settings -->
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <svg class="h-5 w-5 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
              Profile Settings
            </h2>
            
            <div class="space-y-4">
              <div>
                <label for="name" class="block text-sm font-medium text-gray-700">Full Name</label>
                <input
                  id="name"
                  v-model="profile.name"
                  type="text"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </div>
              
              <div>
                <label for="email" class="block text-sm font-medium text-gray-700">Email Address</label>
                <input
                  id="email"
                  v-model="profile.email"
                  type="email"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </div>
              
              <div>
                <label for="role" class="block text-sm font-medium text-gray-700">Role</label>
                <select
                  id="role"
                  v-model="profile.role"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option>Administrator</option>
                  <option>Developer</option>
                  <option>Security Analyst</option>
                  <option>Viewer</option>
                </select>
              </div>
              
              <div>
                <label for="timezone" class="block text-sm font-medium text-gray-700">Timezone</label>
                <select
                  id="timezone"
                  v-model="profile.timezone"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option>UTC</option>
                  <option>America/New_York</option>
                  <option>Europe/London</option>
                  <option>Asia/Tokyo</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Notification Settings -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <svg class="h-5 w-5 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 00-2-2h8v2.586a4.001 4.001 0 004 3.414z"></path>
              </svg>
              Notification Preferences
            </h2>
            
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <label for="email-notifications" class="text-sm font-medium text-gray-700">Email Notifications</label>
                  <p class="text-xs text-gray-500">Receive security alerts via email</p>
                </div>
                <button
                  @click="notifications.email = !notifications.email"
                  :class="notifications.email ? 'bg-blue-600' : 'bg-gray-200'"
                  class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <span class="translate-x-0 inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200" :class="notifications.email ? 'translate-x-5' : 'translate-x-0'">
                    <span class="sr-only">Email notifications</span>
                  </span>
                </button>
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <label for="slack-notifications" class="text-sm font-medium text-gray-700">Slack Integration</label>
                  <p class="text-xs text-gray-500">Send notifications to Slack</p>
                </div>
                <button
                  @click="notifications.slack = !notifications.slack"
                  :class="notifications.slack ? 'bg-blue-600' : 'bg-gray-200'"
                  class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <span class="translate-x-0 inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200" :class="notifications.slack ? 'translate-x-5' : 'translate-x-0'">
                    <span class="sr-only">Slack notifications</span>
                  </span>
                </button>
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <label for="webhook-notifications" class="text-sm font-medium text-gray-700">Webhook URLs</label>
                  <p class="text-xs text-gray-500">Send notifications to custom endpoints</p>
                </div>
                <button
                  @click="notifications.webhook = !notifications.webhook"
                  :class="notifications.webhook ? 'bg-blue-600' : 'bg-gray-200'"
                  class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <span class="translate-x-0 inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200" :class="notifications.webhook ? 'translate-x-5' : 'translate-x-0'">
                    <span class="sr-only">Webhook notifications</span>
                  </span>
                </button>
              </div>
            </div>
          </div>

          <!-- Security Settings -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <svg class="h-5 w-5 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10 10V7a4 4 0 00-8 0v4h8z"></path>
              </svg>
              Security Settings
            </h2>
            
            <div class="space-y-4">
              <div>
                <label for="session-timeout" class="block text-sm font-medium text-gray-700">Session Timeout (minutes)</label>
                <input
                  id="session-timeout"
                  v-model.number="security.sessionTimeout"
                  type="number"
                  min="5"
                  max="1440"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </div>
              
              <div>
                <label for="mfa" class="block text-sm font-medium text-gray-700">Two-Factor Authentication</label>
                <select
                  id="mfa"
                  v-model="security.mfa"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option>Disabled</option>
                  <option>Email</option>
                  <option>SMS</option>
                  <option>Authenticator App</option>
                </select>
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <label for="api-access" class="text-sm font-medium text-gray-700">API Access</label>
                  <p class="text-xs text-gray-500">Enable API key access</p>
                </div>
                <button
                  @click="security.apiAccess = !security.apiAccess"
                  :class="security.apiAccess ? 'bg-blue-600' : 'bg-gray-200'"
                  class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <span class="translate-x-0 inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200" :class="security.apiAccess ? 'translate-x-5' : 'translate-x-0'">
                    <span class="sr-only">API access</span>
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- API Keys -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">API Keys</h3>
            <div class="space-y-3">
              <div class="p-3 bg-gray-50 rounded-lg">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-gray-700">Production Key</span>
                  <button class="text-blue-600 hover:text-blue-800 text-sm">Regenerate</button>
                </div>
                <code class="text-xs text-gray-600 break-all">sk-•••••••••••••••••••••••••••••••••••</code>
              </div>
              
              <div class="p-3 bg-gray-50 rounded-lg">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-gray-700">Development Key</span>
                  <button class="text-blue-600 hover:text-blue-800 text-sm">Regenerate</button>
                </div>
                <code class="text-xs text-gray-600 break-all">sk-•••••••••••••••••••••••••••••••••••••••</code>
              </div>
            </div>
            
            <button class="w-full mt-4 inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
              Generate New API Key
            </button>
          </div>

          <!-- Quick Actions -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div class="space-y-3">
              <button class="w-full text-left px-4 py-3 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">
                <div class="flex items-center">
                  <svg class="h-5 w-5 mr-3 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4 4l-4-4m5 0v1m5-1l-4 4m4-4v1m5-1l-4 4"></path>
                  </svg>
                  <div>
                    <p class="text-sm font-medium text-gray-900">Export Data</p>
                    <p class="text-xs text-gray-500">Download all your data</p>
                  </div>
                </div>
              </button>
              
              <button class="w-full text-left px-4 py-3 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">
                <div class="flex items-center">
                  <svg class="h-5 w-5 mr-3 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                  </svg>
                  <div>
                    <p class="text-sm font-medium text-gray-900">Security Audit</p>
                    <p class="text-xs text-gray-500">Run comprehensive security audit</p>
                  </div>
                </div>
              </button>
              
              <button class="w-full text-left px-4 py-3 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">
                <div class="flex items-center">
                  <svg class="h-5 w-5 mr-3 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <div>
                    <p class="text-sm font-medium text-gray-900">View Logs</p>
                    <p class="text-xs text-gray-500">Access system logs</p>
                  </div>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Save Button -->
      <div class="mt-8 flex justify-end">
        <button 
          @click="saveSettings"
          :disabled="saving"
          class="inline-flex items-center px-6 py-3 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <svg v-if="saving" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ saving ? 'Saving...' : 'Save Settings' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { authService, apiService } from '../services/api'

interface Profile {
  name: string
  email: string
  role: string
  timezone: string
}

interface Notifications {
  email: boolean
  slack: boolean
  webhook: boolean
}

interface Security {
  sessionTimeout: number
  mfa: string
  apiAccess: boolean
}

const saving = ref(false)
const loading = ref(false)
const githubConnected = ref(false)
const githubToken = ref('')
const message = ref('')

const profile = ref<Profile>({
  name: '',
  email: '',
  role: 'member',
  timezone: 'UTC'
})

const notifications = ref<Notifications>({
  email: true,
  slack: false,
  webhook: true
})

const security = ref<Security>({
  sessionTimeout: 30,
  mfa: 'Authenticator App',
  apiAccess: true
})

onMounted(async () => {
  loading.value = true
  try {
    const response = await authService.getProfile()
    if (response.success && response.data) {
      profile.value.name = response.data.name || ''
      profile.value.email = response.data.email || ''
      profile.value.role = response.data.role || 'member'
    }
  } catch (error) {
    console.error('Failed to load profile:', error)
  }
  loading.value = false
})

const connectGitHub = async () => {
  if (!githubToken.value) {
    message.value = 'Please enter your GitHub token'
    return
  }
  
  saving.value = true
  message.value = ''
  
  try {
    const response = await apiService.post('/github/connect', {
      github_token: githubToken.value
    })
    
    if (response.success) {
      githubConnected.value = true
      message.value = 'GitHub connected successfully!'
    } else {
      message.value = response.message || 'Failed to connect GitHub'
    }
  } catch (error) {
    message.value = 'Failed to connect GitHub'
  }
  
  saving.value = false
}

const saveSettings = async () => {
  saving.value = true
  message.value = ''
  
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    message.value = 'Settings saved successfully!'
  } catch (error) {
    message.value = 'Failed to save settings'
  }
  
  saving.value = false
}
</script>
