import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Mock users for MVP demo (no backend required)
const MOCK_USERS = [
  { email: 'admin@devguardian.ai', password: 'admin123', name: 'Admin User', role: 'super_admin', plan: 'enterprise' },
  { email: 'demo@devguardian.ai', password: 'demo123', name: 'Demo User', role: 'free', plan: 'free' },
]

export const useAuthStore = defineStore('auth', () => {
  const user = ref<any>(null)
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const plan = ref<string>('free')
  const scansUsed = ref(0)
  
  // Initialize auth state immediately
  const initAuthState = () => {
    const storedToken = localStorage.getItem('auth_token')
    const storedUser = localStorage.getItem('user')
    const storedPlan = localStorage.getItem('plan')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      try {
        user.value = JSON.parse(storedUser)
      } catch {
        user.value = null
      }
      plan.value = storedPlan || 'free'
    }
  }
  
  // Initialize immediately
  initAuthState()
  
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'super_admin' || user.value?.role === 'admin')
  const canScan = computed(() => {
    if (plan.value === 'free') {
      return scansUsed.value < 3 // Allow 3 scans for demo
    }
    return true
  })
  
  const login = async (credentials: { email: string; password: string }) => {
    // Mock authentication for MVP
    const mockUser = MOCK_USERS.find(
      u => u.email === credentials.email && u.password === credentials.password
    )
    
    if (mockUser) {
      const mockToken = `mock_token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      
      user.value = {
        id: 1,
        name: mockUser.name,
        email: mockUser.email,
        role: mockUser.role,
        plan: mockUser.plan
      }
      token.value = mockToken
      plan.value = mockUser.plan
      scansUsed.value = 0
      
      localStorage.setItem('auth_token', mockToken)
      localStorage.setItem('user', JSON.stringify(user.value))
      localStorage.setItem('plan', plan.value)
      
      return { success: true }
    }
    
    // Also allow any login for demo purposes
    if (credentials.email && credentials.password) {
      const mockToken = `demo_token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      
      user.value = {
        id: 1,
        name: credentials.email.split('@')[0],
        email: credentials.email,
        role: 'free',
        plan: 'free'
      }
      token.value = mockToken
      plan.value = 'free'
      scansUsed.value = 0
      
      localStorage.setItem('auth_token', mockToken)
      localStorage.setItem('user', JSON.stringify(user.value))
      localStorage.setItem('plan', plan.value)
      
      return { success: true }
    }
    
    return { success: false, error: 'Invalid credentials' }
  }
  
  const logout = async () => {
    user.value = null
    token.value = null
    plan.value = 'free'
    scansUsed.value = 0
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
    localStorage.removeItem('plan')
  }

  const register = async (userData: { name: string; email: string; password: string }) => {
    // Mock registration for MVP
    const mockToken = `demo_token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    user.value = {
      id: Date.now(),
      name: userData.name,
      email: userData.email,
      role: 'free',
      plan: 'free'
    }
    token.value = mockToken
    plan.value = 'free'
    
    localStorage.setItem('auth_token', mockToken)
    localStorage.setItem('user', JSON.stringify(user.value))
    localStorage.setItem('plan', plan.value)
    
    return { success: true }
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
