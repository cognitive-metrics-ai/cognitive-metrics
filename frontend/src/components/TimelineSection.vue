<script setup>
import { ref } from 'vue'

const hoveredRow = ref(null)

const timelineEvents = [
  { date: 'Sep 18, 2026', description: 'Nonprofit project proposals due', status: 'Priority Deadline', active: true },
  { date: 'Oct 2', description: 'Accepted nonprofits notified and project spots confirmed', status: 'Selection' },
  { date: 'Oct 16', description: 'Project team assignments finalized (Product Managers, Engineers & Mentors)', status: 'Staffing' },
  { date: 'Oct 25', description: 'Batch begins with an Orientation & Training Week for all participants', status: 'Kickoff' },
  { date: 'Nov 1 - 28', description: 'Project scoping phase: Product Requirements Document (PRD) creation', status: 'Scoping' },
  { date: 'Nov 29', description: 'Project development, benchmark engineering, and design sprints begin', status: 'Development' },
  { date: 'Jan 31, 2027', description: 'Project documentation, testing, and handover phase begins', status: 'Handover' },
  { date: 'Feb 18', description: 'Demo Day & Live Impact Showcase', status: 'Milestone' },
  { date: 'Feb 20', description: '16-week cohort concludes', status: 'Completion' },
  { date: 'Feb 21 - 27', description: 'Nonprofit feedback submission and post-launch review', status: 'Evaluation' }
]
</script>

<template>
  <section id="batch-timeline" class="section section-divider section-light">
    <div class="container-narrow">
      <div class="text-center" style="margin-bottom: 3rem;">
        <span class="section-label">Upcoming Cohort Schedule</span>
        <h2>Winter 2027 batch timeline</h2>
        <p style="margin-top: 0.5rem;">
          Our 16-week structured lifecycle ensures timely alignment, high quality, and seamless handover.
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
          Want to secure your spot for the next cohort? Applications are reviewed on a rolling basis.
        </p>
        <a href="#submit-app" class="btn btn-primary">Apply for Winter 2027 batch</a>
      </div>
    </div>
  </section>
</template>
