<template>
  <transition
    enter-active-class="transform ease-out duration-300 transition"
    enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
    enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
    leave-active-class="transition ease-in duration-100"
    leave-from-class="translate-y-0 opacity-100 sm:translate-x-0"
    leave-to-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
  >
    <div
      v-if="show"
      class="fixed z-50 top-0 right-0 mt-4 mr-4 max-w-sm w-full bg-white/95 backdrop-blur-sm rounded-lg shadow-lg border border-white/20"
      :class="[typeClasses[type], positionClasses[position]]"
    >
      <div class="p-4">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <!-- Success Icon -->
            <svg v-if="type === 'success'" class="h-6 w-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            
            <!-- Error Icon -->
            <svg v-else-if="type === 'error'" class="h-6 w-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
            </svg>
            
            <!-- Warning Icon -->
            <svg v-else-if="type === 'warning'" class="h-6 w-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
            </svg>
            
            <!-- Info Icon -->
            <svg v-else class="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h1v4m-1 4h-1m6-4h1v4h1v4m-1 4h-1m-9-4h1v4h1v4m-1 4h-1m-9-4h1v4h1v4m-1 4h-1m6-4h1v4h1v4"/>
            </svg>
          </div>
          
          <div class="ml-3 w-0 flex-1">
            <p class="text-sm font-medium" :class="[typeClasses[type].title]">
              {{ title }}
            </p>
            <p class="mt-1 text-sm" :class="[typeClasses[type].description]">
              {{ message }}
            </p>
            
            <!-- Action Button -->
            <button
              v-if="action"
              @click="handleAction"
              class="mt-3 text-sm font-medium underline hover:no-underline"
              :class="[typeClasses[type].action]"
            >
              {{ action }}
            </button>
          </div>
          
          <!-- Close Button -->
          <div class="ml-4 flex-shrink-0">
            <button
              @click="close"
              class="inline-flex text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 rounded-md"
            >
              <span class="sr-only">Close</span>
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586 4.293 4.293a1 1 0 011.414 0L15.586 10l-4.293 4.293a1 1 0 010 1.414L10 11.414l4.293 4.293a1 1 0 000 1.414z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  show: boolean
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  action?: string
  position?: 'top-right' | 'top-center' | 'bottom-right'
  duration?: number
}

const props = withDefaults(defineProps<Props>(), {
  position: 'top-right',
  duration: 5000
})

const emit = defineEmits<{
  close: []
  action: []
}>()

const typeClasses = {
  success: {
    container: 'border-green-200 bg-green-50',
    title: 'text-green-800',
    description: 'text-green-700',
    action: 'text-green-800 hover:text-green-900'
  },
  error: {
    container: 'border-red-200 bg-red-50',
    title: 'text-red-800',
    description: 'text-red-700',
    action: 'text-red-800 hover:text-red-900'
  },
  warning: {
    container: 'border-yellow-200 bg-yellow-50',
    title: 'text-yellow-800',
    description: 'text-yellow-700',
    action: 'text-yellow-800 hover:text-yellow-900'
  },
  info: {
    container: 'border-blue-200 bg-blue-50',
    title: 'text-blue-800',
    description: 'text-blue-700',
    action: 'text-blue-800 hover:text-blue-900'
  }
}

const positionClasses = {
  'top-right': 'top-0 right-0 mt-4 mr-4',
  'top-center': 'top-0 left-1/2 transform -translate-x-1/2 mt-4',
  'bottom-right': 'bottom-0 right-0 mb-4 mr-4'
}

const close = () => {
  emit('close')
}

const handleAction = () => {
  emit('action')
}

// Auto-close after duration
if (props.duration > 0) {
  setTimeout(() => {
    close()
  }, props.duration)
}
</script>
