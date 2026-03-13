<template>
  <div class="flex h-screen bg-slate-900">
    <Sidebar />
    
    <!-- Main Content -->
    <main class="flex-1 overflow-auto bg-slate-900">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '../components/Sidebar.vue'
</script>
