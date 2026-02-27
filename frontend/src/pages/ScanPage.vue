<template>
  <div class="scan-page">
    <header class="page-header">
      <h1>Code Vulnerability Scanner</h1>
      <p class="subtitle">Analyze your code for security vulnerabilities</p>
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
        </section>
      </div>

      <!-- Recent Scans -->
      <section class="recent-scans" v-if="recentScans.length > 0">
        <h2>Recent Scans</h2>
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
import { ref } from 'vue'
import CodeInput from '../components/CodeInput.vue'
import ResultsDisplay from '../components/ResultsDisplay.vue'
import { vulnerabilityScannerApi } from '../services/api'

interface AnalysisResult {
  vulnerabilities: any[]
  summary: string
  score: number
  total_vulnerabilities: number
  language: string
  scan_id: string
  timestamp: string
}

const codeInputRef = ref<InstanceType<typeof CodeInput> | null>(null)
const isLoading = ref(false)
const analysisResult = ref<AnalysisResult | null>(null)
const recentScans = ref<AnalysisResult[]>([])

const handleAnalyze = async (payload: { code: string; language: string }) => {
  isLoading.value = true
  analysisResult.value = null
  
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

const loadScan = (scan: AnalysisResult) => {
  analysisResult.value = scan
}

const getScoreClass = (score: number) => {
  if (score >= 80) return 'good'
  if (score >= 50) return 'medium'
  return 'poor'
}

const formatDate = (timestamp: string) => {
  return new Date(timestamp).toLocaleDateString()
}
</script>

<style scoped>
.scan-page {
  max-width: 1200px;
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

.scan-score.good {
  background: linear-gradient(135deg, #10b981, #059669);
}

.scan-score.medium {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.scan-score.poor {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

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
</style>
