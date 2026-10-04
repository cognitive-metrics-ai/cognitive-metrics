<script setup>
import { ref } from 'vue'

const activeCase = ref(null)

const caseStudies = [
  {
    id: 1,
    client: 'Software Engineering & HCI Lab',
    title: 'Human-in-the-Loop ADLC Code Synthesis Benchmark',
    category: 'ADLC Empirical Study',
    description: 'Designed and engineered an experimental IDE testbed measuring developer cognitive load, interruption recovery latency, and task completion fidelity during autonomous agent code synthesis.',
    impact: '12,000+ Empirical Traces · $0 Grant Cost',
    imageBg: 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)',
    tags: ['ADLC Metrics', 'Cognitive Load', 'FastAPI', 'Vue 3', 'Eye-Tracking Hook'],
    fullStory: 'The lab needed a custom web-based IDE testbed to compare traditional development against an Agentic Development Life Cycle (ADLC). We engineered the complete frontend interface, telemetry event loggers, and LLM orchestration layer at zero development expense, enabling the researchers to conduct controlled trials and submit to ACM/IEEE conferences.'
  },
  {
    id: 2,
    client: 'Biomedical Informatics Research Group',
    title: 'Multi-Agent Clinical Diagnostic Decision Testbed',
    category: 'Autonomous Agent Research',
    description: 'Built a multi-agent orchestration testbed allowing medical researchers to evaluate physician trust calibration, cognitive friction, and autonomous verification protocols in healthcare workflows.',
    impact: 'Multi-Center Trial · Zero Development Fees',
    imageBg: 'linear-gradient(135deg, #065f46 0%, #10b981 100%)',
    tags: ['Clinical ADLC', 'Multi-Agent Systems', 'Safety Auditing', 'Python'],
    fullStory: 'Researchers sought to investigate how clinicians interact when AI agents autonomously synthesize lab records and propose differential diagnoses. We designed and built the double-blind experimental software testbed, logging time-to-decision and physician verification steps without charging any consulting or development fees.'
  },
  {
    id: 3,
    client: 'Cognitive Computing & Learning Lab',
    title: 'Cognitive Friction Telemetry & Benchmark Harness',
    category: 'Cognitive Metrics',
    description: 'Constructed an open-source evaluation suite and behavioral telemetry harness quantifying mental fatigue, task switching overhead, and autonomous agent delegation patterns.',
    impact: 'Open Research Artifact · 100% Free Collaboration',
    imageBg: 'linear-gradient(135deg, #4c1d95 0%, #8b5cf6 100%)',
    tags: ['Telemetry Harness', 'Open Science', 'Benchmark Suite', 'Reproducible Protocol'],
    fullStory: 'To evaluate autonomous development agents across complex multi-step workflows, the research team needed standardized cognitive metric logging. We implemented the telemetry collector, benchmark harnesses, and visualization dashboard entirely pro-bono for their academic publication.'
  }
]

const openModal = (caseItem) => {
  activeCase.value = caseItem
}

const closeModal = () => {
  activeCase.value = null
}
</script>

<template>
  <section id="our-work" class="section section-divider section-light">
    <div class="container">
      <div class="text-center" style="margin-bottom: 3rem;">
        <span class="section-label coral">Peer-Reviewed & Empirical Science</span>
        <h2>ADLC research studies & testbeds</h2>
        <p style="max-width: 680px; margin: 0.75rem auto 0 auto;">
          Review sample academic research testbeds and experimental prototypes engineered pro-bono to study the Agentic Development Life Cycle.
        </p>
      </div>

      <div class="grid-3-col">
        <div v-for="item in caseStudies" :key="item.id" class="case-card">
          <!-- Card Visual Cover -->
          <div class="case-image-wrapper" :style="{ background: item.imageBg, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1.5rem', color: '#ffffff' }">
            <div style="text-align: center;">
              <span style="display: inline-block; font-size: 0.75rem; text-transform: uppercase; font-weight: 700; background: rgba(255,255,255,0.2); padding: 0.25rem 0.75rem; border-radius: 9999px; margin-bottom: 0.75rem; backdrop-filter: blur(4px);">
                {{ item.category }}
              </span>
              <div style="font-size: 1.15rem; font-weight: 800; font-family: var(--font-heading);">
                {{ item.impact }}
              </div>
            </div>
          </div>

          <!-- Card Content -->
          <div class="case-card-body">
            <span class="case-client-tag">{{ item.client }}</span>
            <h3 class="case-title">{{ item.title }}</h3>
            <p class="case-desc">{{ item.description }}</p>

            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 1.5rem;">
              <span v-for="tag in item.tags" :key="tag" style="font-size: 0.75rem; font-weight: 600; background: #f1f5f9; color: #475569; padding: 0.2rem 0.5rem; border-radius: 4px;">
                {{ tag }}
              </span>
            </div>

            <button @click="openModal(item)" class="btn btn-secondary" style="width: 100%; margin-top: auto;">
              View study details
            </button>
          </div>
        </div>
      </div>

      <div class="text-center" style="margin-top: 3rem;">
        <a href="#submit-app" class="btn btn-primary btn-large">Propose an ADLC research collaboration</a>
      </div>
    </div>

    <!-- Case Study Detail Modal -->
    <div v-if="activeCase" class="modal-backdrop" @click="closeModal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(4px); z-index: 999; display: flex; align-items: center; justify-content: center; padding: 1.5rem;">
      <div class="modal-content" @click.stop style="background: #ffffff; border-radius: 16px; max-width: 640px; width: 100%; max-height: 90vh; overflow-y: auto; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); padding: 2.5rem; position: relative;">
        <button @click="closeModal" style="position: absolute; top: 1.25rem; right: 1.25rem; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #64748b;">
          &times;
        </button>

        <span class="section-label coral">{{ activeCase.client }}</span>
        <h2 style="font-size: 1.75rem; margin-bottom: 1rem;">{{ activeCase.title }}</h2>
        <div style="background: var(--color-blue-light); color: var(--color-blue-dark); font-weight: 700; padding: 0.6rem 1rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.95rem;">
          Research Milestone: {{ activeCase.impact }}
        </div>

        <h4 style="margin-bottom: 0.5rem;">Experimental Objective</h4>
        <p style="margin-bottom: 1.5rem;">{{ activeCase.description }}</p>

        <h4 style="margin-bottom: 0.5rem;">Technical Implementation ($0 Development Expenses)</h4>
        <p style="margin-bottom: 1.75rem;">{{ activeCase.fullStory }}</p>

        <div style="display: flex; gap: 1rem;">
          <a href="#submit-app" @click="closeModal" class="btn btn-primary" style="flex: 1;">Propose Your Research Project</a>
          <button @click="closeModal" class="btn btn-secondary">Close</button>
        </div>
      </div>
    </div>
  </section>
</template>
