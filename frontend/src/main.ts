import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from './App.vue'
import './styles.css'

// DevGuardian AI - Security Vulnerability Scanner (MVP)

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: () => import('./pages/Landing.vue')
  },
  {
    path: '/scan',
    name: 'Scan',
    component: () => import('./pages/ScanPage.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('./pages/Login.vue')
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('./pages/Signup.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('./pages/Settings.vue')
  },
  {
    path: '/docs',
    name: 'Docs',
    component: () => import('./pages/Documentation.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize stores
import { useThemeStore } from './stores/theme'

const themeStore = useThemeStore()
themeStore.initTheme()

app.mount('#app')
