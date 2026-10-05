<script setup>
import { ref } from 'vue'
import BrandLogo from './BrandLogo.vue'

const emit = defineEmits(['close', 'open-proposal'])

const downloaded = ref(false)

const projects = [
  {
    id: 'PROP-ADLC-9042',
    title: 'Human-in-the-Loop ADLC Code Synthesis Testbed',
    venue: 'Target: ICSE / CHI 2027',
    status: 'Approved · Implementation Active',
    statusClass: 'status-active',
    traces: '14,290 trace events',
    leadArchitect: 'Jeremy Lankford',
    summary: 'Full-stack experimental IDE testbed measuring developer cognitive load, latency, and autonomous agent handoff dynamics.'
  },
  {
    id: 'PROP-ADLC-8411',
    title: 'Clinical Diagnostic Agent Verification Protocol',
    venue: 'Target: JAMIA / AMIA 2027',
    status: 'Protocol Scoped · Pending Pilot',
    statusClass: 'status-scoped',
    traces: '3,100 trace events',
    leadArchitect: 'Jeremy Lankford',
    summary: 'Multi-agent orchestration testbed evaluating physician trust calibration and double-blind verification safety rubrics.'
  }
]

const handleDownloadDataset = () => {
  downloaded.value = true
  setTimeout(() => {
    downloaded.value = false
  }, 3000)
}

const handleGoToProposal = () => {
  emit('open-proposal')
  emit('close')
}
</script>

<template>
  <div class="modal-backdrop" @click.self="emit('close')" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(10, 20, 35, 0.8); backdrop-filter: blur(6px); z-index: 999; display: flex; align-items: center; justify-content: center; padding: 1.5rem;">
    <div class="modal-content" style="background: var(--color-bg-white); border: 1px solid var(--color-border); border-radius: 18px; max-width: 680px; width: 100%; max-height: 90vh; overflow-y: auto; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4); padding: 2.5rem; position: relative;">
      <!-- Close Button -->
      <button @click="emit('close')" style="position: absolute; top: 1.25rem; right: 1.25rem; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--color-text-muted);">
        &times;
      </button>

      <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
        <BrandLogo variant="icon" :height="48" alt="Cognitive Metrics Logo" style="border-radius: 12px; box-shadow: var(--shadow-md);" />
        <div>
          <span class="section-label coral">Researcher Dashboard</span>
          <h2 style="font-size: 1.65rem; margin-top: 0.15rem; color: var(--color-navy);">Approved Research Projects</h2>
          <p style="font-size: 0.9rem; color: var(--color-text-muted); margin-top: 0.2rem;">
            Track your pro-bono experimental software testbeds, telemetry data streams, and ADLC milestones.
          </p>
        </div>
      </div>

      <!-- Project Cards List -->
      <div style="display: flex; flex-direction: column; gap: 1.25rem; margin-bottom: 2rem;">
        <div 
          v-for="p in projects" 
          :key="p.id"
          style="background: var(--color-bg-light); border: 1px solid var(--color-border); border-radius: 12px; padding: 1.5rem; transition: border-color 0.2s ease;"
        >
          <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; margin-bottom: 0.5rem; flex-wrap: wrap;">
            <div>
              <span style="font-family: monospace; font-size: 0.75rem; background: var(--color-border); color: var(--color-text-main); padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 700;">
                {{ p.id }}
              </span>
              <h3 style="font-size: 1.2rem; margin-top: 0.4rem; color: var(--color-navy);">{{ p.title }}</h3>
            </div>
            
            <span style="font-size: 0.75rem; font-weight: 700; color: #059669; background: #d1fae5; padding: 0.25rem 0.65rem; border-radius: 9999px;">
              {{ p.status }}
            </span>
          </div>

          <p style="font-size: 0.9rem; color: #64748b; margin-bottom: 1rem;">
            {{ p.summary }}
          </p>

          <div style="display: flex; gap: 1.5rem; font-size: 0.8rem; color: #475569; margin-bottom: 1rem; flex-wrap: wrap;">
            <div><strong>Target:</strong> {{ p.venue }}</div>
            <div><strong>Lead Architect:</strong> {{ p.leadArchitect }}</div>
            <div><strong>Recorded Data:</strong> {{ p.traces }}</div>
          </div>

          <div style="display: flex; gap: 0.75rem; flex-wrap: wrap; border-top: 1px solid #e2e8f0; padding-top: 1rem;">
            <button 
              @click="handleDownloadDataset" 
              class="btn btn-secondary" 
              style="font-size: 0.8rem; padding: 0.45rem 0.9rem;"
            >
              {{ downloaded ? '✓ Exporting JSONL...' : '📥 Export Anonymized Telemetry' }}
            </button>
            <a 
              href="#lead-researcher" 
              @click="emit('close')" 
              class="btn btn-secondary" 
              style="font-size: 0.8rem; padding: 0.45rem 0.9rem; text-decoration: none;"
            >
              Contact Lead Architect
            </a>
          </div>
        </div>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #e2e8f0; padding-top: 1.5rem; flex-wrap: wrap; gap: 1rem;">
        <span style="font-size: 0.85rem; color: #64748b;">
          Need another experimental testbed or stimulus interface?
        </span>
        <button @click="handleGoToProposal" class="btn btn-primary" style="font-size: 0.875rem;">
          Submit New Proposal ($0 Cost)
        </button>
      </div>
    </div>
  </div>
</template>
