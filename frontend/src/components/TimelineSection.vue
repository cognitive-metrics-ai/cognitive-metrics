<script setup>
import { ref } from 'vue'

const hoveredRow = ref(null)

const timelineEvents = [
  { date: 'Phase 1 · Rolling', description: 'Academic research proposals submitted & initial alignment sync', status: 'Open Now', active: true },
  { date: 'Phase 2 · Week 1-2', description: 'Experimental design review, ADLC hypothesis framing & variable mapping', status: 'Protocol Scoping' },
  { date: 'Phase 3 · Week 3-6', description: 'Full-stack software testbed development & interactive UI engineering', status: 'Implementation ($0 Cost)' },
  { date: 'Phase 4 · Week 7-8', description: 'ADLC telemetry instrumentation, cognitive friction logging & test suite validation', status: 'Instrumentation' },
  { date: 'Phase 5 · Week 9', description: 'Researcher pilot verification & dry-run trial execution', status: 'Pilot Testing' },
  { date: 'Phase 6 · Week 10-14', description: 'Human-subject trials or automated agent evaluation runs', status: 'Empirical Trials' },
  { date: 'Phase 7 · Week 15-16', description: 'Telemetry dataset consolidation, statistical export & academic co-authorship draft', status: 'Dissemination' }
]
</script>

<template>
  <section id="batch-timeline" class="section section-divider section-light">
    <div class="container-narrow">
      <div class="text-center" style="margin-bottom: 3rem;">
        <span class="section-label">Empirical Research Cycle</span>
        <h2>Academic collaboration timeline</h2>
        <p style="margin-top: 0.5rem;">
          A phased methodology built to align with academic conference deadlines, grant reporting, and IRB review schedules.
        </p>
      </div>

      <div class="timeline-table">
        <div 
          v-for="(event, idx) in timelineEvents" 
          :key="idx" 
          class="timeline-row"
          @mouseenter="hoveredRow = idx"
          @mouseleave="hoveredRow = null"
        >
          <div class="timeline-date">{{ event.date }}</div>
          <div class="timeline-desc">{{ event.description }}</div>
          <div>
            <span class="timeline-tag" :class="{ active: event.active }">
              {{ event.status }}
            </span>
          </div>
        </div>
      </div>

      <div class="text-center" style="margin-top: 2.5rem;">
        <p style="font-size: 0.9rem; color: #64748b; margin-bottom: 1.25rem;">
          Have an upcoming conference submission (ICSE, CHI, FSE, NeurIPS, ACL, AAAI)? Reach out early to reserve engineering capacity.
        </p>
        <a href="#submit-app" class="btn btn-primary">Propose an academic study</a>
      </div>
    </div>
  </section>
</template>
