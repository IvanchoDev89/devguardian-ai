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
            <label class="block text-sm text-gray-400 mb-2">Name</label>
            <input v-model="name" type="text" class="w-full bg-slate-900/50 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-cyan-500" />
          </div>
          <div>
            <label class="block text-sm text-gray-400 mb-2">Email</label>
            <input v-model="email" type="email" class="w-full bg-slate-900/50 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-cyan-500" />
          </div>
          <button class="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white font-medium rounded-lg transition-colors">
            Save Changes
          </button>
        </div>
      </div>

      <!-- Account -->
      <div class="bg-slate-800/50 rounded-xl border border-white/10 p-5">
        <h2 class="text-lg font-semibold text-white mb-4">Account</h2>
        <div class="space-y-4">
          <div class="p-3 bg-slate-900/50 rounded-lg">
            <p class="text-gray-400 text-sm">Plan</p>
            <p class="text-white font-medium">{{ plan }}</p>
          </div>
          <div class="p-3 bg-slate-900/50 rounded-lg">
            <p class="text-gray-400 text-sm">Role</p>
            <p class="text-white font-medium">{{ role }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const name = ref(authStore.user?.name || '')
const email = ref(authStore.user?.email || '')
const plan = computed(() => authStore.plan || 'free')
const role = computed(() => authStore.user?.role || 'user')
</script>
