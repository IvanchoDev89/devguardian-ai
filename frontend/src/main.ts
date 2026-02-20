import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from './App.vue'
import './styles.css'

// CodeSentinel - Precision Code Security Scanner

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: () => import('./pages/Landing.vue')
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
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('./pages/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/sql-injection-scanner',
    name: 'SQLInjectionScanner',
    component: () => import('./pages/SQLInjectionScanner.vue')
  },
  {
    path: '/repositories',
    name: 'Repositories',
    component: () => import('./pages/Repositories.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/vulnerabilities',
    name: 'Vulnerabilities',
    component: () => import('./pages/Vulnerabilities.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ai-fixes',
    name: 'AiFixes',
    component: () => import('./pages/AiFixes.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/advanced-ml',
    name: 'AdvancedML',
    component: () => import('./pages/AdvancedML.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/automation',
    name: 'Automation',
    component: () => import('./pages/Automation.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/security-audit',
    name: 'SecurityAudit',
    component: () => import('./pages/SecurityAudit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('./pages/Settings.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/super-admin',
    name: 'SuperAdmin',
    component: () => import('./pages/SuperAdmin.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/pentesting',
    name: 'Pentesting',
    component: () => import('./pages/Pentesting.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for protected routes
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth_token')
  const requiresAuth = to.meta.requiresAuth
  
  if (requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize stores
import { useAuthStore } from './stores/auth'
import { useThemeStore } from './stores/theme'

const authStore = useAuthStore()
const themeStore = useThemeStore()

// Initialize theme and auth
themeStore.initTheme()
authStore.initAuth()

app.mount('#app')
