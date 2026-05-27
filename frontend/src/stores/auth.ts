import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const logger = {
  warn: (msg: string, ...args: any[]) => console.warn(`[Auth] ${msg}`, ...args),
  error: (msg: string, ...args: any[]) => console.error(`[Auth] ${msg}`, ...args),
}

export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  role?: string
  is_superuser?: boolean
  is_active?: boolean
  created_at?: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const isLoading = ref(false)
  const plan = ref<string>('free')
  const scansUsed = ref(0)
  const scansQuota = ref(50)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_superuser === true)

  async function login(email: string, password: string) {
    isLoading.value = true
    try {
      const formData = new URLSearchParams()
      formData.append('username', email)
      formData.append('password', password)

      const response = await fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Login failed')
      }

      const data = await response.json()
      token.value = data.access_token
      refreshToken.value = data.refresh_token

      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('dev_refresh_token', data.refresh_token)

      await fetchUser()
      return { success: true }
    } catch (error: any) {
      return { success: false, message: error.message }
    } finally {
      isLoading.value = false
    }
  }

  async function register(name: string, email: string, password: string) {
    isLoading.value = true
    try {
      const response = await fetch(`${API_BASE}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          email, 
          username: email.split('@')[0], 
          password, 
          full_name: name 
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Registration failed')
      }

      // After registration, try to auto-login
      // Note: User needs to verify email first in production
      return await login(email, password)
    } catch (error: any) {
      return { success: false, message: error.message }
    } finally {
      isLoading.value = false
    }
  }

  async function refreshAccessToken() {
    if (!refreshToken.value) return false
    
    try {
      const response = await fetch(`${API_BASE}/api/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken.value }),
      })

      if (!response.ok) {
        logout()
        return false
      }

      const data = await response.json()
      token.value = data.access_token
      refreshToken.value = data.refresh_token
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('dev_refresh_token', data.refresh_token)
      return true
    } catch {
      logout()
      return false
    }
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      const response = await fetch(`${API_BASE}/api/auth/me`, {
        headers: { Authorization: `Bearer ${token.value}` },
      })
      if (response.ok) {
        const userData = await response.json()
        user.value = userData
        localStorage.setItem('user', JSON.stringify(userData))
      } else if (response.status === 401) {
        // Try to refresh token
        const refreshed = await refreshAccessToken()
        if (refreshed) {
          await fetchUser()
        }
      }
    } catch {
      // Silent fail
    }
  }

  async function logout() {
    if (refreshToken.value) {
      try {
        const response = await fetch(`${API_BASE}/api/auth/logout`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token.value}`
          },
          body: JSON.stringify({ refresh_token: refreshToken.value }),
        })
        
        if (!response.ok) {
          logger.warn('Logout request failed, clearing local state anyway')
        }
      } catch (err) {
        logger.warn('Logout request error, clearing local state:', err)
      }
    }
    
    user.value = null
    token.value = null
    refreshToken.value = null
    plan.value = 'free'
    scansUsed.value = 0
    scansQuota.value = 50
    localStorage.removeItem('user')
    localStorage.removeItem('plan')
    localStorage.removeItem('access_token')
    localStorage.removeItem('dev_refresh_token')
  }

  async function initAuthState() {
    const storedRefresh = localStorage.getItem('dev_refresh_token')
    const storedToken = localStorage.getItem('access_token')
    
    if (storedRefresh) {
      refreshToken.value = storedRefresh
      const success = await refreshAccessToken()
      if (!success) {
        refreshToken.value = null
        token.value = null
        localStorage.removeItem('dev_refresh_token')
        localStorage.removeItem('access_token')
        return
      }
    }
    
    if (storedToken && token.value) {
      if (!user.value) {
        await fetchUser()
      }
    }
  }

  function incrementScans() {
    scansUsed.value++
  }

  return {
    user,
    token,
    refreshToken,
    isLoading,
    plan,
    scansUsed,
    scansQuota,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    fetchUser,
    refreshAccessToken,
    initAuthState,
    incrementScans
  }
})
