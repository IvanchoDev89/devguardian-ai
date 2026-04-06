import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './auth'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002'

export interface Vulnerability {
  id: number
  title: string
  description: string
  severity: 'critical' | 'high' | 'medium' | 'low'
  status: 'open' | 'in_progress' | 'resolved' | 'false_positive'
  cwe_id?: string
  cvss_score?: string
  file_path?: string
  line_number?: number
  created_at: string
}

export interface VulnerabilityStats {
  total: number
  by_severity: {
    critical: number
    high: number
    medium: number
    low: number
  }
  resolved: number
  open: number
}

export const useVulnStore = defineStore('vulnerabilities', () => {
  const vulnerabilities = ref<Vulnerability[]>([])
  const stats = ref<VulnerabilityStats | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const authStore = useAuthStore()

  function getHeaders() {
    return {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${authStore.token}`,
    }
  }

  async function fetchVulnerabilities() {
    if (!authStore.token) return
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(`${API_BASE}/api/vulnerabilities`, {
        headers: getHeaders(),
      })
      if (!response.ok) throw new Error('Failed to fetch')
      vulnerabilities.value = await response.json()
    } catch (e: any) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  async function fetchStats() {
    if (!authStore.token) return
    try {
      const response = await fetch(`${API_BASE}/api/vulnerabilities/stats/summary`, {
        headers: getHeaders(),
      })
      if (response.ok) {
        stats.value = await response.json()
      }
    } catch (e) {
      console.error('Failed to fetch stats:', e)
    }
  }

  async function createVulnerability(data: Partial<Vulnerability>) {
    if (!authStore.token) return { success: false }
    try {
      const response = await fetch(`${API_BASE}/api/vulnerabilities`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to create')
      const vuln = await response.json()
      vulnerabilities.value.unshift(vuln)
      await fetchStats()
      return { success: true, data: vuln }
    } catch (e: any) {
      return { success: false, message: e.message }
    }
  }

  async function updateVulnerability(id: number, data: Partial<Vulnerability>) {
    if (!authStore.token) return { success: false }
    try {
      const response = await fetch(`${API_BASE}/api/vulnerabilities/${id}`, {
        method: 'PUT',
        headers: getHeaders(),
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to update')
      const updated = await response.json()
      const index = vulnerabilities.value.findIndex(v => v.id === id)
      if (index !== -1) {
        vulnerabilities.value[index] = updated
      }
      await fetchStats()
      return { success: true, data: updated }
    } catch (e: any) {
      return { success: false, message: e.message }
    }
  }

  async function deleteVulnerability(id: number) {
    if (!authStore.token) return { success: false }
    try {
      const response = await fetch(`${API_BASE}/api/vulnerabilities/${id}`, {
        method: 'DELETE',
        headers: getHeaders(),
      })
      if (!response.ok) throw new Error('Failed to delete')
      vulnerabilities.value = vulnerabilities.value.filter(v => v.id !== id)
      await fetchStats()
      return { success: true }
    } catch (e: any) {
      return { success: false, message: e.message }
    }
  }

  return {
    vulnerabilities,
    stats,
    isLoading,
    error,
    fetchVulnerabilities,
    fetchStats,
    createVulnerability,
    updateVulnerability,
    deleteVulnerability,
  }
})
