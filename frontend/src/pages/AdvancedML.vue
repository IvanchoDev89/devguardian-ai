<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-lg shadow p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-2">Advanced ML Dashboard</h1>
      <p class="text-gray-600">Monitor and manage steroids-level machine learning capabilities</p>
    </div>

    <!-- ML Capabilities Overview -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">Transformer Models</h3>
            <p class="text-sm text-gray-500">94-97% Accuracy</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">Real-time Processing</h3>
            <p class="text-sm text-gray-500">&lt; 100ms Latency</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">Ensemble Detection</h3>
            <p class="text-sm text-gray-500">Multi-Model Analysis</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Advanced Scan Section -->
    <div class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-medium text-gray-900">Advanced Security Scan</h2>
      </div>
      <div class="p-6">
        <form @submit.prevent="runAdvancedScan" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Code to Analyze</label>
            <textarea
              v-model="scanForm.code"
              rows="8"
              class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Paste your code here for advanced ML analysis..."
            ></textarea>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Language</label>
              <select v-model="scanForm.language" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="php">PHP</option>
                <option value="java">Java</option>
                <option value="csharp">C#</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Scan Mode</label>
              <select v-model="scanForm.scanMode" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="quick">Quick Scan</option>
                <option value="comprehensive">Comprehensive</option>
                <option value="deep">Deep Analysis</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Confidence Threshold</label>
              <input
                v-model.number="scanForm.confidenceThreshold"
                type="number"
                min="0"
                max="1"
                step="0.1"
                class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          
          <div class="flex items-center space-x-4">
            <label class="flex items-center">
              <input v-model="scanForm.includeFixes" type="checkbox" class="mr-2" />
              <span class="text-sm text-gray-700">Generate AI Fixes</span>
            </label>
            <label class="flex items-center">
              <input v-model="scanForm.enableEnsemble" type="checkbox" class="mr-2" />
              <span class="text-sm text-gray-700">Enable Ensemble Detection</span>
            </label>
          </div>
          
          <button
            type="submit"
            :disabled="isScanning"
            class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {{ isScanning ? 'Scanning...' : 'Run Advanced Scan' }}
          </button>
        </form>
      </div>
    </div>

    <!-- Scan Results -->
    <div v-if="scanResults" class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-medium text-gray-900">Scan Results</h2>
      </div>
      <div class="p-6">
        <!-- Performance Metrics -->
        <div class="mb-6">
          <h3 class="text-md font-medium text-gray-900 mb-3">Performance Metrics</h3>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-gray-50 p-3 rounded">
              <p class="text-sm text-gray-600">Processing Time</p>
              <p class="text-lg font-semibold">{{ scanResults.performance_metrics?.total_processing_time || 'N/A' }}s</p>
            </div>
            <div class="bg-gray-50 p-3 rounded">
              <p class="text-sm text-gray-600">Ensemble Confidence</p>
              <p class="text-lg font-semibold">{{ (scanResults.ensemble_detection?.ensemble_confidence * 100).toFixed(1) }}%</p>
            </div>
            <div class="bg-gray-50 p-3 rounded">
              <p class="text-sm text-gray-600">Vulnerabilities Found</p>
              <p class="text-lg font-semibold">{{ scanResults.vulnerabilities?.length || 0 }}</p>
            </div>
            <div class="bg-gray-50 p-3 rounded">
              <p class="text-sm text-gray-600">Anomaly Score</p>
              <p class="text-lg font-semibold">{{ scanResults.ensemble_detection?.anomaly_score?.toFixed(2) || 'N/A' }}</p>
            </div>
          </div>
        </div>

        <!-- Vulnerabilities -->
        <div v-if="scanResults.vulnerabilities && scanResults.vulnerabilities.length > 0">
          <h3 class="text-md font-medium text-gray-900 mb-3">Detected Vulnerabilities</h3>
          <div class="space-y-3">
            <div
              v-for="(vuln, index) in scanResults.vulnerabilities"
              :key="index"
              class="border rounded-lg p-4"
              :class="{
                'border-red-300 bg-red-50': vuln.severity === 'critical',
                'border-orange-300 bg-orange-50': vuln.severity === 'high',
                'border-yellow-300 bg-yellow-50': vuln.severity === 'medium',
                'border-gray-300 bg-gray-50': vuln.severity === 'low'
              }"
            >
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-medium text-gray-900">{{ vuln.type.replace('_', ' ').toUpperCase() }}</h4>
                  <p class="text-sm text-gray-600 mt-1">{{ vuln.description }}</p>
                  <p class="text-xs text-gray-500 mt-2">Line {{ vuln.line }} • Confidence: {{ (vuln.confidence * 100).toFixed(1) }}%</p>
                </div>
                <span
                  class="px-2 py-1 text-xs font-medium rounded"
                  :class="{
                    'bg-red-100 text-red-800': vuln.severity === 'critical',
                    'bg-orange-100 text-orange-800': vuln.severity === 'high',
                    'bg-yellow-100 text-yellow-800': vuln.severity === 'medium',
                    'bg-gray-100 text-gray-800': vuln.severity === 'low'
                  }"
                >
                  {{ vuln.severity.toUpperCase() }}
                </span>
              </div>
              <div class="mt-3">
                <code class="text-sm bg-gray-100 p-2 rounded block">{{ vuln.code_snippet }}</code>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-8 text-gray-500">
          No vulnerabilities detected
        </div>
      </div>
    </div>

    <!-- Model Performance -->
    <div class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-medium text-gray-900">Model Performance Analytics</h2>
      </div>
      <div class="p-6">
        <button
          @click="loadModelPerformance"
          :disabled="isLoadingPerformance"
          class="bg-green-600 text-white px-6 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 mb-4"
        >
          {{ isLoadingPerformance ? 'Loading...' : 'Load Performance Data' }}
        </button>
        
        <div v-if="performanceData" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 class="text-md font-medium text-gray-900 mb-3">Accuracy Comparison</h3>
              <div class="space-y-2">
                <div v-for="(accuracy, model) in performanceData.comparison.accuracy" :key="model" class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 capitalize">{{ model.replace('_', ' ') }}</span>
                  <div class="flex items-center">
                    <div class="w-32 bg-gray-200 rounded-full h-2 mr-2">
                      <div class="bg-blue-600 h-2 rounded-full" :style="{ width: `${accuracy * 100}%` }"></div>
                    </div>
                    <span class="text-sm font-medium">{{ (accuracy * 100).toFixed(1) }}%</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="text-md font-medium text-gray-900 mb-3">Best Performing Models</h3>
              <div class="space-y-3">
                <div class="bg-green-50 p-3 rounded border border-green-200">
                  <p class="text-sm font-medium text-green-900">Highest Accuracy</p>
                  <p class="text-lg font-bold text-green-900">{{ performanceData.best_models.accuracy.model }}</p>
                  <p class="text-sm text-green-700">{{ (performanceData.best_models.accuracy.score * 100).toFixed(1) }}%</p>
                </div>
                <div class="bg-blue-50 p-3 rounded border border-blue-200">
                  <p class="text-sm font-medium text-blue-900">Best ROC AUC</p>
                  <p class="text-lg font-bold text-blue-900">{{ performanceData.best_models.roc_auc.model }}</p>
                  <p class="text-sm text-blue-700">{{ (performanceData.best_models.roc_auc.score * 100).toFixed(1) }}%</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiService } from '../services/api'

