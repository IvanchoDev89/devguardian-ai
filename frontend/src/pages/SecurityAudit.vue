<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6">
      <h1 class="text-2xl font-bold text-white mb-2">Security Audit Dashboard</h1>
      <p class="text-gray-400">AI-powered comprehensive security analysis and vulnerability assessment</p>
    </div>

    <!-- Audit Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-red-500/20 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-sm font-medium text-gray-400">Critical Issues</h3>
            <p class="text-2xl font-bold text-red-400">{{ auditData.summary?.severity_breakdown?.critical || 0 }}</p>
          </div>
        </div>
      </div>

      <div class="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-orange-500/20 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-sm font-medium text-gray-400">High Issues</h3>
            <p class="text-2xl font-bold text-orange-400">{{ auditData.summary?.severity_breakdown?.high || 0 }}</p>
          </div>
        </div>
      </div>

      <div class="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-green-500/20 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-sm font-medium text-gray-400">Security Score</h3>
            <p class="text-2xl font-bold text-green-400">{{ auditData.summary?.security_score || 0 }}/100</p>
          </div>
        </div>
      </div>

      <div class="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-blue-500/20 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-sm font-medium text-gray-400">Performance Score</h3>
            <p class="text-2xl font-bold text-blue-400">{{ auditData.summary?.performance_score || 0 }}/100</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Run Audit -->
    <div class="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl">
      <div class="px-6 py-4 border-b border-gray-700/50">
        <h2 class="text-lg font-medium text-white">Run Security Audit</h2>
      </div>
      <div class="p-6">
        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Audit Scope</label>
              <select v-model="auditForm.scope" class="w-full bg-gray-900/50 border border-gray-600/50 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                <option value="full">Full Project</option>
                <option value="frontend">Frontend Only</option>
                <option value="backend">Backend Only</option>
                <option value="ai-service">AI Service Only</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Analysis Type</label>
              <select v-model="auditForm.analysisType" class="w-full bg-gray-900/50 border border-gray-600/50 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                <option value="comprehensive">Comprehensive</option>
                <option value="security">Security Only</option>
                <option value="performance">Performance Only</option>
                <option value="dependencies">Dependencies Only</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Depth Level</label>
              <select v-model="auditForm.depth" class="w-full bg-gray-900/50 border border-gray-600/50 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                <option value="quick">Quick Scan</option>
                <option value="standard">Standard</option>
                <option value="deep">Deep Analysis</option>
              </select>
            </div>
          </div>
          
          <div class="flex items-center space-x-6">
            <label class="flex items-center">
              <input v-model="auditForm.includeRecommendations" type="checkbox" class="mr-2 rounded bg-gray-700 border-gray-600 text-purple-500 focus:ring-purple-500" />
              <span class="text-sm text-gray-300">Include AI Recommendations</span>
            </label>
            <label class="flex items-center">
              <input v-model="auditForm.generateReport" type="checkbox" class="mr-2 rounded bg-gray-700 border-gray-600 text-purple-500 focus:ring-purple-500" />
              <span class="text-sm text-gray-300">Generate Detailed Report</span>
            </label>
            <label class="flex items-center">
              <input v-model="auditForm.checkDependencies" type="checkbox" class="mr-2 rounded bg-gray-700 border-gray-600 text-purple-500 focus:ring-purple-500" />
              <span class="text-sm text-gray-300">Check Dependencies</span>
            </label>
          </div>
          
          <button
            @click="runAudit"
            :disabled="loading"
            class="bg-gradient-to-r from-red-600 to-orange-600 text-white px-6 py-2 rounded-lg hover:from-red-500 hover:to-orange-500 disabled:opacity-50"
          >
            {{ loading ? 'Loading...' : 'Run Security Audit' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Audit Results -->
    <div v-if="auditData.summary" class="space-y-6">
      <!-- Summary Section -->
      <div class="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl">
        <div class="px-6 py-4 border-b border-gray-700/50">
          <h2 class="text-lg font-medium text-white">Audit Summary</h2>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 class="text-md font-medium text-white mb-3">Security Analysis</h3>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span class="text-sm text-gray-400">Total Security Issues:</span>
                  <span class="text-sm font-medium text-white">{{ auditData.summary.total_issues }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-400">Security Score:</span>
                  <span class="text-sm font-medium text-white">{{ auditData.summary.security_score }}/100</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-400">Critical Vulnerabilities:</span>
                  <span class="text-sm font-medium text-red-400">{{ auditData.summary.severity_breakdown.critical }}</span>
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="text-md font-medium text-white mb-3">Performance Analysis</h3>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span class="text-sm text-gray-400">Performance Score:</span>
                  <span class="text-sm font-medium text-white">{{ auditData.summary.performance_score }}/100</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-400">Performance Issues:</span>
                  <span class="text-sm font-medium text-white">{{ auditData.performance_metrics?.length || 0 }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-400">Memory Issues:</span>
                  <span class="text-sm font-medium text-white">{{ memoryIssuesCount }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Recommendations -->
          <div v-if="auditData.summary.recommendations" class="mt-6">
            <h3 class="text-md font-medium text-white mb-3">AI Recommendations</h3>
            <div class="space-y-2">
              <div
                v-for="(recommendation, index) in auditData.summary.recommendations"
                :key="index"
                class="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3"
              >
                <p class="text-sm text-yellow-300">{{ recommendation }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Security Findings -->
      <div class="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl">
        <div class="px-6 py-4 border-b border-gray-700/50">
          <h2 class="text-lg font-medium text-white">Security Findings</h2>
        </div>
        <div class="p-6">
          <div v-if="loading" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
          </div>
          <div v-else-if="securityFindings.length === 0" class="text-center py-8">
            <svg class="w-12 h-12 mx-auto text-gray-500 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <p class="text-gray-500">No security issues found</p>
          </div>
          
          <div v-else class="space-y-4">
            <div
              v-for="(finding, index) in securityFindings.slice(0, 10)"
              :key="index"
              class="border rounded-lg p-4"
              :class="{
                'border-red-500/30 bg-red-500/10': finding.severity === 'critical',
                'border-orange-500/30 bg-orange-500/10': finding.severity === 'high',
                'border-yellow-500/30 bg-yellow-500/10': finding.severity === 'medium',
                'border-gray-600 bg-gray-700/30': finding.severity === 'low'
              }"
            >
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <h4 class="font-medium text-white">{{ finding.type.replace('_', ' ').toUpperCase() }}</h4>
                  <p class="text-sm text-gray-400 mt-1">{{ finding.description || 'Security vulnerability detected' }}</p>
                  <div class="mt-2 text-xs text-gray-500">
                    <span>File: {{ finding.file }}</span>
                    <span class="mx-2">•</span>
                    <span>Line: {{ finding.line }}</span>
                    <span class="mx-2">•</span>
                    <span>Confidence: {{ (finding.confidence * 100).toFixed(1) }}%</span>
                  </div>
                </div>
                <span
                  class="px-2 py-1 text-xs font-medium rounded ml-4"
                  :class="{
                    'bg-red-500/20 text-red-400': finding.severity === 'critical',
                    'bg-orange-500/20 text-orange-400': finding.severity === 'high',
                    'bg-yellow-500/20 text-yellow-400': finding.severity === 'medium',
                    'bg-gray-500/20 text-gray-400': finding.severity === 'low'
                  }"
                >
                  {{ finding.severity.toUpperCase() }}
                </span>
              </div>
              <div v-if="finding.code" class="mt-3">
                <code class="text-sm bg-gray-900 p-2 rounded block text-gray-300 font-mono">{{ finding.code }}</code>
              </div>
            </div>
            
            <div v-if="securityFindings.length > 10" class="text-center">
              <button class="text-purple-400 hover:text-purple-300 text-sm">
                Show {{ securityFindings.length - 10 }} more findings
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Dependency Vulnerabilities -->
      <div v-if="dependencyVulnerabilities.length > 0" class="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl">
        <div class="px-6 py-4 border-b border-gray-700/50">
          <h2 class="text-lg font-medium text-white">Dependency Vulnerabilities</h2>
        </div>
        <div class="p-6">
          <div class="space-y-3">
            <div
              v-for="(dep, index) in dependencyVulnerabilities"
              :key="index"
              class="border border-orange-500/30 bg-orange-500/10 rounded-lg p-4"
            >
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-medium text-white">{{ dep.package }}</h4>
                  <p class="text-sm text-gray-400 mt-1">{{ dep.description }}</p>
                  <p class="text-xs text-gray-500 mt-2">File: {{ dep.file }}</p>
                </div>
                <span class="px-2 py-1 text-xs font-medium rounded bg-orange-500/20 text-orange-400">
                  HIGH
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Export Options -->
      <div class="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl">
        <div class="px-6 py-4 border-b border-gray-700/50">
          <h2 class="text-lg font-medium text-white">Export Report</h2>
        </div>
        <div class="p-6">
          <div class="flex space-x-4">
            <button
              @click="exportReport('json')"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Export JSON
            </button>
            <button
              @click="exportReport('pdf')"
              class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
            >
              Export PDF
            </button>
            <button
              @click="exportReport('csv')"
              class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
            >
              Export CSV
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { api } from '../services/api_client'
import { useAuthStore } from '../stores/auth'
import { useNotificationStore } from '../stores/notifications'

const authStore = useAuthStore()
const notification = useNotificationStore()

interface AuditForm {
  scope: string
  analysisType: string
  depth: string
  includeRecommendations: boolean
  generateReport: boolean
  checkDependencies: boolean
}

interface AuditData {
  summary: {
    total_issues: number
    severity_breakdown: {
      critical: number
      high: number
      medium: number
      low: number
    }
    security_score: number
    performance_score: number
    recommendations: string[]
  }
  security_findings: Array<{
    type: string
    severity: string
    file: string
    line: number
    code: string
    confidence: number
    description?: string
  }>
  dependency_vulnerabilities: Array<{
    package: string
    file: string
    description: string
  }>
  performance_metrics: Array<{
    type: string
    severity: string
    file: string
    line: number
    code: string
    impact: string
  }>
}

const auditForm = ref<AuditForm>({
  scope: 'full',
  analysisType: 'comprehensive',
  depth: 'standard',
  includeRecommendations: true,
  generateReport: true,
  checkDependencies: true
})

const auditData = ref<AuditData>({
  summary: {
    total_issues: 0,
    severity_breakdown: {
      critical: 0,
      high: 0,
      medium: 0,
      low: 0
    },
    security_score: 0,
    performance_score: 0,
    recommendations: []
  },
  security_findings: [],
  dependency_vulnerabilities: [],
  performance_metrics: []
})

const loading = ref(false)

const securityFindings = computed(() => auditData.value.security_findings || [])
const dependencyVulnerabilities = computed(() => auditData.value.dependency_vulnerabilities || [])
const memoryIssuesCount = computed(() => 
  auditData.value.performance_metrics?.filter(m => m.type === 'inefficient_memory_usage').length || 0
)

const runAudit = async () => {
  loading.value = true
  try {
    const token = authStore.token
    if (!token) {
      notification.error('Not authenticated', 'Please log in first')
      return
    }
    
    const [summaryRes, vulnsRes] = await Promise.all([
      api.get<any>('/api/security-audit/summary', token),
      api.get<any[]>('/api/security-audit/vulnerabilities', token)
    ])
    
    auditData.value = {
      summary: summaryRes.summary,
      security_findings: vulnsRes,
      dependency_vulnerabilities: [],
      performance_metrics: []
    }
  } catch (error: any) {
    console.error('Failed to load audit:', error)
    notification.error('Failed to Load', error.message || 'Could not fetch security audit data')
  } finally {
    loading.value = false
  }
}

const exportReport = (format: string) => {
  alert(`Exporting audit report as ${format.toUpperCase()}...`)
}
</script>
