<script setup>
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
  <section id="lead-researcher" class="section section-divider" style="background: #ffffff;">
    <div class="container">
      <div style="background: linear-gradient(135deg, #0A3D62 0%, #0d466e 100%); border-radius: 20px; padding: 3.5rem; color: #ffffff; box-shadow: var(--shadow-xl); border: 1px solid rgba(255,255,255,0.12);">
        <div style="display: grid; grid-template-columns: 240px 1fr; gap: 3rem; align-items: center;">
          <!-- Profile Badge / Avatar Column -->
          <div style="text-align: center;">
            <div style="width: 170px; height: 170px; border-radius: 50%; background: linear-gradient(135deg, #1B6CA8 0%, #4DA8DA 100%); padding: 5px; margin: 0 auto 1.25rem auto; box-shadow: 0 10px 30px rgba(27, 108, 168, 0.4);">
              <div style="width: 100%; height: 100%; border-radius: 50%; background: #0A3D62; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <span style="font-size: 3rem; font-weight: 800; font-family: var(--font-heading); color: #ffffff; letter-spacing: -0.05em;">JL</span>
                <span style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #4DA8DA; letter-spacing: 0.1em; margin-top: -4px;">RESEARCHER</span>
              </div>
            </div>
            
            <a 
              href="http://jeremylankford.com" 
              target="_blank" 
              rel="noopener noreferrer"
              class="btn btn-primary" 
              style="font-size: 0.85rem; padding: 0.6rem 1.25rem; width: 100%; text-decoration: none;"
            >
              jeremylankford.com ↗
            </a>
          </div>

          <!-- Profile Details Column -->
          <div>
            <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 0.75rem;">
              <span class="section-label" style="margin-bottom: 0; color: #4DA8DA;">Initiative Lead & Software Architect</span>
              <span style="font-size: 0.75rem; font-weight: 700; background: rgba(77, 168, 218, 0.2); color: #bae6fd; padding: 0.2rem 0.6rem; border-radius: 9999px;">
                PhD in IT (AI Focus)
              </span>
            </div>

            <h2 style="color: #ffffff; font-size: 2.25rem; margin-bottom: 0.75rem;">Jeremy Lankford</h2>
            
            <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.65; margin-bottom: 1.5rem;">
              Senior Software Architect and doctoral researcher specializing in advanced systems architecture, autonomous agentic systems, and empirical cognitive metrics. 
            </p>

            <!-- Personal Commitment Callout -->
            <div style="background: rgba(255, 255, 255, 0.05); border-left: 4px solid #4DA8DA; border-radius: 0 10px 10px 0; padding: 1.25rem 1.5rem; margin-bottom: 2rem;">
              <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem; margin-bottom: 0.4rem;">
                &ldquo;I will take on experimental software development for academic research at zero development expenses.&rdquo;
              </div>
              <div style="font-size: 0.9rem; color: #94a3b8; line-height: 1.55;">
                I am offering pro-bono software architecture, testbed implementation, and telemetry instrumentation for qualifying academic studies investigating the <strong>Agentic Development Life Cycle (ADLC)</strong>. No consulting fees, no development expenses, not for business or commercial purposes.
              </div>
            </div>

            <!-- Social Links Grid -->
            <div>
              <div style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.1em; margin-bottom: 0.75rem;">
                Connect & Academic Profiles
              </div>
              
              <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
                <a 
                  v-for="social in socialLinks" 
                  :key="social.name"
                  :href="social.url" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  style="display: inline-flex; align-items: center; gap: 0.5rem; background: rgba(255, 255, 255, 0.08); color: #e2e8f0; padding: 0.5rem 0.9rem; border-radius: 8px; font-size: 0.85rem; font-weight: 600; text-decoration: none; border: 1px solid rgba(255, 255, 255, 0.1); transition: all 0.2s ease;"
                  @mouseenter="$event.currentTarget.style.background = '#1B6CA8'; $event.currentTarget.style.color = '#ffffff'; $event.currentTarget.style.borderColor = '#4DA8DA'"
                  @mouseleave="$event.currentTarget.style.background = 'rgba(255, 255, 255, 0.08)'; $event.currentTarget.style.color = '#e2e8f0'; $event.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'"
                >
                  <span>{{ social.name }}:</span>
                  <span style="opacity: 0.85; font-weight: 400;">{{ social.label }}</span>
                  <span style="font-size: 0.75rem;">↗</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
