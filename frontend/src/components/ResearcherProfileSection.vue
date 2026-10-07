<script setup>
import researcherPhoto from '../assets/jeremy-lankford.png'

const socialLinks = [
  {
    name: 'Personal Website',
    url: 'http://jeremylankford.com',
    label: 'jeremylankford.com',
    icon: 'website'
  },
  {
    name: 'GitHub',
    url: 'https://github.com/jwlankford',
    label: 'github.com/jwlankford',
    icon: 'github'
  },
  {
    name: 'LinkedIn',
    url: 'https://www.linkedin.com/in/jwlankford/',
    label: 'linkedin.com/in/jwlankford',
    icon: 'linkedin'
  },
  {
    name: 'X (Twitter)',
    url: 'https://x.com/jwlankford',
    label: '@jwlankford',
    icon: 'twitter'
  },
  {
    name: 'Substack',
    url: 'https://jwlankford.substack.com',
    label: 'jwlankford.substack.com',
    icon: 'substack'
  },
  {
    name: 'Email Direct',
    url: 'mailto:jwlankford@gmail.com',
    label: 'jwlankford@gmail.com',
    icon: 'mail'
  }
]
</script>

<template>
  <section id="lead-researcher" class="section section-divider lead-researcher-section">
    <div class="container">
      <div class="researcher-card">
        <div class="researcher-grid">
          <!-- Profile Badge / Avatar Column -->
          <div class="researcher-avatar-col">
            <div class="researcher-avatar-wrapper">
              <div class="researcher-avatar-ring">
                <img 
                  :src="researcherPhoto" 
                  alt="Jeremy Lankford - Lead Researcher" 
                  class="researcher-avatar-img"
                />
              </div>
              <span class="researcher-badge">
                RESEARCHER
              </span>
            </div>
            
            <a 
              href="http://jeremylankford.com" 
              target="_blank" 
              rel="noopener noreferrer"
              class="btn btn-primary researcher-btn"
            >
              jeremylankford.com ↗
            </a>
          </div>

          <!-- Profile Details Column -->
          <div class="researcher-details-col">
            <div class="researcher-header-tags">
              <span class="section-label lead-title">Initiative Lead & Software Architect</span>
              <span class="phd-badge">
                PhD in IT (AI Focus)
              </span>
            </div>

            <h2 class="researcher-name">Jeremy Lankford</h2>
            
            <p class="researcher-bio">
              Senior Software Architect and doctoral researcher specializing in advanced systems architecture, autonomous agentic systems, and empirical cognitive metrics. 
            </p>

            <!-- Personal Commitment Callout -->
            <div class="researcher-callout">
              <div class="callout-quote">
                &ldquo;I will take on experimental software development for academic research at zero development expenses.&rdquo;
              </div>
              <div class="callout-text">
                I am offering pro-bono software architecture, testbed implementation, and telemetry instrumentation for qualifying academic studies investigating the <strong>Agentic Development Life Cycle (ADLC)</strong>. No consulting fees, no development expenses, not for business or commercial purposes.
              </div>
            </div>

            <!-- Social Links Grid -->
            <div>
              <div class="social-header">
                Connect & Academic Profiles
              </div>
              
              <div class="social-links-grid">
                <a 
                  v-for="social in socialLinks" 
                  :key="social.name"
                  :href="social.url" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  class="social-link-item"
                  :aria-label="social.name"
                  :title="`${social.name}: ${social.label}`"
                >
                  <!-- Website / Globe -->
                  <svg v-if="social.icon === 'website'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="2" y1="12" x2="22" y2="12"></line>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                  </svg>
                  <!-- GitHub -->
                  <svg v-else-if="social.icon === 'github'" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/>
                  </svg>
                  <!-- LinkedIn -->
                  <svg v-else-if="social.icon === 'linkedin'" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
                  </svg>
                  <!-- X (Twitter) -->
                  <svg v-else-if="social.icon === 'twitter'" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                  </svg>
                  <!-- Substack -->
                  <svg v-else-if="social.icon === 'substack'" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M22.539 8.242H1.46V5.406h21.08v2.836zM1.46 10.812V24L12 18.11 22.54 24V10.812H1.46zM22.54 0H1.46v2.836h21.08V0z"/>
                  </svg>
                  <!-- Mail Direct -->
                  <svg v-else-if="social.icon === 'mail'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                    <polyline points="22,6 12,13 2,6"></polyline>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.lead-researcher-section {
  background-color: var(--color-bg-white);
  transition: background-color 0.25s ease;
}

