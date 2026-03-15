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

// Vulnerabilities API
export const vulnerabilitiesApi = {
  list: () => api.get<any[]>('/api/v1/vulnerabilities'),
  
  get: (id: number) => api.get<any>(`/api/v1/vulnerabilities/${id}`),
  
  update: (id: number, data: any) => api.put<any>(`/api/v1/vulnerabilities/${id}`, data),
  
  getStats: () => api.get<any>('/api/v1/vulnerabilities/stats/summary')
}

// CI/CD Integration API
export const cicdApi = {
  scanPR: (data: {
    repository_url: string
    pr_number: number
    commit_sha: string
    branch: string
    base_branch: string
    files_changed: string[]
    author: string
    github_token?: string
  }, policyId?: string) => 
    api.post<any>(`/api/cicd/scan/pr?policy_id=${policyId || 'default'}`, data),
  
  scanPreCommit: (data: {
    commit_sha: string
    branch: string
    files_changed: string[]
    repository_url: string
  }) => api.post<any>('/api/cicd/scan/pre-commit', data),
  
  getScanResult: (scanId: string) => api.get<any>(`/api/cicd/scan/${scanId}`),
  
  listPolicies: () => api.get<any[]>('/api/cicd/policies'),
  
  togglePolicy: (policyId: string, enabled: boolean) => 
    api.post<any>(`/api/cicd/policies/${policyId}/toggle`, { enabled }),
  
  createPolicy: (policy: any) => api.post<any>('/api/cicd/policies', policy),
  
  getStatus: () => api.get<any>('/api/cicd/status')
}

// Notifications API
export const notificationsApi = {
  getStatus: () => api.get<any>('/api/notifications/status'),
  
  configureSlack: (config: { webhook_url: string; channel?: string; mention_on_critical?: boolean }) =>
    api.post<any>('/api/notifications/slack/configure', config),
  
  configureDiscord: (config: { webhook_url: string }) =>
    api.post<any>('/api/notifications/discord/configure', config),
  
  configureJira: (config: { 
    jira_url: string; email: string; api_token: string; 
    project_key: string; issue_type?: string 
  }) => api.post<any>('/api/notifications/jira/configure', config),
  
  send: (notification: {
    title: string
    message: string
    severity: string
    findings?: any[]
    scan_id?: string
    repository?: string
  }) => api.post<any>('/api/notifications/send', notification),
  
  createJiraTicket: (ticket: {
    title: string
    description: string
    severity: string
    labels?: string[]
  }) => api.post<any>('/api/notifications/jira/ticket', ticket),
  
  removeSlack: () => api.delete<any>('/api/notifications/slack'),
  
  removeDiscord: () => api.delete<any>('/api/notifications/discord'),
  
  removeJira: () => api.delete<any>('/api/notifications/jira')
}

// Health & Metrics API
export const healthApi = {
  check: () => api.get<any>('/api/v1/health'),
  
  ready: () => api.get<any>('/api/v1/health/ready'),
  
  live: () => api.get<any>('/api/v1/health/live'),
  
  metrics: () => api.get<any>('/api/v1/metrics')
}

// Secrets Scanner API
export const secretsApi = {
  scan: (code: string) => api.post<any>('/api/v1/secrets/scan', { code }),
  
  scanFile: (file: any) => api.post<any>('/api/v1/secrets/scan/file', file),
  
  getPatterns: () => api.get<any>('/api/v1/secrets/patterns')
}

// Cloud Scanner API
export const cloudApi = {
  scan: (config: any) => api.post<any>('/api/v1/cloud/scan', config),
  
  scanFile: (file: any) => api.post<any>('/api/v1/cloud/scan/file', file),
  
  getProviders: () => api.get<any>('/api/v1/cloud/providers'),
  
  getRules: (provider: string) => api.get<any>(`/api/v1/cloud/rules/${provider}`)
}

// Compliance API
export const complianceApi = {
  getFrameworks: () => api.get<any>('/api/v1/compliance/frameworks'),
  
  getControls: (framework: string) => api.get<any>(`/api/v1/compliance/frameworks/${framework}/controls`),
  
  generateReport: (data: any) => api.post<any>('/api/v1/compliance/report', data)
}

// Security Posture API
export const postureApi = {
  getStatistics: () => api.get<any>('/api/v1/posture/statistics'),
  
  getTrend: () => api.get<any>('/api/v1/posture/trend'),
  
  getRecommendations: () => api.get<any>('/api/v1/posture/recommendations'),
  
  record: (data: any) => api.post<any>('/api/v1/posture/record', data)
}

// Remediation API
export const remediationApi = {
  scan: (code: string, language: string) => api.post<any>('/api/v1/remediation/scan', { code, language }),
  
  getFix: (vulnerabilityType: string, code: string) => api.post<any>(`/api/v1/remediation/fix/${vulnerabilityType}`, { code }),
  
  getRules: () => api.get<any>('/api/v1/remediation/rules')
}

// SBOM API
export const sbomApi = {
  generate: (data: any) => api.post<any>('/api/v1/sbom/generate', data),
  
  getFormats: () => api.get<any>('/api/v1/sbom/formats'),
  
  getEcosystems: () => api.get<any>('/api/v1/sbom/ecosystems')
}

// Custom Rules API
export const rulesApi = {
  list: () => api.get<any[]>('/api/v1/rules/'),
  
  create: (rule: any) => api.post<any>('/api/v1/rules/', rule),
  
  scan: (code: string, rules: any[]) => api.post<any>('/api/v1/rules/scan', { code, rules }),
  
  toggle: (ruleId: string, enabled: boolean) => api.post<any>(`/api/v1/rules/${ruleId}/toggle`, { enabled }),
  
  delete: (ruleId: string) => api.delete<any>(`/api/v1/rules/${ruleId}`)
}
