import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<any>(null)
  const token = ref(localStorage.getItem('auth_token'))
  
  const isAuthenticated = computed(() => !!token.value)
  
  const login = async (credentials: { email: string; password: string }) => {
    try {
      // Mock API call
      if (credentials.email === 'demo@devguardian.ai' && credentials.password === 'demo123') {
        const mockUser = {
          id: 1,
          name: 'Demo User',
          email: credentials.email,
          avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=32&h=32&fit=crop&crop=face'
        }
        
        const mockToken = 'mock_token_12345'
        
        user.value = mockUser
        token.value = mockToken
        
        localStorage.setItem('auth_token', mockToken)
        localStorage.setItem('user', JSON.stringify(mockUser))
        
        return { success: true }
      } else {
        return { success: false, error: 'Invalid credentials' }
      }
    } catch (error) {
      return { success: false, error: 'Login failed' }
    }
  }
  
  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
  }
  
  const initAuth = () => {
    const storedToken = localStorage.getItem('auth_token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
    }
  }
  
  return {
    user,
    token,
    isAuthenticated,
    login,
    logout,
    initAuth
  }
})
