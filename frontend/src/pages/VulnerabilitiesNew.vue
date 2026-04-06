<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-white">Vulnerabilities</h1>
      <button
        @click="showCreateModal = true"
        class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg"
      >
        + Add Vulnerability
      </button>
    </div>

    <!-- Stats Cards -->
    <div v-if="vulnStore.stats" class="grid grid-cols-4 gap-4">
      <div class="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-4">
        <div class="text-3xl font-bold text-white">{{ vulnStore.stats.total }}</div>
        <div class="text-gray-400 text-sm">Total</div>
      </div>
      <div class="bg-gray-800/50 backdrop-blur-sm border border-red-700/50 rounded-xl p-4">
        <div class="text-3xl font-bold text-red-400">{{ vulnStore.stats.by_severity.critical }}</div>
        <div class="text-gray-400 text-sm">Critical</div>
      </div>
      <div class="bg-gray-800/50 backdrop-blur-sm border border-orange-700/50 rounded-xl p-4">
        <div class="text-3xl font-bold text-orange-400">{{ vulnStore.stats.by_severity.high }}</div>
        <div class="text-gray-400 text-sm">High</div>
      </div>
      <div class="bg-gray-800/50 backdrop-blur-sm border border-green-700/50 rounded-xl p-4">
        <div class="text-3xl font-bold text-green-400">{{ vulnStore.stats.open }}</div>
        <div class="text-gray-400 text-sm">Open</div>
      </div>
    </div>

    <!-- Login Prompt -->
    <div v-if="!authStore.isAuthenticated" class="bg-yellow-500/20 border border-yellow-500/50 rounded-xl p-6 text-center">
      <p class="text-yellow-300">Please login to view vulnerabilities</p>
      <button
        @click="$router.push('/login')"
        class="mt-2 bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg"
      >
        Go to Login
      </button>
    </div>

    <!-- Loading -->
    <div v-else-if="vulnStore.isLoading" class="text-center py-8">
      <div class="animate-spin w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full mx-auto"></div>
    </div>

    <!-- Vulnerabilities List -->
    <div v-else class="space-y-4">
      <div
        v-for="vuln in vulnStore.vulnerabilities"
        :key="vuln.id"
        class="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-4"
      >
        <div class="flex justify-between items-start">
          <div>
            <div class="flex items-center gap-2">
              <h3 class="font-semibold text-white">{{ vuln.title }}</h3>
              <span
                class="px-2 py-0.5 rounded text-xs"
                :class="severityClass(vuln.severity)"
              >
                {{ vuln.severity }}
              </span>
            </div>
            <p class="text-gray-400 text-sm mt-1">{{ vuln.description }}</p>
            <div class="flex items-center gap-4 mt-2 text-xs text-gray-500">
              <span v-if="vuln.cwe_id">CWE: {{ vuln.cwe_id }}</span>
              <span v-if="vuln.file_path">{{ vuln.file_path }}</span>
              <span>{{ formatDate(vuln.created_at) }}</span>
            </div>
          </div>
          <div class="flex gap-2">
            <button
              @click="updateStatus(vuln)"
              class="px-3 py-1 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded"
            >
              Update
            </button>
            <button
              @click="deleteVuln(vuln.id)"
              class="px-3 py-1 text-sm bg-red-600 hover:bg-red-700 text-white rounded"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

      <div v-if="vulnStore.vulnerabilities.length === 0" class="text-center py-8 text-gray-500">
        No vulnerabilities found. Add one to get started.
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-gray-800 border border-gray-700 rounded-xl p-6 w-full max-w-md">
        <h2 class="text-xl font-bold text-white mb-4">Add Vulnerability</h2>
        <form @submit.prevent="createVuln" class="space-y-4">
          <div>
            <label class="block text-gray-400 text-sm mb-1">Title</label>
            <input
              v-model="newVuln.title"
              type="text"
              required
              class="w-full bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-white"
            />
          </div>
          <div>
            <label class="block text-gray-400 text-sm mb-1">Description</label>
            <textarea
              v-model="newVuln.description"
              rows="3"
              class="w-full bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-white"
            ></textarea>
          </div>
          <div>
            <label class="block text-gray-400 text-sm mb-1">Severity</label>
            <select
              v-model="newVuln.severity"
              class="w-full bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-white"
            >
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
          <div>
            <label class="block text-gray-400 text-sm mb-1">CWE ID (optional)</label>
            <input
              v-model="newVuln.cwe_id"
              type="text"
              placeholder="e.g., CWE-89"
              class="w-full bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-white"
            />
          </div>
          <div class="flex gap-3 pt-2">
            <button
              type="submit"
              class="flex-1 bg-purple-600 hover:bg-purple-700 text-white py-2 rounded-lg"
            >
              Create
            </button>
            <button
              type="button"
              @click="showCreateModal = false"
              class="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-2 rounded-lg"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useVulnStore } from '@/stores/vulnerabilities'

const authStore = useAuthStore()
const vulnStore = useVulnStore()

const showCreateModal = ref(false)
const newVuln = ref({
  title: '',
  description: '',
  severity: 'medium',
  cwe_id: '',
})

onMounted(() => {
  if (authStore.isAuthenticated) {
    vulnStore.fetchVulnerabilities()
    vulnStore.fetchStats()
  }
})

function severityClass(severity: string) {
  const classes: Record<string, string> = {
    critical: 'bg-red-500/20 text-red-400',
    high: 'bg-orange-500/20 text-orange-400',
    medium: 'bg-yellow-500/20 text-yellow-400',
    low: 'bg-blue-500/20 text-blue-400',
  }
  return classes[severity] || classes.medium
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString()
}

async function createVuln() {
  const result = await vulnStore.createVulnerability({
    title: newVuln.value.title,
    description: newVuln.value.description,
    severity: newVuln.value.severity,
    cwe_id: newVuln.value.cwe_id || undefined,
  })

  if (result.success) {
    showCreateModal.value = false
    newVuln.value = { title: '', description: '', severity: 'medium', cwe_id: '' }
  }
}

async function updateStatus(vuln: any) {
  const newStatus = vuln.status === 'open' ? 'resolved' : 'open'
  await vulnStore.updateVulnerability(vuln.id, { status: newStatus })
}

async function deleteVuln(id: number) {
  if (confirm('Are you sure you want to delete this vulnerability?')) {
    await vulnStore.deleteVulnerability(id)
  }
}
</script>
