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
            to="/dashboard" 
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/dashboard' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            Dashboard
          </router-link>
          
          <router-link 
            to="/sql-injection-scanner" 
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/sql-injection-scanner' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            Scanner
          </router-link>
          
          <router-link 
            to="/vulnerabilities" 
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/vulnerabilities' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            Vulnerabilities
          </router-link>

          <router-link 
            to="/ai-fixes" 
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/ai-fixes' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            AI Fixes
          </router-link>

          <router-link 
            to="/pentesting" 
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/pentesting' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            Pentesting
          </router-link>

          <router-link 
            to="/docs" 
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/docs' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            Docs
          </router-link>

          <router-link 
            v-if="isAdmin"
            to="/super-admin" 
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/super-admin' ? 'text-white bg-red-600' : 'text-red-400 hover:text-red-300 hover:bg-white/5'"
          >
            Admin
          </router-link>
        </div>

        <!-- Right side items -->
        <div class="flex items-center space-x-3">
          <router-link 
            to="/pricing"
            class="hidden sm:inline-flex px-3 py-1.5 rounded-lg text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 transition-all duration-200"
          >
            Pricing
          </router-link>
          
          <!-- User Menu -->
          <div v-if="isAuthenticated" class="relative">
            <button 
              @click="showUserMenu = !showUserMenu"
              class="flex items-center gap-2 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900 focus:ring-blue-500"
            >
              <img 
                :src="user?.avatar || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=32&h=32&fit=crop&crop=face'" 
                :alt="user?.name" 
                class="h-8 w-8 rounded-full border-2 border-white/20"
              />
            </button>
            
            <div 
              v-if="showUserMenu" 
              class="absolute right-0 mt-3 w-56 bg-slate-800/95 backdrop-blur-md rounded-xl shadow-xl border border-white/10 py-2"
              @click.away="showUserMenu = false"
            >
              <div class="px-4 py-3 border-b border-white/10">
                <p class="text-sm font-medium text-white">{{ user?.name }}</p>
                <p class="text-xs text-gray-400">{{ user?.email }}</p>
                <span 
                  v-if="user?.role === 'admin'" 
                  class="inline-block mt-1 text-xs px-2 py-0.5 rounded-full bg-red-500/20 text-red-400"
                >
                  Admin
                </span>
              </div>
              <div class="py-1">
                <router-link 
                  to="/settings" 
                  class="flex items-center px-4 py-2 text-sm text-gray-300 hover:bg-white/5 hover:text-white transition-colors"
                  @click="showUserMenu = false"
                >
                  <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  Settings
                </router-link>
                <router-link 
                  to="/billing" 
                  class="flex items-center px-4 py-2 text-sm text-gray-300 hover:bg-white/5 hover:text-white transition-colors"
                  @click="showUserMenu = false"
                >
                  <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
                  </svg>
                  Billing
                </router-link>
              </div>
              <div class="border-t border-white/10 py-1">
                <button 
                  @click="handleLogout"
                  class="flex items-center w-full px-4 py-2 text-sm text-red-400 hover:bg-white/5 hover:text-red-300 transition-colors"
                >
                  <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                  </svg>
                  Sign out
                </button>
              </div>
            </div>
          </div>
          
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
            to="/dashboard" 
            class="block px-4 py-2 rounded-lg text-base font-medium"
            :class="$route.path === '/dashboard' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
            @click="showMobileMenu = false"
          >
            Dashboard
          </router-link>
          <router-link 
            to="/sql-injection-scanner" 
            class="block px-4 py-2 rounded-lg text-base font-medium"
            :class="$route.path === '/sql-injection-scanner' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
            @click="showMobileMenu = false"
          >
            Scanner
          </router-link>
          <router-link 
            to="/vulnerabilities" 
            class="block px-4 py-2 rounded-lg text-base font-medium"
            :class="$route.path === '/vulnerabilities' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
            @click="showMobileMenu = false"
          >
            Vulnerabilities
          </router-link>
          <router-link 
            to="/ai-fixes" 
            class="block px-4 py-2 rounded-lg text-base font-medium"
            :class="$route.path === '/ai-fixes' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
            @click="showMobileMenu = false"
          >
            AI Fixes
          </router-link>
          <router-link 
            to="/pentesting" 
            class="block px-4 py-2 rounded-lg text-base font-medium"
            :class="$route.path === '/pentesting' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
            @click="showMobileMenu = false"
          >
            Pentesting
          </router-link>
          <router-link 
            to="/pricing" 
            class="block px-4 py-2 rounded-lg text-base font-medium"
            :class="$route.path === '/pricing' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
            @click="showMobileMenu = false"
          >
            Pricing
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
            v-if="isAdmin"
            to="/super-admin" 
            class="block px-4 py-2 rounded-lg text-base font-medium text-red-400 hover:text-red-300 hover:bg-white/5"
            @click="showMobileMenu = false"
          >
            Admin Panel
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

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const showUserMenu = ref(false)
const showMobileMenu = ref(false)

const user = computed(() => authStore.user as any)
const isAuthenticated = computed(() => authStore.isAuthenticated)
const isAdmin = computed(() => user.value?.role === 'admin' || user.value?.role === 'super_admin')

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
  showUserMenu.value = false
}
</script>
