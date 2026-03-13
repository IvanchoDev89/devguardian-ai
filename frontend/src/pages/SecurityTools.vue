<template>
  <div class="p-6">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-white">Security Tools</h1>
      <p class="text-gray-400 mt-2">Advanced security scanning and compliance tools</p>
    </div>

    <!-- Tool Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <!-- Secrets Scanner -->
      <div 
        @click="activeTool = 'secrets'"
        class="p-6 rounded-2xl cursor-pointer transition-all duration-300 border"
        :class="activeTool === 'secrets' ? 'bg-red-500/20 border-red-500' : 'bg-slate-800/50 border-white/10 hover:border-white/20'"
      >
        <div class="w-12 h-12 rounded-xl bg-red-500/20 flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-white">Secrets Scanner</h3>
        <p class="text-sm text-gray-400 mt-1">Detect exposed API keys, tokens, and credentials</p>
        <div class="mt-3 flex items-center text-xs text-green-400">
          <span class="w-2 h-2 rounded-full bg-green-400 mr-2"></span>
          {{ secretPatterns }} patterns
        </div>
      </div>

      <!-- Cloud Scanner -->
      <div 
        @click="activeTool = 'cloud'"
        class="p-6 rounded-2xl cursor-pointer transition-all duration-300 border"
        :class="activeTool === 'cloud' ? 'bg-blue-500/20 border-blue-500' : 'bg-slate-800/50 border-white/10 hover:border-white/20'"
      >
        <div class="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/>
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-white">Cloud Scanner</h3>
        <p class="text-sm text-gray-400 mt-1">Scan AWS, Azure, GCP, K8s, Docker configs</p>
        <div class="mt-3 flex items-center text-xs text-green-400">
          <span class="w-2 h-2 rounded-full bg-green-400 mr-2"></span>
          {{ cloudProviders }} providers
        </div>
      </div>

      <!-- Security Posture -->
      <div 
        @click="activeTool = 'posture'"
        class="p-6 rounded-2xl cursor-pointer transition-all duration-300 border"
        :class="activeTool === 'posture' ? 'bg-green-500/20 border-green-500' : 'bg-slate-800/50 border-white/10 hover:border-white/20'"
      >
        <div class="w-12 h-12 rounded-xl bg-green-500/20 flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-white">Security Posture</h3>
        <p class="text-sm text-gray-400 mt-1">Track security trends over time</p>
        <div class="mt-3 flex items-center text-xs" :class="postureTrend === 'improving' ? 'text-green-400' : postureTrend === 'declining' ? 'text-red-400' : 'text-yellow-400'">
          <span class="w-2 h-2 rounded-full mr-2" :class="postureTrend === 'improving' ? 'bg-green-400' : postureTrend === 'declining' ? 'bg-red-400' : 'bg-yellow-400'"></span>
          {{ postureTrend === 'insufficient_data' ? 'No data yet' : postureTrend }}
        </div>
      </div>

      <!-- Custom Rules -->
      <div 
        @click="activeTool = 'rules'"
        class="p-6 rounded-2xl cursor-pointer transition-all duration-300 border"
        :class="activeTool === 'rules' ? 'bg-purple-500/20 border-purple-500' : 'bg-slate-800/50 border-white/10 hover:border-white/20'"
      >
        <div class="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-white">Custom Rules</h3>
        <p class="text-sm text-gray-400 mt-1">Define your own security rules</p>
        <div class="mt-3 flex items-center text-xs text-green-400">
          <span class="w-2 h-2 rounded-full bg-green-400 mr-2"></span>
          {{ customRulesCount }} rules
        </div>
      </div>

      <!-- Compliance -->
      <div 
        @click="activeTool = 'compliance'"
        class="p-6 rounded-2xl cursor-pointer transition-all duration-300 border"
        :class="activeTool === 'compliance' ? 'bg-yellow-500/20 border-yellow-500' : 'bg-slate-800/50 border-white/10 hover:border-white/20'"
      >
        <div class="w-12 h-12 rounded-xl bg-yellow-500/20 flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-white">Compliance</h3>
        <p class="text-sm text-gray-400 mt-1">SOC2, ISO27001, HIPAA, PCI-DSS</p>
        <div class="mt-3 flex items-center text-xs text-green-400">
          <span class="w-2 h-2 rounded-full bg-green-400 mr-2"></span>
          4 frameworks
        </div>
      </div>

      <!-- Auto Remediation -->
      <div 
        @click="activeTool = 'remediation'"
        class="p-6 rounded-2xl cursor-pointer transition-all duration-300 border"
        :class="activeTool === 'remediation' ? 'bg-cyan-500/20 border-cyan-500' : 'bg-slate-800/50 border-white/10 hover:border-white/20'"
      >
        <div class="w-12 h-12 rounded-xl bg-cyan-500/20 flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-white">Auto Remediation</h3>
        <p class="text-sm text-gray-400 mt-1">Automated vulnerability fixes</p>
        <div class="mt-3 flex items-center text-xs text-green-400">
          <span class="w-2 h-2 rounded-full bg-green-400 mr-2"></span>
          {{ remediationRules }} fix types
        </div>
      </div>
    </div>

    <!-- Tool Content -->
    <div v-if="activeTool" class="bg-slate-800/50 rounded-2xl border border-white/10 p-6">
      <!-- Secrets Scanner -->
      <div v-if="activeTool === 'secrets'">
        <h2 class="text-xl font-semibold text-white mb-4">Secrets Scanner</h2>
        <div class="mb-4">
          <label class="block text-sm text-gray-400 mb-2">Code to scan</label>
          <textarea 
            v-model="secretsCode" 
            class="w-full h-40 bg-slate-900/50 border border-white/10 rounded-xl p-4 text-white text-sm font-mono"
            placeholder="Paste code here to scan for secrets..."
          ></textarea>
        </div>
        <button 
          @click="scanSecrets" 
          :disabled="secretsLoading"
          class="px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl font-medium transition-colors disabled:opacity-50"
        >
          {{ secretsLoading ? 'Scanning...' : 'Scan for Secrets' }}
        </button>
        
        <div v-if="secretsResults.length" class="mt-6">
          <h3 class="text-lg font-medium text-white mb-3">Findings ({{ secretsResults.length }})</h3>
          <div class="space-y-3">
            <div v-for="(finding, idx) in secretsResults" :key="idx" class="p-4 bg-slate-900/50 rounded-xl border border-red-500/30">
              <div class="flex items-center justify-between mb-2">
                <span class="px-2 py-1 text-xs rounded-full" :class="{
                  'bg-red-500/20 text-red-400': finding.severity === 'critical',
                  'bg-orange-500/20 text-orange-400': finding.severity === 'high',
                  'bg-yellow-500/20 text-yellow-400': finding.severity === 'medium',
                  'bg-gray-500/20 text-gray-400': finding.severity === 'low'
                }">{{ finding.severity }}</span>
                <span class="text-sm text-gray-400">Line {{ finding.line_number }}</span>
              </div>
              <p class="text-white text-sm mb-2">{{ finding.description }}</p>
              <code class="text-xs text-red-300 bg-red-500/10 px-2 py-1 rounded">{{ finding.match }}</code>
              <p class="text-xs text-gray-400 mt-2">{{ finding.remediation }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Cloud Scanner -->
      <div v-if="activeTool === 'cloud'">
        <h2 class="text-xl font-semibold text-white mb-4">Cloud Security Scanner</h2>
        <div class="mb-4">
          <label class="block text-sm text-gray-400 mb-2">Provider</label>
          <select v-model="cloudProvider" class="w-full bg-slate-900/50 border border-white/10 rounded-xl p-3 text-white">
            <option value="aws">AWS</option>
            <option value="azure">Azure</option>
            <option value="gcp">GCP</option>
            <option value="k8s">Kubernetes</option>
            <option value="docker">Docker</option>
          </select>
        </div>
        <div class="mb-4">
          <label class="block text-sm text-gray-400 mb-2">Configuration (Terraform/K8s/YAML)</label>
          <textarea 
            v-model="cloudConfig" 
            class="w-full h-40 bg-slate-900/50 border border-white/10 rounded-xl p-4 text-white text-sm font-mono"
            placeholder="Paste cloud configuration here..."
          ></textarea>
        </div>
        <button 
          @click="scanCloud" 
          :disabled="cloudLoading"
          class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-medium transition-colors disabled:opacity-50"
        >
          {{ cloudLoading ? 'Scanning...' : 'Scan Configuration' }}
        </button>
        
        <div v-if="cloudResults.length" class="mt-6">
          <h3 class="text-lg font-medium text-white mb-3">Issues Found ({{ cloudResults.length }})</h3>
          <div class="space-y-3">
            <div v-for="(finding, idx) in cloudResults" :key="idx" class="p-4 bg-slate-900/50 rounded-xl border border-blue-500/30">
              <div class="flex items-center justify-between mb-2">
                <span class="text-white font-medium">{{ finding.resource }}</span>
                <span class="px-2 py-1 text-xs rounded-full" :class="{
                  'bg-red-500/20 text-red-400': finding.severity === 'critical',
                  'bg-orange-500/20 text-orange-400': finding.severity === 'high',
                  'bg-yellow-500/20 text-yellow-400': finding.severity === 'medium',
                  'bg-gray-500/20 text-gray-400': finding.severity === 'low'
                }">{{ finding.severity }}</span>
              </div>
              <p class="text-gray-300 text-sm mb-2">{{ finding.issue }}</p>
              <p class="text-xs text-gray-400">{{ finding.remediation }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Security Posture -->
      <div v-if="activeTool === 'posture'">
        <h2 class="text-xl font-semibold text-white mb-4">Security Posture</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div class="p-4 bg-slate-900/50 rounded-xl border border-white/10">
            <p class="text-sm text-gray-400">Average Score</p>
            <p class="text-3xl font-bold text-white">{{ postureData.average_score || 0 }}</p>
          </div>
          <div class="p-4 bg-slate-900/50 rounded-xl border border-white/10">
            <p class="text-sm text-gray-400">Total Scans</p>
            <p class="text-3xl font-bold text-white">{{ postureData.total_scans || 0 }}</p>
          </div>
          <div class="p-4 bg-slate-900/50 rounded-xl border border-white/10">
            <p class="text-sm text-gray-400">Trend</p>
            <p class="text-3xl font-bold" :class="{
              'text-green-400': postureData.trend === 'improving',
              'text-red-400': postureData.trend === 'declining',
              'text-yellow-400': postureData.trend === 'stable' || postureData.trend === 'insufficient_data'
            }">{{ postureData.trend || 'N/A' }}</p>
          </div>
        </div>
        
        <div v-if="postureData.historical_scores?.length" class="mb-4">
          <p class="text-sm text-gray-400 mb-2">Score History</p>
          <div class="flex items-end gap-1 h-24">
            <div 
              v-for="(score, idx) in postureData.historical_scores" 
              :key="idx"
              class="flex-1 bg-green-500 rounded-t"
              :style="{ height: `${score}%` }"
              :title="`Score: ${score}`"
            ></div>
          </div>
        </div>
      </div>

      <!-- Custom Rules -->
      <div v-if="activeTool === 'rules'">
        <h2 class="text-xl font-semibold text-white mb-4">Custom Rules</h2>
        
        <div class="mb-4">
          <label class="block text-sm text-gray-400 mb-2">Code to scan</label>
          <textarea 
            v-model="rulesCode" 
            class="w-full h-32 bg-slate-900/50 border border-white/10 rounded-xl p-4 text-white text-sm font-mono"
            placeholder="Paste code here..."
          ></textarea>
        </div>
        <button 
          @click="scanWithRules" 
          :disabled="rulesLoading"
          class="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-medium transition-colors disabled:opacity-50"
        >
          {{ rulesLoading ? 'Scanning...' : 'Scan with Custom Rules' }}
        </button>

        <div class="mt-6">
          <h3 class="text-lg font-medium text-white mb-3">Available Rules</h3>
          <div class="space-y-2">
            <div v-for="rule in availableRules" :key="rule.id" class="p-3 bg-slate-900/50 rounded-xl border border-white/10 flex items-center justify-between">
              <div>
                <p class="text-white font-medium">{{ rule.name }}</p>
                <p class="text-xs text-gray-400">{{ rule.description }}</p>
              </div>
              <span class="px-2 py-1 text-xs rounded-full" :class="{
                'bg-red-500/20 text-red-400': rule.severity === 'critical',
                'bg-orange-500/20 text-orange-400': rule.severity === 'high',
                'bg-yellow-500/20 text-yellow-400': rule.severity === 'medium',
                'bg-gray-500/20 text-gray-400': rule.severity === 'low'
              }">{{ rule.severity }}</span>
            </div>
          </div>
        </div>
        
        <div v-if="rulesResults.length" class="mt-6">
          <h3 class="text-lg font-medium text-white mb-3">Findings ({{ rulesResults.length }})</h3>
          <div class="space-y-2">
            <div v-for="(finding, idx) in rulesResults" :key="idx" class="p-3 bg-slate-900/50 rounded-xl border border-purple-500/30">
              <div class="flex items-center justify-between">
                <span class="text-white">{{ finding.rule_name }}</span>
                <span class="text-xs text-gray-400">Line {{ finding.line_number }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Compliance -->
      <div v-if="activeTool === 'compliance'">
        <h2 class="text-xl font-semibold text-white mb-4">Compliance Reports</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button 
            v-for="framework in ['SOC2', 'ISO27001', 'HIPAA', 'PCI-DSS']" 
            :key="framework"
            @click="generateCompliance(framework)"
            class="p-4 bg-slate-900/50 border border-white/10 rounded-xl hover:border-yellow-500/50 transition-colors"
          >
            <p class="text-white font-medium">{{ framework }}</p>
            <p class="text-xs text-gray-400">Generate Report</p>
          </button>
        </div>
      </div>

      <!-- Auto Remediation -->
      <div v-if="activeTool === 'remediation'">
        <h2 class="text-xl font-semibold text-white mb-4">Auto Remediation</h2>
        <p class="text-gray-400 mb-4">Available automatic fixes:</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div v-for="rule in remediationTypes" :key="rule.type" class="p-3 bg-slate-900/50 border border-white/10 rounded-xl">
            <div class="flex items-center justify-between">
              <span class="text-white font-medium">{{ rule.type }}</span>
              <span v-if="rule.can_auto_fix" class="px-2 py-1 text-xs bg-green-500/20 text-green-400 rounded-full">Auto-fix</span>
            </div>
            <p class="text-xs text-gray-400 mt-1">{{ rule.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const activeTool = ref('')
const API_URL = 'http://localhost:8003'

// Secrets
const secretPatterns = ref(0)
const secretsCode = ref('')
const secretsLoading = ref(false)
const secretsResults = ref<any[]>([])

// Cloud
const cloudProviders = ref(0)
const cloudProvider = ref('aws')
const cloudConfig = ref('')
const cloudLoading = ref(false)
const cloudResults = ref<any[]>([])

// Posture
const postureTrend = ref('insufficient_data')
const postureData = ref<any>({})

// Custom Rules
const customRulesCount = ref(0)
const availableRules = ref<any[]>([])
const rulesCode = ref('')
const rulesLoading = ref(false)
const rulesResults = ref<any[]>([])

// Remediation
const remediationRules = ref(0)
const remediationTypes = ref<any[]>([])

onMounted(async () => {
  // Load initial data
  try {
    const patternsRes = await fetch(`${API_URL}/api/v1/secrets/patterns`)
    const patternsData = await patternsRes.json()
    secretPatterns.value = patternsData.total_patterns || 0
    
    const providersRes = await fetch(`${API_URL}/api/v1/cloud/providers`)
    const providersData = await providersRes.json()
    cloudProviders.value = providersData.total || 0
    
    const postureRes = await fetch(`${API_URL}/api/v1/posture/trend`)
    postureData.value = await postureRes.json()
    postureTrend.value = postureData.value.trend || 'insufficient_data'
    
    const rulesRes = await fetch(`${API_URL}/api/v1/rules/`)
    availableRules.value = await rulesRes.json()
    customRulesCount.value = availableRules.value.length
    
    const remediRes = await fetch(`${API_URL}/api/v1/remediation/rules`)
    remediationTypes.value = await remediRes.json()
    remediationRules.value = remediationTypes.value.length
  } catch (e) {
    console.error('Failed to load initial data:', e)
  }
})

async function scanSecrets() {
  if (!secretsCode.value) return
  secretsLoading.value = true
  try {
    const res = await fetch(`${API_URL}/api/v1/secrets/scan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: secretsCode.value })
    })
    const data = await res.json()
    secretsResults.value = data.findings || []
  } catch (e) {
    console.error('Scan failed:', e)
  }
  secretsLoading.value = false
}

async function scanCloud() {
  if (!cloudConfig.value) return
  cloudLoading.value = true
  try {
    const res = await fetch(`${API_URL}/api/v1/cloud/scan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ config: cloudConfig.value, provider: cloudProvider.value })
    })
    const data = await res.json()
    cloudResults.value = data.findings || []
  } catch (e) {
    console.error('Scan failed:', e)
  }
  cloudLoading.value = false
}

async function scanWithRules() {
  if (!rulesCode.value) return
  rulesLoading.value = true
  try {
    const res = await fetch(`${API_URL}/api/v1/rules/scan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: rulesCode.value })
    })
    const data = await res.json()
    rulesResults.value = data.findings || []
  } catch (e) {
    console.error('Scan failed:', e)
  }
  rulesLoading.value = false
}

function generateCompliance(framework: string) {
  alert(`Generating ${framework} compliance report... (API endpoint: /api/v1/compliance/scan)`)
}
</script>
