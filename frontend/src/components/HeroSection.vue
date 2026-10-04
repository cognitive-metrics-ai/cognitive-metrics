<script setup>
import { ref } from 'vue'

const isSimulating = ref(false)
const auditProgress = ref(100)
const metricsStatus = ref('All 14 Benchmarks Passed')
const alignmentScore = ref(99.4)
const latencyScore = ref('124ms')

const runAuditSimulation = () => {
  if (isSimulating.value) return
  isSimulating.value = true
  auditProgress.value = 0
  metricsStatus.value = 'Running evaluation suite...'
  
  const interval = setInterval(() => {
    if (auditProgress.value >= 100) {
      clearInterval(interval)
      isSimulating.value = false
      metricsStatus.value = 'Verification Complete: Certified High-Fidelity'
      alignmentScore.value = (98.8 + Math.random() * 0.9).toFixed(1)
      latencyScore.value = `${Math.floor(110 + Math.random() * 20)}ms`
    } else {
      auditProgress.value += 20
    }
  }, 250)
}
</script>

<template>
  <section class="section section-divider" style="padding-top: 4.5rem; padding-bottom: 5.5rem;">
    <div class="container">
      <div class="hero-grid">
        <!-- Hero Content Left -->
        <div class="hero-content">
          <span class="section-label coral">Design · Benchmarks · AI Strategy</span>
          <h1>Get the cognitive & AI support your mission needs</h1>
          <p class="hero-subtitle">
            We design research-backed cognitive apps, build intelligence-optimized websites & dashboards, and provide AI audit & strategy services by connecting mission-driven teams with squads of elite university researchers and engineers.
          </p>

          <div class="hero-buttons">
            <a href="#submit-app" class="btn btn-primary btn-large">Submit a proposal</a>
            <a href="#client-services" class="btn btn-secondary btn-large">Our services</a>
          </div>

          <!-- Trust Badges -->
          <div class="hero-trust-badges">
            <div class="trust-item">
              <span class="trust-number">~800 hrs</span>
              <span class="trust-label">Technical work per batch</span>
            </div>
            <div class="trust-item">
              <span class="trust-number">$1,000</span>
              <span class="trust-label">Flat nonprofit fee</span>
            </div>
            <div class="trust-item">
              <span class="trust-number">100%</span>
              <span class="trust-label">Vetted student talent</span>
            </div>
          </div>
        </div>

        <!-- Hero Graphic Right: Interactive Diagnostic Mockup -->
        <div class="hero-visual-card">
          <div class="mockup-header">
            <div class="mockup-dots">
              <span class="mockup-dot red"></span>
              <span class="mockup-dot yellow"></span>
              <span class="mockup-dot green"></span>
            </div>
            <span class="mockup-badge">LIVE COGNITIVE METRICS ENGINE</span>
          </div>

          <div class="mockup-body">
            <!-- Top stats card -->
            <div style="background: #f8fafc; border-radius: 12px; padding: 1.25rem; border: 1px solid #e2e8f0; margin-bottom: 1.25rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #64748b; letter-spacing: 0.05em;">Current Batch Deployment</span>
                <span style="display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.75rem; font-weight: 700; color: #10b981; background: #ecfdf5; padding: 0.2rem 0.6rem; border-radius: 9999px;">
                  <span style="width: 6px; height: 6px; border-radius: 50%; background: #10b981;"></span>
                  Active Squad
                </span>
              </div>
              <div style="font-size: 1.15rem; font-weight: 700; color: #0e1b2f; margin-bottom: 0.25rem;">
                Global Health WASH Model & Dashboard
              </div>
              <div style="font-size: 0.85rem; color: #64748b;">
                Partner: World Health Organization · Lead: Stanford & UC Berkeley
              </div>
            </div>

            <!-- Dynamic Metrics Grid -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem;">
              <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem; background: #ffffff;">
                <div style="font-size: 0.75rem; color: #64748b; font-weight: 600;">ALIGNMENT FIDELITY</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #f52c68; margin: 0.2rem 0;">{{ alignmentScore }}%</div>
                <div style="font-size: 0.75rem; color: #10b981; font-weight: 600;">▲ +4.2% vs baseline</div>
              </div>
              <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem; background: #ffffff;">
                <div style="font-size: 0.75rem; color: #64748b; font-weight: 600;">INFERENCE LATENCY</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #2563eb; margin: 0.2rem 0;">{{ latencyScore }}</div>
                <div style="font-size: 0.75rem; color: #64748b;">3.2x throughput speed</div>
              </div>
            </div>

            <!-- Progress & Simulation Bar -->
            <div style="background: #f1f5f9; border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 1.25rem;">
              <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 600; color: #334155; margin-bottom: 0.4rem;">
                <span>{{ metricsStatus }}</span>
                <span>{{ auditProgress }}%</span>
              </div>
              <div style="height: 6px; width: 100%; background: #e2e8f0; border-radius: 9999px; overflow: hidden;">
                <div :style="{ width: `${auditProgress}%`, background: 'linear-gradient(90deg, #f52c68, #2563eb)' }" style="height: 100%; transition: width 0.3s ease;"></div>
              </div>
            </div>

            <!-- Interactive Action Button -->
            <button 
              @click="runAuditSimulation" 
              :disabled="isSimulating"
              class="btn btn-secondary" 
              style="width: 100%; font-size: 0.875rem; padding: 0.65rem 1rem;"
            >
              <svg v-if="!isSimulating" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
              <svg v-else class="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
                <path d="M12 2a10 10 0 0 1 10 10" stroke="#f52c68"></path>
              </svg>
              {{ isSimulating ? 'Evaluating Safety & Alignment...' : 'Run Interactive Audit Check' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
