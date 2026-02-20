import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  action?: string
  duration?: number
  timestamp: number
}

export const useNotificationStore = defineStore('notifications', () => {
  const notifications = ref<Notification[]>([])

  const addNotification = (notification: Omit<Notification, 'id' | 'timestamp'>) => {
    const id = Date.now().toString()
    const timestamp = Date.now()
    
    const newNotification: Notification = {
      id,
      timestamp,
      ...notification
    }
    
    notifications.value.unshift(newNotification)
    
    // Auto-remove after duration
    if (notification.duration && notification.duration > 0) {
      setTimeout(() => {
        removeNotification(id)
      }, notification.duration)
    }
  }

  const removeNotification = (id: string) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const clearAll = () => {
    notifications.value = []
  }

  // Convenience methods
  const success = (title: string, message: string, options?: Partial<Notification>) => {
    addNotification({ type: 'success', title, message, ...options })
  }

  const error = (title: string, message: string, options?: Partial<Notification>) => {
    addNotification({ type: 'error', title, message, duration: 5000, ...options })
  }

  const warning = (title: string, message: string, options?: Partial<Notification>) => {
    addNotification({ type: 'warning', title, message, duration: 4000, ...options })
  }

  const info = (title: string, message: string, options?: Partial<Notification>) => {
    addNotification({ type: 'info', title, message, duration: 3000, ...options })
  }

  return {
    notifications,
    addNotification,
    removeNotification,
    clearAll,
    success,
    error,
    warning,
    info
  }
})
