<template>
  <div id="app">
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-xl font-bold text-gray-900">DevGuardian AI</h1>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                to="/"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="route.path === '/' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                Dashboard
              </router-link>
              <router-link
                to="/repositories"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="route.path === '/repositories' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                Repositories
              </router-link>
              <router-link
                to="/vulnerabilities"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="route.path === '/vulnerabilities' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                Vulnerabilities
              </router-link>
              <router-link
                to="/ai-fixes"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="route.path === '/ai-fixes' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                AI Fixes
              </router-link>
            </div>
          </div>
          <div class="flex items-center">
            <router-link
              to="/settings"
              class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="route.path === '/settings' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
            >
              Settings
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>
