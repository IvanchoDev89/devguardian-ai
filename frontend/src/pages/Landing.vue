<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
    <!-- SEO Meta Tags would go in index.html, but we add structured content here -->
    
    <!-- Hero Section -->
    <div class="relative overflow-hidden">
      <!-- Background Pattern -->
      <div class="absolute inset-0 bg-grid-white/5 bg-grid-16"></div>
      
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative">
        <div class="text-center">
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6">
            <span class="bg-gradient-to-r from-blue-400 via-cyan-300 to-blue-400 bg-clip-text text-transparent">
              DevGuardian AI
            </span>
          </h1>
          <p class="text-lg sm:text-xl text-gray-300 mb-6 max-w-4xl mx-auto leading-relaxed">
            Precision security scanner that detects <span class="text-blue-400 font-semibold">only real vulnerabilities</span>. 
            No false positives, no noise, just actionable security insights powered by advanced AI.
          </p>
          
          <!-- Stats -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto mb-10">
            <div class="text-center">
              <div class="text-3xl sm:text-4xl font-bold text-blue-400">98.5%</div>
              <div class="text-sm text-gray-400 mt-1">Detection Accuracy</div>
            </div>
            <div class="text-center">
              <div class="text-3xl sm:text-4xl font-bold text-cyan-400">0%</div>
              <div class="text-sm text-gray-400 mt-1">False Positives</div>
            </div>
            <div class="text-center">
              <div class="text-3xl sm:text-4xl font-bold text-blue-400">2.3s</div>
              <div class="text-sm text-gray-400 mt-1">Avg Scan Time</div>
            </div>
            <div class="text-center">
              <div class="text-3xl sm:text-4xl font-bold text-cyan-400">50K+</div>
              <div class="text-sm text-gray-400 mt-1">Vulns Found</div>
            </div>
          </div>
          
          <div class="flex flex-col sm:flex-row gap-4 justify-center mb-8">
            <router-link
              to="/sql-injection-scanner"
              class="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-cyan-500/25"
            >
              <span class="relative z-10">Try Free Scanner</span>
              <div class="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg blur opacity-50 group-hover:opacity-75 transition duration-300"></div>
            </router-link>
            <router-link
              to="/pricing"
              class="px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-lg border border-white/20 hover:bg-white/20 transition-all duration-300"
            >
              View Pricing
            </router-link>
          </div>
          
          <p class="text-sm text-gray-500">
            No credit card required • Free plan available • Setup in 2 minutes
          </p>
        </div>
      </div>
    </div>

    <!-- Trusted By Section -->
    <div class="py-12 border-y border-white/5 bg-black/20">
      <div class="max-w-7xl mx-auto px-4">
        <p class="text-center text-gray-500 text-sm mb-8">TRUSTED BY SECURITY TEAMS AT</p>
        <div class="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-50">
          <div class="text-white font-bold text-xl">Acme Corp</div>
          <div class="text-white font-bold text-xl">TechFlow</div>
          <div class="text-white font-bold text-xl">DataSecure</div>
          <div class="text-white font-bold text-xl">CloudGuard</div>
          <div class="text-white font-bold text-xl">DevOps Inc</div>
        </div>
      </div>
    </div>

    <!-- Problem/Solution Section -->
    <div class="py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            The Problem with Traditional Scanners
          </h2>
          <p class="text-xl text-gray-400 max-w-3xl mx-auto">
            Security teams waste 70% of their time on false positives. We fix that.
          </p>
        </div>
        
        <div class="grid md:grid-cols-2 gap-8">
          <div class="bg-red-500/10 rounded-2xl p-8 border border-red-500/20">
            <h3 class="text-xl font-bold text-red-400 mb-4 flex items-center">
              <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              Traditional Scanners
            </h3>
            <ul class="space-y-4 text-gray-300">
              <li class="flex items-start">
                <svg class="w-5 h-5 text-red-400 mr-3 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
                <span>Thousands of false positives daily</span>
              </li>
              <li class="flex items-start">
                <svg class="w-5 h-5 text-red-400 mr-3 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
                <span>Hours of manual triage required</span>
              </li>
              <li class="flex items-start">
                <svg class="w-5 h-5 text-red-400 mr-3 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
                <span>Slow scans that slow down development</span>
              </li>
              <li class="flex items-start">
                <svg class="w-5 h-5 text-red-400 mr-3 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
                <span>No actionable remediation advice</span>
              </li>
            </ul>
          </div>
          
          <div class="bg-green-500/10 rounded-2xl p-8 border border-green-500/20">
            <h3 class="text-xl font-bold text-green-400 mb-4 flex items-center">
              <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              DevGuardian AI
            </h3>
            <ul class="space-y-4 text-gray-300">
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-400 mr-3 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                <span>Zero false positives with AI validation</span>
              </li>
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-400 mr-3 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                <span>Instant results, no manual work</span>
              </li>
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-400 mr-3 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                <span>Lightning-fast 2-second scans</span>
              </li>
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-400 mr-3 mt-1 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                <span>AI-generated secure code fixes</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="py-20 bg-slate-800/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            Everything You Need for Code Security
          </h2>
          <p class="text-xl text-gray-400 max-w-3xl mx-auto">
            Comprehensive security scanning with AI-powered accuracy
          </p>
        </div>
        
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="bg-slate-900/50 rounded-xl p-6 border border-white/10 hover:border-blue-500/30 transition-all duration-300">
            <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">SQL Injection Detection</h3>
            <p class="text-gray-400 text-sm">Advanced pattern matching and AI validation to detect SQL injection vulnerabilities with zero false positives.</p>
          </div>
          
          <div class="bg-slate-900/50 rounded-xl p-6 border border-white/10 hover:border-cyan-500/30 transition-all duration-300">
            <div class="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">XSS Protection</h3>
            <p class="text-gray-400 text-sm">Detect cross-site scripting vulnerabilities across all input vectors with context-aware analysis.</p>
          </div>
          
          <div class="bg-slate-900/50 rounded-xl p-6 border border-white/10 hover:border-blue-500/30 transition-all duration-300">
            <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">AI Code Fixes</h3>
            <p class="text-gray-400 text-sm">Not just detection—our AI generates secure code fixes you can apply instantly.</p>
          </div>
          
          <div class="bg-slate-900/50 rounded-xl p-6 border border-white/10 hover:border-cyan-500/30 transition-all duration-300">
            <div class="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">GitHub Integration</h3>
            <p class="text-gray-400 text-sm">Automatic scanning on every pull request. Block vulnerabilities before they merge.</p>
          </div>
          
          <div class="bg-slate-900/50 rounded-xl p-6 border border-white/10 hover:border-blue-500/30 transition-all duration-300">
            <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">API-First Design</h3>
            <p class="text-gray-400 text-sm">Full REST API for integration into your CI/CD pipelines and workflows.</p>
          </div>
          
          <div class="bg-slate-900/50 rounded-xl p-6 border border-white/10 hover:border-cyan-500/30 transition-all duration-300">
            <div class="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white mb-2">Compliance Reports</h3>
            <p class="text-gray-400 text-sm">Generate SOC 2, HIPAA, and PCI compliance reports with one click.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- How It Works -->
    <div class="py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            How DevGuardian AI Works
          </h2>
          <p class="text-xl text-gray-400">
            Get started in minutes, not days
          </p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-full flex items-center justify-center mx-auto mb-6 text-2xl font-bold text-white">1</div>
            <h3 class="text-xl font-semibold text-white mb-3">Connect Your Code</h3>
            <p class="text-gray-400">Connect your GitHub repository or paste code directly. We support all major languages.</p>
          </div>
          
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-full flex items-center justify-center mx-auto mb-6 text-2xl font-bold text-white">2</div>
            <h3 class="text-xl font-semibold text-white mb-3">AI Analysis</h3>
            <p class="text-gray-400">Our AI scans for vulnerabilities, validates each finding, and filters out false positives.</p>
          </div>
          
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-full flex items-center justify-center mx-auto mb-6 text-2xl font-bold text-white">3</div>
            <h3 class="text-xl font-semibold text-white mb-3">Get Fixed Code</h3>
            <p class="text-gray-400">Receive detailed reports with AI-generated secure code fixes. Apply with one click.</p>
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
          <div class="bg-slate-900/50 rounded-xl p-8 border border-slate-700">
            <h3 class="text-xl font-bold text-white mb-2">Free</h3>
            <div class="text-4xl font-bold text-white mb-4">$0<span class="text-lg text-gray-400">/mo</span></div>
            <ul class="space-y-3 text-gray-400 mb-8">
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>1 security scan</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Basic vulnerability detection</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Community support</li>
            </ul>
            <router-link to="/signup" class="block w-full py-3 px-4 bg-slate-700 text-white text-center rounded-lg hover:bg-slate-600 transition">Get Started</router-link>
          </div>
          
          <div class="bg-gradient-to-b from-cyan-500/20 to-blue-500/20 rounded-xl p-8 border border-cyan-500 relative">
            <div class="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gradient-to-r from-cyan-500 to-blue-500 text-white text-sm font-semibold px-4 py-1 rounded-full">Popular</div>
            <h3 class="text-xl font-bold text-white mb-2">Pro</h3>
            <div class="text-4xl font-bold text-white mb-4">$29<span class="text-lg text-gray-400">/mo</span></div>
            <ul class="space-y-3 text-gray-300 mb-8">
              <li class="flex items-center"><svg class="w-5 h-5 text-cyan-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>1,000 scans/month</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-cyan-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>AI-powered fixes</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-cyan-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Priority support</li>
              <li class="flex items-center"><svg class="w-5 h-5 text-cyan-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>GitHub integration</li>
            </ul>
            <router-link to="/signup?plan=pro" class="block w-full py-3 px-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white text-center rounded-lg hover:from-cyan-600 hover:to-blue-600 transition">Upgrade to Pro</router-link>
          </div>
          
          <div class="bg-slate-900/50 rounded-xl p-8 border border-slate-700">
            <h3 class="text-xl font-bold text-white mb-2">Enterprise</h3>
            <div class="text-4xl font-bold text-white mb-4">$199<span class="text-lg text-gray-400">/mo</span></div>
            <ul class="space-y-3 text-gray-400 mb-8">
              <li class="flex items-center"><svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>Unlimited scans</li>
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
    <div class="py-20">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div class="bg-gradient-to-r from-blue-600/20 to-cyan-600/20 rounded-2xl p-12 border border-blue-500/30">
          <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to Eliminate Security Noise?
          </h2>
          <p class="text-xl text-gray-300 mb-8">
            Join thousands of developers who ship secure code without the alert fatigue.
          </p>
          <router-link
            to="/sql-injection-scanner"
            class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all duration-300 transform hover:scale-105"
          >
            Start Free Scanner
            <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Footer Links for SEO -->
    <div class="py-12 border-t border-white/10 bg-black/20">
      <div class="max-w-7xl mx-auto px-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">
          <div>
            <h4 class="text-white font-semibold mb-4">Product</h4>
            <ul class="space-y-2 text-gray-400 text-sm">
              <li><router-link to="/sql-injection-scanner" class="hover:text-white">Scanner</router-link></li>
              <li><router-link to="/pricing" class="hover:text-white">Pricing</router-link></li>
              <li><router-link to="/docs" class="hover:text-white">API Docs</router-link></li>
            </ul>
          </div>
          <div>
            <h4 class="text-white font-semibold mb-4">Company</h4>
            <ul class="space-y-2 text-gray-400 text-sm">
              <li><a href="#" class="hover:text-white">About</a></li>
              <li><a href="#" class="hover:text-white">Blog</a></li>
              <li><a href="#" class="hover:text-white">Careers</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-white font-semibold mb-4">Legal</h4>
            <ul class="space-y-2 text-gray-400 text-sm">
              <li><a href="#" class="hover:text-white">Privacy Policy</a></li>
              <li><a href="#" class="hover:text-white">Terms of Service</a></li>
              <li><a href="#" class="hover:text-white">Security</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-white font-semibold mb-4">Support</h4>
            <ul class="space-y-2 text-gray-400 text-sm">
              <li><a href="#" class="hover:text-white">Documentation</a></li>
              <li><a href="#" class="hover:text-white">Help Center</a></li>
              <li><a href="#" class="hover:text-white">Contact</a></li>
            </ul>
          </div>
        </div>
        <div class="text-center text-gray-500 text-sm">
          &copy; 2026 DevGuardian AI. All rights reserved.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Landing page for DevGuardian AI - SEO optimized
</script>
