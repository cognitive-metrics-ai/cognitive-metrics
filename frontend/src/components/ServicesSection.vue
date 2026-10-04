<script setup>
const emit = defineEmits(['select-service'])

const services = [
  {
    id: 'ux_design',
    title: 'UX research & UI design',
    iconColor: '#2563eb',
    desc: 'From uncovering user needs to defining research-backed product strategies, our student designers uncover insights that drive intuitive and effective design solutions.',
    sprintTypes: [
      'User personas & journey maps and flows',
      'Competitive analyses & cognitive friction audits',
      'Information architecture (IA)',
      'Design systems & visual design tokens',
      'Interactive clickable prototypes'
    ],
    techOptions: 'Design & Prototyping: Figma, FigJam\nResearch: Dovetail, Optimal Workshop\nSurveys: Typeform, Google Forms',
    requirements: "A clear understanding of your product's objectives, target demographic user groups, key functionalities, and access to brand guidelines."
  },
  {
    id: 'web_dev',
    title: 'Website & application development',
    iconColor: '#f52c68',
    desc: 'Our tech students craft intuitive, accessible, and high-performance websites and digital tools. At minimum, websites include responsive Home (impact), Donate, and About Us pages.',
    sprintTypes: [
      'Greenfield responsive web & app builds',
      'Interactive metric & impact dashboards',
      'Custom HTML, CSS, JavaScript, or Vue 3',
      'Third-party tools and API integrations',
      'SEO & accessibility compliance'
    ],
    techOptions: 'Frontend: Vue 3, Vite, Webflow, Squarespace\nBackend: FastAPI, REST APIs, Python\nHosting & CI/CD: Netlify, Vercel, Docker',
    requirements: "Brand guidelines and existing assets (if applicable). Technical familiarity with requested technologies and handover maintenance plans."
  },
  {
    id: 'ai_audit',
    title: 'AI audit & strategy',
    badge: 'NEW COHORT PILOT',
    iconColor: '#10b981',
    desc: 'We evaluate and audit AI readiness, data workflows, and LLM implementations for mission-driven teams, establishing verifiable accuracy and ethical safety guardrails.',
    sprintTypes: [
      'AI readiness assessment & model feasibility',
      'Workflow audits & operational pain points',
      'Use case identification & prioritization',
      'Model safety, hallucination & bias evaluation',
      'Implementation roadmap & tool selection'
    ],
    techOptions: 'Frameworks: AI risk management, custom safety rubrics\nModels Evaluated: Claude, ChatGPT, Gemini, Open Source LLMs\nAutomation: Slack, Airtable, Zapier',
    requirements: "A dedicated point-of-contact familiar with current tools. Openness to process improvements. NDAs available for sensitive organizational data."
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
        <span class="section-label coral">Menu of Services</span>
        <h2>Our services & batch model</h2>
        <div style="max-width: 860px; margin: 1.25rem auto 0 auto; background: var(--color-blue-light); border: 1px solid #bfdbfe; border-radius: 12px; padding: 1.5rem; text-align: left;">
          <h5 style="color: var(--color-navy); margin-bottom: 0.5rem; font-weight: 700;">
            16-Week Custom Sprints · 800 Hours of Technical Work · $1,000 Flat Fee
          </h5>
          <p style="font-size: 0.95rem; color: #334155; margin: 0;">
            Each project squad consists of: <strong>1 student Product Manager</strong>, <strong>1 student Design or Tech Lead</strong>, <strong>4–6 Engineers/Designers</strong>, and <strong>industry professional mentors</strong>. Together, they dedicate ~800 hours of technical execution at our unbeatable flat fee of $1,000. We are also open to considering further discounting to accommodate extenuating financial circumstances.
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

          <!-- Sprints -->
          <div class="service-section-block">
            <div class="service-section-label">SPRINT TYPES</div>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.875rem; color: var(--color-text-main);">
              <li v-for="st in service.sprintTypes" :key="st" style="display: flex; align-items: flex-start; gap: 0.4rem;">
                <span style="color: var(--color-blue); font-weight: bold;">•</span>
                <span>{{ st }}</span>
              </li>
            </ul>
          </div>

          <!-- Technologies -->
          <div class="service-section-block">
            <div class="service-section-label">TECHNOLOGY OPTIONS</div>
            <div class="service-section-content" style="white-space: pre-line;">{{ service.techOptions }}</div>
          </div>

          <!-- Requirements -->
          <div class="service-section-block" style="flex-grow: 1;">
            <div class="service-section-label">PRE-PROJECT REQUIREMENTS</div>
            <div class="service-section-content">{{ service.requirements }}</div>
          </div>

          <!-- Select Button -->
          <div style="margin-top: 1.75rem; padding-top: 1rem; border-top: 1px solid var(--color-border);">
            <button @click="handleSelect(service.id)" class="btn btn-primary" style="width: 100%; font-size: 0.9rem;">
              Select for proposal
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
