import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient } from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<any>(null)
  const token = ref(localStorage.getItem('auth_token'))
  const plan = ref<string>('free')
  const scansUsed = ref(0)
  
  // Initialize auth state immediately
  const initAuthState = () => {
    const storedToken = localStorage.getItem('auth_token')
    const storedUser = localStorage.getItem('user')
    const storedPlan = localStorage.getItem('plan')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
      plan.value = storedPlan || 'free'
    }
  }
  
  // Initialize immediately
  initAuthState()
  
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'super_admin')
  const canScan = computed(() => {
    if (plan.value === 'free') {
      return scansUsed.value < 1
    }
    return true // Pro/Enterprise have unlimited scans
  })
  
  const login = async (credentials: { email: string; password: string }) => {
    try {
      const response = await apiClient.post<any>('/auth/login', credentials)
      
      if (response.success && response.data) {
        user.value = response.data.user
        token.value = response.data.token
        plan.value = response.data.user?.plan || 'free'
        scansUsed.value = response.data.user?.scans_used || 0
        
        localStorage.setItem('auth_token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        localStorage.setItem('plan', plan.value)
        
        return { success: true }
      } else {
        return { success: false, error: response.message || 'Invalid credentials' }
      }
    } catch (error: any) {
      return { success: false, error: error.message || 'Login failed' }
    }
  }
  
  const logout = async () => {
    try {
      await apiClient.post('/auth/logout')
    } catch (error) {
      // Ignore logout API errors
    } finally {
      user.value = null
      token.value = null
      plan.value = 'free'
      scansUsed.value = 0
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
      localStorage.removeItem('plan')
    }
  }

  const register = async (userData: { name: string; email: string; password: string }) => {
    try {
      const response = await apiClient.post<any>('/auth/register', userData)
      
      if (response.success && response.data) {
        user.value = response.data.user
        token.value = response.data.token
        plan.value = response.data.user?.plan || 'free'
        
        localStorage.setItem('auth_token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        localStorage.setItem('plan', plan.value)
        
        return { success: true }
      } else {
        return { success: false, error: response.message || 'Registration failed' }
      }
    } catch (error: any) {
      return { success: false, error: error.message || 'Registration failed' }
    }
  }
  
  const initAuth = () => {
    initAuthState()
  }
  
  const incrementScans = () => {
    scansUsed.value++
  }
  
  const resetScans = () => {
    scansUsed.value = 0
  }
  
  return {
    user,
    token,
    plan,
    scansUsed,
    isAuthenticated,
    isAdmin,
    canScan,
    login,
    register,
    logout,
    initAuth,
    incrementScans,
    resetScans
  }
})
