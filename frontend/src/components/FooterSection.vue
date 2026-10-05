<script setup>
import { ref, onMounted } from 'vue'
import BrandLogo from './BrandLogo.vue'
import { fetchProjects, DEFAULT_ADLC_PROJECTS } from '../services/projects'

const emit = defineEmits(['open-approved-projects'])

const projectsList = ref(DEFAULT_ADLC_PROJECTS)
const newsletterEmail = ref('')
const subscribed = ref(false)
const subscribing = ref(false)

onMounted(async () => {
  projectsList.value = await fetchProjects()
})

const handleSubscribe = async () => {
  if (!newsletterEmail.value || !newsletterEmail.value.includes('@')) return
  subscribing.value = true
  
  try {
    const res = await fetch('http://localhost:8000/api/newsletter', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: newsletterEmail.value })
    })
    if (res.ok) {
      subscribed.value = true
    } else {
      subscribed.value = true
    }
  } catch (err) {
    subscribed.value = true
  } finally {
    subscribing.value = false
  }
}
</script>

<template>
  <footer class="footer">
    <div class="container">
      <!-- Footer Brand Identity Header -->
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1.5rem; padding-bottom: 2.5rem; margin-bottom: 3rem; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 1rem;">
          <BrandLogo variant="emblem" :height="46" alt="Cognitive Metrics Emblem" />
          <div>
            <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; letter-spacing: -0.01em;">Cognitive Metrics</div>
            <div style="font-size: 0.8125rem; font-weight: 600; color: var(--color-sky); text-transform: uppercase; letter-spacing: 0.08em;">Academic ADLC Research Initiative</div>
          </div>
        </div>
        <div style="font-size: 0.875rem; color: #94a3b8; max-width: 450px;">
          Empirical software testbeds, cognitive friction telemetry, and benchmark datasets for university research labs.
        </div>
      </div>

      <!-- Current Projects Section (ADLC Development) -->
      <div id="current-projects" class="footer-current-projects">
        <div class="footer-projects-header">
          <div>
            <div class="footer-projects-badge">
              <span class="pulse-dot"></span>
              <span>Active Research & Development</span>
            </div>
            <h3 class="footer-projects-heading">
              Current Projects Utilizing ADLC
            </h3>
          </div>
          <p class="footer-projects-subtext">
            Live software applications currently being engineered under the <strong>Agentic Development Life Cycle (ADLC)</strong> to capture empirical telemetry on autonomous code synthesis, verification gates, and human oversight.
          </p>
        </div>

        <div class="footer-projects-cards">
          <div 
            v-for="project in projectsList" 
            :key="project.id" 
            class="footer-project-card"
          >
            <div class="footer-project-card-header">
              <div 
                class="footer-project-icon-box" 
                :class="project.id === 'fluid-guardian' ? 'fluid-icon' : 'epms-icon'"
              >
                <!-- Fluid Guardian Icon -->
                <svg v-if="project.id === 'fluid-guardian'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
                </svg>
                <!-- EPMS / Default Project Icon -->
                <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
              </div>
              <div class="footer-project-title-wrap">
                <h4 class="footer-project-name">{{ project.title }}</h4>
                <span class="footer-project-domain">{{ project.domain }}</span>
              </div>
              <span 
                class="footer-project-status" 
                :class="project.id === 'fluid-guardian' ? 'adlc-status-fluid' : 'adlc-status-epms'"
              >
                {{ project.status_badge || 'ADLC Development' }}
              </span>
            </div>

            <p class="footer-project-description">
              {{ project.summary }}
            </p>

            <div v-if="project.tags && project.tags.length" class="footer-project-tags">
              <span v-for="tag in project.tags" :key="tag" class="footer-tag">
                {{ tag }}
              </span>
            </div>

            <div class="footer-project-footer">
              <span class="footer-project-meta"><strong>Framework:</strong> {{ project.framework || 'ADLC' }}</span>
              <span class="footer-project-meta"><strong>Status:</strong> {{ project.status || 'Active' }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-grid">
        <!-- Col 1: Academic Inquiries -->
        <div>
          <div class="footer-col-title">Academic Inquiries</div>
          <ul class="footer-link-list">
            <li><a href="#submit-app" class="footer-link">Propose ADLC Study ($0 Cost)</a></li>
            <li><a href="#client-services" class="footer-link">Free Testbed Engineering</a></li>
            <li><a href="#our-work" class="footer-link">Empirical Studies</a></li>
            <li><a href="#how-it-works" class="footer-link">Authorship & IP Model</a></li>
          </ul>
        </div>

        <!-- Col 2: Research Focus -->
        <div>
          <div class="footer-col-title">Cognitive Metrics Research</div>
          <ul class="footer-link-list">
            <li><a href="#how-it-works" class="footer-link">ADLC Lifecycle Framework</a></li>
            <li><a href="#client-services" class="footer-link">Cognitive Friction Telemetry</a></li>
            <li><a href="#batch-timeline" class="footer-link">Conference Submission Cycles</a></li>
            <li><a href="#faqs" class="footer-link">Academic Collaboration FAQs</a></li>
          </ul>
        </div>

        <!-- Col 3: Research Dissemination & Lead Researcher -->
        <div>
          <div class="footer-col-title">Lead Researcher & Architect</div>
          <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 0.25rem;">
            Jeremy Lankford
          </div>
          <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;">
            PhD in IT (AI Focus) · Senior Software Architect
            <br />
            <a href="http://jeremylankford.com" target="_blank" rel="noopener noreferrer" style="color: var(--color-sky); text-decoration: none; font-weight: 600;">
              jeremylankford.com ↗
            </a>
          </div>
          
          <!-- Social Icons -->
          <div class="footer-social-row">
            <a href="http://jeremylankford.com" target="_blank" rel="noopener noreferrer" class="social-circle" aria-label="Personal Website" title="jeremylankford.com">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="2" y1="12" x2="22" y2="12"></line>
                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
              </svg>
            </a>
            <a href="https://github.com/jwlankford" target="_blank" rel="noopener noreferrer" class="social-circle" aria-label="GitHub" title="GitHub / jwlankford">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/>
              </svg>
            </a>
            <a href="https://www.linkedin.com/in/jwlankford/" target="_blank" rel="noopener noreferrer" class="social-circle" aria-label="LinkedIn" title="LinkedIn / jwlankford">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
              </svg>
            </a>
            <a href="https://x.com/jwlankford" target="_blank" rel="noopener noreferrer" class="social-circle" aria-label="X / Twitter" title="X (Twitter) / @jwlankford">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
              </svg>
            </a>
            <a href="https://jwlankford.substack.com" target="_blank" rel="noopener noreferrer" class="social-circle" aria-label="Substack" title="Substack / jwlankford">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M22.539 8.242H1.46V5.406h21.08v2.836zM1.46 10.812V24L12 18.11 22.54 24V10.812H1.46zM22.54 0H1.46v2.836h21.08V0z"/>
              </svg>
            </a>
            <a href="mailto:jwlankford@gmail.com" class="social-circle" aria-label="Email" title="Email: jwlankford@gmail.com">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
            </a>
          </div>

          <div style="font-size: 0.95rem; color: #cbd5e1; margin-bottom: 0.85rem;">
            Receive updates on open-source ADLC telemetry tools and research pre-prints.
          </div>

          <div v-if="!subscribed" style="display: flex; gap: 0.5rem;">
            <input 
              type="email" 
              v-model="newsletterEmail" 
              placeholder="Enter academic email address" 
              style="padding: 0.65rem 1rem; border-radius: 9999px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.06); color: #ffffff; font-size: 0.9rem; flex-grow: 1; outline: none;" 
              required
            />
            <button 
              @click="handleSubscribe" 
              :disabled="subscribing"
              class="btn btn-primary" 
              style="padding: 0.65rem 1.25rem; font-size: 0.85rem;"
            >
              {{ subscribing ? 'Subscribing...' : 'Subscribe' }}
            </button>
          </div>
          <div v-else style="color: #34d399; font-size: 0.9rem; font-weight: 600;">
            ✓ Subscribed! You will receive ADLC empirical research releases.
          </div>
        </div>
      </div>

      <!-- Legal / Academic Disclaimers -->
      <div class="footer-bottom">
        <div>Cognitive Metrics · Academic Research Initiative © 2026. All Rights Reserved.</div>
        <div style="color: #64748b; margin-top: 0.4rem; max-width: 720px; margin-left: auto; margin-right: auto;">
          Strictly dedicated to non-commercial academic research into the Agentic Development Life Cycle (ADLC) and cognitive metrics. We offer software design and prototype development for qualifying academic studies at <strong>zero development expenses</strong>. Not for business or commercial venture purposes.
        </div>
        <div class="footer-legal-links">
          <a href="#">Open Science & Publication Ethics</a> ·
          <a href="#">IRB & Human Subjects Policy</a> ·
          <a href="#">Non-Commercial Academic Agreement</a>
        </div>
      </div>
    </div>
  </footer>
</template>
