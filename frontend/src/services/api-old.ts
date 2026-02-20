// API client for DevGuardian AI

const API_BASE_URL = '/api'
const AI_SERVICE_BASE_URL = 'http://localhost:8000/api'

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
export const aiServiceClient = {
  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${AI_SERVICE_BASE_URL}${endpoint}`)
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
      const response = await fetch(`${AI_SERVICE_BASE_URL}${endpoint}`, {
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
    return aiServiceClient.get('/ai-fixes')
  },

  async generateFixes(vulnerabilities: any[]) {
    return aiServiceClient.post('/ai-fixes/generate', { vulnerabilities })
  },

  async approveFix(fixId: string, approved: boolean, notes?: string) {
    return aiServiceClient.post(`/ai-fixes/${fixId}/approve`, { approved, notes })
  },

  async applyFix(fixId: string) {
    return aiServiceClient.post(`/ai-fixes/${fixId}/apply`, {})
  },

  async rejectFix(fixId: string, notes?: string) {
    return aiServiceClient.post(`/ai-fixes/${fixId}/approve`, { approved: false, notes })
  },

  async getFixDetails(fixId: string) {
    return aiServiceClient.get(`/ai-fixes/${fixId}`)
  },

  async deleteFix(fixId: string) {
    return aiServiceClient.delete(`/ai-fixes/${fixId}`)
  },

  async getFixStats() {
    return aiServiceClient.get('/ai-fixes/stats')
  },

  async generateFix(file: File, vulnerabilityType: string = 'general') {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('vulnerability_type', vulnerabilityType)
    
    try {
      const response = await fetch(`${AI_SERVICE_BASE_URL}/pytorch-scanner/scan/file`, {
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
}

// Health check
export const healthApi = {
  async checkBackend() {
    return apiClient.get('/health')
  },

  async checkAiService() {
    return aiServiceClient.get('/health')
  },
}
