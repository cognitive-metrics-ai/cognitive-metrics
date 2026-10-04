<script setup>
import { ref } from 'vue'

const isSimulating = ref(false)
const telemetryProgress = ref(100)
const telemetryStatus = ref('Telemetry stream active · 1,480 trace events recorded')
const autonomyScore = ref(89.2)
const frictionIndex = ref(0.12)

const runTelemetrySimulation = () => {
  if (isSimulating.value) return
  isSimulating.value = true
  telemetryProgress.value = 0
  telemetryStatus.value = 'Capturing agent-human handoff & cognitive latency...'
  
  const interval = setInterval(() => {
    if (telemetryProgress.value >= 100) {
      clearInterval(interval)
      isSimulating.value = false
      telemetryStatus.value = 'ADLC Experiment Run Complete: Empirical Dataset Ready'
      autonomyScore.value = (87.5 + Math.random() * 4.5).toFixed(1)
      frictionIndex.value = (0.08 + Math.random() * 0.07).toFixed(2)
    } else {
      telemetryProgress.value += 20
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
          <span class="section-label coral">Pro-Bono Academic Collaboration · Zero Development Expenses</span>
          <h1>Free development services for academic ADLC research</h1>
          <p class="hero-subtitle">
            We partner with university research labs, principal investigators, and scholars to design, build, and deploy experimental software testbeds at <strong>zero development cost</strong>. We take on qualifying projects strictly to advance empirical research on the <strong>Agentic Development Life Cycle (ADLC)</strong>, autonomous agent coordination, and cognitive metrics.
          </p>

          <div class="hero-buttons">
            <a href="#submit-app" class="btn btn-primary btn-large">Submit research proposal</a>
            <a href="#client-services" class="btn btn-secondary btn-large">Our research services</a>
          </div>

          <!-- Trust Badges -->
          <div class="hero-trust-badges">
            <div class="trust-item">
              <span class="trust-number">$0 cost</span>
              <span class="trust-label">No development expenses</span>
            </div>
            <div class="trust-item">
              <span class="trust-number">ADLC focus</span>
              <span class="trust-label">Agentic lifecycle inquiry</span>
            </div>
            <div class="trust-item">
              <span class="trust-number">100% academic</span>
              <span class="trust-label">Non-commercial & peer-reviewed</span>
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
            <span class="mockup-badge">ADLC EXPERIMENTAL TELEMETRY SUITE</span>
          </div>

          <div class="mockup-body">
            <!-- Active Research Study Banner -->
            <div style="background: #f8fafc; border-radius: 12px; padding: 1.25rem; border: 1px solid #e2e8f0; margin-bottom: 1.25rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #64748b; letter-spacing: 0.05em;">Current Research Study</span>
                <span style="display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.75rem; font-weight: 700; color: var(--color-primary); background: var(--color-primary-light); padding: 0.2rem 0.6rem; border-radius: 9999px;">
                  <span style="width: 6px; height: 6px; border-radius: 50%; background: var(--color-primary);"></span>
                  Active Protocol
                </span>
              </div>
              <div style="font-size: 1.1rem; font-weight: 700; color: var(--color-navy); margin-bottom: 0.25rem;">
                Agentic Lifecycle & Cognitive Workload in Software Synthesis
              </div>
              <div style="font-size: 0.85rem; color: #64748b;">
                Principal Investigator Lab · Non-Commercial Empirical Testbed
              </div>
            </div>

            <!-- Dynamic Metrics Grid -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem;">
              <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem; background: #ffffff;">
                <div style="font-size: 0.72rem; color: #64748b; font-weight: 700;">AUTONOMY RATIO</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: var(--color-primary); margin: 0.2rem 0;">{{ autonomyScore }}%</div>
                <div style="font-size: 0.75rem; color: #10b981; font-weight: 600;">Autonomous step execution</div>
              </div>
              <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem; background: #ffffff;">
                <div style="font-size: 0.72rem; color: #64748b; font-weight: 700;">COGNITIVE FRICTION (CFI)</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: var(--color-sky); margin: 0.2rem 0;">{{ frictionIndex }}</div>
                <div style="font-size: 0.75rem; color: #64748b;">Low mental handover load</div>
              </div>
            </div>

            <!-- Telemetry Trace Status -->
            <div style="background: #f1f5f9; border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 1.25rem;">
              <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 600; color: #334155; margin-bottom: 0.4rem;">
                <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 80%;">{{ telemetryStatus }}</span>
                <span>{{ telemetryProgress }}%</span>
              </div>
              <div style="height: 6px; width: 100%; background: #e2e8f0; border-radius: 9999px; overflow: hidden;">
                <div :style="{ width: `${telemetryProgress}%`, background: 'linear-gradient(90deg, #1B6CA8, #4DA8DA)' }" style="height: 100%; transition: width 0.3s ease;"></div>
              </div>
            </div>

            <!-- Interactive Action Button -->
            <button 
              @click="runTelemetrySimulation" 
              :disabled="isSimulating"
              class="btn btn-secondary" 
              style="width: 100%; font-size: 0.875rem; padding: 0.65rem 1rem;"
            >
              <svg v-if="!isSimulating" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
              <svg v-else class="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
                <path d="M12 2a10 10 0 0 1 10 10" stroke="#1B6CA8"></path>
              </svg>
              {{ isSimulating ? 'Executing ADLC Instrumentation...' : 'Simulate ADLC Telemetry Run' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
