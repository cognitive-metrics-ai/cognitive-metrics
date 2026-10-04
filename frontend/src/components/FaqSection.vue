<script setup>
import { ref } from 'vue'

const openIndices = ref([0]) // First FAQ open by default

const faqsCol1 = [
  {
    q: 'Why are development services offered with zero development expenses?',
    a: 'Our focus is strictly on advancing empirical academic research into the Agentic Development Life Cycle (ADLC) and cognitive metrics in software engineering. We offer full design and software development at no cost because your project serves as an empirical research study, yielding valuable scientific data and joint peer-reviewed publications.'
  },
  {
    q: 'Who is eligible to propose an academic research collaboration?',
    a: 'Eligible collaborators include university professors, principal investigators (PIs), postdoctoral fellows, doctoral candidates, and academic research institutions. The proposed study must be targeted for academic conference/journal publication or thesis defense.'
  },
  {
    q: 'Can commercial businesses or startups apply for this service?',
    a: 'No. This service is strictly non-commercial. We do not take on business ventures, commercial software products, or corporate consulting. Every project taken on must be an academic study with open or peer-reviewed scientific deliverables.'
  },
  {
    q: 'What types of projects qualify under ADLC research?',
    a: 'Qualifying projects investigate the Agentic Development Life Cycle. This includes human-agent paired development, autonomous multi-agent task orchestration, developer cognitive friction, mental workload measurement, hallucination guardrails, and agent evaluation benchmarks.'
  }
]

const faqsCol2 = [
  {
    q: 'How are intellectual property (IP) and publication authorship handled?',
    a: 'Your university or research lab retains full ownership of your domain hypotheses, proprietary datasets, and core research concepts. Because we provide complete pro-bono software engineering and telemetry instrumentation, we participate as technical co-authors or collaborators on resulting scholarly publications.'
  },
  {
    q: 'What kind of software testbeds can you build for our lab?',
    a: 'We build complete full-stack web applications, interactive stimulus presentation interfaces, experimental IDE testbeds, participant onboarding flows, multi-agent execution harnesses, and real-time cognitive telemetry collectors (exporting directly to JSONL, SQLite, or Parquet).'
  },
  {
    q: 'What is expected of our lab during the research engagement?',
    a: 'Your lab provides the experimental design, participant recruitment protocols, and an academic point-of-contact for a weekly technical sync. You are also responsible for securing your institution’s IRB (Institutional Review Board) approval if conducting human-subject trials.'
  },
  {
    q: 'How fast can our experimental testbed be built and deployed?',
    a: 'Most experimental prototypes and instrumented testbeds are fully engineered and verified within 4 to 8 weeks, ensuring your team has sufficient runway to gather participant data ahead of major academic submission deadlines (ICSE, CHI, FSE, NeurIPS, ACL, AAAI).'
  }
]

const toggleFaq = (key) => {
  const idx = openIndices.value.indexOf(key)
  if (idx > -1) {
    openIndices.value.splice(idx, 1)
  } else {
    openIndices.value.push(key)
  }
}

const isOpen = (key) => openIndices.value.includes(key)
</script>

<template>
  <section id="faqs" class="section section-divider">
    <div class="container">
      <div class="text-center" style="margin-bottom: 3.5rem;">
        <span class="section-label coral">Academic Inquiry FAQ</span>
        <h2>Frequently asked questions</h2>
        <p style="max-width: 620px; margin: 0.5rem auto 0 auto;">
          Key details about our pro-bono academic development model, ADLC research scope, and collaboration terms.
        </p>
      </div>

      <div class="faq-grid">
        <!-- Column 1 -->
        <div class="faq-column">
          <div 
            v-for="(faq, i) in faqsCol1" 
            :key="'col1-' + i" 
            class="faq-item"
            :class="{ open: isOpen('col1-' + i) }"
          >
            <button 
              class="faq-trigger" 
              @click="toggleFaq('col1-' + i)"
              :aria-expanded="isOpen('col1-' + i)"
            >
              <span class="faq-question">{{ faq.q }}</span>
              <div class="faq-circle-btn">
                <span class="line-h"></span>
                <span class="line-v"></span>
              </div>
            </button>
            <div v-show="isOpen('col1-' + i)" class="faq-body" style="white-space: pre-line;">
              {{ faq.a }}
            </div>
          </div>
        </div>

        <!-- Column 2 -->
        <div class="faq-column">
          <div 
            v-for="(faq, i) in faqsCol2" 
            :key="'col2-' + i" 
            class="faq-item"
            :class="{ open: isOpen('col2-' + i) }"
          >
            <button 
              class="faq-trigger" 
              @click="toggleFaq('col2-' + i)"
              :aria-expanded="isOpen('col2-' + i)"
            >
              <span class="faq-question">{{ faq.q }}</span>
              <div class="faq-circle-btn">
                <span class="line-h"></span>
                <span class="line-v"></span>
              </div>
            </button>
            <div v-show="isOpen('col2-' + i)" class="faq-body" style="white-space: pre-line;">
              {{ faq.a }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
