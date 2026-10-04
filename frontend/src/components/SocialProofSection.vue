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
      <!-- Academic Testimonial Quote Block -->
      <div class="quote-box" style="margin-bottom: 5rem;">
        <div class="quote-avatar-wrapper">
          <div style="width: 130px; height: 130px; border-radius: 50%; background: linear-gradient(135deg, #1e3a8a, #0e1b2f); display: flex; align-items: center; justify-content: center; margin: 0 auto; color: white; font-weight: 800; font-size: 1.6rem; box-shadow: 0 10px 25px rgba(30, 58, 138, 0.25);">
            LAB
          </div>
        </div>
        <div class="quote-content">
          <div class="quote-text">
            &ldquo;Collaborating with Cognitive Metrics gave our lab a production-grade experimental software testbed without having to deplete our research grant on outside engineering contractors. Their pro-bono development support made collecting high-fidelity ADLC telemetry and running human-subject trials seamlessly achievable.&rdquo;
          </div>
          <div class="quote-author">Dr. Marcus Vance, Ph.D.</div>
          <div class="quote-title">Principal Investigator, Human-Computer Interaction & Systems Group</div>
        </div>
      </div>

      <!-- University Institutions -->
      <div class="text-center" style="margin-bottom: 3.5rem;">
        <span class="section-label">Academic & Research Alignment</span>
        <h3>Built for university researchers, labs, and doctoral candidates</h3>
        <p style="max-width: 640px; margin: 0.5rem auto 0 auto;">
          We support research initiatives across premier university departments in Computer Science, Cognitive Science, and Information Systems.
        </p>

        <div class="logo-grid">
          <div v-for="school in universities" :key="school" class="logo-badge-item">
            {{ school }}
          </div>
        </div>
      </div>

      <!-- Criteria for Pro-Bono Research Selection -->
      <div style="margin-top: 5rem; padding-top: 3.5rem; border-top: 1px solid var(--color-border);">
        <div class="text-center" style="margin-bottom: 3rem;">
          <span class="section-label coral">Project Scope Requirements</span>
          <h2>Criteria for taking on research projects at zero expense</h2>
          <p style="max-width: 680px; margin: 0.5rem auto 0 auto;">
            Because we provide full design and software development at <strong>zero development cost</strong>, we select projects based on their scientific contribution to ADLC research.
          </p>
        </div>

        <div class="grid-3-col">
          <div style="background: #ffffff; border: 1px solid var(--color-border); border-radius: 12px; padding: 2rem;">
            <div style="width: 50px; height: 50px; border-radius: 10px; background: var(--color-blue-light); color: var(--color-blue); display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
              </svg>
            </div>
            <h4 style="margin-bottom: 0.75rem;">Academic & Non-Commercial</h4>
            <p style="font-size: 0.95rem;">
              Projects must be explicitly for academic research, PhD dissertations, or non-commercial scientific inquiry. We do not take on business ventures, commercial SaaS, or startup consulting.
            </p>
          </div>

          <div style="background: #ffffff; border: 1px solid var(--color-border); border-radius: 12px; padding: 2rem;">
            <div style="width: 50px; height: 50px; border-radius: 10px; background: var(--color-primary-light); color: var(--color-primary); display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <h4 style="margin-bottom: 0.75rem;">ADLC & Cognitive Focus</h4>
            <p style="font-size: 0.95rem;">
              The study must examine questions relevant to the <strong>Agentic Development Life Cycle (ADLC)</strong>, human-agent delegation, cognitive workload, or benchmark metrics in autonomous systems.
            </p>
          </div>

          <div style="background: #ffffff; border: 1px solid var(--color-border); border-radius: 12px; padding: 2rem;">
            <div style="width: 50px; height: 50px; border-radius: 10px; background: var(--color-blue-light); color: var(--color-blue); display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="18" cy="5" r="3"></circle>
                <circle cx="6" cy="12" r="3"></circle>
                <circle cx="18" cy="19" r="3"></circle>
                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
              </svg>
            </div>
            <h4 style="margin-bottom: 0.75rem;">Open Science & Dissemination</h4>
            <p style="font-size: 0.95rem;">
              The research team agrees to collaborative publication of empirical findings and anonymized telemetry datasets to advance peer-reviewed scientific understanding.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
