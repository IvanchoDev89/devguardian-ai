import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from './App.vue'
import './styles.css'

const routes = [
  // Public routes - no layout
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
  
  // Protected routes - with AppLayout
  {
    path: '/app',
    component: () => import('./components/AppLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/app/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('./pages/Dashboard.vue')
      },
      {
        path: 'scan',
        name: 'Scan',
        component: () => import('./pages/ScanPage.vue')
      },
      {
        path: 'repositories',
        name: 'Repositories',
        component: () => import('./pages/Repositories.vue')
      },
      {
        path: 'vulnerabilities',
        name: 'Vulnerabilities',
        component: () => import('./pages/VulnerabilitiesNew.vue')
      },
      {
        path: 'security-tools',
        name: 'SecurityTools',
        component: () => import('./pages/SecurityTools.vue')
      },
      {
        path: 'pentesting',
        name: 'Pentesting',
        component: () => import('./pages/Pentesting.vue')
      },
      {
        path: 'advanced-ml',
        name: 'AdvancedML',
        component: () => import('./pages/AdvancedML.vue')
      },
      {
        path: 'ai-fixes',
        name: 'AiFixes',
        component: () => import('./pages/AiFixes.vue')
      },
      {
        path: 'security-audit',
        name: 'SecurityAudit',
        component: () => import('./pages/SecurityAudit.vue')
      },
      {
        path: 'enterprise-assets',
        name: 'EnterpriseAssets',
        component: () => import('./pages/EnterpriseAssets.vue')
      },
      {
        path: 'billing',
        name: 'Billing',
        component: () => import('./pages/Billing.vue')
      },
      {
        path: 'teams',
        name: 'Teams',
        component: () => import('./pages/Settings.vue')
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('./pages/Settings.vue')
      },
      {
        path: 'admin',
        name: 'Admin',
        component: () => import('./pages/Admin.vue')
      },
      {
        path: 'super-admin',
        name: 'SuperAdmin',
        component: () => import('./pages/SuperAdmin.vue')
      }
    ]
  },
  
  // Redirect old paths to new ones
  {
    path: '/dashboard',
    redirect: '/app/dashboard'
  },
  {
    path: '/scan',
    redirect: '/app/scan'
  },
  {
    path: '/repositories',
    redirect: '/app/repositories'
  },
  {
    path: '/vulnerabilities',
    redirect: '/app/vulnerabilities'
  },
  {
    path: '/security-tools',
    redirect: '/app/security-tools'
  },
  {
    path: '/admin',
    redirect: '/app/admin'
  },
  {
    path: '/settings',
    redirect: '/app/settings'
  },
  {
    path: '/docs',
    name: 'Docs',
    component: () => import('./pages/Documentation.vue')
  },
  
  // Catch-all for 404
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
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

// Navigation guard for protected routes
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Protected routes
  if (to.path.startsWith('/app')) {
    if (!authStore.isAuthenticated) {
      next({ path: '/login', query: { redirect: to.fullPath } })
      return
    }
  }
  
  // Auth routes (already logged in)
  if ((to.path === '/login' || to.path === '/signup') && authStore.isAuthenticated) {
    next('/app/dashboard')
    return
  }
  
  next()
})

// Initialize stores
import { useThemeStore } from './stores/theme'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
authStore.initAuthState()

const themeStore = useThemeStore()
themeStore.initTheme()

app.mount('#app')