.researcher-card {
  background: linear-gradient(135deg, #0A3D62 0%, #0d466e 100%);
  border-radius: 20px;
  padding: 3.5rem;
  color: #ffffff;
  box-shadow: var(--shadow-xl);
  border: 1px solid rgba(255, 255, 255, 0.12);
  transition: background 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}

:global([data-theme="dark"]) .researcher-card,
:global(.dark-theme) .researcher-card {
  background: linear-gradient(135deg, #0f233a 0%, #153252 100%);
  border-color: rgba(56, 189, 248, 0.25);
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.7), 0 0 25px rgba(56, 189, 248, 0.04);
}

.researcher-grid {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 3rem;
  align-items: center;
}

.researcher-avatar-col {
  text-align: center;
}

.researcher-avatar-wrapper {
  position: relative;
  width: 170px;
  height: 170px;
  margin: 0 auto 1.25rem auto;
}

.researcher-avatar-ring {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #1B6CA8 0%, #4DA8DA 100%);
  padding: 4px;
  box-shadow: 0 10px 30px rgba(27, 108, 168, 0.4);
  overflow: hidden;
  transition: all 0.25s ease;
}

:global([data-theme="dark"]) .researcher-avatar-ring,
:global(.dark-theme) .researcher-avatar-ring {
  background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);
  box-shadow: 0 10px 30px rgba(56, 189, 248, 0.35);
}

.researcher-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  display: block;
}

.researcher-badge {
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  background: #0A3D62;
  color: #4DA8DA;
  border: 1.5px solid #1B6CA8;
  padding: 2px 10px;
  border-radius: 9999px;
  letter-spacing: 0.12em;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
  transition: all 0.25s ease;
}

:global([data-theme="dark"]) .researcher-badge,
:global(.dark-theme) .researcher-badge {
  background: #0d2038;
  color: #38bdf8;
  border-color: #0284c7;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.researcher-btn {
  font-size: 0.85rem;
  padding: 0.6rem 1.25rem;
  width: 100%;
  text-decoration: none;
}

.researcher-header-tags {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 0.75rem;
}

.lead-title {
  margin-bottom: 0;
  color: #4DA8DA;
  transition: color 0.25s ease;
}

:global([data-theme="dark"]) .lead-title,
:global(.dark-theme) .lead-title {
  color: #38bdf8;
}

.phd-badge {
  font-size: 0.75rem;
  font-weight: 700;
  background: rgba(77, 168, 218, 0.2);
  color: #bae6fd;
  padding: 0.2rem 0.6rem;
  border-radius: 9999px;
  transition: all 0.25s ease;
}

:global([data-theme="dark"]) .phd-badge,
:global(.dark-theme) .phd-badge {
  background: rgba(56, 189, 248, 0.15);
  color: #7dd3fc;
  border: 1px solid rgba(56, 189, 248, 0.25);
}

.researcher-name {
  color: #ffffff;
  font-size: 2.25rem;
  margin-bottom: 0.75rem;
  transition: color 0.25s ease;
}

:global([data-theme="dark"]) .researcher-name,
:global(.dark-theme) .researcher-name {
  color: #f8fafc;
}

.researcher-bio {
  color: #cbd5e1;
  font-size: 1.05rem;
  line-height: 1.65;
  margin-bottom: 1.5rem;
  transition: color 0.25s ease;
}

:global([data-theme="dark"]) .researcher-bio,
:global(.dark-theme) .researcher-bio {
  color: #cbd5e1;
}

.researcher-callout {
  background: rgba(255, 255, 255, 0.05);
  border-left: 4px solid #4DA8DA;
  border-radius: 0 10px 10px 0;
  padding: 1.25rem 1.5rem;
  margin-bottom: 2rem;
  transition: all 0.25s ease;
}

:global([data-theme="dark"]) .researcher-callout,
:global(.dark-theme) .researcher-callout {
  background: rgba(56, 189, 248, 0.06);
  border-left-color: #38bdf8;
}

.callout-quote {
  font-weight: 700;
  color: #f8fafc;
  font-size: 1.05rem;
  margin-bottom: 0.4rem;
  transition: color 0.25s ease;
}

:global([data-theme="dark"]) .callout-quote,
:global(.dark-theme) .callout-quote {
  color: #f1f5f9;
}

.callout-text {
  font-size: 0.9rem;
  color: #cbd5e1;
  line-height: 1.55;
  transition: color 0.25s ease;
}

:global([data-theme="dark"]) .callout-text,
:global(.dark-theme) .callout-text {
  color: #94a3b8;
}

.social-header {
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #94a3b8;
  letter-spacing: 0.1em;
  margin-bottom: 0.75rem;
}

.social-links-grid {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  align-items: center;
}

.social-link-item {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  color: #e2e8f0;
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.12);
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.social-link-item:hover {
  background: #1B6CA8;
  color: #ffffff;
  border-color: #4DA8DA;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(27, 108, 168, 0.4);
}

:global([data-theme="dark"]) .social-link-item,
:global(.dark-theme) .social-link-item {
  background: rgba(255, 255, 255, 0.04);
  color: #cbd5e1;
  border-color: rgba(255, 255, 255, 0.08);
}

:global([data-theme="dark"]) .social-link-item:hover,
:global(.dark-theme) .social-link-item:hover {
  background: rgba(56, 189, 248, 0.18);
  color: #38bdf8;
  border-color: #38bdf8;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(56, 189, 248, 0.25);
}

@media (max-width: 991px) {
  .researcher-card {
    padding: 2.25rem 1.75rem;
  }
  .researcher-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>
