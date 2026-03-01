<template>
  <div class="scan-page">
    <header class="page-header">
      <h1>🔒 DevGuardian Vulnerability Scanner</h1>
      <p class="subtitle">AI-powered security analysis for your code</p>
      
      <!-- Service Status -->
      <div class="service-status">
        <span class="status-badge" :class="serviceStatus.class">
          {{ serviceStatus.text }}
        </span>
        <span v-if="llmStatus" class="status-badge llm" :class="llmStatus.api_configured ? 'active' : 'inactive'">
          LLM: {{ llmStatus.api_configured ? 'Ready' : 'Fallback mode' }}
        </span>
      </div>
    </header>

    <main class="page-content">
      <div class="scanner-container">
        <!-- Input Section -->
        <section class="input-section">
          <CodeInput 
            ref="codeInputRef"
            @analyze="handleAnalyze"
          />
        </section>

        <!-- Results Section -->
        <section class="results-section">
          <ResultsDisplay 
            :result="analysisResult"
            :loading="isLoading"
          />
          
          <!-- AI Analysis Button -->
          <div v-if="analysisResult?.vulnerabilities?.length > 0" class="ai-analysis-section">
            <button 
              class="btn-ai-analyze"
              :disabled="isAnalyzing"
              @click="analyzeWithLLM"
            >
              <span v-if="isAnalyzing" class="spinner"></span>
              <span v-else>🤖</span>
              {{ isAnalyzing ? 'Analyzing with AI...' : 'Get AI Fix Suggestions' }}
            </button>
          </div>

          <!-- AI Analysis Results -->
          <div v-if="llmAnalysis.length > 0" class="llm-results">
            <h3>🤖 AI Analysis</h3>
            <div 
              v-for="(analysis, index) in llmAnalysis" 
              :key="index"
              class="llm-analysis-card"
            >
              <div class="llm-header">
                <span class="vuln-type">{{ analysis.type }}</span>
                <span class="confidence" :class="getConfidenceClass(analysis.confidence)">
                  {{ Math.round(analysis.confidence * 100) }}% confidence
                </span>
              </div>
              <p class="llm-explanation">{{ analysis.explanation }}</p>
              <div v-if="analysis.suggested_fix" class="llm-fix">
                <h4>Suggested Fix:</h4>
                <pre><code>{{ analysis.suggested_fix }}</code></pre>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Recent Scans -->
      <section class="recent-scans" v-if="recentScans.length > 0">
        <h2>📊 Recent Scans</h2>
        <div class="scans-list">
          <div 
            v-for="scan in recentScans" 
            :key="scan.scan_id"
            class="scan-item"
            @click="loadScan(scan)"
          >
            <div class="scan-score" :class="getScoreClass(scan.score)">
              {{ scan.score }}
            </div>
            <div class="scan-info">
              <span class="scan-lang">{{ scan.language }}</span>
              <span class="scan-date">{{ formatDate(scan.timestamp) }}</span>
            </div>
            <div class="scan-count">
              {{ scan.total_vulnerabilities }} issues
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import CodeInput from '../components/CodeInput.vue'
import ResultsDisplay from '../components/ResultsDisplay.vue'
import { vulnerabilityScannerApi, llmAnalyzerApi } from '../services/api'

interface Vulnerability {
  line_number: number
  line_content: string
  vulnerability_type: string
  severity: string
  description: string
  match: string
  cwe_id?: string
}

interface AnalysisResult {
  vulnerabilities: Vulnerability[]
  summary: string
  score: number
  total_vulnerabilities: number
  language: string
  scan_id: string
  timestamp: string
}

interface LLMAnalysis {
  type: string
  explanation: string
  suggested_fix?: string
  confidence: number
}

const codeInputRef = ref<InstanceType<typeof CodeInput> | null>(null)
const isLoading = ref(false)
const isAnalyzing = ref(false)
const analysisResult = ref<AnalysisResult | null>(null)
const recentScans = ref<AnalysisResult[]>([])
const llmAnalysis = ref<LLMAnalysis[]>([])

const serviceStatus = ref({ text: 'Checking...', class: 'unknown' })
const llmStatus = ref<{ api_configured: boolean; provider: string } | null>(null)

onMounted(async () => {
  await checkServicesHealth()
})

const checkServicesHealth = async () => {
  try {
    const health = await vulnerabilityScannerApi.checkHealth()
    serviceStatus.value = {
      text: health.status === 'ok' ? '✅ Service Online' : '❌ Service Offline',
      class: health.status === 'ok' ? 'online' : 'offline'
    }
  } catch (error) {
    serviceStatus.value = {
      text: '❌ Service Unreachable',
      class: 'error'
    }
  }

  try {
    llmStatus.value = await llmAnalyzerApi.checkHealth()
  } catch (error) {
    llmStatus.value = { api_configured: false, provider: 'unknown' }
  }
}

