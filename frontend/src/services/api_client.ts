const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function getToken(): string | null {
  return localStorage.getItem('access_token')
}

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    method: string,
    endpoint: string,
    data?: any,
    token?: string
  ): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    const authToken = token || getToken()
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`
    }

    const options: RequestInit = {
      method,
      headers,
    }

    if (data && method !== 'GET') {
      options.body = JSON.stringify(data)
    }

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, options)

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }))
        throw new Error(error.detail || `HTTP ${response.status}`)
      }

      return response.json()
    } catch (e) {
      console.error(`API call to ${endpoint} failed:`, e)
      throw e
    }
  }

  async get<T>(endpoint: string, token?: string): Promise<T> {
    return this.request<T>('GET', endpoint, undefined, token)
  }

  async post<T>(endpoint: string, data: any, token?: string): Promise<T> {
    return this.request<T>('POST', endpoint, data, token)
  }

  async put<T>(endpoint: string, data: any, token?: string): Promise<T> {
    return this.request<T>('PUT', endpoint, data, token)
  }

  async delete<T>(endpoint: string, token?: string): Promise<T> {
    return this.request<T>('DELETE', endpoint, undefined, token)
  }
}

export const api = new ApiClient()

// Auth API
export const authApi = {
  register: async (data: { email: string; username: string; password: string; full_name?: string }) => {
    return api.post<{ email: string; username: string; id: number }>('/api/auth/register', data)
  },

  login: async (email: string, password: string) => {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    })
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Login failed' }))
      throw new Error(error.detail || 'Login failed')
    }
    
    const data = await response.json()
    
    if (!data.access_token) {
      throw new Error('Invalid response from server')
    }
    
    return data
  },

  logout: async (token: string) => api.post('/api/auth/logout', {}, token),
  
  refresh: async (refreshToken: string) => api.post('/api/auth/refresh', { refresh_token: refreshToken }),
  
  getMe: (token: string) => api.get<{ id: number; email: string; username: string; full_name?: string }>('/api/auth/me', token),
  
  requestPasswordReset: (email: string) => api.post('/api/auth/request-password-reset', { email }),
  
  resetPassword: (token: string, newPassword: string) => api.post('/api/auth/reset-password', { token, new_password: newPassword }),
}

// Vulnerabilities API
export const vulnApi = {
  list: (token: string, params?: { skip?: number; limit?: number; severity?: string; status?: string }) => {
    const query = new URLSearchParams()
    if (params?.skip) query.append('skip', params.skip.toString())
    if (params?.limit) query.append('limit', params.limit.toString())
    if (params?.severity) query.append('severity', params.severity)
    if (params?.status) query.append('status', params.status)
    return api.get<any[]>(`/api/vulnerabilities?${query}`, token)
  },

  create: (token: string, data: any) => api.post<any>('/api/vulnerabilities', data, token),
  
  get: (token: string, id: number) => api.get<any>(`/api/vulnerabilities/${id}`, token),
  
  update: (token: string, id: number, data: any) => api.put<any>(`/api/vulnerabilities/${id}`, data, token),
  
  delete: (token: string, id: number) => api.delete<any>(`/api/vulnerabilities/${id}`, token),
  
  getStats: (token: string) => api.get<any>('/api/vulnerabilities/stats/summary', token),
}

// Scans API
export const scansApi = {
  list: (token: string, params?: { skip?: number; limit?: number; status?: string; scan_type?: string }) => {
    const query = new URLSearchParams()
    if (params?.skip) query.append('skip', params.skip.toString())
    if (params?.limit) query.append('limit', params.limit.toString())
    if (params?.status) query.append('status', params.status)
    if (params?.scan_type) query.append('scan_type', params.scan_type)
    return api.get<any[]>(`/api/scans?${query}`, token)
  },

  create: (token: string, data: { name: string; scan_type: string; target?: string }) => 
    api.post<any>('/api/scans', data, token),
  
  get: (token: string, id: number) => api.get<any>(`/api/scans/${id}`, token),
  
  update: (token: string, id: number, data: any) => 
    api.put<any>(`/api/scans/${id}`, data, token),
  
  delete: (token: string, id: number) => api.delete<any>(`/api/scans/${id}`, token),
  
  getStats: (token: string) => api.get<any>('/api/scans/stats/summary', token),

  run: (token: string, data: { scan_type: string; target: string; options?: any }) => 
    api.post<any>('/api/scans/run', data, token),

  scanCode: (token: string, data: { code: string; language: string; filename?: string }) =>
    api.post<any>('/api/scans/scan-code', data, token),
}

// Health check
export const healthApi = {
  check: () => api.get<{ status: string }>('/health'),
}

// Settings API (placeholder)
export const settingsApi = {
  get: (token: string) => api.get<any>('/api/users/me/settings', token),
  update: (token: string, data: any) => api.put<any>('/api/users/me/settings', data, token),
}

// Notifications API (placeholder)
export const notificationsApi = {
  list: (token: string) => api.get<any[]>('/api/notifications', token),
  markRead: (token: string, id: number) => api.post(`/api/notifications/${id}/read`, {}, token),
  delete: (token: string, id: number) => api.delete(`/api/notifications/${id}`, token),
}

// Messages API (placeholder)
export const messagesApi = {
  list: (token: string) => api.get<any[]>('/api/messages', token),
  send: (token: string, data: any) => api.post('/api/messages', data, token),
  delete: (token: string, id: number) => api.delete(`/api/messages/${id}`, token),
}

// Billing API (placeholder)
export const billingApi = {
  getSubscription: (token: string) => api.get<any>('/api/billing/subscription', token),
  createCheckout: (token: string, planId: string) => api.post('/api/billing/checkout', { plan_id: planId }, token),
  getInvoices: (token: string) => api.get<any[]>('/api/billing/invoices', token),
}

// Assets API (placeholder)
export const assetsApi = {
  list: (token: string) => api.get<any[]>('/api/assets', token),
  create: (token: string, data: any) => api.post('/api/assets', data, token),
  update: (token: string, id: number, data: any) => api.put(`/api/assets/${id}`, data, token),
  delete: (token: string, id: number) => api.delete(`/api/assets/${id}`, token),
}

// Admin API
export const adminApi = {
  getStats: (token: string) => api.get<any>('/api/admin/stats', token),
  getUsers: (token: string) => api.get<any[]>('/api/admin/users', token),
  updateUser: (token: string, id: number, data: any) => api.put(`/api/admin/users/${id}`, data, token),
}

// Repository API (maps to real /api/scans endpoints)
export const repoApi = {
  list: (token: string) => api.get<any[]>('/api/scans', token),
  add: (token: string, data: any) => api.post('/api/scans/run', data, token),
  scan: (token: string, id: number) => api.post(`/api/scans/run`, { scan_type: 'all', target: `scan_${id}` }, token),
  delete: (token: string, id: number) => api.delete(`/api/scans/${id}`, token),
  scanRepo: (token: string, repoUrl: string, provider?: string, branch?: string) =>
    api.post('/api/scans/run', { scan_type: 'all', target: repoUrl, options: { provider, branch } }, token),
  getResults: (token: string, scanId: string) => api.get(`/api/scans/${scanId}`, token),
  getRepoScanResults: (token: string, scanId: string) => api.get(`/api/scans/${scanId}`, token),
}

// AI Fixes API
export const aiFixApi = {
  list: (token: string) => api.get<any[]>('/api/ai-fixes', token),
  getAiFixes: (token: string) => api.get<any[]>('/api/vulnerabilities?ai_fixed=true', token),
  approve: (token: string, id: number) => api.post(`/api/vulnerabilities/${id}/approve`, {}, token),
  reject: (token: string, id: number) => api.post(`/api/vulnerabilities/${id}/reject`, {}, token),
  applyFix: (token: string, id: number) => api.post(`/api/vulnerabilities/${id}/apply-fix`, {}, token),
}

// Pentest API
export const pentestApi = {
  startScan: (token: string, data: any) => api.post('/api/scans/run', data, token),
  getStatus: (token: string, scanId: string) => api.get(`/api/scans/${scanId}`, token),
  getFindings: (token: string, scanId: string) => api.get(`/api/vulnerabilities?scan_id=${scanId}`, token),
  stopScan: (token: string, scanId: string) => api.put(`/api/scans/${scanId}`, { status: 'stopped' }, token),
  getScanStatus: (token: string, scanId: string) => api.get(`/api/scans/${scanId}`, token),
  getScanFindings: (token: string, scanId: string) => api.get(`/api/vulnerabilities?scan_id=${scanId}`, token),
  getZeroDayThreats: (token: string, scanId: string) => api.get(`/api/vulnerabilities?type=zero_day&scan_id=${scanId}`, token),
}

// Scanner API (maps to real /api/scans endpoints)
export const scannerApi = {
  analyze: (token: string, code: string, language: string) => 
    api.post('/api/scans/scan-code', { code, language }, token),
  scanRepo: (token: string, repoUrl: string, provider?: string, branch?: string) =>
    api.post('/api/scans/run', { scan_type: 'all', target: repoUrl, options: { provider, branch } }, token),
  getResults: (token: string, scanId: string) => api.get(`/api/scans/${scanId}`, token),
  getZeroDayThreats: (token: string, scanId: string) => api.get(`/api/vulnerabilities?scan_id=${scanId}&type=zero_day`, token),
  getRepoScanResults: (token: string, scanId: string) => api.get(`/api/scans/${scanId}`, token),
}

// Super Admin API
export const superAdminApi = {
  getStats: (token: string) => api.get<any>('/api/admin/stats', token),
  getUsers: (token: string) => api.get<any[]>('/api/admin/users', token),
  updateUser: (token: string, id: number, data: any) => api.put(`/api/admin/users/${id}`, data, token),
  fetchAuditLogs: (token: string, params?: any) => api.get<any[]>('/api/admin/audit-logs', token),
}

// AI Service API
export const aiService = {
  analyze: (token: string, code: string, language: string) => 
    api.post('/api/scanner/analyze', { code, language }, token),
  getZeroDayThreats: (token: string) => api.get('/api/vulnerabilities?type=zero_day', token),
  scanDependencies: (token: string, target: string) => 
    api.post('/api/scans/run', { scan_type: 'dependencies', target }, token),
}

// Pricing API
export const pricingApi = {
  list: () => api.get<any[]>('/api/users/me/settings'),
  getCurrent: (token: string) => api.get<any>('/api/users/me', token),
}



// Asset Service API (placeholder — backend endpoints not yet implemented)
export const assetService = {
  list: (token: string) => api.get<any[]>('/api/assets', token),
  create: (token: string, data: any) => api.post('/api/assets', data, token),
  update: (token: string, id: number, data: any) => api.put(`/api/assets/${id}`, data, token),
  delete: (token: string, id: number) => api.delete(`/api/assets/${id}`, token),
}

// Message Service API (placeholder — backend endpoints not yet implemented)
export const messageService = {
  list: (token: string) => api.get<any[]>('/api/messages', token),
  send: (token: string, data: any) => api.post('/api/messages', data, token),
  delete: (token: string, id: number) => api.delete(`/api/messages/${id}`, token),
}

// API Client service for legacy compatibility
export const apiClient = api

// apiService alias for backwards compatibility
export const apiService = {
  ...scansApi,
  ...vulnApi,
}