import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, apiKeysApi, scannerApi } from '../services/api_new'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<any>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const plan = ref<string>('free')
  const scansUsed = ref(0)
  const scansQuota = ref(50)
  const isLoading = ref(false)
  
  const initAuthState = () => {
    const storedToken = localStorage.getItem('access_token')
    const storedRefresh = localStorage.getItem('refresh_token')
    const storedUser = localStorage.getItem('user')
    const storedPlan = localStorage.getItem('plan')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      refreshToken.value = storedRefresh
      try {
        user.value = JSON.parse(storedUser)
      } catch {
        user.value = null
      }
      plan.value = storedPlan || 'free'
    }
  }
  
  initAuthState()
  
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'super_admin' || user.value?.role === 'admin')
  
  const login = async (email: string, password: string) => {
    isLoading.value = true
    try {
      const response = await authApi.login(email, password)
      
      token.value = response.access_token
      refreshToken.value = response.refresh_token
      
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)
      
      // Get user info
      const userInfo = await authApi.me()
      user.value = userInfo
      localStorage.setItem('user', JSON.stringify(userInfo))
      
      // Get usage stats
      try {
        const usage = await apiKeysApi.getUsage()
        plan.value = usage.plan
        scansUsed.value = usage.scans_used
        scansQuota.value = usage.monthly_quota
        localStorage.setItem('plan', usage.plan)
      } catch (e) {
        console.error('Failed to get usage:', e)
      }
      
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message || 'Login failed' }
    } finally {
      isLoading.value = false
    }
  }
  
  const logout = async () => {
    user.value = null
    token.value = null
    refreshToken.value = null
    plan.value = 'free'
    scansUsed.value = 0
    scansQuota.value = 50
    
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    localStorage.removeItem('plan')
  }

  const register = async (name: string, email: string, password: string) => {
    isLoading.value = true
    try {
      const response = await authApi.register(name, email, password)
      
      // Auto login after register
      return await login(email, password)
    } catch (error: any) {
      return { success: false, error: error.message || 'Registration failed' }
    } finally {
      isLoading.value = false
    }
  }
  
  const refreshUsage = async () => {
    try {
      const usage = await apiKeysApi.getUsage()
      plan.value = usage.plan
      scansUsed.value = usage.scans_used
      scansQuota.value = usage.monthly_quota
      localStorage.setItem('plan', usage.plan)
    } catch (e) {
      console.error('Failed to refresh usage:', e)
    }
  }

  return {
    user,
    token,
    refreshToken,
    plan,
    scansUsed,
    scansQuota,
    isLoading,
    isAuthenticated,
    isAdmin,
    login,
    logout,
    register,
    refreshUsage,
    initAuthState
  }
})
