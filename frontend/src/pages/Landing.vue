<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <div class="hero">
      <div class="hero-content">
        <div class="logo">
          <span class="logo-icon">🛡️</span>
          <span class="logo-text">DevGuardian</span>
        </div>
        
        <h1>Code Security Scanner<br/><span>Pattern-Based Analysis</span></h1>
        
        <p class="subtitle">
          Detect common security issues in your code with pattern-based analysis.
          For educational purposes and basic security hygiene.
        </p>
        
        <div class="cta-buttons">
          <router-link to="/scan" class="btn-primary">
            <span>🔍</span> Scan Code
          </router-link>
          <router-link to="/login" class="btn-secondary">
            Sign In
          </router-link>
        </div>
        
        <!-- Quick Stats -->
        <div class="stats">
          <div class="stat">
            <span class="stat-value">18+</span>
            <span class="stat-label">Vuln Types</span>
          </div>
          <div class="stat">
            <span class="stat-value">$0</span>
            <span class="stat-label">Free</span>
          </div>
          <div class="stat">
            <span class="stat-value">&lt;1s</span>
            <span class="stat-label">Scan Time</span>
          </div>
        </div>
      </div>
      
      <!-- Demo Preview -->
      <div class="demo-card">
        <div class="demo-header">
          <span class="dot red"></span>
          <span class="dot yellow"></span>
          <span class="dot green"></span>
          <span class="demo-title">Live Demo</span>
        </div>
        <div class="demo-content">
          <div class="code-example">
            <pre><code><span class="keyword">password</span> = <span class="string">"secret123"</span></code></pre>
          </div>
          <div class="demo-result">
            <div class="vuln-found">
              <span class="severity critical">CRITICAL</span>
              <span>Hardcoded Password</span>
            </div>
            <div class="score">
              Security Score: <strong>75</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Features -->
    <div class="features">
      <h2>What We Detect</h2>
      <div class="features-grid">
        <div class="feature">
          <div class="feature-icon">🔑</div>
          <h3>Hardcoded Secrets</h3>
          <p>Detects passwords, API keys, and tokens in source code.</p>
        </div>
        <div class="feature">
          <div class="feature-icon">💉</div>
          <h3>SQL Injection</h3>
          <p>Identifies string concatenation in SQL queries.</p>
        </div>
        <div class="feature">
          <div class="feature-icon">⚡</div>
          <h3>Command Injection</h3>
          <p>Finds unsafe system command execution patterns.</p>
        </div>
        <div class="feature">
          <div class="feature-icon">🔓</div>
          <h3>Weak Cryptography</h3>
          <p>Detects usage of deprecated algorithms like MD5.</p>
        </div>
      </div>
    </div>
    
    <!-- Disclaimer -->
    <div class="disclaimer">
      <div class="disclaimer-content">
        <h3>⚠️ Important Disclaimer</h3>
        <p>
          This tool uses <strong>pattern-based detection</strong> and cannot find all security vulnerabilities. 
          It will not detect business logic flaws, authentication bypasses, or complex attack vectors. 
          For comprehensive security testing, use professional penetration testing services.
        </p>
        <p class="disclaimer-note">
          This is a code quality tool, not a replacement for security audits.
        </p>
      </div>
    </div>
    
    <!-- Supported Languages -->
    <div class="languages">
      <h2>Supported Languages</h2>
      <div class="lang-grid">
        <span class="lang">Python</span>
        <span class="lang">JavaScript</span>
        <span class="lang">TypeScript</span>
        <span class="lang">Java</span>
        <span class="lang">PHP</span>
        <span class="lang">Go</span>
        <span class="lang">Rust</span>
        <span class="lang">C#</span>
        <span class="lang">C/C++</span>
        <span class="lang">Ruby</span>
      </div>
    </div>
    
    <!-- How It Works -->
    <div class="how-it-works">
      <h2>How It Works</h2>
      <div class="steps">
        <div class="step">
          <div class="step-num">1</div>
          <h3>Paste Your Code</h3>
          <p>Copy and paste the code you want to analyze</p>
        </div>
        <div class="step">
          <div class="step-num">2</div>
          <h3>Automatic Scan</h3>
          <p>We detect vulnerabilities in seconds</p>
        </div>
        <div class="step">
          <div class="step-num">3</div>
          <h3>Get Results</h3>
          <p>View vulnerabilities with severity and AI fixes</p>
        </div>
      </div>
    </div>
    
    <!-- CTA -->
    <div class="cta-section">
      <h2>Get Started</h2>
      <p>No registration. Completely free.</p>
      <router-link to="/scan" class="btn-primary btn-large">
        🚀 Scan Now
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: white;
  font-family: 'Inter', system-ui, sans-serif;
}

