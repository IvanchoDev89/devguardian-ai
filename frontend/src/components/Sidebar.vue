<template>
  <div class="fixed inset-y-0 left-0 z-50 w-72 bg-slate-900/95 backdrop-blur-xl border-r border-white/10 flex flex-col">
    
    <!-- Logo -->
    <div class="h-18 flex items-center px-5 border-b border-white/10">
      <router-link to="/app/dashboard" class="flex items-center group">
        <div class="w-10 h-10 bg-gradient-to-br from-blue-500 via-cyan-500 to-teal-500 rounded-xl flex items-center justify-center mr-3 shadow-lg shadow-blue-500/25 group-hover:scale-105 transition-transform">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
        </div>
        <div>
          <span class="text-lg font-bold text-white tracking-tight">DevGuardian</span>
          <span class="text-xs font-medium text-cyan-400 ml-1">AI</span>
        </div>
      </router-link>
    </div>

    <!-- User Info Card -->
    <div v-if="isAuthenticated" class="px-4 py-4 border-b border-white/10">
      <div class="flex items-center gap-3 p-3 bg-gradient-to-r from-white/5 to-white/[0.02] rounded-xl border border-white/5">
        <div class="w-11 h-11 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-white font-bold text-sm shadow-lg">
          {{ userInitials }}
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-semibold text-white truncate">{{ userName }}</p>
          <div class="flex items-center gap-2 mt-0.5">
            <span class="px-2 py-0.5 text-[10px] font-medium rounded-full" :class="roleBadgeClass">
              {{ userRoleDisplay }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- Plan Badge -->
      <div v-if="plan !== 'free'" class="mt-2 flex items-center justify-center px-3 py-1.5 bg-gradient-to-r from-amber-500/10 to-yellow-500/10 rounded-lg border border-amber-500/20">
        <span class="text-xs font-medium text-amber-400">{{ plan.toUpperCase() }} Plan</span>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto p-3 space-y-6">
      <div v-for="(items, category) in groupedNavigation" :key="category">
        <!-- Category Header -->
        <div class="flex items-center gap-2 px-3 mb-2">
          <span class="text-[10px] font-bold uppercase tracking-wider text-gray-500">{{ categoryLabels[category] || category }}</span>
          <div class="flex-1 h-px bg-gradient-to-r from-white/5 to-transparent"></div>
        </div>
        
        <!-- Nav Items -->
        <div class="space-y-1">
          <router-link 
            v-for="item in items" 
            :key="item.path"
            :to="item.path"
            class="flex items-center px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 group relative overflow-hidden"
            :class="$route.path === item.path 
              ? 'bg-gradient-to-r from-blue-600/20 to-cyan-600/20 text-white shadow-lg shadow-blue-500/10' 
              : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            <!-- Active Indicator -->
            <div v-if="$route.path === item.path" class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-gradient-to-b from-blue-500 to-cyan-500 rounded-r-full"></div>
            
            <div class="w-8 h-8 rounded-lg flex items-center justify-center mr-3 transition-transform group-hover:scale-110" :class="item.iconBgClass">
              <span v-html="item.icon"></span>
            </div>
            {{ item.name }}
            <span v-if="item.badge" class="ml-auto px-2 py-0.5 text-xs rounded-full" :class="item.badgeClass">
              {{ item.badge }}
            </span>
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Bottom Section -->
    <div class="p-4 border-t border-white/10">
      <div v-if="isAuthenticated" class="space-y-2">
        <router-link to="/settings" class="flex items-center px-4 py-2.5 text-sm font-medium text-gray-400 hover:text-white hover:bg-white/5 rounded-xl transition-colors">
          <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
          Settings
        </router-link>
        
        <button @click="handleLogout" class="flex items-center w-full px-4 py-2.5 text-sm font-medium text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-xl transition-colors">
          <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
          Logout
        </button>
      </div>
      
      <div v-else class="space-y-2">
        <router-link to="/login" class="flex items-center justify-center w-full px-4 py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 rounded-xl transition-all shadow-lg shadow-blue-500/25">
          Login
        </router-link>
        <router-link to="/signup" class="flex items-center justify-center w-full px-4 py-2.5 text-sm font-medium text-gray-300 hover:text-white bg-white/5 hover:bg-white/10 rounded-xl transition-colors">
          Sign Up Free
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useNavigation } from '../composables/useNavigation'

const router = useRouter()
const authStore = useAuthStore()
const { groupedNavigation, categoryLabels, hasAccess } = useNavigation()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const userName = computed(() => authStore.user?.name || 'User')
const userEmail = computed(() => authStore.user?.email || 'user@example.com')
const userRole = computed(() => authStore.user?.role || 'user')
const plan = computed(() => authStore.plan || 'free')

const userInitials = computed(() => {
  const name = userName.value
  return name.split(' ').map((n: string) => n[0]).join('').toUpperCase().slice(0, 2)
})

const userRoleDisplay = computed(() => {
  const role = userRole.value
  const labels: Record<string, string> = {
    super_admin: 'Super Admin',
    admin: 'Admin',
    pro: 'Pro',
    enterprise: 'Enterprise',
    user: 'User',
    member: 'Member',
    viewer: 'Viewer'
  }
  return labels[role] || role
})

const roleBadgeClass = computed(() => {
  const role = userRole.value
  if (role === 'super_admin') return 'bg-gradient-to-r from-red-500/20 to-pink-500/20 text-red-400 border border-red-500/30'
  if (role === 'admin') return 'bg-gradient-to-r from-violet-500/20 to-purple-500/20 text-violet-400 border border-violet-500/30'
  if (role === 'enterprise') return 'bg-gradient-to-r from-amber-500/20 to-yellow-500/20 text-amber-400 border border-amber-500/30'
  if (role === 'pro') return 'bg-gradient-to-r from-cyan-500/20 to-blue-500/20 text-cyan-400 border border-cyan-500/30'
  return 'bg-gray-500/20 text-gray-400 border border-gray-500/30'
})

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.h-18 {
  height: 4.5rem;
}
</style>
