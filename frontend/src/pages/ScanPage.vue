<template>
  <div class="scan-page">
    <header class="page-header">
      <h1>🔍 Vulnerability Scanner</h1>
      <p class="subtitle">Paste your code and discover security issues</p>
      
      <div class="service-status">
        <span class="status-badge" :class="serviceStatus.class">
          {{ serviceStatus.text }}
        </span>
      </div>
    </header>

    <main class="page-content">
      <!-- Input -->
      <section class="input-section">
        <div class="language-selector">
          <label>Language:</label>
          <select v-model="selectedLanguage">
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="typescript">TypeScript</option>
            <option value="java">Java</option>
            <option value="php">PHP</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
            <option value="csharp">C#</option>
          </select>
        </div>

        <textarea
          v-model="code"
          class="code-textarea"
          :disabled="isLoading"
          placeholder="// Paste your code here...
Example:
password = 'my_password'
query = f'SELECT * FROM users WHERE id = {user_id}'"
          rows="10"
          spellcheck="false"
        ></textarea>
        
        <div class="actions">
          <button class="btn-scan" :disabled="isLoading || !code.trim()" @click="handleAnalyze">
            <span v-if="isLoading" class="spinner"></span>
            <span v-else>🔍</span>
            {{ isLoading ? 'Analyzing...' : 'Scan' }}
          </button>
          <button class="btn-clear" @click="clearCode">Clear</button>
        </div>

        <div v-if="error" class="error">{{ error }}</div>
      </section>

      <!-- Results -->
      <section class="results-section">
        <!-- Score -->
        <div v-if="analysisResult" class="score-card" :class="scoreClass">
          <div class="score-value">{{ analysisResult.score }}</div>
          <div class="score-label">Security Score</div>
        </div>

        <!-- Summary -->
        <div v-if="analysisResult?.summary" class="summary">
          {{ analysisResult.summary }}
        </div>

        <!-- Vulns -->
        <div v-if="analysisResult?.vulnerabilities?.length" class="vulns-section">
          <div class="vulns-header">
            <h3>📋 {{ analysisResult.vulnerabilities.length }} Vulnerabilities Found</h3>
            <button class="btn-ai" :disabled="isAnalyzing" @click="analyzeWithLLM">
              {{ isAnalyzing ? '...' : '🤖 AI Fix' }}
            </button>
          </div>
          
          <div class="vuln-list">
            <div v-for="(v, i) in analysisResult.vulnerabilities" :key="i" class="vuln-card" :class="v.severity">
              <div class="vuln-top">
                <span class="severity" :class="v.severity">{{ v.severity.toUpperCase() }}</span>
                <span class="line">L{{ v.line_number }}</span>
              </div>
              <div class="vuln-type">{{ v.vulnerability_type }}</div>
              <div class="vuln-desc">{{ v.description }}</div>
            </div>
          </div>
        </div>

        <!-- AI Results -->
        <div v-if="llmResults.length" class="ai-section">
          <h3>🤖 AI Analysis</h3>
          <div v-for="(r, i) in llmResults" :key="i" class="ai-card">
            <p>{{ r.explanation }}</p>
          </div>
        </div>

        <!-- No vulns -->
        <div v-if="analysisResult && !analysisResult.vulnerabilities.length" class="no-vulns">
          <div class="check">✅</div>
          <h3>Code is Secure!</h3>
        </div>

        <!-- Loading -->
        <div v-if="isLoading" class="loading">
          <div class="spinner-lg"></div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { vulnerabilityScannerApi, llmAnalyzerApi } from '../services/api'

const code = ref('')
const selectedLanguage = ref('python')
const isLoading = ref(false)
const isAnalyzing = ref(false)
const error = ref('')
const analysisResult = ref<any>(null)
const llmResults = ref<any[]>([])
const serviceStatus = ref({ text: '...', class: '' })

onMounted(async () => {
  try {
    const h = await vulnerabilityScannerApi.checkHealth()
    serviceStatus.value = { text: h.status === 'ok' ? '✅ Online' : '❌ Offline', class: h.status === 'ok' ? 'online' : 'offline' }
  } catch { serviceStatus.value = { text: '❌ Error', class: 'error' } }
})

const scoreClass = computed(() => {
  if (!analysisResult.value) return ''
  if (analysisResult.value.score >= 80) return 'good'
  if (analysisResult.value.score >= 50) return 'medium'
  return 'poor'
})

async function handleAnalyze() {
  error.value = ''
  llmResults.value = []
  if (!code.value.trim()) { error.value = 'Please enter code'; return }
  isLoading.value = true
  try {
    analysisResult.value = await vulnerabilityScannerApi.analyzeCode(code.value, selectedLanguage.value)
  } catch (e) { error.value = String(e) }
  finally { isLoading.value = false }
}

async function analyzeWithLLM() {
  if (!analysisResult.value?.vulnerabilities?.length) return
  isAnalyzing.value = true
  llmResults.value = []
  for (const v of analysisResult.value.vulnerabilities) {
    try {
      const r = await llmAnalyzerApi.analyzeVulnerability(
        { type: v.vulnerability_type.toLowerCase(), severity: v.severity, message: v.description },
        v.description, selectedLanguage.value, true
      )
      llmResults.value.push(r)
    } catch {}
  }
  isAnalyzing.value = false
}

