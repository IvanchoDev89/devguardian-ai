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
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('./pages/Dashboard.vue')
  },
  {
    path: '/scan',
    name: 'Scan',
    component: () => import('./pages/ScanPage.vue')
  },
  {
    path: '/repositories',
    name: 'Repositories',
    component: () => import('./pages/Repositories.vue')
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
    path: '/admin',
    name: 'Admin',
    component: () => import('./pages/Admin.vue')
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
  },
  {
    path: '/security-tools',
    name: 'SecurityTools',
    component: () => import('./pages/SecurityTools.vue')
  },
  {
    path: '/vulnerabilities',
    name: 'Vulnerabilities',
    component: () => import('./pages/Vulnerabilities.vue')
  },
  {
    path: '/pentesting',
    name: 'Pentesting',
    component: () => import('./pages/Pentesting.vue')
  },
  {
    path: '/advanced-ml',
    name: 'AdvancedML',
    component: () => import('./pages/AdvancedML.vue')
  },
  {
    path: '/ai-fixes',
    name: 'AiFixes',
    component: () => import('./pages/AiFixes.vue')
  },
  {
    path: '/security-audit',
    name: 'SecurityAudit',
    component: () => import('./pages/SecurityAudit.vue')
  },
  {
    path: '/enterprise-assets',
    name: 'EnterpriseAssets',
    component: () => import('./pages/EnterpriseAssets.vue')
  },
  {
    path: '/billing',
    name: 'Billing',
    component: () => import('./pages/Billing.vue')
  },
  {
    path: '/teams',
    name: 'Teams',
    component: () => import('./pages/Settings.vue') // Reuse Settings for now
  },
  {
    path: '/super-admin',
    name: 'SuperAdmin',
    component: () => import('./pages/SuperAdmin.vue')
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
