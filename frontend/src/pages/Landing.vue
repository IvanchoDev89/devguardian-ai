<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
    <!-- Header -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-white/10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <div class="w-9 h-9 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
              </div>
              <span class="text-xl font-bold text-white">DevGuardian<span class="text-cyan-400">AI</span></span>
            </router-link>
          </div>
          
          <div class="flex items-center gap-4">
            <router-link to="/login" class="text-gray-300 hover:text-white px-3 py-2 text-sm font-medium transition-colors">
              Sign In
            </router-link>
            <router-link to="/scan" class="px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white text-sm font-medium rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all">
              Start Scanning
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-32 pb-20 px-4">
      <div class="max-w-7xl mx-auto">
        <div class="text-center">
          <div class="inline-flex items-center px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full mb-6">
            <span class="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
            <span class="text-blue-400 text-sm font-medium">AI-Powered Security Scanner</span>
          </div>
          
          <h1 class="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Find & Fix Security
            <span class="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent"> Vulnerabilities</span>
            in Your Code
          </h1>
          
          <p class="text-xl text-gray-400 max-w-2xl mx-auto mb-10">
            AI-powered security scanner with automatic fix suggestions. 
            Protect your applications with API Keys, Webhooks, and Team collaboration.
          </p>
          
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link to="/scan" class="px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-cyan-700 transition-all transform hover:scale-105 shadow-lg shadow-blue-500/25">
              <span class="flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                Start Free Scan
              </span>
            </router-link>
            <router-link to="/login" class="px-8 py-4 bg-white/10 border border-white/20 text-white font-semibold rounded-xl hover:bg-white/20 transition-all">
              Sign In
            </router-link>
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mt-16 max-w-3xl mx-auto">
            <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-4">
              <p class="text-3xl font-bold text-white">50+</p>
              <p class="text-gray-400 text-sm">Vulnerability Types</p>
            </div>
            <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-4">
              <p class="text-3xl font-bold text-white">&lt;1s</p>
              <p class="text-gray-400 text-sm">Scan Time</p>
            </div>
            <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-4">
              <p class="text-3xl font-bold text-white">AI</p>
              <p class="text-gray-400 text-sm">Fix Suggestions</p>
            </div>
            <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-4">
              <p class="text-3xl font-bold text-white">$0</p>
              <p class="text-gray-400 text-sm">Free Plan</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="py-20 px-4 bg-white/5">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-white mb-4">Everything You Need to Secure Your Code</h2>
          <p class="text-gray-400">From individual developers to enterprise teams</p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Feature 1: Code Scanner -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6 hover:border-blue-500/30 transition-all group">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white mb-2">Code Scanner</h3>
            <p class="text-gray-400">Scan your code for 50+ vulnerability types including SQL injection, XSS, hardcoded secrets, and more.</p>
          </div>

          <!-- Feature 2: AI Fix Suggestions -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6 hover:border-purple-500/30 transition-all group">
            <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white mb-2">AI Fix Suggestions</h3>
            <p class="text-gray-400">Get AI-powered recommendations to fix vulnerabilities with secure code examples.</p>
          </div>

          <!-- Feature 3: API Keys -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6 hover:border-green-500/30 transition-all group">
            <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white mb-2">API Keys</h3>
            <p class="text-gray-400">Integrate security scanning into your CI/CD with API keys. Free 50 scans/month.</p>
          </div>

          <!-- Feature 4: Webhooks -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6 hover:border-yellow-500/30 transition-all group">
            <div class="w-12 h-12 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white mb-2">Webhooks</h3>
            <p class="text-gray-400">Receive notifications when scans complete. Integrate with Slack, Teams, and more.</p>
          </div>

          <!-- Feature 5: Team Management -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6 hover:border-indigo-500/30 transition-all group">
            <div class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white mb-2">Team Management</h3>
            <p class="text-gray-400">Invite team members, manage permissions, and track team security posture.</p>
          </div>

          <!-- Feature 6: PDF Reports -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6 hover:border-red-500/30 transition-all group">
            <div class="w-12 h-12 bg-gradient-to-br from-red-500 to-pink-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white mb-2">PDF Reports</h3>
            <p class="text-gray-400">Generate professional security reports in PDF or HTML format for compliance.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing -->
    <section class="py-20 px-4">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-white mb-4">Simple, Transparent Pricing</h2>
          <p class="text-gray-400">Start free, scale as you grow</p>
        </div>

        <div class="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          <!-- Free -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6">
            <h3 class="text-xl font-semibold text-white mb-2">Free</h3>
            <p class="text-4xl font-bold text-white mb-4">$0<span class="text-lg text-gray-400 font-normal">/mo</span></p>
            <ul class="space-y-3 text-gray-400 mb-6">
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>50 scans/month</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Basic vulnerability detection</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>AI fix suggestions</li>
            </ul>
            <router-link to="/signup" class="block w-full py-3 bg-white/10 text-white text-center rounded-lg hover:bg-white/20 transition-colors">
              Get Started
            </router-link>
          </div>

          <!-- Pro -->
          <div class="bg-gradient-to-br from-blue-600/20 to-cyan-600/20 backdrop-blur-sm rounded-xl border border-blue-500/30 p-6 transform scale-105">
            <div class="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 bg-gradient-to-r from-blue-600 to-cyan-600 text-white text-sm font-medium rounded-full">Popular</div>
            <h3 class="text-xl font-semibold text-white mb-2">Pro</h3>
            <p class="text-4xl font-bold text-white mb-4">$29<span class="text-lg text-gray-400 font-normal">/mo</span></p>
            <ul class="space-y-3 text-gray-300 mb-6">
              <li class="flex items-center"><svg class="w-5 h-5 text-cyan-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>500 scans/month</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-cyan-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>API Keys</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-cyan-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Webhooks</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-cyan-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>PDF Reports</li>
            </ul>
            <router-link to="/signup" class="block w-full py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white text-center rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all">
              Start Pro Trial
            </router-link>
          </div>

          <!-- Enterprise -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6">
            <h3 class="text-xl font-semibold text-white mb-2">Enterprise</h3>
            <p class="text-4xl font-bold text-white mb-4">$99<span class="text-lg text-gray-400 font-normal">/mo</span></p>
            <ul class="space-y-3 text-gray-400 mb-6">
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Unlimited scans</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Team Management</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>GitHub Integration</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Priority Support</li>
            </ul>
            <router-link to="/signup" class="block w-full py-3 bg-white/10 text-white text-center rounded-lg hover:bg-white/20 transition-colors">
              Contact Sales
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-20 px-4 bg-gradient-to-r from-blue-600/20 to-cyan-600/20">
      <div class="max-w-3xl mx-auto text-center">
        <h2 class="text-3xl font-bold text-white mb-4">Ready to Secure Your Code?</h2>
        <p class="text-gray-400 mb-8">Start scanning in seconds. No credit card required.</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link to="/scan" class="px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-cyan-700 transition-all">
            Start Free Scan
          </router-link>
          <router-link to="/login" class="px-8 py-4 bg-white/10 border border-white/20 text-white font-semibold rounded-xl hover:bg-white/20 transition-all">
            Sign In
          </router-link>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-8 px-4 border-t border-white/10">
      <div class="max-w-7xl mx-auto text-center text-gray-500 text-sm">
        <p>© 2026 DevGuardian AI. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  if (authStore.isAuthenticated) {
    router.replace('/dashboard')
  }
})
</script>
