import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api as apiClient } from '../services/api_client'

export interface UserNotification {
  id: number
  user_id: number
  title: string
  message: string
  type: 'info' | 'warning' | 'success' | 'error'
  is_read: boolean
  created_at: string
  read_at?: string
}

export const useUserNotificationsStore = defineStore('userNotifications', () => {
  const notifications = ref<UserNotification[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const unreadCount = computed(() => 
    notifications.value.filter(n => !n.is_read).length
  )

  const fetchNotifications = async () => {
    loading.value = true
    error.value = null
    try {
      const token = localStorage.getItem('access_token') || ''
      const data = await apiClient.get<UserNotification[]>('/api/notifications', token)
      if (Array.isArray(data)) {
        notifications.value = data
      }
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch notifications'
      console.error('Error fetching notifications:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchUnreadCount = async () => {
    try {
      const token = localStorage.getItem('access_token') || ''
      const data = await apiClient.get<{ count: number }>('/api/notifications/unread', token)
      if (typeof data.count === 'number') {
        return data.count
      }
      return 0
    } catch {
      return 0
    }
  }

  const markAsRead = async (id: number) => {
    try {
      const token = localStorage.getItem('access_token') || ''
      await apiClient.post(`/api/notifications/${id}/read`, {}, token)
      const notification = notifications.value.find(n => n.id === id)
      if (notification) {
        notification.is_read = true
        notification.read_at = new Date().toISOString()
      }
    } catch (err) {
      console.error('Error marking notification as read:', err)
    }
  }

  const markAllAsRead = async () => {
    try {
      const token = localStorage.getItem('access_token') || ''
      await apiClient.post('/api/notifications/read-all', {}, token)
      notifications.value.forEach(n => {
        n.is_read = true
        n.read_at = new Date().toISOString()
      })
    } catch (err) {
      console.error('Error marking all notifications as read:', err)
    }
  }

  return {
    notifications,
    loading,
    error,
    unreadCount,
    fetchNotifications,
    fetchUnreadCount,
    markAsRead,
    markAllAsRead
  }
})