function clearCode() { code.value = ''; error.value = ''; analysisResult.value = null; llmResults.value = [] }
</script>

<style scoped>
.scan-page { max-width: 1200px; margin: 0 auto; padding: 2rem; }
.page-header { text-align: center; margin-bottom: 2rem; }
.page-header h1 { font-size: 1.75rem; font-weight: 700; color: #111827; margin: 0; }
.subtitle { color: #6b7280; margin-top: 0.5rem; }
.service-status { margin-top: 1rem; }
.status-badge { padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; }
.status-badge.online { background: #d1fae5; color: #065f46; }
.status-badge.error { background: #fee2e2; color: #991b1b; }

.page-content { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
@media (max-width: 1024px) { .page-content { grid-template-columns: 1fr; } }

.input-section, .results-section { background: white; border-radius: 0.75rem; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }

.language-selector { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.language-selector label { font-weight: 500; }
.language-selector select { padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 0.375rem; }

.code-textarea { width: 100%; font-family: 'Fira Code', monospace; font-size: 0.875rem; padding: 1rem; border: 1px solid #d1d5db; border-radius: 0.5rem; background: #1e1e1e; color: #d4d4d4; line-height: 1.5; resize: vertical; }
.code-textarea:focus { outline: none; border-color: #3b82f6; }

.actions { display: flex; gap: 1rem; margin-top: 1rem; }
.btn-scan { flex: 1; padding: 0.75rem; background: linear-gradient(135deg, #3b82f6, #06b6d4); color: white; border: none; border-radius: 0.5rem; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
.btn-scan:disabled { opacity: 0.6; }
.btn-clear { padding: 0.75rem 1.5rem; background: white; border: 1px solid #d1d5db; border-radius: 0.5rem; cursor: pointer; }
.error { margin-top: 1rem; padding: 0.75rem; background: #fef2f2; color: #dc2626; border-radius: 0.5rem; font-size: 0.875rem; }

.score-card { padding: 1.5rem; border-radius: 0.75rem; text-align: center; color: white; margin-bottom: 1rem; }
.score-card.good { background: linear-gradient(135deg, #10b981, #059669); }
.score-card.medium { background: linear-gradient(135deg, #f59e0b, #d97706); }
.score-card.poor { background: linear-gradient(135deg, #ef4444, #dc2626); }
.score-value { font-size: 3rem; font-weight: 700; }
.score-label { font-size: 0.875rem; opacity: 0.9; }

.summary { padding: 1rem; background: #f9fafb; border-radius: 0.5rem; border-left: 4px solid #3b82f6; font-size: 0.875rem; color: #4b5563; margin-bottom: 1rem; }

.vulns-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.vulns-header h3 { margin: 0; font-size: 1rem; }
.btn-ai { padding: 0.5rem 1rem; background: linear-gradient(135deg, #7c3aed, #5b21b6); color: white; border: none; border-radius: 0.375rem; font-size: 0.875rem; cursor: pointer; }

.vuln-list { display: flex; flex-direction: column; gap: 0.75rem; }
.vuln-card { padding: 1rem; border-radius: 0.5rem; border-left: 4px solid; }
.vuln-card.critical { background: #fef2f2; border-color: #dc2626; }
.vuln-card.high { background: #fff7ed; border-color: #ea580c; }
.vuln-card.medium { background: #fefce8; border-color: #ca8a04; }
.vuln-card.low { background: #f0fdf4; border-color: #16a34a; }

.vuln-top { display: flex; justify-content: space-between; margin-bottom: 0.5rem; }
.severity { font-size: 0.625rem; font-weight: 700; padding: 0.125rem 0.375rem; border-radius: 0.25rem; }
.severity.critical { background: #dc2626; color: white; }
.severity.high { background: #ea580c; color: white; }
.severity.medium { background: #ca8a04; color: white; }
.severity.low { background: #16a34a; color: white; }
.line { font-size: 0.75rem; color: #6b7280; }
.vuln-type { font-weight: 600; color: #111827; margin-bottom: 0.25rem; }
.vuln-desc { font-size: 0.875rem; color: #4b5563; }

.ai-section { margin-top: 1.5rem; border-top: 1px solid #e5e7eb; padding-top: 1rem; }
.ai-section h3 { margin: 0 0 1rem 0; font-size: 1rem; }
.ai-card { background: #f9fafb; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.75rem; font-size: 0.875rem; color: #4b5563; }

.no-vulns { text-align: center; padding: 2rem; }
.no-vulns .check { font-size: 3rem; }
.no-vulns h3 { margin: 0.5rem 0; color: #065f46; }

.loading { text-align: center; padding: 2rem; }
.spinner { width: 1rem; height: 1rem; border: 2px solid white; border-top-color: transparent; border-radius: 50%; animation: spin 0.8s linear infinite; }
.spinner-lg { width: 2rem; height: 2rem; border: 3px solid #e5e7eb; border-top-color: #3b82f6; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
