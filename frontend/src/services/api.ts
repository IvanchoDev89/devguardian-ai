import { useNotificationStore } from '../stores/notifications'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'
const AI_SERVICE_URL = import.meta.env.VITE_AI_SERVICE_URL || 'http://localhost:8000/api'

interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  errors?: Record<string, string[]>
}

class ApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message)
    this.name = 'ApiError'
  }
}

class ApiClient {
  private baseUrl: string
  private defaultHeaders: Record<string, string>

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  }

  private async request<T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    const token = localStorage.getItem('auth_token')
    
    const headers = {
      ...this.defaultHeaders,
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new ApiError(
          errorData.message || `HTTP ${response.status}: ${response.statusText}`,
          response.status
        )
      }

      return await response.json()
    } catch (error) {
      if (error instanceof ApiError) {
        throw error
      }
      throw new ApiError(error instanceof Error ? error.message : 'Network error')
    }
  }

  async get<T = any>(endpoint: string, params?: Record<string, any>): Promise<T> {
    const url = params ? `${endpoint}?${new URLSearchParams(params)}` : endpoint
    return this.request<T>(url)
  }

  async post<T = any>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  async put<T = any>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  async delete<T = any>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'DELETE'
    })
  }
}

// API Services
export const apiClient = new ApiClient(API_BASE_URL)
const aiServiceClient = new ApiClient(AI_SERVICE_URL)

