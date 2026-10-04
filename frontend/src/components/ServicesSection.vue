<script setup>
const emit = defineEmits(['select-service'])

const services = [
  {
    id: 'testbed_dev',
    title: 'Experimental Testbed & Prototype Engineering',
    iconColor: '#1B6CA8',
    desc: 'We design and build production-grade web applications, interactive software testbeds, and stimulus control environments tailored specifically to your lab’s experimental requirements.',
    sprintTypes: [
      'Interactive web-based study testbeds & UI',
      'Full-stack stimulus & task presentation tools',
      'Subject trial interfaces & participant onboarding',
      'Researcher control consoles & session management',
      'Cross-platform responsiveness & accessibility'
    ],
    techOptions: 'Frontend: Vue 3, Vite, HTML5 Canvas, WebSockets\nBackend: FastAPI, Python, PostgreSQL, Docker\nDeployment: University servers, Cloud testbeds',
    requirements: 'A defined study protocol, description of participant tasks, and clear experimental variables/conditions to be evaluated.'
  },
  {
    id: 'telemetry_metrics',
    title: 'ADLC Telemetry & Cognitive Metric Instrumentation',
    iconColor: '#4DA8DA',
    desc: 'We instrument software prototypes with granular behavioral event logging and cognitive friction tracking to capture developer interaction dynamics during agentic workflows.',
    sprintTypes: [
      'Micro-interaction & cognitive latency loggers',
      'Developer friction & handoff telemetry pipelines',
      'Interruption recovery & task-switching monitors',
      'Anonymized session recording & trace export',
      'Automated empirical data aggregation & CSV/JSON export'
    ],
    techOptions: 'Instrumentation: Custom event SDKs, OpenTelemetry\nStorage: Structured JSONL, SQLite, DuckDB, Parquet\nAnalytics: Python Pandas/Polars scripts, R export',
    requirements: 'Defined dependent variables, telemetry schema preferences, and IRB/ethics-compliant participant data handling procedures.'
  },
  {
    id: 'agentic_arch',
    title: 'Agentic Architectures & Benchmark Evaluation',
    badge: 'CORE ADLC FOCUS',
    iconColor: '#10b981',
    desc: 'We implement and evaluate autonomous agent architectures, multi-agent coordination loops, and human-in-the-loop validation frameworks to test your theoretical ADLC models.',
    sprintTypes: [
      'Multi-agent task decomposition pipelines',
      'Autonomous code synthesis & review harnesses',
      'Human-in-the-loop intervention gates & metrics',
      'Systematic error & hallucination benchmarks',
      'Comparative baseline model testing'
    ],
    techOptions: 'Agent Frameworks: LangGraph, AutoGen, custom state machines\nModels: Claude, OpenAI, Gemini, Local Open-Weights (Ollama/vLLM)\nBenchmarking: Automated evaluation scripts',
    requirements: 'Research hypotheses regarding agent behavior, target evaluation rubrics, and model access credentials for your experiment.'
  }
]

const handleSelect = (serviceId) => {
  emit('select-service', serviceId)
  const el = document.getElementById('submit-app')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<template>
  <section id="client-services" class="section section-divider">
    <div class="container">
      <div class="text-center" style="margin-bottom: 3.5rem;">
        <span class="section-label coral">Zero-Expense Research Engineering</span>
        <h2>Pro-bono development for ADLC research</h2>
        <div style="max-width: 860px; margin: 1.25rem auto 0 auto; background: var(--color-blue-light); border: 1px solid #bfdbfe; border-radius: 12px; padding: 1.5rem; text-align: left;">
          <h5 style="color: var(--color-navy); margin-bottom: 0.5rem; font-weight: 700;">
            100% Free Development · No Consulting Fees · No Development Expenses
          </h5>
          <p style="font-size: 0.95rem; color: #334155; margin: 0;">
            I offer full software design and development capabilities directly to academic researchers with <strong>zero development expenses</strong>. This is not a commercial service, commercial product, or consulting business. I take on software development for qualifying research projects in exchange for the opportunity to advance empirical scientific discovery on the <strong>Agentic Development Life Cycle (ADLC)</strong> and co-author peer-reviewed publications.
          </p>
        </div>
      </div>

      <div class="grid-3-col">
        <div v-for="service in services" :key="service.id" class="service-card">
          <!-- Icon & Header -->
          <div class="service-icon-banner">
            <div :style="{ width: '52px', height: '52px', borderRadius: '12px', background: `${service.iconColor}15`, color: service.iconColor, display: 'flex', alignItems: 'center', justifyContent: 'center' }">
              <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21 15 16 10 5 21"></polyline>
              </svg>
            </div>
            <span v-if="service.badge" style="margin-left: auto; font-size: 0.75rem; font-weight: 700; color: #059669; background: #d1fae5; padding: 0.25rem 0.6rem; border-radius: 9999px;">
              {{ service.badge }}
            </span>
          </div>

          <h3 style="margin-bottom: 0.75rem; font-size: 1.35rem;">{{ service.title }}</h3>
          <p style="font-size: 0.95rem; margin-bottom: 1.25rem;">{{ service.desc }}</p>

          <!-- Sprints / Research Areas -->
          <div class="service-section-block">
            <div class="service-section-label">DEVELOPMENT DELIVERABLES</div>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.875rem; color: var(--color-text-main);">
              <li v-for="st in service.sprintTypes" :key="st" style="display: flex; align-items: flex-start; gap: 0.4rem;">
                <span style="color: var(--color-blue); font-weight: bold;">•</span>
                <span>{{ st }}</span>
              </li>
            </ul>
          </div>

          <!-- Technologies -->
          <div class="service-section-block">
            <div class="service-section-label">STACK & INSTRUMENTATION</div>
            <div class="service-section-content" style="white-space: pre-line;">{{ service.techOptions }}</div>
          </div>

          <!-- Requirements -->
          <div class="service-section-block" style="flex-grow: 1;">
            <div class="service-section-label">LAB PRE-REQUISITES</div>
            <div class="service-section-content">{{ service.requirements }}</div>
          </div>

          <!-- Select Button -->
          <div style="margin-top: 1.75rem; padding-top: 1rem; border-top: 1px solid var(--color-border);">
            <button @click="handleSelect(service.id)" class="btn btn-primary" style="width: 100%; font-size: 0.9rem;">
              Request for research study
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
