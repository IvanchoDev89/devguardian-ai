<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800">
    <Navbar />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Admin Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-white">Admin Dashboard</h1>
        <p class="text-gray-400 mt-2">Manage your DevGuardian AI account</p>
      </div>

      <!-- User Info Card -->
      <div class="bg-gray-800 rounded-xl border border-gray-700 p-6 mb-6">
        <h2 class="text-xl font-semibold text-white mb-4">Account Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p class="text-gray-400 text-sm">Name</p>
            <p class="text-white text-lg">{{ user?.name || 'User' }}</p>
          </div>
          <div>
            <p class="text-gray-400 text-sm">Email</p>
            <p class="text-white text-lg">{{ user?.email || 'user@example.com' }}</p>
          </div>
          <div>
            <p class="text-gray-400 text-sm">Role</p>
            <span 
              class="inline-block px-3 py-1 rounded-full text-sm font-medium mt-1"
              :class="roleBadgeClass"
            >
              {{ userRole }}
            </span>
          </div>
          <div>
            <p class="text-gray-400 text-sm">Plan</p>
            <span 
              class="inline-block px-3 py-1 rounded-full text-sm font-medium mt-1"
              :class="planBadgeClass"
            >
              {{ userPlan }}
            </span>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="bg-gray-800 rounded-xl border border-gray-700 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Total Scans</p>
              <p class="text-3xl font-bold text-white mt-1">{{ scansCount }}</p>
            </div>
            <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 rounded-xl border border-gray-700 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Vulnerabilities Found</p>
              <p class="text-3xl font-bold text-white mt-1">{{ vulnCount }}</p>
            </div>
            <div class="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 rounded-xl border border-gray-700 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">Security Score</p>
              <p class="text-3xl font-bold text-green-400 mt-1">{{ securityScore }}</p>
            </div>
            <div class="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-gray-800 rounded-xl border border-gray-700 p-6">
        <h2 class="text-xl font-semibold text-white mb-4">Quick Actions</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <router-link 
            to="/scan"
            class="flex items-center p-4 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors"
          >
            <svg class="w-8 h-8 text-blue-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <div>
              <p class="text-white font-medium">New Scan</p>
              <p class="text-gray-400 text-sm">Analyze code for vulnerabilities</p>
            </div>
          </router-link>

          <router-link 
            to="/settings"
            class="flex items-center p-4 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors"
          >
            <svg class="w-8 h-8 text-purple-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            <div>
              <p class="text-white font-medium">Settings</p>
              <p class="text-gray-400 text-sm">Configure your account</p>
            </div>
          </router-link>

          <router-link 
            to="/docs"
            class="flex items-center p-4 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors"
          >
            <svg class="w-8 h-8 text-green-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
            </svg>
            <div>
              <p class="text-white font-medium">Documentation</p>
              <p class="text-gray-400 text-sm">Learn how to use</p>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Navbar from '../components/Navbar.vue'

const user = computed(() => {
  const stored = localStorage.getItem('user')
  if (stored) {
    try {
      return JSON.parse(stored)
    } catch {
      return null
    }
  }
  return null
})

const userRole = computed(() => {
  return user.value?.role || 'free'
})

const userPlan = computed(() => {
  const plan = localStorage.getItem('plan')
  return plan || 'free'
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

const planBadgeClass = computed(() => {
  const plan = userPlan.value
  if (plan === 'enterprise') {
    return 'bg-purple-500/20 text-purple-400'
  }
  if (plan === 'pro') {
    return 'bg-blue-500/20 text-blue-400'
  }
  return 'bg-gray-500/20 text-gray-400'
})

const scansCount = computed(() => {
  const stored = localStorage.getItem('scans_count')
  return stored ? parseInt(stored) : 0
})

const vulnCount = computed(() => {
  const stored = localStorage.getItem('vuln_count')
  return stored ? parseInt(stored) : 0
})

const securityScore = computed(() => {
  return scansCount.value > 0 ? Math.max(0, 100 - (vulnCount.value * 10)) : 100
})
</script>
