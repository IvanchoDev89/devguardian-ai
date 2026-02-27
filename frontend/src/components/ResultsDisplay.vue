<template>
  <div class="results-display">
    <!-- Score Card -->
    <div class="score-card" :class="scoreClass">
      <div class="score-value">{{ result?.score ?? 0 }}</div>
      <div class="score-label">Security Score</div>
      <div class="score-details">
        <span class="critical" v-if="severityCounts.critical > 0">
          {{ severityCounts.critical }} Critical
        </span>
        <span class="high" v-if="severityCounts.high > 0">
          {{ severityCounts.high }} High
        </span>
        <span class="medium" v-if="severityCounts.medium > 0">
          {{ severityCounts.medium }} Medium
        </span>
        <span class="low" v-if="severityCounts.low > 0">
          {{ severityCounts.low }} Low
        </span>
      </div>
    </div>

    <!-- Summary -->
    <div class="summary" v-if="result?.summary">
      <h3>Analysis Summary</h3>
      <p>{{ result.summary }}</p>
    </div>

    <!-- Vulnerabilities Table -->
    <div class="vulnerabilities-section" v-if="result?.vulnerabilities?.length > 0">
      <h3>Found Vulnerabilities ({{ result.vulnerabilities.length }})</h3>
      
      <div class="table-container">
        <table class="vulnerabilities-table">
          <thead>
            <tr>
              <th>Line</th>
              <th>Type</th>
              <th>Severity</th>
              <th>Description</th>
              <th>CWE</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="(vuln, index) in result.vulnerabilities" 
              :key="index"
              :class="`severity-${vuln.severity}`"
            >
              <td class="line-number">{{ vuln.line_number }}</td>
              <td class="type">{{ vuln.vulnerability_type }}</td>
              <td>
                <span class="severity-badge" :class="vuln.severity">
                  {{ vuln.severity.toUpperCase() }}
                </span>
              </td>
              <td class="description">{{ vuln.description }}</td>
              <td class="cwe">
                <a 
                  v-if="vuln.cwe_id" 
                  :href="`https://cwe.mitre.org/data/definitions/${vuln.cwe_id.replace('CWE-', '')}.html`"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {{ vuln.cwe_id }}
                </a>
                <span v-else>-</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- No Vulnerabilities -->
    <div class="no-vulnerabilities" v-else-if="result">
      <div class="success-icon">✓</div>
      <h3>No Vulnerabilities Found!</h3>
      <p>Your code looks secure based on our analysis.</p>
    </div>

    <!-- Loading State -->
    <div class="loading-state" v-if="loading">
      <div class="spinner"></div>
      <p>Analyzing your code...</p>
    </div>

    <!-- Scan Info -->
    <div class="scan-info" v-if="result?.scan_id">
      <span>Scan ID: {{ result.scan_id }}</span>
      <span>Language: {{ result.language }}</span>
      <span>{{ formatDate(result.timestamp) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Vulnerability {
  line_number: number
  line_content: string
  vulnerability_type: string
  severity: string
  description: string
  match: string
  cwe_id?: string
  owasp_category?: string
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

const props = defineProps<{
  result?: AnalysisResult | null
  loading?: boolean
}>()

const severityCounts = computed(() => {
  if (!props.result?.vulnerabilities) {
    return { critical: 0, high: 0, medium: 0, low: 0 }
  }
  
  return props.result.vulnerabilities.reduce((acc, vuln) => {
    const severity = vuln.severity.toLowerCase()
    if (severity in acc) {
      acc[severity as keyof typeof acc]++
    }
    return acc
  }, { critical: 0, high: 0, medium: 0, low: 0 })
})

const scoreClass = computed(() => {
  if (!props.result) return ''
  const score = props.result.score
  if (score >= 80) return 'good'
  if (score >= 50) return 'medium'
  return 'poor'
})

const formatDate = (timestamp: string) => {
  return new Date(timestamp).toLocaleString()
}
</script>

<style scoped>
.results-display {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.score-card {
  padding: 1.5rem;
  border-radius: 0.5rem;
  text-align: center;
  color: white;
}

.score-card.good {
  background: linear-gradient(135deg, #10b981, #059669);
}

.score-card.medium {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.score-card.poor {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.score-value {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1;
}

.score-label {
  font-size: 0.875rem;
  opacity: 0.9;
  margin-top: 0.25rem;
}

.score-details {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 0.75rem;
  font-size: 0.75rem;
}

.score-details span {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  background: rgba(255,255,255,0.2);
}

.summary {
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 0.375rem;
  border-left: 4px solid #3b82f6;
}

.summary h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: #111827;
}

.summary p {
  margin: 0;
  color: #4b5563;
  font-size: 0.875rem;
}

.vulnerabilities-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.125rem;
  color: #111827;
}

.table-container {
  overflow-x: auto;
}

.vulnerabilities-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.vulnerabilities-table th,
.vulnerabilities-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.vulnerabilities-table th {
  background-color: #f9fafb;
  font-weight: 600;
  color: #374151;
}

.vulnerabilities-table tr:hover {
  background-color: #f9fafb;
}

.severity-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.severity-badge.critical {
  background-color: #fef2f2;
  color: #dc2626;
}

.severity-badge.high {
  background-color: #fff7ed;
  color: #ea580c;
}

.severity-badge.medium {
  background-color: #fefce8;
  color: #ca8a04;
}

.severity-badge.low {
  background-color: #f0fdf4;
  color: #16a34a;
}

.line-number {
  font-family: monospace;
  color: #6b7280;
}

.type {
  font-weight: 500;
  color: #111827;
}

.description {
  color: #4b5563;
  max-width: 300px;
}

.cwe a {
  color: #3b82f6;
  text-decoration: none;
}

.cwe a:hover {
  text-decoration: underline;
}

.no-vulnerabilities {
  text-align: center;
  padding: 2rem;
  background-color: #f0fdf4;
  border-radius: 0.5rem;
}

.success-icon {
  font-size: 3rem;
  color: #10b981;
}

.no-vulnerabilities h3 {
  margin: 0.5rem 0;
  color: #065f46;
}

.no-vulnerabilities p {
  margin: 0;
  color: #047857;
}

.loading-state {
  text-align: center;
  padding: 2rem;
}

.loading-state .spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto;
}

.loading-state p {
  margin-top: 1rem;
  color: #6b7280;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.scan-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #9ca3af;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}
</style>
