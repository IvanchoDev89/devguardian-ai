<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
    <!-- Navigation -->
    <Navbar />
    
    <!-- Toast Notifications -->
    <div class="fixed top-20 right-4 z-50 space-y-2">
      <Toast
        v-for="notification in notifications"
        :key="notification.id"
        :show="true"
        :type="notification.type"
        :title="notification.title"
        :message="notification.message"
        :action="notification.action"
        @close="removeNotification(notification.id)"
        @action="handleNotificationAction(notification)"
      />
    </div>
    
    <!-- Main Content -->
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useAuthStore } from './stores/auth'
import { useNotificationStore } from './stores/notifications'
import Navbar from './components/Navbar.vue'
import Toast from './components/Toast.vue'

const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const notifications = computed(() => notificationStore.notifications)

const removeNotification = (id: string) => {
  notificationStore.removeNotification(id)
}

const handleNotificationAction = (notification: any) => {
  // Handle notification actions (like retry, view details, etc.)
  console.log('Notification action:', notification.action, notification)
}

onMounted(() => {
  // Initialize auth state
  authStore.initAuth()
})
</script>

<style>
/* Global styles for DevGuardian AI */
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Grid background pattern */
.bg-grid-white\/5 {
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
  background-size: 20px 20px;
}

.bg-grid-16 {
  background-size: 16px 16px;
}

/* Smooth transitions */
* {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Focus styles */
button:focus-visible,
input:focus-visible,
textarea:focus-visible,
a:focus-visible {
  outline: 2px solid rgba(59, 130, 246, 0.5);
  outline-offset: 2px;
}

/* Animation utilities */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Glassmorphism effects */
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}

.backdrop-blur-md {
  backdrop-filter: blur(8px);
}

.backdrop-blur-lg {
  backdrop-filter: blur(16px);
}
</style>
