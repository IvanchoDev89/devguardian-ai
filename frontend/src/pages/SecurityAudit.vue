<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-lg shadow p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-2">Security Audit Dashboard</h1>
      <p class="text-gray-600">AI-powered comprehensive security analysis and vulnerability assessment</p>
    </div>

    <!-- Audit Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">Critical Issues</h3>
            <p class="text-2xl font-bold text-red-600">{{ auditData.summary?.severity_breakdown?.critical || 0 }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">High Issues</h3>
            <p class="text-2xl font-bold text-orange-600">{{ auditData.summary?.severity_breakdown?.high || 0 }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">Security Score</h3>
            <p class="text-2xl font-bold text-green-600">{{ auditData.summary?.security_score || 0 }}/100</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">Performance Score</h3>
            <p class="text-2xl font-bold text-blue-600">{{ auditData.summary?.performance_score || 0 }}/100</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Run Audit -->
    <div class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-medium text-gray-900">Run Security Audit</h2>
      </div>
      <div class="p-6">
        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Audit Scope</label>
              <select v-model="auditForm.scope" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="full">Full Project</option>
                <option value="frontend">Frontend Only</option>
                <option value="backend">Backend Only</option>
                <option value="ai-service">AI Service Only</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Analysis Type</label>
              <select v-model="auditForm.analysisType" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="comprehensive">Comprehensive</option>
                <option value="security">Security Only</option>
                <option value="performance">Performance Only</option>
                <option value="dependencies">Dependencies Only</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Depth Level</label>
              <select v-model="auditForm.depth" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="quick">Quick Scan</option>
                <option value="standard">Standard</option>
                <option value="deep">Deep Analysis</option>
              </select>
            </div>
          </div>
          
          <div class="flex items-center space-x-4">
            <label class="flex items-center">
              <input v-model="auditForm.includeRecommendations" type="checkbox" class="mr-2" />
              <span class="text-sm text-gray-700">Include AI Recommendations</span>
            </label>
            <label class="flex items-center">
              <input v-model="auditForm.generateReport" type="checkbox" class="mr-2" />
              <span class="text-sm text-gray-700">Generate Detailed Report</span>
            </label>
            <label class="flex items-center">
              <input v-model="auditForm.checkDependencies" type="checkbox" class="mr-2" />
              <span class="text-sm text-gray-700">Check Dependencies</span>
            </label>
          </div>
          
          <button
            @click="runAudit"
            :disabled="isRunningAudit"
            class="bg-red-600 text-white px-6 py-2 rounded-md hover:bg-red-700 disabled:opacity-50"
          >
            {{ isRunningAudit ? 'Running Audit...' : 'Run Security Audit' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Audit Progress -->
    <div v-if="isRunningAudit" class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-medium text-gray-900">Audit Progress</h2>
      </div>
      <div class="p-6">
        <div class="space-y-4">
          <div>
            <div class="flex justify-between text-sm text-gray-600 mb-1">
              <span>{{ currentPhase }}</span>
              <span>{{ auditProgress }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div class="bg-blue-600 h-2 rounded-full transition-all duration-300" :style="{ width: `${auditProgress}%` }"></div>
            </div>
          </div>
          <div class="text-sm text-gray-600">
            <p>Files scanned: {{ filesScanned }}</p>
            <p>Issues found: {{ issuesFound }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Audit Results -->
    <div v-if="auditData.summary && !isRunningAudit" class="space-y-6">
      <!-- Summary Section -->
      <div class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">Audit Summary</h2>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 class="text-md font-medium text-gray-900 mb-3">Security Analysis</h3>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">Total Security Issues:</span>
                  <span class="text-sm font-medium">{{ auditData.summary.total_issues }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">Security Score:</span>
                  <span class="text-sm font-medium">{{ auditData.summary.security_score }}/100</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">Critical Vulnerabilities:</span>
                  <span class="text-sm font-medium text-red-600">{{ auditData.summary.severity_breakdown.critical }}</span>
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="text-md font-medium text-gray-900 mb-3">Performance Analysis</h3>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">Performance Score:</span>
                  <span class="text-sm font-medium">{{ auditData.summary.performance_score }}/100</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">Performance Issues:</span>
                  <span class="text-sm font-medium">{{ auditData.performance_metrics?.length || 0 }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600">Memory Issues:</span>
                  <span class="text-sm font-medium">{{ memoryIssuesCount }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Recommendations -->
          <div v-if="auditData.summary.recommendations" class="mt-6">
            <h3 class="text-md font-medium text-gray-900 mb-3">AI Recommendations</h3>
            <div class="space-y-2">
              <div
                v-for="(recommendation, index) in auditData.summary.recommendations"
                :key="index"
                class="bg-yellow-50 border border-yellow-200 rounded-lg p-3"
              >
                <p class="text-sm text-yellow-800">{{ recommendation }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Security Findings -->
      <div class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">Security Findings</h2>
        </div>
        <div class="p-6">
          <div v-if="securityFindings.length === 0" class="text-center py-8 text-gray-500">
            No security issues found
          </div>
          
          <div v-else class="space-y-4">
            <div
              v-for="(finding, index) in securityFindings.slice(0, 10)"
              :key="index"
              class="border rounded-lg p-4"
              :class="{
                'border-red-300 bg-red-50': finding.severity === 'critical',
                'border-orange-300 bg-orange-50': finding.severity === 'high',
                'border-yellow-300 bg-yellow-50': finding.severity === 'medium',
                'border-gray-300 bg-gray-50': finding.severity === 'low'
              }"
            >
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <h4 class="font-medium text-gray-900">{{ finding.type.replace('_', ' ').toUpperCase() }}</h4>
                  <p class="text-sm text-gray-600 mt-1">{{ finding.description || 'Security vulnerability detected' }}</p>
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
                    'bg-red-100 text-red-800': finding.severity === 'critical',
                    'bg-orange-100 text-orange-800': finding.severity === 'high',
                    'bg-yellow-100 text-yellow-800': finding.severity === 'medium',
                    'bg-gray-100 text-gray-800': finding.severity === 'low'
                  }"
                >
                  {{ finding.severity.toUpperCase() }}
                </span>
              </div>
              <div v-if="finding.code" class="mt-3">
                <code class="text-sm bg-gray-100 p-2 rounded block">{{ finding.code }}</code>
              </div>
            </div>
            
            <div v-if="securityFindings.length > 10" class="text-center">
              <button class="text-blue-600 hover:text-blue-800 text-sm">
                Show {{ securityFindings.length - 10 }} more findings
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Dependency Vulnerabilities -->
      <div v-if="dependencyVulnerabilities.length > 0" class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">Dependency Vulnerabilities</h2>
        </div>
        <div class="p-6">
          <div class="space-y-3">
            <div
              v-for="(dep, index) in dependencyVulnerabilities"
              :key="index"
              class="border border-orange-300 bg-orange-50 rounded-lg p-4"
            >
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-medium text-gray-900">{{ dep.package }}</h4>
                  <p class="text-sm text-gray-600 mt-1">{{ dep.description }}</p>
                  <p class="text-xs text-gray-500 mt-2">File: {{ dep.file }}</p>
                </div>
                <span class="px-2 py-1 text-xs font-medium rounded bg-orange-100 text-orange-800">
                  HIGH
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Export Options -->
      <div class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">Export Report</h2>
        </div>
        <div class="p-6">
          <div class="flex space-x-4">
            <button
              @click="exportReport('json')"
              class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
            >
              Export JSON
            </button>
            <button
              @click="exportReport('pdf')"
              class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700"
            >
              Export PDF
            </button>
            <button
              @click="exportReport('csv')"
              class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
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
import { ref, computed, onMounted } from 'vue'
import { apiService } from '../services/api'

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

const isRunningAudit = ref(false)
const auditProgress = ref(0)
const currentPhase = ref('')
const filesScanned = ref(0)
const issuesFound = ref(0)

const securityFindings = computed(() => auditData.value.security_findings || [])
const dependencyVulnerabilities = computed(() => auditData.value.dependency_vulnerabilities || [])
const memoryIssuesCount = computed(() => 
  auditData.value.performance_metrics?.filter(m => m.type === 'inefficient_memory_usage').length || 0
)

const runAudit = async () => {
  isRunningAudit.value = true
  auditProgress.value = 0
  filesScanned.value = 0
  issuesFound.value = 0
  
  const phases = [
    { name: 'Initializing audit...', duration: 10 },
    { name: 'Scanning files...', duration: 30 },
    { name: 'Analyzing security patterns...', duration: 25 },
    { name: 'Checking dependencies...', duration: 15 },
    { name: 'Analyzing performance...', duration: 15 },
    { name: 'Generating recommendations...', duration: 5 }
  ]
  
  try {
    for (let i = 0; i < phases.length; i++) {
      const phase = phases[i]
      currentPhase.value = phase.name
      
      // Simulate progress
      for (let j = 0; j <= phase.duration; j += 5) {
        await new Promise(resolve => setTimeout(resolve, 100))
        auditProgress.value = Math.round(((i * phase.duration) + j) / 150 * 100)
        
        // Simulate finding issues
        if (Math.random() > 0.7) {
          issuesFound.value += Math.floor(Math.random() * 3) + 1
        }
        filesScanned.value += Math.floor(Math.random() * 10) + 5
      }
    }
    
    // Generate mock audit results
    auditData.value = generateMockAuditResults()
    
  } catch (error) {
    console.error('Audit error:', error)
    alert('Failed to run security audit. Please try again.')
  } finally {
    isRunningAudit.value = false
    auditProgress.value = 100
  }
}

const generateMockAuditResults = (): AuditData => {
  const mockFindings = [
    {
      type: 'sql_injection',
      severity: 'critical',
      file: '/backend/app/controllers/UserController.php',
      line: 45,
      code: '$query = "SELECT * FROM users WHERE id = " . $_GET["id"];',
      confidence: 0.95,
      description: 'SQL injection vulnerability detected'
    },
    {
      type: 'xss',
      severity: 'high',
      file: '/frontend/src/components/UserProfile.vue',
      line: 23,
      code: 'document.getElementById("output").innerHTML = userInput;',
      confidence: 0.88,
      description: 'Cross-site scripting vulnerability detected'
    },
    {
      type: 'hardcoded_secrets',
      severity: 'critical',
      file: '/ai-service/config.py',
      line: 12,
      code: 'API_KEY = "sk-1234567890abcdef"',
      confidence: 0.92,
      description: 'Hardcoded API key detected'
    },
    {
      type: 'weak_crypto',
      severity: 'medium',
      file: '/backend/app/utils/encryption.php',
      line: 8,
      code: '$hash = md5($password);',
      confidence: 0.85,
      description: 'Weak cryptographic algorithm detected'
    }
  ]
  
  const mockDeps = [
    {
      package: 'requests<2.25.0',
      file: '/requirements.txt',
      description: 'Known vulnerable package detected'
    },
    {
      package: 'lodash<4.17.21',
      file: '/frontend/package.json',
      description: 'Known vulnerable npm package detected'
    }
  ]
  
  const mockPerf = [
    {
      type: 'n_plus_one_query',
      severity: 'medium',
      file: '/backend/app/models/Repository.php',
      line: 67,
      code: 'foreach ($users as $user) { $user->getDetails(); }',
      impact: 'high_database_load'
    },
    {
      type: 'missing_error_handling',
      severity: 'medium',
      file: '/ai-service/app/api/endpoints/scan.py',
      line: 34,
      code: 'except: pass',
      impact: 'debugging_difficulty'
    }
  ]
  
  return {
    summary: {
      total_issues: mockFindings.length + mockDeps.length + mockPerf.length,
      severity_breakdown: {
        critical: 2,
        high: 1,
        medium: 3,
        low: 0
      },
      security_score: 65,
      performance_score: 78,
      recommendations: [
        '🚨 CRITICAL: Address all critical security vulnerabilities immediately',
        '📦 Update all vulnerable dependencies to latest secure versions',
        '🔗 Implement proper authentication and authorization for all API endpoints',
        '⚙️ Review and secure all configuration files',
        '⚡ Optimize performance issues to improve application responsiveness'
      ]
    },
    security_findings: mockFindings,
    dependency_vulnerabilities: mockDeps,
    performance_metrics: mockPerf
  }
}

const exportReport = (format: string) => {
  alert(`Exporting audit report as ${format.toUpperCase()}...`)
  // In a real implementation, this would generate and download the report
}

onMounted(() => {
  // Load any existing audit data
})
</script>
