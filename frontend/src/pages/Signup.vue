<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center px-4">
    <!-- Background Pattern -->
    <div class="absolute inset-0 bg-grid-white/5 bg-grid-16"></div>
    
    <div class="relative w-full max-w-md">
      <!-- Logo/Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-white mb-2">
          <span class="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            DevGuardian AI
          </span>
        </h1>
        <p class="text-gray-400">Create your security account</p>
      </div>

      <!-- Signup Form -->
      <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-8 border border-white/10">
        <form @submit.prevent="handleSignup" class="space-y-6">
          <!-- Name -->
          <div>
            <label for="name" class="block text-sm font-medium text-gray-300 mb-2">
              Full Name
            </label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              placeholder="John Doe"
            />
          </div>

          <!-- Email -->
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

          <!-- Company -->
          <div>
            <label for="company" class="block text-sm font-medium text-gray-300 mb-2">
              Company (Optional)
            </label>
            <input
              id="company"
              v-model="form.company"
              type="text"
              class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              placeholder="Acme Corp"
            />
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-300 mb-2">
              Password
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              placeholder="•••••••••"
            />
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-300 mb-2">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              required
              class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              placeholder="•••••••••"
            />
          </div>

          <!-- Terms -->
          <div class="flex items-center">
            <input
              id="terms"
              v-model="form.agreeTerms"
              type="checkbox"
              required
              class="w-4 h-4 bg-white/5 border-white/10 rounded text-blue-500 focus:ring-blue-500 focus:ring-offset-0"
            />
            <label for="terms" class="ml-2 text-sm text-gray-300">
              I agree to the 
              <a href="#" class="text-blue-400 hover:text-blue-300 transition-colors">Terms of Service</a>
              and 
              <a href="#" class="text-blue-400 hover:text-blue-300 transition-colors">Privacy Policy</a>
            </label>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
            <div class="flex">
              <svg class="w-5 h-5 text-red-400 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
              </svg>
              <p class="text-sm text-red-400">{{ error }}</p>
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-slate-900 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-[1.02]"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Creating account...
            </span>
            <span v-else>Create Account</span>
          </button>
        </form>

        <!-- Divider -->
        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-white/10"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-transparent text-gray-400">Or continue with</span>
          </div>
        </div>

        <!-- Social Signup -->
        <div class="grid grid-cols-2 gap-3">
          <button
            @click="handleGitHubSignup"
            class="flex items-center justify-center px-4 py-2 bg-white/5 border border-white/10 rounded-lg hover:bg-white/10 transition-all duration-200"
          >
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.051 0-1.846.076-2.28.151.076-.432.186-.749.426-1.003.426-.449 0-.793-.276-.903-.646-.144-.503-.432-1.545-.432-1.545-.144-.382-.326-.762-.326-1.141 0-1.426.766-2.87 2-2.87.825 0 1.662.245 2.874.118.318.099.659.297 1.01.484.397.183.846.468 1.333.468.435 0 .793-.149 1.081-.448.288-.299.58-.748.58-1.141 0-.855-.422-1.743-1.195-2.674-1.773-1.699-2.542-2.919-2.542-1.9 0-3.476 1.135-3.476 2.54 0 .305.034.618.094.918.094.266 0 .524-.039.735-.127-.265-.653-.369-1.363-.369-1.363-.546-1.387-1.333-1.756-1.333-1.051 0-1.846.076-2.28.151.076-.432.186-.749.426-1.003.426-.449 0-.793-.276-.903-.646-.144-.503-.432-1.545-.432-1.545-.144-.382-.326-.762-.326-1.141 0-1.426.766-2.87 2-2.87.825 0 1.662.245 2.874.118.318.099.659.297 1.01.484.397.183.846.468 1.333.468.435 0 .793-.149 1.081-.448.288-.299.58-.748.58-1.141 0-.855-.422-1.743-1.195-2.674-1.773-1.699-2.542-2.919-2.542-1.9 0-3.476 1.135-3.476 2.54 0 .305.034.618.094.918.094.266 0 .524-.039.735-.127-.265-.653-.369-1.363-.369-1.363z"/>
            </svg>
            <span class="text-gray-300 text-sm">GitHub</span>
          </button>
          
          <button
            @click="handleGoogleSignup"
            class="flex items-center justify-center px-4 py-2 bg-white/5 border border-white/10 rounded-lg hover:bg-white/10 transition-all duration-200"
          >
            <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            <span class="text-gray-300 text-sm">Google</span>
          </button>
        </div>

        <!-- Sign In Link -->
        <p class="text-center text-gray-400 text-sm mt-6">
          Already have an account?
          <router-link to="/login" class="text-blue-400 hover:text-blue-300 font-medium transition-colors">
            Sign in
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { authService } from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  name: '',
  email: '',
  company: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

const loading = ref(false)
const error = ref('')

const handleSignup = async () => {
  loading.value = true
  error.value = ''
  
  try {
    if (form.value.password !== form.value.confirmPassword) {
      error.value = 'Passwords do not match'
      loading.value = false
      return
    }
    
    const result = await authStore.register({
      name: form.value.name,
      email: form.value.email,
      password: form.value.password,
    })
    
    if (result.success) {
      router.push('/dashboard')
    } else {
      error.value = result.error || 'Registration failed'
    }
  } catch (err: any) {
    error.value = err.message || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}

const handleGitHubSignup = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const response = await authService.getGitHubAuthUrl()
    
    if (response.success && response.data?.url) {
      window.location.href = response.data.url
    } else {
      throw new Error(response.message || 'Failed to get GitHub auth URL')
    }
  } catch (err: any) {
    error.value = err.message || 'GitHub signup failed'
    loading.value = false
  }
}

const handleGoogleSignup = () => {
  error.value = 'Google OAuth will be available soon. Please sign up with email or GitHub.'
}
</script>
