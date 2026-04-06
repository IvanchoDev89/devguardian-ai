const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002'

interface ApiResponse<T> {
  data: T | null
  success: boolean
  message?: string
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

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const options: RequestInit = {
      method,
      headers,
    }

    if (data && method !== 'GET') {
      options.body = JSON.stringify(data)
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, options)

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }

    return response.json()
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
    
    if (!response.ok) throw new Error('Login failed')
    return response.json()
  },

  getMe: (token: string) => api.get<{ id: number; email: string; username: string }>('/api/auth/me', token),
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

// Health check
export const healthApi = {
  check: () => api.get<{ status: string }>('/health'),
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
}