.hero {
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
    text-align: center;
  }
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.logo-icon { font-size: 2rem; }
.logo-text { font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #3b82f6, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

.hero h1 { font-size: 3.5rem; font-weight: 800; line-height: 1.1; margin-bottom: 1rem; }
.hero h1 span { background: linear-gradient(135deg, #3b82f6, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.subtitle { color: #94a3b8; font-size: 1.125rem; margin-bottom: 2rem; line-height: 1.6; }

.cta-buttons { display: flex; gap: 1rem; margin-bottom: 3rem; }
@media (max-width: 768px) { .cta-buttons { justify-content: center; } }

.btn-primary, .btn-secondary {
  padding: 0.875rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary { background: linear-gradient(135deg, #3b82f6, #06b6d4); color: white; }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 40px rgba(59, 130, 246, 0.3); }

.btn-secondary { background: rgba(255, 255, 255, 0.1); color: white; border: 1px solid rgba(255, 255, 255, 0.2); }
.btn-secondary:hover { background: rgba(255, 255, 255, 0.2); }

.stats { display: flex; gap: 2rem; }
@media (max-width: 768px) { .stats { justify-content: center; } }
.stat { display: flex; flex-direction: column; }
.stat-value { font-size: 1.5rem; font-weight: 700; color: #06b6d4; }
.stat-label { font-size: 0.875rem; color: #64748b; }

/* Demo Card */
.demo-card { background: #1e293b; border-radius: 1rem; overflow: hidden; box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3); }
.demo-header { background: #0f172a; padding: 0.75rem 1rem; display: flex; align-items: center; gap: 0.5rem; }
.dot { width: 12px; height: 12px; border-radius: 50%; }
.dot.red { background: #ef4444; }
.dot.yellow { background: #eab308; }
.dot.green { background: #22c55e; }
.demo-title { margin-left: auto; font-size: 0.75rem; color: #64748b; }
.demo-content { padding: 1.5rem; }
.code-example { background: #0f172a; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; font-family: 'Fira Code', monospace; font-size: 0.875rem; }
.keyword { color: #c084fc; }
.string { color: #4ade80; }

.vuln-found { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 0.5rem; margin-bottom: 0.75rem; }
.severity.critical { background: #dc2626; color: white; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.75rem; font-weight: 700; }
.score { font-size: 0.875rem; color: #94a3b8; }
.score strong { color: #f59e0b; }

/* Features */
.features { max-width: 1200px; margin: 0 auto; padding: 4rem 2rem; }
.features h2, .how-it-works h2, .cta-section h2, .languages h2 { text-align: center; font-size: 2rem; margin-bottom: 3rem; }

.features-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; }
@media (max-width: 1024px) { .features-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .features-grid { grid-template-columns: 1fr; } }

.feature { background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border-radius: 1rem; text-align: center; border: 1px solid rgba(255, 255, 255, 0.1); }
.feature-icon { font-size: 2.5rem; margin-bottom: 1rem; }
.feature h3 { font-size: 1.125rem; margin-bottom: 0.5rem; }
.feature p { font-size: 0.875rem; color: #94a3b8; line-height: 1.5; }

/* Languages */
.languages { max-width: 1200px; margin: 0 auto; padding: 2rem; }
.lang-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.75rem; }
.lang { background: rgba(59, 130, 246, 0.2); color: #60a5fa; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.875rem; }

/* How It Works */
.how-it-works { max-width: 1200px; margin: 0 auto; padding: 4rem 2rem; }
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; }
@media (max-width: 768px) { .steps { grid-template-columns: 1fr; } }
.step { text-align: center; }
.step-num { width: 3rem; height: 3rem; background: linear-gradient(135deg, #3b82f6, #06b6d4); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; font-weight: 700; margin: 0 auto 1rem; }

/* CTA */
.cta-section { text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(6, 182, 212, 0.1)); }
.cta-section p { color: #94a3b8; margin-bottom: 2rem; }
.btn-large { font-size: 1.125rem; padding: 1rem 2rem; }

/* Disclaimer */
.disclaimer { max-width: 1200px; margin: 0 auto; padding: 2rem; }
.disclaimer-content { background: rgba(234, 179, 8, 0.1); border: 1px solid rgba(234, 179, 8, 0.3); border-radius: 1rem; padding: 1.5rem; }
.disclaimer-content h3 { color: #facc15; margin-bottom: 1rem; font-size: 1.125rem; }
.disclaimer-content p { color: #d1d5db; font-size: 0.875rem; line-height: 1.6; margin-bottom: 0.75rem; }
.disclaimer-content strong { color: #fef08a; }
.disclaimer-note { color: #9ca3af !important; font-size: 0.8rem !important; font-style: italic; }
</style>
