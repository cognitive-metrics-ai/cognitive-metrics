<script setup>
import { ref } from 'vue'

const openIndices = ref([0]) // First FAQ open by default

const faqsCol1 = [
  {
    q: 'Is my organization eligible for our services?',
    a: 'All eligible nonprofits or organizations must be able to present documents officiating their status as any of the following:\n\n• U.S.-based nonprofits: 501(c)(3) letter of determination\n• Non-U.S.-based nonprofits: Proof of registered charity/nonprofit status in home country\n• Governing agencies or international organizations: Official charter or NGO registration\n\nAlthough we resonate with the missions of social impact startups, we cannot match volunteer developers and designers with for-profit organizations under the Fair Labor Standards Act.'
  },
  {
    q: 'How will Cognitive Metrics ensure a smooth project handover?',
    a: 'At the end of the program, we make sure to document all work before the handover. Your student squad will organize and deliver all Figma design files, research assets, production code repositories, and step-by-step documentation guiding your team on maintenance and future updates.'
  },
  {
    q: 'How do you source top tech & design talent?',
    a: "Each student and mentor volunteer matched to your project is carefully evaluated by our management team. Candidates are scored across Technical skill, Passion, Resilience, and Leadership. Key roles are handpicked, while others are paired via our matching system based on technical competencies and social cause alignment."
  },
  {
    q: 'What can I expect from this 16-week program?',
    a: 'You can expect a dedicated team of 4–6 university students and mentors dedicating ~800 hours over 16 weeks. Students commit 5–10 hours per week, supported by professional industry mentors. While teams work diligently to complete scope, projects focus on delivering verified, high-quality milestones.'
  }
]

const faqsCol2 = [
  {
    q: 'How is my project proposal reviewed and scoped?',
    a: 'After you submit your proposal, our Product Leads screen it to ensure alignment with technologies our talent pool excels in. Nonprofits accepted into the cohort enter a month-long scoping phase where the team collaborates with you on a formal Product Requirements Document (PRD) before development begins.'
  },
  {
    q: 'What if I need both design and engineering work done?',
    a: 'Our multidisciplinary squads are built specifically for full-lifecycle delivery! Teams typically include both UI/UX designers and software engineers, allowing us to simultaneously conduct user research, build design systems, and implement full-stack code or CMS integrations.'
  },
  {
    q: 'What is expected of my nonprofit during the program?',
    a: 'Your organization must provide a dedicated point-of-contact available for a ~1 hour sync every week throughout the 16-week engagement. Additionally, we ask clients to provide necessary brand assets, credentials, and respond to team inquiries within 48 business hours.'
  },
  {
    q: 'Can we continue our partnership in subsequent batches?',
    a: 'Absolutely! Many of our nonprofit partners engage with us across multiple successive batches to expand product capabilities, launch secondary features, or audit newer models. Each 16-week batch carries the standard flat fee of $1,000.'
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
        <span class="section-label coral">Help Center</span>
        <h2>Frequently asked questions</h2>
        <p style="max-width: 620px; margin: 0.5rem auto 0 auto;">
          Everything you need to know about our student squads, deliverables, and partnership process.
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
