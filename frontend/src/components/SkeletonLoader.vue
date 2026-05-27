<template>
  <div class="animate-pulse">
    <div class="bg-slate-800/50 rounded-xl border border-white/10 p-5">
      <div v-if="type === 'card'">
        <div class="h-4 bg-slate-700 rounded w-1/3 mb-3"></div>
        <div class="h-20 bg-slate-700 rounded"></div>
      </div>
      <div v-else-if="type === 'list'">
        <div v-for="i in count" :key="i" class="flex items-center gap-4 mb-4">
          <div class="w-10 h-10 bg-slate-700 rounded-lg"></div>
          <div class="flex-1">
            <div class="h-3 bg-slate-700 rounded w-1/2 mb-2"></div>
            <div class="h-2 bg-slate-700 rounded w-1/3"></div>
          </div>
        </div>
      </div>
      <div v-else-if="type === 'stats'">
        <div class="grid grid-cols-4 gap-4">
          <div v-for="i in 4" :key="i">
            <div class="h-3 bg-slate-700 rounded w-1/2 mb-2"></div>
            <div class="h-8 bg-slate-700 rounded"></div>
          </div>
        </div>
      </div>
      <div v-else>
        <div class="h-4 bg-slate-700 rounded w-1/3 mb-3"></div>
        <div class="h-32 bg-slate-700 rounded"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  type?: 'card' | 'list' | 'stats' | 'default'
  count?: number
}>()
</script>