import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient } from '../services/api'

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
      const response = await apiClient.get<{ success: boolean; data: UserNotification[] }>('/v1/notifications')
      if (response.success && response.data) {
        notifications.value = response.data
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
      const response = await apiClient.get<{ success: boolean; data: { count: number } }>('/v1/notifications/unread')
      if (response.success && response.data) {
        return response.data.count
      }
      return 0
    } catch {
      return 0
    }
  }

  const markAsRead = async (id: number) => {
    try {
      const response = await apiClient.post<{ success: boolean }>(`/v1/notifications/${id}/read`)
      if (response.success) {
        const notification = notifications.value.find(n => n.id === id)
        if (notification) {
          notification.is_read = true
          notification.read_at = new Date().toISOString()
        }
      }
    } catch (err) {
      console.error('Error marking notification as read:', err)
    }
  }

  const markAllAsRead = async () => {
    try {
      const response = await apiClient.post<{ success: boolean }>('/v1/notifications/read-all')
      if (response.success) {
        notifications.value.forEach(n => {
          n.is_read = true
          n.read_at = new Date().toISOString()
        })
      }
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
