<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-white">Settings</h1>
      <p class="text-gray-400 mt-1">Manage your account settings</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Profile -->
      <div class="lg:col-span-2 bg-slate-800/50 rounded-xl border border-white/10 p-5">
        <h2 class="text-lg font-semibold text-white mb-4">Profile</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm text-gray-400 mb-2">Full Name</label>
            <input 
              v-model="form.name" 
              type="text" 
              class="w-full bg-slate-900/50 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-cyan-500"
              placeholder="Your full name"
            />
          </div>
          <div>
            <label class="block text-sm text-gray-400 mb-2">Email</label>
            <input 
              v-model="form.email" 
              type="email" 
              class="w-full bg-slate-900/50 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-cyan-500"
              placeholder="your@email.com"
            />
          </div>
          <button 
            @click="saveProfile" 
            :disabled="saving"
            class="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors flex items-center gap-2"
          >
            <svg v-if="saving" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ saving ? 'Saving...' : 'Save Changes' }}</span>
          </button>
        </div>
      </div>

      <!-- Account -->
      <div class="bg-slate-800/50 rounded-xl border border-white/10 p-5">
        <h2 class="text-lg font-semibold text-white mb-4">Account</h2>
        <div class="space-y-4">
          <div class="p-3 bg-slate-900/50 rounded-lg">
            <p class="text-gray-400 text-sm">Plan</p>
            <p class="text-white font-medium capitalize">{{ plan }}</p>
          </div>
          <div class="p-3 bg-slate-900/50 rounded-lg">
            <p class="text-gray-400 text-sm">Role</p>
            <p class="text-white font-medium capitalize">{{ role }}</p>
          </div>
          <div class="p-3 bg-slate-900/50 rounded-lg">
            <p class="text-gray-400 text-sm">Member Since</p>
            <p class="text-white font-medium">{{ createdAt }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useNotificationStore } from '../stores/notifications'
import { api } from '../services/api_client'

const authStore = useAuthStore()
const notification = useNotificationStore()

const form = ref({
  name: authStore.user?.full_name || authStore.user?.username || '',
  email: authStore.user?.email || ''
})

const saving = ref(false)

const plan = computed(() => authStore.plan || 'free')
const role = computed(() => authStore.user?.role || 'user')
const createdAt = computed(() => {
  const date = authStore.user?.created_at
  if (date) {
    return new Date(date).toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  }
  return 'N/A'
})

const saveProfile = async () => {
  saving.value = true
  try {
    const token = authStore.token
    if (!token) throw new Error('Not authenticated')
    
    const updatedUser: { full_name?: string } = await api.put('/api/users/me', {
      full_name: form.value.name,
    }, token)
    
    if (authStore.user) {
      authStore.user.full_name = updatedUser.full_name || form.value.name
      localStorage.setItem('user', JSON.stringify(authStore.user))
    }
    
    notification.success('Profile Updated', 'Your profile has been saved successfully')
  } catch (err: any) {
    notification.error('Save Failed', err.message || 'Could not save profile')
  } finally {
    saving.value = false
  }
}
</script>