interface ScanForm {
  code: string
  language: string
  scanMode: string
  confidenceThreshold: number
  includeFixes: boolean
  enableEnsemble: boolean
}

interface ScanResults {
  vulnerabilities: Array<{
    type: string
    severity: string
    confidence: number
    line: number
    code_snippet: string
    description: string
  }>
  ensemble_detection: {
    ensemble_confidence: number
    anomaly_score: number
  }
  performance_metrics: {
    total_processing_time: number
  }
}

interface PerformanceData {
  comparison: {
    accuracy: Record<string, number>
    roc_auc: Record<string, number>
  }
  best_models: {
    accuracy: { model: string; score: number }
    roc_auc: { model: string; score: number }
  }
}

const scanForm = ref<ScanForm>({
  code: '',
  language: 'python',
  scanMode: 'comprehensive',
  confidenceThreshold: 0.7,
  includeFixes: true,
  enableEnsemble: true
})

const isScanning = ref(false)
const scanResults = ref<ScanResults | null>(null)
const isLoadingPerformance = ref(false)
const performanceData = ref<PerformanceData | null>(null)

const runAdvancedScan = async () => {
  if (!scanForm.value.code.trim()) {
    alert('Please enter code to analyze')
    return
  }

  isScanning.value = true
  try {
    const response = await apiService.post('/api/advanced-ml/advanced-scan', scanForm.value)
    scanResults.value = response.data.results
  } catch (error) {
    console.error('Advanced scan error:', error)
    alert('Failed to run advanced scan. Please try again.')
  } finally {
    isScanning.value = false
  }
}

const loadModelPerformance = async () => {
  isLoadingPerformance.value = true
  try {
    const response = await apiService.get('/api/advanced-ml/model-performance')
    performanceData.value = response.data.performance_comparison
  } catch (error) {
    console.error('Performance data error:', error)
    alert('Failed to load performance data. Please try again.')
  } finally {
    isLoadingPerformance.value = false
  }
}

onMounted(() => {
  // Load initial data
})
</script>
