<template>
  <nav class="bg-white/5 backdrop-blur-sm border-b border-white/10 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center">
            <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <span class="text-xl font-bold text-white">DevGuardian AI</span>
          </router-link>
        </div>

        <!-- Navigation Links -->
        <div class="hidden md:flex items-center space-x-8">
          <router-link 
            to="/dashboard" 
            class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            :class="{ 'text-white bg-blue-600': $route.path === '/dashboard' }"
          >
            Dashboard
          </router-link>
          <router-link 
            to="/sql-injection-scanner" 
            class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            :class="{ 'text-white bg-blue-600': $route.path === '/sql-injection-scanner' }"
          >
            Scanner
          </router-link>
          <router-link 
            to="/vulnerabilities" 
            class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            :class="{ 'text-white bg-blue-600': $route.path === '/vulnerabilities' }"
          >
            Vulnerabilities
          </router-link>
          <router-link 
            to="/ai-fixes" 
            class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            :class="{ 'text-white bg-blue-600': $route.path === '/ai-fixes' }"
          >
            AI Fixes
          </router-link>
          <router-link 
            to="/pentesting" 
            class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            :class="{ 'text-white bg-blue-600': $route.path === '/pentesting' }"
          >
            Pentest
          </router-link>
          <router-link 
            to="/super-admin" 
            class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            :class="{ 'text-white bg-red-600': $route.path === '/super-admin' }"
          >
            Admin
          </router-link>
        </div>

        <!-- Right side items -->
        <div class="flex items-center space-x-4">
          <!-- Theme Toggle -->
          <ThemeToggle />
          
          <!-- User Menu -->
          <div v-if="isAuthenticated" class="relative">
            <button 
              @click="showUserMenu = !showUserMenu"
              class="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <img 
                :src="user?.avatar || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=32&h=32&fit=crop&crop=face'" 
                :alt="user?.name" 
                class="h-8 w-8 rounded-full"
              />
            </button>
            
            <!-- Dropdown Menu -->
            <div 
              v-if="showUserMenu" 
              class="absolute right-0 mt-2 w-48 bg-white/95 backdrop-blur-sm rounded-lg shadow-lg border border-white/20 py-1"
              @click.away="showUserMenu = false"
            >
              <div class="px-4 py-2 border-b border-white/10">
                <p class="text-sm font-medium text-gray-900">{{ user?.name }}</p>
                <p class="text-xs text-gray-500">{{ user?.email }}</p>
              </div>
              <router-link 
                to="/settings" 
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
              >
                Settings
              </router-link>
              <button 
                @click="handleLogout"
                class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
              >
                Sign out
              </button>
            </div>
          </div>
          
          <div v-if="!isAuthenticated" class="flex items-center space-x-2">
            <router-link 
              to="/login"
              class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Sign In
            </router-link>
            <router-link 
              to="/signup"
              class="bg-gradient-to-r from-blue-600 to-cyan-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:from-blue-700 hover:to-cyan-700 transition-all duration-200"
            >
              Sign Up
            </router-link>
          </div>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden">
          <button 
            @click="showMobileMenu = !showMobileMenu"
            class="text-gray-400 hover:text-white p-2 rounded-md"
          >
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile menu -->
      <div v-if="showMobileMenu" class="md:hidden">
        <div class="px-2 pt-2 pb-3 space-y-1">
          <router-link 
            to="/dashboard" 
            class="text-gray-300 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
          >
            Dashboard
          </router-link>
          <router-link 
            to="/sql-injection-scanner" 
            class="text-gray-300 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
          >
            Scanner
          </router-link>
          <router-link 
            to="/vulnerabilities" 
            class="text-gray-300 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
          >
            Vulnerabilities
          </router-link>
          <router-link 
            to="/ai-fixes" 
            class="text-gray-300 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
          >
            AI Fixes
          </router-link>
          <router-link 
            to="/pentesting" 
            class="text-gray-300 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
          >
            Pentest
          </router-link>
          <router-link 
            to="/super-admin" 
            class="text-gray-300 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
          >
            Admin
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ThemeToggle from './ThemeToggle.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const showUserMenu = ref(false)
const showMobileMenu = ref(false)

const user = computed(() => authStore.user as any)
const isAuthenticated = computed(() => authStore.isAuthenticated)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
  showUserMenu.value = false
}
</script>
