<template>
  <div class="flex h-screen bg-slate-900">
    <!-- Sidebar -->
    <aside 
      class="fixed inset-y-0 left-0 z-40 w-64 bg-slate-800/50 backdrop-blur-sm border-r border-white/10 transform transition-transform duration-300"
      :class="[collapsed ? '-translate-x-full' : 'translate-x-0', 'lg:relative']"
    >
      <!-- Logo -->
      <div class="flex items-center h-16 px-6 border-b border-white/10">
        <router-link to="/" class="flex items-center">
          <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center mr-3">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <span class="text-lg font-bold text-white">DevGuardian</span>
        </router-link>
      </div>

      <!-- Navigation -->
      <nav class="px-3 py-4 space-y-1">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200"
          :class="[
            $route.path === item.path 
              ? 'bg-gradient-to-r from-blue-600/20 to-cyan-600/20 text-white border-l-2 border-cyan-400' 
              : 'text-gray-400 hover:text-white hover:bg-white/5'
          ]"
          @click="$emit('navigate')"
        >
          <component :is="item.icon" class="w-5 h-5 mr-3" />
          {{ item.name }}
          <span 
            v-if="item.badge" 
            class="ml-auto bg-red-500 text-white text-xs px-2 py-0.5 rounded-full"
          >
            {{ item.badge }}
          </span>
        </router-link>
      </nav>

      <!-- User Section -->
      <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-white/10">
        <div class="flex items-center">
          <img 
            :src="user?.avatar || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=32&h=32&fit=crop&crop=face'" 
            class="w-10 h-10 rounded-full border-2 border-white/20"
          />
          <div class="ml-3 flex-1 min-w-0">
            <p class="text-sm font-medium text-white truncate">{{ user?.name || 'User' }}</p>
            <p class="text-xs text-gray-400 truncate">{{ user?.email || '' }}</p>
          </div>
          <button 
            @click="handleLogout"
            class="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Mobile Overlay -->
    <div 
      v-if="!collapsed" 
      class="fixed inset-0 bg-black/50 z-30 lg:hidden"
      @click="$emit('close')"
    />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col min-h-screen overflow-hidden">
      <!-- Top Bar -->
      <header class="flex items-center h-16 px-4 bg-slate-900/50 backdrop-blur-sm border-b border-white/10">
        <button 
          @click="$emit('toggle')"
          class="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg lg:hidden"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
        
        <div class="flex-1 flex items-center justify-between px-4">
          <h1 class="text-lg font-semibold text-white">{{ pageTitle }}</h1>
          
          <div class="flex items-center gap-3">
            <!-- Notifications -->
            <button class="relative p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
              </svg>
              <span v-if="notificationCount > 0" class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="flex-1 overflow-y-auto p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

defineProps<{
  collapsed: boolean
}>()

defineEmits(['toggle', 'close', 'navigate'])

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)
const notificationCount = ref(0)

const pageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/dashboard': 'Dashboard',
    '/repositories': 'Repositories',
    '/vulnerabilities': 'Vulnerabilities',
    '/sql-injection-scanner': 'Scanner',
    '/ai-fixes': 'AI Fixes',
    '/pentesting': 'Pentesting',
    '/settings': 'Settings',
    '/billing': 'Billing',
    '/super-admin': 'Admin Panel',
    '/docs': 'Documentation'
  }
  return titles[route.path] || 'DevGuardian AI'
})

const DashboardIcon = {
  render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' })
  ])
}

const ScannerIcon = {
  render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
  ])
}

const VulnIcon = {
  render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z' })
  ])
}

const AiFixIcon = {
  render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4' })
  ])
}

const RepoIcon = {
  render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z' })
  ])
}

const PentagonIcon = {
  render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z' })
  ])
}

const SettingsIcon = {
  render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }),
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z' })
  ])
}

const BillingIcon = {
  render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z' })
  ])
}

const AdminIcon = {
  render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z' })
  ])
}

const navItems = computed(() => {
  const items = [
    { name: 'Dashboard', path: '/dashboard', icon: DashboardIcon },
    { name: 'Scanner', path: '/sql-injection-scanner', icon: ScannerIcon },
    { name: 'Repositories', path: '/repositories', icon: RepoIcon },
    { name: 'Vulnerabilities', path: '/vulnerabilities', icon: VulnIcon },
    { name: 'AI Fixes', path: '/ai-fixes', icon: AiFixIcon },
    { name: 'Pentesting', path: '/pentesting', icon: PentagonIcon },
  ]
  
  if (authStore.isAdmin) {
    items.push({ name: 'Admin Panel', path: '/super-admin', icon: AdminIcon })
  }
  
  items.push({ name: 'Enterprise Assets', path: '/enterprise-assets', icon: RepoIcon })
  
  items.push(
    { name: 'Billing', path: '/billing', icon: BillingIcon },
    { name: 'Settings', path: '/settings', icon: SettingsIcon }
  )
  
  return items
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
