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
        <span class="section-label">Featured Publication</span>
        <h2>Resources for mission-driven leaders</h2>
      </div>

      <div style="background: #ffffff; border-radius: 16px; border: 1px solid var(--color-border); box-shadow: var(--shadow-md); overflow: hidden; display: grid; grid-template-columns: 1fr 1.3fr; gap: 2.5rem; align-items: center; padding: 2.5rem;">
        <!-- Left Book Mockup Graphic -->
        <div style="background: linear-gradient(135deg, #0e1b2f 0%, #1e3a8a 100%); border-radius: 12px; padding: 3rem 2rem; color: white; text-align: center; box-shadow: 0 15px 30px rgba(14, 27, 47, 0.25);">
          <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #f52c68; letter-spacing: 0.15em; margin-bottom: 1rem;">
            Cognitive Metrics Field Guide
          </div>
          <div style="font-size: 1.75rem; font-weight: 800; font-family: var(--font-heading); margin-bottom: 1rem; line-height: 1.25;">
            Nonprofit AI & Systems Optimization Guide
          </div>
          <div style="font-size: 0.9rem; color: #94a3b8;">
            A practical handbook for social impact executives navigating modern AI, web performance, and cognitive benchmarks.
          </div>
        </div>

        <!-- Right Content -->
        <div>
          <span class="section-label coral">Free Strategy Guide</span>
          <h3 style="font-size: 1.6rem; margin-bottom: 0.75rem;">Your organization’s roadmap to responsible digital innovation</h3>
          <p style="font-size: 0.95rem; margin-bottom: 1.25rem;">
            94% of first impressions are based on digital design and system responsiveness. For nonprofits, modern AI and digital tools aren't just technical upgrades—they are your primary levers for donor trust, volunteer mobilization, and program delivery.
          </p>

          <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.9rem; color: #334155; margin-bottom: 1.75rem;">
            <li style="display: flex; align-items: center; gap: 0.5rem;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f52c68" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Why ethical AI benchmarks matter for community trust</span>
            </li>
            <li style="display: flex; align-items: center; gap: 0.5rem;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f52c68" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Key elements of high-converting nonprofit websites & donation funnels</span>
            </li>
            <li style="display: flex; align-items: center; gap: 0.5rem;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f52c68" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Actionable metrics: Google Analytics, model observability, and SEO</span>
            </li>
          </ul>

          <button @click="openGuide" class="btn btn-secondary">
            Read optimization summary
          </button>
        </div>
      </div>
    </div>

    <!-- Guide Summary Modal -->
    <div v-if="showGuideModal" class="modal-backdrop" @click="closeGuide" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(4px); z-index: 999; display: flex; align-items: center; justify-content: center; padding: 1.5rem;">
      <div class="modal-content" @click.stop style="background: #ffffff; border-radius: 16px; max-width: 600px; width: 100%; max-height: 85vh; overflow-y: auto; padding: 2.5rem; position: relative;">
        <button @click="closeGuide" style="position: absolute; top: 1.25rem; right: 1.25rem; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #64748b;">
          &times;
        </button>

        <span class="section-label coral">Executive Summary</span>
        <h2 style="font-size: 1.6rem; margin-bottom: 1rem;">Nonprofit AI & Systems Optimization Guide</h2>
        <div style="font-size: 0.95rem; color: #475569; line-height: 1.65; margin-bottom: 1.5rem;">
          <p style="margin-bottom: 1rem;">
            This publication outlines the critical technical infrastructure modern mission-driven organizations need. By pairing human-centered UX research with verifiable cognitive evaluations, nonprofits can maximize their operational efficiency while upholding community privacy and safety standards.
          </p>
          <p>
            When applying for our 16-week project batches, teams receive an in-depth custom audit and implementation roadmap aligned with this framework.
          </p>
        </div>

        <div style="display: flex; gap: 1rem;">
          <a href="#submit-app" @click="closeGuide" class="btn btn-primary" style="flex: 1;">Apply for Project Batch</a>
          <button @click="closeGuide" class="btn btn-secondary">Close</button>
        </div>
      </div>
    </div>
  </section>
</template>
