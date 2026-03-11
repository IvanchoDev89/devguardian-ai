const API_BASE_URL = ''

interface ApiResponse<T = any> {
  data?: T
  message?: string
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

  private getToken(): string | null {
    return localStorage.getItem('access_token')
  }

  private async request<T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    const token = this.getToken()
    
    const headers = {
      ...this.defaultHeaders,
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
        credentials: 'include'
      })

      const data = await response.json().catch(() => ({}))

      if (!response.ok) {
        throw new Error(data.detail || data.message || `HTTP ${response.status}`)
      }

      return data
    } catch (error: any) {
      if (error.message && !error.message.includes('Failed to fetch')) {
        throw error
      }
      // Network error - throw a more descriptive error
      throw new Error(`Cannot connect to server at ${this.baseUrl}. Is the backend running?`)
    }
  }

  get<T = any>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint)
  }

  post<T = any>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  put<T = any>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  delete<T = any>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'DELETE'
    })
  }
}

export const api = new ApiClient(API_BASE_URL)

// Auth API
export const authApi = {
  login: (email: string, password: string) => 
    api.post<{ access_token: string; refresh_token: string }>('/api/auth/login', { email, password }),
  
  register: (name: string, email: string, password: string) =>
    api.post<{ user_id: string; email: string; name: string; role: string }>('/api/auth/register', { name, email, password }),
  
  me: () => api.get<{ user_id: string; email: string; name: string; role: string }>('/api/auth/me'),
  
  refresh: (refreshToken: string) => 
    api.post<{ access_token: string; refresh_token: string }>('/api/auth/refresh', refreshToken)
}

// API Keys API
export const apiKeysApi = {
  list: () => api.get<any[]>('/api/keys'),
  
  create: (name: string, plan: string = 'free', expiresDays?: number) =>
    api.post<any>('/api/keys', { name, plan, expires_days: expiresDays }),
  
  delete: (keyId: string) => api.delete(`/api/keys/${keyId}`),
  
  revoke: (keyId: string) => api.post(`/api/keys/${keyId}/revoke`),
  
  getUsage: () => api.get<any>('/api/keys/usage/stats')
}

// Reports API
export const reportsApi = {
  generate: (scanId: string, vulnerabilities: any[], score: number, language: string, format: string = 'pdf') =>
    api.post('/api/reports/generate', { scan_id: scanId, vulnerabilities, score, language, format })
}

// Webhooks API
export const webhooksApi = {
  list: () => api.get<any[]>('/api/webhooks'),
  
  create: (url: string, events: string[], name: string) =>
    api.post<any>('/api/webhooks', { url, events, name }),
  
  delete: (webhookId: string) => api.delete(`/api/webhooks/${webhookId}`),
  
  test: (webhookId: string) => api.post(`/api/webhooks/${webhookId}/test`)
}

// Teams API
export const teamsApi = {
  list: () => api.get<any[]>('/api/teams/teams'),
  
  create: (name: string, plan: string = 'free') =>
    api.post<any>('/api/teams/teams', { name, plan }),
  
  get: (teamId: string) => api.get<any>(`/api/teams/teams/${teamId}`),
  
  invite: (teamId: string, email: string, role: string = 'member') =>
    api.post(`/api/teams/teams/${teamId}/invite`, { email, role }),
  
  removeMember: (teamId: string, memberId: string) => 
    api.delete(`/api/teams/teams/${teamId}/members/${memberId}`),
  
  getUsage: (teamId: string) => api.get<any>(`/api/teams/teams/${teamId}/usage`)
}

// Scanner API
export const scannerApi = {
  analyze: (code: string, language: string) =>
    api.post<any>('/api/v1/analyze-code', { code, language }),
  
  health: () => api.get<any>('/health'),
  
  getScans: (limit: number = 20) => api.get<any>(`/api/v1/scans?limit=${limit}`),
  
  getScanDetails: (scanId: string) => api.get<any>(`/api/v1/scans/${scanId}`),
  
  getAdminStats: () => api.get<any>('/api/v1/admin/stats'),
  
  // Repository Scanner
  scanRepo: (repoUrl: string, provider?: string, branch?: string) =>
    api.post<any>('/api/v1/repos/scan', { 
      repo_url: repoUrl, 
      provider, 
      branch: branch || 'main' 
    }),
  
  getRepoProviders: () => api.get<any>('/api/v1/repos/providers'),
  
  getRepoScanResults: (scanId: string) => api.get<any>(`/api/v1/repos/scan/${scanId}`)
}

// LLM Analyzer API  
export const llmApi = {
  analyze: (vulnerability: any, codeSnippet: string, language: string, generateFix: boolean = true) =>
    api.post<any>('/api/llm/analyze', {
      vulnerability,
      code_snippet: codeSnippet,
      language,
      generate_fix: generateFix
    })
}

// Audit API
export const auditApi = {
  getLogs: (limit: number = 50) => api.get<any>(`/api/auth/audit?limit=${limit}`),
  getSuspicious: () => api.get<any>('/api/auth/audit/suspicious')
}

// GitHub Integration API
export const githubApi = {
  list: () => api.get<any[]>('/api/github/integrations'),
  create: (data: any) => api.post<any>('/api/github/integrations', data),
  delete: (id: string) => api.delete(`/api/github/integrations/${id}`)
}
