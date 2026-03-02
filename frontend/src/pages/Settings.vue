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
          <!-- API Access Info -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">API Access</h3>
            <p class="text-sm text-gray-600 mb-4">
              API access requires a Pro subscription. Contact your administrator to enable API access.
            </p>
            <div class="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p class="text-sm text-yellow-800">
                Current plan: <strong>Free</strong>
              </p>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div class="space-y-3">
              <button 
                @click="clearSettings"
                class="w-full text-left px-4 py-3 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
              >
                <div class="flex items-center">
                  <svg class="h-5 w-5 mr-3 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                  <div>
                    <p class="text-sm font-medium text-gray-900">Reset Settings</p>
                    <p class="text-xs text-gray-500">Reset all settings to defaults</p>
                  </div>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Save Button -->
      <div class="mt-8 flex justify-end gap-3">
        <button 
          @click="clearSettings"
          class="px-6 py-3 border border-gray-300 rounded-md shadow-sm text-base font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
        >
          Reset
        </button>
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
import { useNotificationStore } from '../stores/notifications'

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
const notificationStore = useNotificationStore()

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
  mfa: 'Disabled',
  apiAccess: false
})

const STORAGE_KEY = 'devguardian_settings'

onMounted(() => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      const data = JSON.parse(saved)
      profile.value = { ...profile.value, ...data.profile }
      notifications.value = { ...notifications.value, ...data.notifications }
      security.value = { ...security.value, ...data.security }
    }
    
    const userStr = localStorage.getItem('user')
    if (userStr) {
      const user = JSON.parse(userStr)
      profile.value.name = user.name || profile.value.name
      profile.value.email = user.email || profile.value.email
    }
  } catch (e) {
    console.error('Failed to load settings:', e)
  }
})

const saveSettings = async () => {
  saving.value = true
  
  try {
    const settings = {
      profile: profile.value,
      notifications: notifications.value,
      security: security.value,
      savedAt: new Date().toISOString()
    }
    
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings))
    
    try {
      const userStr = localStorage.getItem('user')
      if (userStr) {
        const user = JSON.parse(userStr)
        user.name = profile.value.name
        localStorage.setItem('user', JSON.stringify(user))
      }
    } catch (e) {
      // Ignore user update errors
    }
    
    notificationStore.success('Saved', 'Settings saved successfully')
  } catch (error) {
    notificationStore.error('Error', 'Failed to save settings')
  }
   
  saving.value = false
}

const clearSettings = () => {
  localStorage.removeItem(STORAGE_KEY)
  profile.value = { name: '', email: '', role: 'member', timezone: 'UTC' }
  notifications.value = { email: true, slack: false, webhook: true }
  security.value = { sessionTimeout: 30, mfa: 'Disabled', apiAccess: false }
  notificationStore.info('Cleared', 'Settings reset to defaults')
}
</script>
