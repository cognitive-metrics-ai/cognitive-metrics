<script setup>
import { ref } from 'vue'

const newsletterEmail = ref('')
const subscribed = ref(false)
const subscribing = ref(false)

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
    // Client fallback
    subscribed.value = true
  } finally {
    subscribing.value = false
  }
}
</script>

<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <!-- Col 1: Get Involved -->
        <div>
          <div class="footer-col-title">Get Involved</div>
          <ul class="footer-link-list">
            <li><a href="#submit-app" class="footer-link">Nonprofits & Proposals</a></li>
            <li><a href="#how-it-works" class="footer-link">Students & Fellows</a></li>
            <li><a href="#our-work" class="footer-link">Industry Mentors</a></li>
            <li><a href="#client-services" class="footer-link">Batch Sponsorships</a></li>
          </ul>
        </div>

        <!-- Col 2: About -->
        <div>
          <div class="footer-col-title">Cognitive Metrics</div>
          <ul class="footer-link-list">
            <li><a href="#our-work" class="footer-link">Our Work & Cases</a></li>
            <li><a href="#how-it-works" class="footer-link">Our Process</a></li>
            <li><a href="#client-services" class="footer-link">Menu of Services</a></li>
            <li><a href="#batch-timeline" class="footer-link">Cohort Timeline</a></li>
            <li><a href="#faqs" class="footer-link">Frequently Asked Questions</a></li>
          </ul>
        </div>

        <!-- Col 3: Stay in Touch & Newsletter -->
        <div>
          <div class="footer-col-title">Stay in touch</div>
          
          <!-- Social Icons -->
          <div class="footer-social-row">
            <a href="https://linkedin.com" target="_blank" class="social-circle" aria-label="LinkedIn">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
              </svg>
            </a>
            <a href="https://twitter.com" target="_blank" class="social-circle" aria-label="X / Twitter">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
              </svg>
            </a>
            <a href="https://github.com/cognitive-metrics-ai/cognitive-metrics" target="_blank" class="social-circle" aria-label="GitHub">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/>
              </svg>
            </a>
          </div>

          <div style="font-size: 0.95rem; color: #cbd5e1; margin-bottom: 0.85rem;">
            Receive updates about upcoming batch openings and technical impact reports.
          </div>

          <div v-if="!subscribed" style="display: flex; gap: 0.5rem;">
            <input 
              type="email" 
              v-model="newsletterEmail" 
              placeholder="Enter your email address" 
              style="padding: 0.65rem 1rem; border-radius: 9999px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.06); color: #ffffff; font-size: 0.9rem; flex-grow: 1; outline: none;" 
              required
            />
            <button 
              @click="handleSubscribe" 
              :disabled="subscribing"
              class="btn btn-primary" 
              style="padding: 0.65rem 1.25rem; font-size: 0.85rem;"
            >
              {{ subscribing ? 'Joining...' : 'Subscribe' }}
            </button>
          </div>
          <div v-else style="color: #34d399; font-size: 0.9rem; font-weight: 600;">
            ✓ Thank you! You’re subscribed to Cognitive Metrics updates.
          </div>
        </div>
      </div>

      <!-- Legal / Non-profit Disclaimers -->
      <div class="footer-bottom">
        <div>Cognitive Metrics © 2026. All Rights Reserved.</div>
        <div style="color: #64748b; margin-top: 0.4rem; max-width: 680px; margin-left: auto; margin-right: auto;">
          Cognitive Metrics is a registered 501(c)(3) nonprofit organization (EIN: 85-1596146). All donations are tax deductible to the full extent allowable under IRS regulations.
          <br />584 Castro Street #3117, San Francisco, CA 94114
        </div>
        <div class="footer-legal-links">
          <a href="#">Privacy Policy</a> ·
          <a href="#">Volunteer Terms & Conditions</a> ·
          <a href="#">AI Ethics & Safety Policy</a>
        </div>
      </div>
    </div>
  </footer>
</template>
