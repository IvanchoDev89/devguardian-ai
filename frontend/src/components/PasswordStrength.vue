<template>
  <div class="mt-2">
    <div class="flex gap-1 mb-1">
      <div 
        v-for="i in 4" 
        :key="i"
        class="h-1 flex-1 rounded-full transition-colors duration-300"
        :class="strength >= i ? strengthColors[strength - 1] : 'bg-gray-600'"
      ></div>
    </div>
    <p class="text-xs" :class="strengthTextColors[strength - 1]">
      {{ strengthLabels[strength - 1] }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  password: string
}>()

const strength = computed(() => {
  const p = props.password
  if (!p) return 0
  
  let score = 0
  
  if (p.length >= 8) score++
  if (p.length >= 12) score++
  if (/[a-z]/.test(p) && /[A-Z]/.test(p)) score++
  if (/\d/.test(p)) score++
  if (/[!@#$%^&*(),.?":{}|<>]/.test(p)) score++
  
  return Math.min(score, 4)
})

const strengthLabels = [
  'Very Weak',
  'Weak',
  'Fair',
  'Strong'
]

const strengthColors = [
  'bg-red-500',
  'bg-orange-500',
  'bg-yellow-500',
  'bg-green-500'
]

const strengthTextColors = [
  'text-red-400',
  'text-orange-400',
  'text-yellow-400',
  'text-green-400'
]
</script>