import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(true) // Default to dark theme for DevGuardian AI
  
  const toggleTheme = () => {
    isDark.value = !isDark.value
    updateTheme()
  }
  
  const setTheme = (dark: boolean) => {
    isDark.value = dark
    updateTheme()
  }
  
  const updateTheme = () => {
    if (isDark.value) {
      document.documentElement.classList.add('dark')
      document.body.classList.add('dark-theme')
      document.body.classList.remove('light-theme')
    } else {
      document.documentElement.classList.remove('dark')
      document.body.classList.add('light-theme')
      document.body.classList.remove('dark-theme')
    }
    
    // Save preference
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  }
  
  const initTheme = () => {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      isDark.value = savedTheme === 'dark'
    } else {
      // Check system preference
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    updateTheme()
  }
  
  return {
    isDark,
    toggleTheme,
    setTheme,
    initTheme
  }
})
