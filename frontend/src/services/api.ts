// API client for DevGuardian AI

const API_BASE_URL = '/api'
const AI_API_BASE_URL = '/ai-api'

interface ApiResponse<T> {
  data?: T
  error?: string
  message?: string
}

// Backend API client
export const apiClient = {
  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      return { data }
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Unknown error' }
    }
  },

  async post<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      return { data }
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Unknown error' }
    }
  },

  async put<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      return { data }
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Unknown error' }
    }
  },

  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'DELETE',
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      return { data }
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Unknown error' }
    }
  },
}

// AI Service API client
export const aiApiClient = {
  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${AI_API_BASE_URL}${endpoint}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      return { data }
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Unknown error' }
    }
  },

  async post<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${AI_API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      return { data }
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Unknown error' }
    }
  },
}

// Repository API
export const repositoryApi = {
  async getRepositories() {
    return apiClient.get('/repositories')
  },

  async addRepository(repoData: any) {
    return apiClient.post('/repositories', repoData)
  },

  async scanRepository(repoId: string) {
    return apiClient.post(`/repositories/${repoId}/scan`, {})
  },
}

// Vulnerability API
export const vulnerabilityApi = {
  async getVulnerabilities() {
    return apiClient.get('/vulnerabilities')
  },

  async getVulnerability(id: string) {
    return apiClient.get(`/vulnerabilities/${id}`)
  },
}

// AI Fix API
export const aiFixApi = {
  async getAiFixes() {
    return aiApiClient.get('/api/ai-fix')
  },

  async generateFix(file: File, vulnerabilityType: string = 'general') {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('vulnerability_type', vulnerabilityType)
    
    try {
      const response = await fetch(`${AI_API_BASE_URL}/api/ai-fix/generate-fix`, {
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
  },

  async validateFix(fixId: string) {
    return aiApiClient.post('/api/ai-fix/validate-fix', { fix_id: fixId })
  },

  async applyAiFix(fixId: string) {
    return aiApiClient.post(`/api/ai-fix/${fixId}/apply`, {})
  },
}

// Health check
export const healthApi = {
  async checkBackend() {
    return apiClient.get('/health')
  },

  async checkAiService() {
    return aiApiClient.get('/health')
  },
}
