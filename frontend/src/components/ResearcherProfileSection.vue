<script setup>
import researcherPhoto from '../assets/jeremy-lankford.png'

const socialLinks = [
  {
    name: 'Personal Website',
    url: 'http://jeremylankford.com',
    label: 'jeremylankford.com',
    type: 'primary'
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
                >
                  <span>{{ social.name }}:</span>
                  <span class="social-label">{{ social.label }}</span>
                  <span class="social-arrow">↗</span>
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
}

.social-link-item {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.08);
  color: #e2e8f0;
  padding: 0.5rem 0.9rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s ease;
}

.social-link-item:hover {
  background: #1B6CA8;
  color: #ffffff;
  border-color: #4DA8DA;
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
}

.social-label {
  opacity: 0.85;
  font-weight: 400;
}

.social-arrow {
  font-size: 0.75rem;
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
