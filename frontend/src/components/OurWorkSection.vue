<script setup>
import { ref } from 'vue'

const activeCase = ref(null)

const caseStudies = [
  {
    id: 1,
    client: 'World Health Organization',
    title: 'WASH Healthcare Intelligence & Monitoring Application',
    category: 'Full-Stack & Benchmarks',
    description: 'A student team engineered a responsive platform empowering healthcare workers to track, benchmark, and improve water and hygiene standards in decentralized facilities worldwide.',
    impact: '1,200+ Facilities Monitored',
    imageBg: 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)',
    tags: ['Vue 3', 'FastAPI', 'Offline First', 'Healthcare'],
    fullStory: 'The team worked directly with technical officers at WHO to transform complex spreadsheet-based audit protocols into an intuitive, touch-friendly web application with real-time analytics and automated PDF report generation.'
  },
  {
    id: 2,
    client: 'Pangolino Wildlife Network',
    title: 'Designing & Developing a Digital Presence for Pangolin Conservation',
    category: 'Web & Visual Design',
    description: 'A dedicated team crafted a high-converting marketing website and interactive donation funnel with custom animations for Nigerian wildlife conservation organization Pangolino.',
    impact: '3.4x Donor Conversion',
    imageBg: 'linear-gradient(135deg, #065f46 0%, #10b981 100%)',
    tags: ['UX Research', 'Webflow', 'Custom Animations', 'Stripe'],
    fullStory: 'Students developed end-to-end interactive storyboards, visual asset libraries, and high-performance Webflow pages, enabling international supporters to sponsor conservation ranger patrols.'
  },
  {
    id: 3,
    client: 'Energy Policy Institute (UChicago)',
    title: 'Crowdsourcing Platform to Empower Community Donors & Volunteers',
    category: 'Platform Engineering',
    description: 'Designed and deployed a responsive platform empowering community residents to coordinate solid-waste management and environmental benchmarking in urban micro-neighborhoods.',
    impact: '80,000+ Citizens Engaged',
    imageBg: 'linear-gradient(135deg, #4c1d95 0%, #8b5cf6 100%)',
    tags: ['Geospatial AI', 'Vue.js', 'PostgreSQL', 'Civic Tech'],
    fullStory: 'By integrating community mapping with localized reporting metrics, this project provided actionable insights to municipal authorities while incentivizing volunteer participation.'
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
        <span class="section-label coral">Case Studies</span>
        <h2>Our work & nonprofit impact</h2>
        <p style="max-width: 640px; margin: 0.75rem auto 0 auto;">
          Explore how our university student squads have delivered research-backed websites, applications, and AI benchmarks for organizations around the globe.
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
              <div style="font-size: 1.25rem; font-weight: 800; font-family: var(--font-heading);">
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
              Read case study
            </button>
          </div>
        </div>
      </div>

      <div class="text-center" style="margin-top: 3rem;">
        <a href="#submit-app" class="btn btn-primary btn-large">Start your project with us</a>
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
          Verified Impact: {{ activeCase.impact }}
        </div>

        <h4 style="margin-bottom: 0.5rem;">Project Overview</h4>
        <p style="margin-bottom: 1.5rem;">{{ activeCase.description }}</p>

        <h4 style="margin-bottom: 0.5rem;">Implementation & Results</h4>
        <p style="margin-bottom: 1.75rem;">{{ activeCase.fullStory }}</p>

        <div style="display: flex; gap: 1rem;">
          <a href="#submit-app" @click="closeModal" class="btn btn-primary" style="flex: 1;">Request Similar Solution</a>
          <button @click="closeModal" class="btn btn-secondary">Close</button>
        </div>
      </div>
    </div>
  </section>
</template>
