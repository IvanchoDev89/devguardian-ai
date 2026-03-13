<template>
  <div class="flex min-h-screen bg-slate-900">
    <!-- Sidebar -->
    <aside class="fixed inset-y-0 left-0 w-72 bg-slate-900/95 backdrop-blur-xl border-r border-white/10 z-40 flex flex-col">
      <Sidebar />
    </aside>
    
    <!-- Main Content with left margin -->
    <div class="ml-72 flex-1 min-h-screen">
      <main class="p-6 overflow-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '../components/Sidebar.vue'
</script>
