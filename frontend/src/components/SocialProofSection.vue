<script setup>
const universities = [
  'Stanford', 'UC Berkeley', 'MIT', 'Carnegie Mellon',
  'Harvard', 'Cornell', 'Brown', 'Columbia',
  'Georgia Tech', 'UPenn', 'Princeton', 'Caltech'
]
</script>

<template>
  <section class="section section-divider">
    <div class="container">
      <!-- WHO Testimonial Quote Block -->
      <div class="quote-box" style="margin-bottom: 5rem;">
        <div class="quote-avatar-wrapper">
          <div style="width: 130px; height: 130px; border-radius: 50%; background: linear-gradient(135deg, #0284c7, #0369a1); display: flex; align-items: center; justify-content: center; margin: 0 auto; color: white; font-weight: 800; font-size: 2.2rem; box-shadow: 0 10px 25px rgba(2, 132, 199, 0.25);">
            WHO
          </div>
        </div>
        <div class="quote-content">
          <div class="quote-text">
            &ldquo;Cognitive Metrics and Develop for Good provided us with smart, creative, and mature researchers and developers who took the WHO tool for improving water, sanitation, and hygiene in healthcare facilities and built a simple, robust application to better track and drive field improvements.&rdquo;
          </div>
          <div class="quote-author">Maggie Montgomery</div>
          <div class="quote-title">Technical Officer, World Health Organization</div>
        </div>
      </div>

      <!-- University Talent Logos -->
      <div class="text-center" style="margin-bottom: 3.5rem;">
        <span class="section-label">Top Tier Technical Talent</span>
        <h3>Our volunteer engineers and designers come from leading programs</h3>
        <p style="max-width: 600px; margin: 0.5rem auto 0 auto;">
          We handpick student fellows and mentors actively engaged at top computer science and design institutions.
        </p>

        <div class="logo-grid">
          <div v-for="school in universities" :key="school" class="logo-badge-item">
            {{ school }}
          </div>
        </div>
      </div>

      <!-- How We Maximize Project Success -->
      <div style="margin-top: 5rem; padding-top: 3.5rem; border-top: 1px solid var(--color-border);">
        <div class="text-center" style="margin-bottom: 3rem;">
          <span class="section-label coral">Partnership Criteria</span>
          <h2>How we maximize project success</h2>
          <p style="max-width: 620px; margin: 0.5rem auto 0 auto;">
            We look for key criteria that make projects ideal for our dedicated university student squads.
          </p>
        </div>

        <div class="grid-3-col">
          <div style="background: #ffffff; border: 1px solid var(--color-border); border-radius: 12px; padding: 2rem;">
            <div style="width: 50px; height: 50px; border-radius: 10px; background: var(--color-blue-light); color: var(--color-blue); display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <h4 style="margin-bottom: 0.75rem;">Flexible timeline</h4>
            <p style="font-size: 0.95rem;">
              Some timeline flexibility with your project helps us navigate students’ academic calendars and exam schedules, ensuring all deliverables receive rigorous attention.
            </p>
          </div>

          <div style="background: #ffffff; border: 1px solid var(--color-border); border-radius: 12px; padding: 2rem;">
            <div style="width: 50px; height: 50px; border-radius: 10px; background: var(--color-primary-light); color: var(--color-primary); display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <h4 style="margin-bottom: 0.75rem;">Dedicated point person</h4>
            <p style="font-size: 0.95rem;">
              Our program is highly personalized. We require a nonprofit point-of-contact to meet with our student team for a 1-hour weekly sync to provide prompt feedback.
            </p>
          </div>

          <div style="background: #ffffff; border: 1px solid var(--color-border); border-radius: 12px; padding: 2rem;">
            <div style="width: 50px; height: 50px; border-radius: 10px; background: var(--color-blue-light); color: var(--color-blue); display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>
                <rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>
                <line x1="6" y1="6" x2="6.01" y2="6"></line>
                <line x1="6" y1="18" x2="6.01" y2="18"></line>
              </svg>
            </div>
            <h4 style="margin-bottom: 0.75rem;">Capacity for maintenance</h4>
            <p style="font-size: 0.95rem;">
              Your organization must have someone on hand who understands the technology requested, with viable plans in place for ongoing adoption after final handover.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
