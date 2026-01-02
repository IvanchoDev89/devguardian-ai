import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './styles.css'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('./pages/Dashboard.vue')
  },
  {
    path: '/repositories',
    name: 'Repositories',
    component: () => import('./pages/Repositories.vue')
  },
  {
    path: '/vulnerabilities',
    name: 'Vulnerabilities',
    component: () => import('./pages/Vulnerabilities.vue')
  },
  {
    path: '/ai-fixes',
    name: 'AiFixes',
    component: () => import('./pages/AiFixes.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('./pages/Settings.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