// Auth Service
export const authService = {
  async login(credentials: { email: string; password: string }) {
    try {
      const response = await apiClient.post<ApiResponse<{ token: string; user: any }>>('/auth/login', credentials)
      
      if (response.success && response.data) {
        localStorage.setItem('auth_token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        return { success: true, user: response.data.user }
      } else {
        throw new ApiError(response.message || 'Login failed')
      }
    } catch (error) {
      const notificationStore = useNotificationStore()
      notificationStore.error('Login Failed', error instanceof Error ? error.message : 'Authentication failed')
      throw error
    }
  },

  async logout() {
    try {
      await apiClient.post('/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
    }
  },

  async register(userData: { name: string; email: string; password: string; company?: string }) {
    try {
      const response = await apiClient.post<ApiResponse<{ token: string; user: any }>>('/auth/register', userData)
      
      if (response.success && response.data) {
        localStorage.setItem('auth_token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        return { success: true, user: response.data.user }
      } else {
        throw new ApiError(response.message || 'Registration failed')
      }
    } catch (error) {
      const notificationStore = useNotificationStore()
      notificationStore.error('Registration Failed', error instanceof Error ? error.message : 'Registration failed')
      throw error
    }
  },

  async getProfile() {
    return apiClient.get<ApiResponse>('/auth/me')
  },

  async getGitHubAuthUrl() {
    const response = await apiClient.get<ApiResponse<{ url: string }>>('/auth/github')
    return response
  },

  async handleGitHubCallback(code: string, state: string) {
    const response = await apiClient.get<ApiResponse<{ token: string; user: any }>>(`/auth/github/callback?code=${code}&state=${state}`)
    
    if (response.success && response.data) {
      localStorage.setItem('auth_token', response.data.token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
      return { success: true, user: response.data.user }
    }
    throw new ApiError(response.message || 'GitHub login failed')
  }
}

// Dashboard Service
export const dashboardService = {
  async getStats() {
    return apiClient.get<ApiResponse>('/v1/dashboard/stats')
  },

  async getRecentScans() {
    return apiClient.get<ApiResponse>('/v1/dashboard/recent-scans')
  },

  async getVulnerabilities(params?: { page?: number; severity?: string; status?: string }) {
    return apiClient.get<ApiResponse>('/v1/dashboard/vulnerabilities', params)
  }
}

// Settings Service
export const settingsService = {
  async getSettings() {
    return apiClient.get<ApiResponse>('/v1/settings')
  },

  async updateSettings(settings: any) {
    return apiClient.put<ApiResponse>('/v1/settings', settings)
  },

  async updatePassword(data: { current_password: string; new_password: string; new_password_confirmation: string }) {
    return apiClient.post<ApiResponse>('/v1/settings/password', data)
  },

  async deleteAccount() {
    return apiClient.delete<ApiResponse>('/v1/settings')
  }
}

// Repository Service
export const repositoryService = {
  async getRepositories() {
    return apiClient.get<ApiResponse>('/repositories')
  },

  async addRepository(repoData: { url: string; name: string }) {
    return apiClient.post<ApiResponse>('/repositories', repoData)
  },

  async deleteRepository(id: string) {
    return apiClient.delete<ApiResponse>(`/repositories/${id}`)
  },

  async scanRepository(id: string) {
    return apiClient.post<ApiResponse>(`/repositories/${id}/scan`)
  }
}

// Vulnerability Service
export const vulnerabilityService = {
  async getVulnerabilities(params?: { page?: number; severity?: string; status?: string }) {
    return apiClient.get<ApiResponse>('/vulnerabilities', params)
  },

  async getVulnerability(id: string) {
    return apiClient.get<ApiResponse>(`/vulnerabilities/${id}`)
  },

  async updateVulnerability(id: string, data: { status?: string; notes?: string }) {
    return apiClient.put<ApiResponse>(`/vulnerabilities/${id}`, data)
  },

  async createFix(vulnerabilityId: string, fixData: { code: string; description: string }) {
    return apiClient.post<ApiResponse>(`/vulnerabilities/${vulnerabilityId}/fixes`, fixData)
  }
}

// AI Service
export const aiService = {
  async scanCode(code: string, options?: { scanType?: string; checkBlindSQL?: boolean }) {
    return aiServiceClient.post<ApiResponse>('/security/scan', { 
      code, 
      options: options || {} 
    })
  },

  async generateFix(vulnerabilityId: string, code: string) {
    return aiServiceClient.post<ApiResponse>('/ai/fix', {
      vulnerability_id: vulnerabilityId,
      code
    })
  },

  async analyzeCode(code: string) {
    return aiServiceClient.post<ApiResponse>('/code/analyze', { code })
  }
}
// Health check
export const healthApi = {
  async checkBackend() {
    return apiClient.get<ApiResponse>('/health')
  },

  async checkAiService() {
    return aiServiceClient.get<ApiResponse>('/health')
  }
}

// AI Fix Service
export const aiFixApi = {
  async getAiFixes() {
    return aiServiceClient.get<ApiResponse>('/ai-fixes')
  },

  async generateFixes(vulnerabilities: any[]) {
    return aiServiceClient.post<ApiResponse>('/ai-fixes/generate', { vulnerabilities })
  },

  async approveFix(fixId: string, approved: boolean, notes?: string) {
    return aiServiceClient.post<ApiResponse>(`/ai-fixes/${fixId}/approve`, { approved, notes })
  },

  async applyFix(fixId: string) {
    return aiServiceClient.post<ApiResponse>(`/ai-fixes/${fixId}/apply`)
  },

  async rejectFix(fixId: string, notes?: string) {
    return aiServiceClient.post<ApiResponse>(`/ai-fixes/${fixId}/reject`, { approved: false, notes })
  },

  async getFixDetails(fixId: string) {
    return aiServiceClient.get<ApiResponse>(`/ai-fixes/${fixId}`)
  },

  async deleteFix(fixId: string) {
    return aiServiceClient.delete<ApiResponse>(`/ai-fixes/${fixId}`)
  },

  async getFixStats() {
    return aiServiceClient.get<ApiResponse>('/ai-fixes/stats')
  },

  async generateFix(file: File, vulnerabilityType: string = 'general') {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('vulnerability_type', vulnerabilityType)
    
    try {
      const response = await fetch(`${AI_SERVICE_URL}/pytorch-scanner/scan/file`, {
        method: 'POST',
        body: formData,
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      return { data }
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Unknown error' }
    }
  }
}

// Advanced ML API
export const advancedMlApi = {
  async getCapabilities() {
    return aiServiceClient.get<ApiResponse>('/advanced-ml/ml-capabilities')
  },

  async runAdvancedScan(scanData: any) {
    return aiServiceClient.post<ApiResponse>('/advanced-ml/advanced-scan', scanData)
  },

  async getModelPerformance() {
    return aiServiceClient.get<ApiResponse>('/advanced-ml/model-performance')
  },

  async trainModel(trainingData: any) {
    return aiServiceClient.post<ApiResponse>('/advanced-ml/train-model', trainingData)
  },

  async getTrainingStatus(trainingId: string) {
    return aiServiceClient.get<ApiResponse>(`/advanced-ml/training-status/${trainingId}`)
  }
}

// Automation API
export const automationApi = {
  async getWorkflows() {
    return aiServiceClient.get<ApiResponse>('/advanced-ml/workflows')
  },

  async createWorkflow(workflowData: any) {
    return aiServiceClient.post<ApiResponse>('/advanced-ml/setup-workflow', workflowData)
  },

  async triggerWorkflow(workflowId: string, data?: any) {
    return aiServiceClient.post<ApiResponse>(`/advanced-ml/trigger-workflow/${workflowId}`, data || {})
  },

  async deleteWorkflow(workflowId: string) {
    return aiServiceClient.delete<ApiResponse>(`/advanced-ml/workflows/${workflowId}`)
  },

  async getWorkflowStats() {
    return aiServiceClient.get<ApiResponse>('/advanced-ml/workflow-stats')
  }
}

// Security Audit API
export const securityAuditApi = {
  async runAudit(auditConfig: any) {
    return aiServiceClient.post<ApiResponse>('/security-audit/run', auditConfig)
  },

  async getAuditResults(auditId: string) {
    return aiServiceClient.get<ApiResponse>(`/security-audit/results/${auditId}`)
  },

  async getAuditHistory() {
    return aiServiceClient.get<ApiResponse>('/security-audit/history')
  },

  async exportReport(auditId: string, format: string) {
    return aiServiceClient.get<ApiResponse>(`/security-audit/export/${auditId}?format=${format}`)
  },

  async getSecurityMetrics() {
    return aiServiceClient.get<ApiResponse>('/security-audit/metrics')
  }
}

// Unified API service for easy access
export const apiService = {
  // Backend APIs
  get: apiClient.get,
  post: apiClient.post,
  put: apiClient.put,
  delete: apiClient.delete,
  
  // AI Service APIs
  aiGet: aiServiceClient.get,
  aiPost: aiServiceClient.post,
  aiDelete: aiServiceClient.delete,
  
  // Specific APIs
  repository: repositoryService,
  vulnerability: vulnerabilityService,
  aiFix: aiFixApi,
  health: healthApi,
  advancedMl: advancedMlApi,
  automation: automationApi,
  securityAudit: securityAuditApi
}

// Super Admin API
export const superAdminApi = {
  async getDashboard(timeRange: string = '24h') {
    return apiClient.get<ApiResponse>(`/v1/admin/dashboard`, { range: timeRange })
  },

  async runSystemScan(scanType: string, target: string) {
    return apiClient.post<ApiResponse>('/v1/admin/system-scan', { scan_type: scanType, target })
  },

  async getAuditLogs(limit: number = 100, offset: number = 0) {
    return apiClient.get<ApiResponse>('/v1/admin/audit-logs', { limit, offset })
  },

  async manageUsers(action: string, userData?: any) {
    return apiClient.post<ApiResponse>('/v1/admin/users', { action, ...userData })
  },

  async generateReport(type: string, dateFrom: string, dateTo: string, format: string) {
    return apiClient.post<ApiResponse>('/v1/admin/generate-report', {
      type,
      date_from: dateFrom,
      date_to: dateTo,
      format
    })
  }
}

// Pentesting API
export const pentestApi = {
  async startScan(scanConfig: {
    target: string
    target_type: string
    auth_type?: string
    credentials?: string
    intensity?: string
    use_zero_day_detection?: boolean
    exploitability_analysis?: boolean
    generate_poc?: boolean
  }) {
    try {
      const data = await aiServiceClient.post('/pentest/start-scan', scanConfig)
      return { success: true, data }
    } catch (err) {
      return { success: false, message: 'Failed to start scan', data: null }
    }
  },

  async getScanStatus(scanId: string) {
    try {
      const data = await aiServiceClient.get(`/pentest/scan/${scanId}`)
      return { success: true, data }
    } catch (err) {
      return { success: false, message: 'Failed to get scan status', data: null }
    }
  },

  async getScanFindings(scanId: string) {
    try {
      const data = await aiServiceClient.get(`/pentest/scan/${scanId}/findings`)
      return { success: true, data }
    } catch (err) {
      return { success: false, message: 'Failed to get findings', data: null }
    }
  },

  async listScans() {
    try {
      const data = await aiServiceClient.get('/pentest/scans')
      return { success: true, data }
    } catch (err) {
      return { success: false, message: 'Failed to list scans', data: [] }
    }
  },

  async stopScan(scanId: string) {
    try {
      const data = await aiServiceClient.post(`/pentest/scan/${scanId}/stop`, {})
      return { success: true, data }
    } catch (err) {
      return { success: false, message: 'Failed to stop scan', data: null }
    }
  },

  async getZeroDayThreats() {
    try {
      const data = await aiServiceClient.get('/pentest/zero-day-threats')
      return { success: true, data }
    } catch (err) {
      return { success: false, message: 'Failed to get threats', data: null }
    }
  }
}

// Billing Service
export const billingService = {
  async getSubscription() {
    return apiClient.get('/billing/subscription')
  },

  async createCheckout(planId: string) {
    return apiClient.post('/billing/checkout', { plan_id: planId })
  },

  async changePlan(planId: string) {
    return apiClient.post('/billing/change-plan', { plan_id: planId })
  },

  async cancelSubscription() {
    return apiClient.post('/billing/cancel')
  },

  async getInvoices() {
    return apiClient.get('/billing/invoices')
  },

  async getPaymentMethods() {
    return apiClient.get('/billing/payment-methods')
  },

  async addPaymentMethod(paymentMethodId: string) {
    return apiClient.post('/billing/payment-methods', { payment_method_id: paymentMethodId })
  }
}
