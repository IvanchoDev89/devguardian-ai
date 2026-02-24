<template>
  <div class="min-h-screen bg-slate-900">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-white">Notifications</h1>
          <p class="text-gray-400 mt-1">View all your notifications</p>
        </div>
        <button 
          v-if="notificationsStore.unreadCount > 0"
          @click="notificationsStore.markAllAsRead()"
          class="px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-sm font-medium text-white hover:bg-white/20 transition-all"
        >
          Mark all as read
        </button>
      </div>

      <div v-if="notificationsStore.loading" class="text-center py-12 text-gray-400">
        Loading notifications...
      </div>
      
      <div v-else-if="notificationsStore.notifications.length === 0" class="text-center py-12">
        <svg class="w-16 h-16 mx-auto text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
        </svg>
        <p class="text-gray-400">No notifications yet</p>
      </div>
      
      <div v-else class="space-y-4">
        <div
          v-for="notification in notificationsStore.notifications"
          :key="notification.id"
          class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-4 hover:bg-white/10 transition-colors cursor-pointer border-l-4"
          :class="notification.is_read ? 'border-transparent' : notification.type === 'error' ? 'border-red-500' : notification.type === 'warning' ? 'border-yellow-500' : notification.type === 'success' ? 'border-green-500' : 'border-blue-500'"
          @click="handleNotificationClick(notification)"
        >
          <div class="flex items-start">
            <div class="flex-shrink-0 mr-4">
              <span 
                class="w-3 h-3 rounded-full"
                :class="notification.type === 'error' ? 'bg-red-500' : notification.type === 'warning' ? 'bg-yellow-500' : notification.type === 'success' ? 'bg-green-500' : 'bg-blue-500'"
              ></span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between">
                <p class="text-sm font-medium text-white">{{ notification.title }}</p>
                <span 
                  v-if="!notification.is_read"
                  class="px-2 py-0.5 text-xs bg-blue-500/20 text-blue-400 rounded-full"
                >
                  New
                </span>
              </div>
              <p class="text-sm text-gray-400 mt-1">{{ notification.message }}</p>
              <p class="text-xs text-gray-500 mt-2">{{ formatDate(notification.created_at) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserNotificationsStore } from '../stores/userNotifications'

const notificationsStore = useUserNotificationsStore()

onMounted(async () => {
  await notificationsStore.fetchNotifications()
})

const handleNotificationClick = async (notification: any) => {
  if (!notification.is_read) {
    await notificationsStore.markAsRead(notification.id)
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) {
    const hours = Math.floor(diff / (1000 * 60 * 60))
    if (hours === 0) {
      const minutes = Math.floor(diff / (1000 * 60))
      return minutes <= 1 ? 'Just now' : `${minutes} minutes ago`
    }
    return hours === 1 ? '1 hour ago' : `${hours} hours ago`
  }
  if (days === 1) return 'Yesterday'
  if (days < 7) return `${days} days ago`
  
  return date.toLocaleDateString()
}
</script>
