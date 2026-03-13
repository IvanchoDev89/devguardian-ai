<template>
  <div class="flex h-screen bg-slate-900">
    <NewSidebar />
    
    <!-- Main Content -->
    <main class="flex-1 overflow-auto">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import NewSidebar from '../components/Sidebar.vue'
</script>
