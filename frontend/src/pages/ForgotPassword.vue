<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center px-4">
    <div class="absolute inset-0 bg-grid-white/5 bg-grid-16"></div>
    
    <div class="relative w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-white mb-2">
          <span class="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            DevGuardian AI
          </span>
        </h1>
        <p class="text-gray-400">Reset your password</p>
      </div>

      <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-8 border border-white/10">
        <div v-if="!emailSent">
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-300 mb-2">
                Email Address
              </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                placeholder="you@example.com"
              />
            </div>

            <div v-if="error" class="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
              <p class="text-sm text-red-400">{{ error }}</p>
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-slate-900 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            >
              <span v-if="loading">Sending...</span>
              <span v-else>Send Reset Link</span>
            </button>
          </form>
          
          <div class="mt-6 text-center">
            <router-link to="/login" class="text-sm text-gray-400 hover:text-blue-400 transition-colors">
              Back to login
            </router-link>
          </div>
        </div>

        <div v-else class="text-center py-8">
          <div class="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Check your email</h3>
          <p class="text-gray-400 mb-6">
            We've sent a password reset link to<br/>
            <span class="text-white">{{ form.email }}</span>
          </p>
          <router-link 
            to="/login"
            class="inline-block px-6 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors"
          >
            Back to Login
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { authApi } from '../services/api_client'
import { useNotificationStore } from '../stores/notifications'

const notification = useNotificationStore()

const form = ref({
  email: ''
})

const loading = ref(false)
const error = ref('')
const emailSent = ref(false)

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  
  try {
    await authApi.requestPasswordReset(form.value.email)
    emailSent.value = true
    notification.success('Email Sent', 'Check your inbox for the reset link')
  } catch (err: any) {
    error.value = err.message || 'Failed to send reset email'
  } finally {
    loading.value = false
  }
}
</script>