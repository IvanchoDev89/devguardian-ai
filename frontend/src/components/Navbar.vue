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
            v-if="isAdmin"
            to="/admin" 
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/admin' ? 'text-white bg-red-600' : 'text-red-400 hover:text-white hover:bg-white/5'"
          >
            ⚙️ Admin
          </router-link>
          
          <router-link 
            to="/docs" 
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/docs' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            Docs
          </router-link>
        </div>

        <!-- Right side - User Menu -->
        <div class="flex items-center space-x-3">
          <!-- Authenticated User Menu -->
          <div v-if="isAuthenticated" class="relative">
            <button 
              @click="showUserMenu = !showUserMenu"
              class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white/5 transition-colors"
            >
              <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-white text-sm font-medium">
                {{ userInitials }}
              </div>
              <span class="text-sm text-gray-300 hidden md:block">{{ userName }}</span>
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>
            
            <!-- Dropdown Menu -->
            <div 
              v-if="showUserMenu" 
              class="absolute right-0 mt-2 w-56 bg-slate-800/95 backdrop-blur-md rounded-xl shadow-xl border border-white/10 py-2"
            >
              <div class="px-4 py-3 border-b border-white/10">
                <p class="text-sm font-medium text-white">{{ userName }}</p>
                <p class="text-xs text-gray-400">{{ userEmail }}</p>
                <span 
                  class="inline-block mt-1 text-xs px-2 py-0.5 rounded-full"
                  :class="roleBadgeClass"
                >
                  {{ userRole }}
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

          <!-- Guest Buttons -->
          <div v-else class="flex items-center space-x-2">
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
            class="flex items-center px-4 py-2 rounded-lg text-base font-medium"
            :class="$route.path === '/scan' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
            @click="showMobileMenu = false"
          >
            <span class="mr-3">🔍</span> Scan
          </router-link>
          
          <router-link 
            to="/docs" 
            class="flex items-center px-4 py-2 rounded-lg text-base font-medium"
            :class="$route.path === '/docs' ? 'text-white bg-white/10' : 'text-gray-400 hover:text-white hover:bg-white/5'"
            @click="showMobileMenu = false"
          >
            <span class="mr-3">📚</span> Documentation
          </router-link>
          
          <template v-if="isAuthenticated">
            <div class="border-t border-white/10 my-2 pt-2">
              <div class="px-4 py-2">
                <p class="text-sm font-medium text-white">{{ userName }}</p>
                <p class="text-xs text-gray-400">{{ userEmail }}</p>
              </div>
            </div>
            <router-link 
              v-if="isAdmin"
              to="/admin" 
              class="flex items-center px-4 py-2 rounded-lg text-base font-medium text-red-400 hover:bg-white/5"
              @click="showMobileMenu = false"
            >
              <span class="mr-3">⚙️</span> Admin
            </router-link>
            <router-link 
              to="/settings" 
              class="flex items-center px-4 py-2 rounded-lg text-base font-medium text-gray-400 hover:text-white hover:bg-white/5"
              @click="showMobileMenu = false"
            >
              <span class="mr-3">🔧</span> Settings
            </router-link>
            <button 
              @click="handleLogout"
              class="flex items-center w-full px-4 py-2 rounded-lg text-base font-medium text-red-400 hover:bg-white/5"
            >
              <span class="mr-3">🚪</span> Sign out
            </button>
          </template>
          
          <template v-else>
            <div class="border-t border-white/10 my-2 pt-2">
              <router-link 
                to="/login" 
                class="flex items-center px-4 py-2 rounded-lg text-base font-medium text-gray-400 hover:text-white hover:bg-white/5"
                @click="showMobileMenu = false"
              >
                Sign In
              </router-link>
              <router-link 
                to="/signup" 
                class="flex items-center px-4 py-2 rounded-lg text-base font-medium text-blue-400 hover:text-blue-300"
                @click="showMobileMenu = false"
              >
                Get Started
              </router-link>
            </div>
          </template>
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
const showUserMenu = ref(false)

const isAuthenticated = computed(() => authStore.isAuthenticated)

const userData = computed(() => {
  return authStore.user
})

const userName = computed(() => {
  return userData.value?.name || 'User'
})

const userEmail = computed(() => {
  return userData.value?.email || 'user@example.com'
})

const userRole = computed(() => {
  return userData.value?.role || 'free'
})

const isAdmin = computed(() => {
  const role = userRole.value
  return role === 'super_admin' || role === 'admin'
})

const userInitials = computed(() => {
  const name = userName.value
  if (name && name.length > 0) {
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
  }
  return 'U'
})

const roleBadgeClass = computed(() => {
  const role = userRole.value
  if (role === 'super_admin' || role === 'admin') {
    return 'bg-red-500/20 text-red-400'
  }
  if (role === 'pro') {
    return 'bg-blue-500/20 text-blue-400'
  }
  return 'bg-gray-500/20 text-gray-400'
})

const handleLogout = () => {
  authStore.logout()
  showUserMenu.value = false
  showMobileMenu.value = false
  router.push('/login')
}
</script>
