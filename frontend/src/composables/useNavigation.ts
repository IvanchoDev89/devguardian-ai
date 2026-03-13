import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

export interface NavItem {
  name: string
  path: string
  icon: string
  iconBgClass: string
  badge?: string
  badgeClass?: string
  roles?: string[]  // undefined = all roles, empty array = no one
  category?: string
  children?: NavItem[]
}

export function useNavigation() {
  const authStore = useAuthStore()

  const userRole = computed(() => authStore.user?.role || 'guest')
  const userPlan = computed(() => authStore.plan || 'free')

  const hasAccess = (requiredRoles?: string[]): boolean => {
    if (!requiredRoles || requiredRoles.length === 0) return true
    return requiredRoles.includes(userRole.value)
  }

  const navigation: NavItem[] = [
    // Dashboard
    {
      name: 'Dashboard',
      path: '/dashboard',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-blue-500 to-cyan-500 text-white',
      category: 'main'
    },

    // Security Scanning
    {
      name: 'Code Scanner',
      path: '/scan',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-cyan-500 to-teal-500 text-white',
      category: 'scanning'
    },
    {
      name: 'Repositories',
      path: '/repositories',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-purple-500 to-pink-500 text-white',
      category: 'scanning'
    },
    {
      name: 'Vulnerabilities',
      path: '/vulnerabilities',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-red-500 to-orange-500 text-white',
      category: 'scanning'
    },

    // Advanced Security
    {
      name: 'Security Tools',
      path: '/security-tools',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-yellow-500 to-amber-500 text-white',
      category: 'advanced',
      roles: ['admin', 'super_admin', 'pro', 'enterprise']
    },
    {
      name: 'Pentesting',
      path: '/pentesting',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-orange-500 to-red-500 text-white',
      category: 'advanced',
      roles: ['admin', 'super_admin']
    },
    {
      name: 'Advanced ML',
      path: '/advanced-ml',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-indigo-500 to-purple-500 text-white',
      category: 'advanced',
      roles: ['admin', 'super_admin']
    },

    // AI Features
    {
      name: 'AI Fixes',
      path: '/ai-fixes',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-emerald-500 to-green-500 text-white',
      category: 'ai'
    },
    {
      name: 'Security Audit',
      path: '/security-audit',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-teal-500 to-cyan-500 text-white',
      category: 'ai'
    },

    // Enterprise
    {
      name: 'Enterprise Assets',
      path: '/enterprise-assets',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-slate-500 to-zinc-500 text-white',
      category: 'enterprise',
      roles: ['admin', 'super_admin', 'enterprise']
    },
    {
      name: 'Billing',
      path: '/billing',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-green-500 to-emerald-500 text-white',
      category: 'enterprise'
    },
    {
      name: 'Teams',
      path: '/teams',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-blue-500 to-indigo-500 text-white',
      category: 'enterprise'
    },

    // Admin
    {
      name: 'Admin Panel',
      path: '/admin',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-violet-500 to-purple-500 text-white',
      category: 'admin',
      roles: ['admin', 'super_admin']
    },
    {
      name: 'Super Admin',
      path: '/super-admin',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-red-500 to-pink-500 text-white',
      category: 'admin',
      roles: ['super_admin']
    },

    // Settings & Docs
    {
      name: 'Settings',
      path: '/settings',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-gray-500 to-slate-500 text-white',
      category: 'system'
    },
    {
      name: 'Documentation',
      path: '/docs',
      icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>',
      iconBgClass: 'bg-gradient-to-br from-sky-500 to-blue-500 text-white',
      category: 'system'
    }
  ]

  const filteredNavigation = computed(() => {
    return navigation.filter(item => hasAccess(item.roles))
  })

  const groupedNavigation = computed(() => {
    const groups: Record<string, NavItem[]> = {}
    
    filteredNavigation.value.forEach(item => {
      const category = item.category || 'other'
      if (!groups[category]) {
        groups[category] = []
      }
      groups[category].push(item)
    })
    
    return groups
  })

  const categoryLabels: Record<string, string> = {
    main: 'Overview',
    scanning: 'Security Scanning',
    advanced: 'Advanced Security',
    ai: 'AI Features',
    enterprise: 'Enterprise',
    admin: 'Administration',
    system: 'System'
  }

  const categoryIcons: Record<string, string> = {
    main: '📊',
    scanning: '🔒',
    advanced: '🛡️',
    ai: '🤖',
    enterprise: '🏢',
    admin: '⚙️',
    system: '📁'
  }

  return {
    navigation,
    filteredNavigation,
    groupedNavigation,
    categoryLabels,
    categoryIcons,
    hasAccess,
    userRole,
    userPlan
  }
}
