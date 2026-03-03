<template>
  <nav class="bg-slate-900/95 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center group">
            <div class="w-9 h-9 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center mr-3 shadow-lg shadow-blue-500/20 group-hover:shadow-blue-500/40 transition-shadow">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <span class="text-xl font-bold text-white">DevGuardian<span class="text-cyan-400">AI</span></span>
          </router-link>
        </div>

        <!-- Navigation Links - Desktop -->
        <div class="hidden lg:flex items-center space-x-1">
          <router-link 
            to="/scan" 
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/scan' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            🔍 Scan
          </router-link>
          
          <router-link 
            to="/docs" 
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/docs' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            Docs
          </router-link>
        </div>

        <!-- Right side items -->
        <div class="flex items-center space-x-3">
          <!-- Auth Buttons -->
          <div v-if="!isAuthenticated" class="flex items-center space-x-2">
            <router-link 
              to="/login"
              class="px-4 py-2 rounded-lg text-sm font-medium text-gray-300 hover:text-white transition-colors"
            >
              Sign In
            </router-link>
            <router-link 
              to="/signup"
              class="px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg text-sm font-medium hover:from-blue-500 hover:to-cyan-500 transition-all duration-200 shadow-lg shadow-blue-500/20"
            >
              Get Started
            </router-link>
          </div>

          <!-- Mobile menu button -->
          <button 
            @click="showMobileMenu = !showMobileMenu"
            class="md:hidden text-gray-400 hover:text-white p-2 rounded-lg hover:bg-white/5 transition-colors"
          >
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile menu -->
      <div v-if="showMobileMenu" class="md:hidden border-t border-white/10 py-3">
        <div class="space-y-1">
          <router-link 
            to="/scan" 
            class="block px-4 py-2 rounded-lg text-base font-medium"
            :class="$route.path === '/scan' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
            @click="showMobileMenu = false"
          >
            🔍 Scan
          </router-link>
          <router-link 
            to="/docs" 
            class="block px-4 py-2 rounded-lg text-base font-medium"
            :class="$route.path === '/docs' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
            @click="showMobileMenu = false"
          >
            Documentation
          </router-link>
          <router-link 
            to="/login" 
            class="block px-4 py-2 rounded-lg text-base font-medium text-gray-400 hover:text-white hover:bg-white/5"
            @click="showMobileMenu = false"
          >
            Sign In
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const showMobileMenu = ref(false)

const isAuthenticated = computed(() => authStore.isAuthenticated)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
  showMobileMenu.value = false
}
</script>
