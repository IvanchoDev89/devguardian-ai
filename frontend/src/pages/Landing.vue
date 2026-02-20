<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
    <!-- Hero Section -->
    <div class="relative overflow-hidden">
      <!-- Background Pattern -->
      <div class="absolute inset-0 bg-grid-white/5 bg-grid-16"></div>
      
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 relative">
        <div class="text-center">
          <!-- Badge -->
          <div class="inline-flex items-center px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-8">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
              <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
            </svg>
            Zero-Noise Detection Technology
          </div>
          
          <h1 class="text-5xl sm:text-7xl font-bold text-white mb-6">
            <span class="bg-gradient-to-r from-blue-400 via-cyan-300 to-blue-400 bg-clip-text text-transparent">
              DevGuardian AI
            </span>
          </h1>
          <p class="text-xl sm:text-2xl text-gray-300 mb-8 max-w-4xl mx-auto leading-relaxed">
            Precision security scanner that detects <span class="text-blue-400 font-semibold">only real vulnerabilities</span>. 
            No false positives, no noise, just actionable security insights.
          </p>
          
          <!-- Stats -->
          <div class="grid grid-cols-3 gap-8 max-w-2xl mx-auto mb-12">
            <div class="text-center">
              <div class="text-3xl font-bold text-blue-400">98.5%</div>
              <div class="text-sm text-gray-400">Detection Accuracy</div>
            </div>
            <div class="text-center">
              <div class="text-3xl font-bold text-cyan-400">0</div>
              <div class="text-sm text-gray-400">False Positives</div>
            </div>
            <div class="text-center">
              <div class="text-3xl font-bold text-blue-400">2.3s</div>
              <div class="text-sm text-gray-400">Avg Scan Time</div>
            </div>
          </div>
          
          <div class="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <router-link
              to="/sql-injection-scanner"
              class="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-cyan-500/25"
            >
              <span class="relative z-10">🚀 Try Live Scanner</span>
              <div class="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg blur opacity-50 group-hover:opacity-75 transition duration-300"></div>
            </router-link>
            <router-link
              to="/dashboard"
              class="px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-lg border border-white/20 hover:bg-white/20 transition-all duration-300"
            >
              📊 View Dashboard
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="py-20 relative">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            Why Choose DevGuardian AI?
          </h2>
          <p class="text-xl text-gray-400 max-w-3xl mx-auto">
            Traditional security scanners overwhelm you with false alerts. We focus on what matters.
          </p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8">
          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10 hover:border-blue-500/30 transition-all duration-300">
            <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-6">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white mb-4">Zero-Noise Detection</h3>
            <p class="text-gray-400">Our AI-powered engine only reports exploitable vulnerabilities. No more chasing false positives.</p>
          </div>
          
          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10 hover:border-cyan-500/30 transition-all duration-300">
            <div class="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center mb-6">
              <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white mb-4">Lightning Fast</h3>
            <p class="text-gray-400">Scan entire codebases in seconds, not hours. Get results while you're still developing.</p>
          </div>
          
          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10 hover:border-blue-500/30 transition-all duration-300">
            <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-6">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white mb-4">AI-Powered Fixes</h3>
            <p class="text-gray-400">Not just detection. Our AI generates secure code fixes and creates pull requests automatically.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Pricing Section -->
    <div class="py-20 bg-slate-800/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            Simple, Transparent Pricing
          </h2>
          <p class="text-xl text-gray-400">
            Start free, scale as you grow
          </p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <!-- Free -->
          <div class="bg-slate-900/50 rounded-xl p-8 border border-slate-700">
            <h3 class="text-xl font-bold text-white mb-2">Free</h3>
            <div class="text-4xl font-bold text-white mb-4">$0<span class="text-lg text-gray-400">/mo</span></div>
            <ul class="space-y-3 text-gray-400 mb-8">
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>100 scans/month</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Basic vulnerability detection</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Email support</li>
            </ul>
            <router-link to="/signup" class="block w-full py-3 px-4 bg-slate-700 text-white text-center rounded-lg hover:bg-slate-600 transition">Get Started</router-link>
          </div>
          
          <!-- Pro -->
          <div class="bg-gradient-to-b from-cyan-500/20 to-blue-500/20 rounded-xl p-8 border border-cyan-500 relative">
            <div class="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gradient-to-r from-cyan-500 to-blue-500 text-white text-sm font-semibold px-4 py-1 rounded-full">Popular</div>
            <h3 class="text-xl font-bold text-white mb-2">Pro</h3>
            <div class="text-4xl font-bold text-white mb-4">$29<span class="text-lg text-gray-400">/mo</span></div>
            <ul class="space-y-3 text-gray-300 mb-8">
              <li class="flex items-center"><svg class="w-5 h-5 text-cyan-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>1,000 scans/month</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-cyan-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>AI-powered fixes</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-cyan-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Priority support</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-cyan-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>API access</li>
            </ul>
            <router-link to="/signup?plan=pro" class="block w-full py-3 px-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white text-center rounded-lg hover:from-cyan-600 hover:to-blue-600 transition">Upgrade to Pro</router-link>
          </div>
          
          <!-- Enterprise -->
          <div class="bg-slate-900/50 rounded-xl p-8 border border-slate-700">
            <h3 class="text-xl font-bold text-white mb-2">Enterprise</h3>
            <div class="text-4xl font-bold text-white mb-4">$199<span class="text-lg text-gray-400">/mo</span></div>
            <ul class="space-y-3 text-gray-400 mb-8">
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>10,000 scans/month</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Everything in Pro</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Dedicated support</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>SSO/SAML</li>
            </ul>
            <router-link to="/contact" class="block w-full py-3 px-4 bg-slate-700 text-white text-center rounded-lg hover:bg-slate-600 transition">Contact Sales</router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="py-20 relative">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div class="bg-gradient-to-r from-blue-600/20 to-cyan-600/20 rounded-2xl p-12 border border-blue-500/30">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to Eliminate Security Noise?
          </h2>
          <p class="text-xl text-gray-300 mb-8">
            Join teams that ship secure code without the alert fatigue.
          </p>
          <router-link
            to="/sql-injection-scanner"
            class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all duration-300 transform hover:scale-105"
          >
            Start Scanning Now
            <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Landing page component for DevGuardian AI
</script>
