<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <div class="hero">
      <div class="hero-content">
        <div class="logo">
          <span class="logo-icon">🛡️</span>
          <span class="logo-text">DevGuardian</span>
        </div>
        
        <h1>Security Scanner<br/><span>Powered by AI</span></h1>
        
        <p class="subtitle">
          Detecta vulnerabilidades en tu código con análisis inteligente. 
          Escaneo gratuito, sin注册 required.
        </p>
        
        <div class="cta-buttons">
          <router-link to="/scan" class="btn-primary">
            <span>🔍</span> Escanear Código
          </router-link>
          <router-link to="/login" class="btn-secondary">
            Iniciar Sesión
          </router-link>
        </div>
        
        <!-- Quick Stats -->
        <div class="stats">
          <div class="stat">
            <span class="stat-value">18+</span>
            <span class="stat-label">Tipos de Vulns</span>
          </div>
          <div class="stat">
            <span class="stat-value">0€</span>
            <span class="stat-label">Gratis</span>
          </div>
          <div class="stat">
            <span class="stat-value">&lt;1s</span>
            <span class="stat-label">Tiempo</span>
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
      <h2>Características</h2>
      <div class="features-grid">
        <div class="feature">
          <div class="feature-icon">🔍</div>
          <h3>Escaneo Rápido</h3>
          <p>Analiza tu código en segundos. Detecta SQL Injection, XSS, credenciales hardcoded, y más.</p>
        </div>
        <div class="feature">
          <div class="feature-icon">🤖</div>
          <h3>IA Explicativa</h3>
          <p>Cada vulnerabilidad incluye explicación clara y sugerencia de fix generada por IA.</p>
        </div>
        <div class="feature">
          <div class="feature-icon">🔒</div>
          <h3>Semgrep Pro</h3>
          <p>Motor profesional de escaneo con reglas OWASP Top 10 y detección de secrets.</p>
        </div>
        <div class="feature">
          <div class="feature-icon">💾</div>
          <h3>Historial</h3>
          <p>Guarda tus escaneos. Compara resultados anteriores y sigue tu postura de seguridad.</p>
        </div>
      </div>
    </div>
    
    <!-- How It Works -->
    <div class="how-it-works">
      <h2>Cómo Funciona</h2>
      <div class="steps">
        <div class="step">
          <div class="step-num">1</div>
          <h3>Pega tu código</h3>
          <p>Copia y pega el código que quieres analizar</p>
        </div>
        <div class="step">
          <div class="step-num">2</div>
          <h3>Escaneo automático</h3>
          <p>Detecta vulnerabilidades en segundos</p>
        </div>
        <div class="step">
          <div class="step-num">3</div>
          <h3>Obtén resultados</h3>
          <p>Ver vulnerabilidads con severity y fix</p>
        </div>
      </div>
    </div>
    
    <!-- CTA -->
    <div class="cta-section">
      <h2>Empieza Ahora</h2>
      <p>Sin registro. Totalmente gratis.</p>
      <router-link to="/scan" class="btn-primary btn-large">
        🚀 Escanear Ahora
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

.logo-icon {
  font-size: 2rem;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #3b82f6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero h1 {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1rem;
}

.hero h1 span {
  background: linear-gradient(135deg, #3b82f6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  color: #94a3b8;
  font-size: 1.125rem;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 3rem;
}

@media (max-width: 768px) {
  .cta-buttons {
    justify-content: center;
  }
}

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

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #06b6d4);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 40px rgba(59, 130, 246, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
}

.stats {
  display: flex;
  gap: 2rem;
}

@media (max-width: 768px) {
  .stats {
    justify-content: center;
  }
}

.stat {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #06b6d4;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
}

/* Demo Card */
.demo-card {
  background: #1e293b;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
}

.demo-header {
  background: #0f172a;
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.dot.red { background: #ef4444; }
.dot.yellow { background: #eab308; }
.dot.green { background: #22c55e; }

.demo-title {
  margin-left: auto;
  font-size: 0.75rem;
  color: #64748b;
}

.demo-content {
  padding: 1.5rem;
}

.code-example {
  background: #0f172a;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  font-family: 'Fira Code', monospace;
  font-size: 0.875rem;
}

.keyword { color: #c084fc; }
.string { color: #4ade80; }

.vuln-found {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 0.5rem;
  margin-bottom: 0.75rem;
}

.severity.critical {
  background: #dc2626;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 700;
}

.score {
  font-size: 0.875rem;
  color: #94a3b8;
}

.score strong {
  color: #f59e0b;
}

/* Features */
.features {
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.features h2, .how-it-works h2, .cta-section h2 {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

@media (max-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .features-grid {
    grid-template-columns: 1fr;
  }
}

.feature {
  background: rgba(255, 255, 255, 0.05);
  padding: 1.5rem;
  border-radius: 1rem;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature h3 {
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
}

.feature p {
  font-size: 0.875rem;
  color: #94a3b8;
  line-height: 1.5;
}

/* How It Works */
.how-it-works {
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

@media (max-width: 768px) {
  .steps {
    grid-template-columns: 1fr;
  }
}

.step {
  text-align: center;
}

.step-num {
  width: 3rem;
  height: 3rem;
  background: linear-gradient(135deg, #3b82f6, #06b6d4);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 auto 1rem;
}

/* CTA Section */
.cta-section {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(6, 182, 212, 0.1));
}

.cta-section p {
  color: #94a3b8;
  margin-bottom: 2rem;
}

.btn-large {
  font-size: 1.125rem;
  padding: 1rem 2rem;
}
</style>
