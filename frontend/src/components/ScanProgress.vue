<template>
  <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-white">Scan Progress</h3>
      <span class="text-sm text-gray-400">{{ progress.percentage }}%</span>
    </div>
    
    <!-- Progress Bar -->
    <div class="w-full bg-white/10 rounded-full h-3 mb-4 overflow-hidden">
      <div 
        class="h-full bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full transition-all duration-500 ease-out"
        :style="{ width: progress.percentage + '%' }"
      >
        <div class="h-full bg-white/20 animate-pulse"></div>
      </div>
    </div>
    
    <!-- Current Status -->
    <div class="flex items-center justify-between text-sm">
      <div class="flex items-center">
        <div class="w-2 h-2 rounded-full mr-2" :class="getStatusColor()"></div>
        <span class="text-gray-300">{{ progress.currentFile }}</span>
      </div>
      <span class="text-gray-400">{{ progress.filesScanned }} / {{ progress.totalFiles }} files</span>
    </div>
    
    <!-- Vulnerabilities Found -->
    <div v-if="progress.vulnerabilitiesFound > 0" class="mt-4 p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>
        <span class="text-red-400 font-medium">{{ progress.vulnerabilitiesFound }} vulnerabilities found</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const progress = ref({
  percentage: 0,
  currentFile: 'Initializing scan...',
  filesScanned: 0,
  totalFiles: 0,
  vulnerabilitiesFound: 0,
  status: 'idle' // idle, scanning, completed, error
})

let interval: number | null = null

const startScan = () => {
  progress.value = {
    percentage: 0,
    currentFile: 'app.js',
    filesScanned: 0,
    totalFiles: 45,
    vulnerabilitiesFound: 0,
    status: 'scanning'
  }
  
  interval = setInterval(() => {
    if (progress.value.percentage < 100) {
      progress.value.percentage += Math.random() * 15
      progress.value.filesScanned = Math.floor((progress.value.percentage / 100) * progress.value.totalFiles)
      
      // Simulate finding vulnerabilities
      if (Math.random() > 0.7 && progress.value.vulnerabilitiesFound === 0) {
        progress.value.vulnerabilitiesFound = Math.floor(Math.random() * 3) + 1
      }
      
      // Update current file
      const files = ['app.js', 'utils.js', 'config.js', 'database.js', 'auth.js', 'api.js']
      progress.value.currentFile = files[Math.floor(Math.random() * files.length)]
      
      if (progress.value.percentage >= 100) {
        progress.value.percentage = 100
        progress.value.status = 'completed'
        progress.value.currentFile = 'Scan completed'
        clearInterval(interval!)
      }
    }
  }, 500)
}

const getStatusColor = () => {
  switch (progress.value.status) {
    case 'scanning': return 'bg-blue-400 animate-pulse'
    case 'completed': return 'bg-green-400'
    case 'error': return 'bg-red-400'
    default: return 'bg-gray-400'
  }
}

onMounted(() => {
  // Auto-start scan after 2 seconds
  setTimeout(startScan, 2000)
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})

defineExpose({
  startScan
})
</script>