const handleAnalyze = async (payload: { code: string; language: string }) => {
  isLoading.value = true
  analysisResult.value = null
  llmAnalysis.value = []
  
  try {
    const result = await vulnerabilityScannerApi.analyzeCode(payload.code, payload.language)
    analysisResult.value = result
    
    // Add to recent scans (keep last 5)
    recentScans.value = [result, ...recentScans.value].slice(0, 5)
  } catch (error) {
    console.error('Analysis failed:', error)
    if (codeInputRef.value) {
      codeInputRef.value.setError(error instanceof Error ? error.message : 'Analysis failed')
    }
  } finally {
    isLoading.value = false
    if (codeInputRef.value) {
      codeInputRef.value.setLoading(false)
    }
  }
}

const analyzeWithLLM = async () => {
  if (!analysisResult.value?.vulnerabilities?.length) return

  isAnalyzing.value = true
  llmAnalysis.value = []

  try {
    const vulnerabilities = analysisResult.value.vulnerabilities.map(v => ({
      type: v.vulnerability_type.toLowerCase().replace(/\s+/g, '-'),
      severity: v.severity,
      message: v.description,
      line_content: v.line_content
    }))

    // Analyze each vulnerability
    for (const vuln of vulnerabilities) {
      try {
        const result = await llmAnalyzerApi.analyzeVulnerability(
          vuln,
          vuln.line_content || '',
          analysisResult.value.language,
          true
        )
        llmAnalysis.value.push({
          type: vuln.type,
          explanation: result.explanation,
          suggested_fix: result.suggested_fix,
          confidence: result.confidence
        })
      } catch (error) {
        console.error('LLM analysis failed for:', vuln.type, error)
      }
    }
  } catch (error) {
    console.error('Batch LLM analysis failed:', error)
  } finally {
    isAnalyzing.value = false
  }
}

const loadScan = (scan: AnalysisResult) => {
  analysisResult.value = scan
  llmAnalysis.value = []
}

const getScoreClass = (score: number) => {
  if (score >= 80) return 'good'
  if (score >= 50) return 'medium'
  return 'poor'
}

const getConfidenceClass = (confidence: number) => {
  if (confidence >= 0.8) return 'high'
  if (confidence >= 0.5) return 'medium'
  return 'low'
}

const formatDate = (timestamp: string) => {
  return new Date(timestamp).toLocaleDateString()
}
</script>

<style scoped>
.scan-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.subtitle {
  color: #6b7280;
  margin-top: 0.5rem;
}

.service-status {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.online { background: #d1fae5; color: #065f46; }
.status-badge.offline { background: #fee2e2; color: #991b1b; }
.status-badge.unknown { background: #f3f4f6; color: #6b7280; }
.status-badge.active { background: #dbeafe; color: #1e40af; }
.status-badge.inactive { background: #fef3c7; color: #92400e; }

.scanner-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 1024px) {
  .scanner-container {
    grid-template-columns: 1fr 1fr;
  }
}

.input-section,
.results-section {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.ai-analysis-section {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.btn-ai-analyze {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #7c3aed, #5b21b6);
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: background 0.2s;
}

.btn-ai-analyze:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d28d9, #4c1d95);
}

.btn-ai-analyze:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.llm-results {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.llm-results h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 1rem;
}

.llm-analysis-card {
  background: #f9fafb;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.llm-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.vuln-type {
  font-weight: 600;
  color: #111827;
  text-transform: capitalize;
}

.confidence {
  font-size: 0.75rem;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
}

.confidence.high { background: #d1fae5; color: #065f46; }
.confidence.medium { background: #fef3c7; color: #92400e; }
.confidence.low { background: #fee2e2; color: #991b1b; }

.llm-explanation {
  color: #4b5563;
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
}

.llm-fix {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
}

.llm-fix h4 {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  margin: 0 0 0.5rem 0;
}

.llm-fix pre {
  background: #1f2937;
  color: #e5e7eb;
  padding: 0.75rem;
  border-radius: 0.375rem;
  overflow-x: auto;
  font-size: 0.75rem;
}

.llm-fix code {
  font-family: 'Fira Code', monospace;
}

.recent-scans {
  margin-top: 2rem;
}

.recent-scans h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 1rem;
}

.scans-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.scan-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: white;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.scan-item:hover {
  background-color: #f9fafb;
}

.scan-score {
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  font-weight: 700;
  font-size: 1.25rem;
  color: white;
}

.scan-score.good { background: linear-gradient(135deg, #10b981, #059669); }
.scan-score.medium { background: linear-gradient(135deg, #f59e0b, #d97706); }
.scan-score.poor { background: linear-gradient(135deg, #ef4444, #dc2626); }

.scan-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.scan-lang {
  font-weight: 500;
  color: #111827;
  text-transform: capitalize;
}

.scan-date {
  font-size: 0.75rem;
  color: #6b7280;
}

.scan-count {
  font-size: 0.875rem;
  color: #6b7280;
}

.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
