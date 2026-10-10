<script setup>
import { ref } from 'vue'

const showGuideModal = ref(false)

const openGuide = () => {
  showGuideModal.value = true
}

const closeGuide = () => {
  showGuideModal.value = false
}
</script>

<template>
  <section class="section section-divider section-light">
    <div class="container">
      <div class="text-center" style="margin-bottom: 3rem;">
        <span class="section-label">Open Science Publication</span>
        <h2>Research frameworks & telemetry standards</h2>
      </div>

      <div style="background: var(--color-bg-white); border-radius: 16px; border: 1px solid var(--color-border); box-shadow: var(--shadow-md); overflow: hidden; display: grid; grid-template-columns: 1fr 1.3fr; gap: 2.5rem; align-items: center; padding: 2.5rem;">
        <!-- Left Book Mockup Graphic -->
        <div style="background: linear-gradient(135deg, #0A3D62 0%, #1B6CA8 100%); border-radius: 12px; padding: 3rem 2rem; color: white; text-align: center; box-shadow: 0 15px 30px rgba(10, 61, 98, 0.3);">
          <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #4DA8DA; letter-spacing: 0.15em; margin-bottom: 1rem;">
            Cognitive Metrics Monograph
          </div>
          <div style="font-size: 1.7rem; font-weight: 800; font-family: var(--font-heading); margin-bottom: 1rem; line-height: 1.25;">
            The ADLC Empirical Research Handbook
          </div>
          <div style="font-size: 0.9rem; color: #94a3b8;">
            A methodological handbook on telemetry schemas, cognitive friction indices, and evaluation protocols in the Agentic Development Life Cycle.
          </div>
        </div>

        <!-- Right Content -->
        <div>
          <span class="section-label" style="color: #1B6CA8;">Methodological Guide</span>
          <h3 style="font-size: 1.55rem; margin-bottom: 0.75rem;">Standardizing empirical evaluation for autonomous & agentic software engineering</h3>
          <p style="font-size: 0.95rem; margin-bottom: 1.25rem;">
            As software engineering shifts toward autonomous agent architectures, traditional developer productivity metrics fail to capture the nuances of human-agent cognitive handoff, supervisory fatigue, and context degradation.
          </p>

          <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.9rem; color: #334155; margin-bottom: 1.75rem;">
            <li style="display: flex; align-items: center; gap: 0.5rem;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1B6CA8" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Granular telemetry models for human-agent handoffs & latency</span>
            </li>
            <li style="display: flex; align-items: center; gap: 0.5rem;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1B6CA8" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Cognitive Friction Index (CFI) formulation & statistical validity</span>
            </li>
            <li style="display: flex; align-items: center; gap: 0.5rem;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1B6CA8" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Open-source experimental testbed designs and stimulus generators</span>
            </li>
          </ul>

          <button @click="openGuide" class="btn btn-secondary">
            Read research methodology summary
          </button>
        </div>
      </div>
    </div>

    <!-- Guide Summary Modal -->
    <Teleport to="body">
      <div v-if="showGuideModal" class="modal-backdrop" @click="closeGuide">
        <div class="modal-content" @click.stop style="max-width: 600px;">
          <button @click="closeGuide" style="position: absolute; top: 1.25rem; right: 1.25rem; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--color-text-muted);" aria-label="Close guide modal">
            &times;
          </button>

          <span class="section-label coral">Academic Overview</span>
          <h2 style="font-size: 1.6rem; margin-bottom: 1rem; color: var(--color-navy);">The ADLC Research Framework</h2>
          <div style="font-size: 0.95rem; color: var(--color-text-muted); line-height: 1.65; margin-bottom: 1.5rem;">
            <p style="margin-bottom: 1rem;">
              This publication outlines our standardized telemetry architecture for human-subject and automated benchmarking in ADLC environments. By instrumenting micro-interaction events alongside model reasoning steps, researchers can objectively measure cognitive overhead, trust calibration, and autonomous fidelity.
            </p>
            <p>
              When partnering on a pro-bono academic project, your experimental testbed will automatically incorporate these standardized logging harnesses for seamless data analysis.
            </p>
          </div>

          <div style="display: flex; gap: 1rem;">
            <a href="#submit-app" @click="closeGuide" class="btn btn-primary" style="flex: 1;">Propose an ADLC Study</a>
            <button @click="closeGuide" class="btn btn-secondary">Close</button>
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>
