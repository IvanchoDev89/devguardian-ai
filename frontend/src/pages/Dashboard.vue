<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="border-4 border-dashed border-gray-200 rounded-lg h-96 flex items-center justify-center">
      <div class="text-center">
        <h1 class="text-2xl font-bold text-gray-900 mb-4">DevGuardian AI Dashboard</h1>
        <p class="text-gray-600 mb-8">Welcome to your security command center</p>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 mb-2">Total Vulnerabilities</h3>
            <p class="text-3xl font-bold text-danger-600">0</p>
          </div>
          
          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 mb-2">Repositories</h3>
            <p class="text-3xl font-bold text-primary-600">0</p>
          </div>
          
          <div class="card">
            <h3 class="text-lg font-medium text-gray-900 mb-2">AI Fixes Generated</h3>
            <p class="text-3xl font-bold text-success-600">0</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Dashboard component logic will go here
</script>
