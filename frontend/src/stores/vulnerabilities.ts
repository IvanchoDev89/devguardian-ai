import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { vulnApi } from '../services/api_client'
import { useAuthStore } from './auth'

export const useVulnStore = defineStore('vulnerabilities', () => {
  const authStore = useAuthStore()
  const vulnerabilities = ref<any[]>([])
  const stats = ref<any>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function fetchVulnerabilities() {
    if (!authStore.token) return
    isLoading.value = true
    error.value = null
    try {
      const data = await vulnApi.list(authStore.token)
      vulnerabilities.value = data || []
    } catch (e: any) {
      error.value = e.message
    } finally {
      isLoading.value = false
    }
  }

  async function fetchStats() {
    if (!authStore.token) return
    try {
      const data = await vulnApi.getStats(authStore.token)
      stats.value = data
    } catch (e: any) {
      error.value = e.message
    }
  }

  async function createVulnerability(data: { title: string; description: string; severity: string; cwe_id?: string }) {
    if (!authStore.token) return { success: false }
    try {
      await vulnApi.create(authStore.token, data)
      await fetchVulnerabilities()
      await fetchStats()
      return { success: true }
    } catch (e: any) {
      error.value = e.message
      return { success: false, message: e.message }
    }
  }

  async function updateVulnerability(id: number, data: any) {
    if (!authStore.token) return
    try {
      await vulnApi.update(authStore.token, id, data)
      await fetchVulnerabilities()
    } catch (e: any) {
      error.value = e.message
    }
  }

  async function deleteVulnerability(id: number) {
    if (!authStore.token) return
    try {
      await vulnApi.delete(authStore.token, id)
      await fetchVulnerabilities()
      await fetchStats()
    } catch (e: any) {
      error.value = e.message
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
