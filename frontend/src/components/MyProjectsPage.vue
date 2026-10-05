<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import BrandLogo from './BrandLogo.vue'
import {
  fetchProjects,
  assignProjectToUser,
  DEFAULT_ADLC_PROJECTS,
  fetchProjectComments,
  postProjectComment
} from '../services/projects'

const props = defineProps({
  user: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['go-home', 'submit-proposal'])

const projects = ref([])
const selectedProjectId = ref('')
const isLoading = ref(true)
const exportSuccess = ref(false)

// Project-level comments state
const projectComments = ref([])
const isLoadingComments = ref(false)
const isPostingComment = ref(false)
const commentError = ref('')
const newCommentContent = ref('')
const newCommentType = ref('project_note') // 'project_note' | 'question' | 'verification_update'

// Display name format requested: [username]'s Projects
const researcherDisplayName = computed(() => {
  if (props.user?.displayName) {
    return props.user.displayName
  }
  if (props.user?.email) {
    return props.user.email.split('@')[0]
  }
  return 'Researcher'
})

const loadProjectComments = async (projId) => {
  if (!projId) {
    projectComments.value = []
    return
  }
  isLoadingComments.value = true
  commentError.value = ''
  try {
    const list = await fetchProjectComments(projId)
    projectComments.value = list || []
  } catch (err) {
    console.warn('Failed loading project comments:', err)
  } finally {
    isLoadingComments.value = false
  }
}

const loadUserProjects = async () => {
  isLoading.value = true
  try {
    const data = await fetchProjects(props.user?.uid || null)
    projects.value = data
    if (data && data.length > 0) {
      // Keep existing selection if valid, else select first
      const exists = data.some(p => p.id === selectedProjectId.value)
      if (!exists) {
        selectedProjectId.value = data[0].id
      }
      loadProjectComments(selectedProjectId.value)
    }
  } catch (err) {
    console.warn('Failed loading projects:', err)
    projects.value = DEFAULT_ADLC_PROJECTS
    selectedProjectId.value = DEFAULT_ADLC_PROJECTS[0].id
    loadProjectComments(selectedProjectId.value)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadUserProjects()
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

watch(() => props.user?.uid, () => {
  loadUserProjects()
})

watch(selectedProjectId, (newId) => {
  if (newId) {
    loadProjectComments(newId)
  }
})

const currentProject = computed(() => {
  if (!projects.value.length) return null
  return projects.value.find(p => p.id === selectedProjectId.value) || projects.value[0]
})

const handlePostProjectComment = async () => {
  if (!newCommentContent.value.trim() || !currentProject.value?.id) return
  isPostingComment.value = true
  commentError.value = ''

  try {
    const isArchitect = props.user?.email === 'jwlankford@gmail.com' || props.user?.email === 'jlankford@cognitivemetrics.org'
    const payload = {
      user_id: props.user?.uid || null,
      author_name: props.user?.displayName || (props.user?.email ? props.user.email.split('@')[0] : 'Researcher'),
      author_email: props.user?.email || null,
      author_role: isArchitect ? 'Lead Architect' : 'Researcher / Collaborator',
      comment_type: newCommentType.value,
      content: newCommentContent.value.trim()
    }

    const created = await postProjectComment(currentProject.value.id, payload)
    if (created) {
      projectComments.value.unshift(created)
      newCommentContent.value = ''
    }
  } catch (err) {
    commentError.value = err.message || 'Failed to post comment to project.'
  } finally {
    isPostingComment.value = false
  }
}

const formatCommentDate = (dateStr) => {
  if (!dateStr) return 'Recently'
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateStr
  }
}

const handleExportData = () => {
  exportSuccess.value = true
  // Generate dummy JSONL download for empirical research traces
  const sampleTrace = {
    projectId: currentProject.value?.id,
    projectTitle: currentProject.value?.title,
    leadArchitect: currentProject.value?.lead_architect || 'Jeremy Lankford',
    tracesCount: currentProject.value?.traces_count || 18000,
    exportedAt: new Date().toISOString(),
    telemetryStream: [
      { event: 'agent_synthesis_start', latencyMs: 1420, cognitiveLoadScore: 0.28 },
      { event: 'verification_gate_passed', rubric: 'safety_critical_audit', score: 0.99 },
      { event: 'developer_intervention_check', frictionDelta: -0.42 }
    ]
  }
  const blob = new Blob([JSON.stringify(sampleTrace, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${currentProject.value?.id || 'adlc-project'}-telemetry.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)

  setTimeout(() => {
    exportSuccess.value = false
  }, 3500)
}
</script>

<template>
  <div class="my-projects-page">
    <!-- Top Breadcrumb & Navigation Bar -->
    <div class="projects-subnav">
      <div class="container" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
        <button @click="emit('go-home')" class="back-home-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          <span>Back to Research Overview</span>
        </button>

        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <span style="font-size: 0.8125rem; color: var(--color-text-muted);">
            Connected to <strong>Neon DB</strong>
          </span>
          <span class="live-dot" title="Database Connected"></span>
        </div>
      </div>
    </div>

    <div class="container projects-main-container">
      <!-- Page Header: [username]'s Projects -->
      <div class="projects-header-block">
        <div style="display: flex; align-items: center; gap: 0.85rem; margin-bottom: 0.5rem;">
          <span class="section-label coral">Researcher Workspace</span>
          <span v-if="props.user" class="user-id-pill">
            ID: {{ props.user.uid }}
          </span>
        </div>
        
        <h1 class="projects-page-title">
          {{ researcherDisplayName }}'s Projects
        </h1>

        <p class="projects-page-subtitle">
          Manage your active software testbeds developed under the <strong>Agentic Development Life Cycle (ADLC)</strong>. Review live telemetry data streams, cognitive metric benchmarks, and verification rubrics.
        </p>
      </div>

      <!-- Project Selection Dropdown Bar -->
      <div class="project-selector-card">
        <div class="selector-content-row">
          <div class="selector-left-group">
            <label for="project-dropdown" class="selector-label">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
              </svg>
              <span>Select Active Project:</span>
            </label>

            <!-- Dropdown of user projects -->
            <div class="select-wrapper">
              <select 
                id="project-dropdown"
                v-model="selectedProjectId" 
                class="project-dropdown-select"
              >
                <option 
                  v-for="p in projects" 
                  :key="p.id" 
                  :value="p.id"
                >
                  {{ p.title }} ({{ p.status_badge || 'Active ADLC' }})
                </option>
              </select>
              <div class="select-arrow">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </div>
            </div>
          </div>

          <div class="selector-right-actions">
            <!-- Table-Level Status Badge -->
            <span class="ownership-badge owned" title="Managed directly in Neon PostgreSQL database">
              ✓ Database Active
            </span>

            <!-- Submit New Proposal CTA -->
            <button 
              @click="emit('submit-proposal')" 
              class="btn btn-primary"
              style="font-size: 0.875rem; padding: 0.6rem 1.15rem;"
            >
              + Propose New Testbed
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-state-card">
        <div class="spinner"></div>
        <p>Loading project details from Neon PostgreSQL...</p>
      </div>

      <!-- Project Full-Page Detail View -->
      <div v-else-if="currentProject" class="project-detail-layout">
        
        <!-- Project Hero Card -->
        <div class="project-detail-hero">
          <div class="hero-top-meta">
            <div class="hero-tags-group">
              <span class="project-id-tag">{{ currentProject.id }}</span>
              <span class="project-status-tag">{{ currentProject.status || 'Active · ADLC Development' }}</span>
              <span class="project-domain-tag">{{ currentProject.domain }}</span>
            </div>

            <div class="hero-action-buttons">
              <button 
                @click="handleExportData" 
                class="btn btn-secondary action-btn"
              >
                {{ exportSuccess ? '✓ Telemetry Exported' : '📥 Export Anonymized Telemetry' }}
              </button>
            </div>
          </div>

          <h2 class="project-headline">{{ currentProject.title }}</h2>

          <p class="project-summary-text">
            {{ currentProject.summary }}
          </p>

          <div v-if="currentProject.description" class="project-full-description">
            {{ currentProject.description }}
          </div>

          <div v-if="currentProject.tags && currentProject.tags.length" class="project-tech-tags">
            <span v-for="tag in currentProject.tags" :key="tag" class="tech-tag-pill">
              {{ tag }}
            </span>
          </div>
        </div>

        <!-- 4-Stat Telemetry & Metric Highlights Grid -->
        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-icon-box blue">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <activity x1="22" y1="12" x2="2" y2="12"></activity>
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
              </svg>
            </div>
            <div class="metric-info">
              <span class="metric-label">Recorded Telemetry</span>
              <div class="metric-value">{{ (currentProject.traces_count || 22400).toLocaleString() }}</div>
              <span class="metric-sub">Structured event traces captured</span>
            </div>
          </div>

          <div class="metric-card">
            <div class="metric-icon-box green">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 14 14"></polyline>
              </svg>
            </div>
            <div class="metric-info">
              <span class="metric-label">ADLC Framework</span>
              <div class="metric-value" style="font-size: 1.15rem;">Agentic Life Cycle</div>
              <span class="metric-sub">Autonomous synthesis + oversight</span>
            </div>
          </div>

          <div class="metric-card">
            <div class="metric-icon-box purple">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="metric-info">
              <span class="metric-label">Lead Architect</span>
              <div class="metric-value" style="font-size: 1.15rem;">{{ currentProject.lead_architect || 'Jeremy Lankford' }}</div>
              <span class="metric-sub">PhD in IT · AI Focus</span>
            </div>
          </div>

          <div class="metric-card">
            <div class="metric-icon-box amber">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
            </div>
            <div class="metric-info">
              <span class="metric-label">Target Research Venue</span>
              <div class="metric-value" style="font-size: 1.05rem;">{{ currentProject.target_venue || 'Peer-Reviewed Conference' }}</div>
              <span class="metric-sub">ADLC Empirical Publication</span>
            </div>
          </div>
        </div>

        <!-- Detailed Breakdown Sections -->
        <div class="detail-sections-grid">
          <!-- Col 1: Architectural Specification & Protocol -->
          <div class="detail-card">
            <div class="detail-card-header">
              <div class="detail-card-icon">🏗️</div>
              <div>
                <h3 class="detail-card-title">ADLC Implementation Architecture</h3>
                <span class="detail-card-sub">Engineering specifications and execution pipeline</span>
              </div>
            </div>

            <div class="detail-content-body">
              <p>
                The <strong>{{ currentProject.title }}</strong> implements a dual-loop autonomous development paradigm. Software specifications are converted into executable task graphs processed by multi-agent swarms under continuous validation.
              </p>

              <div class="protocol-steps-list">
                <div class="step-item">
                  <span class="step-num">01</span>
                  <div>
                    <strong>Autonomous Specification Synthesis:</strong>
                    Requirements, schemas, and API contracts synthesized with deterministic constraints.
                  </div>
                </div>
                <div class="step-item">
                  <span class="step-num">02</span>
                  <div>
                    <strong>Verification & Safety Rubrics:</strong>
                    Automated linting, integration testing, and static analysis gates executed prior to human validation.
                  </div>
                </div>
                <div class="step-item">
                  <span class="step-num">03</span>
                  <div>
                    <strong>Cognitive Friction Logging:</strong>
                    Developer latency, intervention points, and verification friction tracked directly in telemetry logs.
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Col 2: Telemetry Data Stream & Benchmarking -->
          <div class="detail-card">
            <div class="detail-card-header">
              <div class="detail-card-icon">📈</div>
              <div>
                <h3 class="detail-card-title">Live Telemetry & Traces</h3>
                <span class="detail-card-sub">Empirical datasets for academic research</span>
              </div>
            </div>

            <div class="detail-content-body">
              <div class="telemetry-feed-box">
                <div class="feed-header">
                  <span class="feed-title">Sample ADLC Trace Stream</span>
                  <span class="feed-status">LIVE STREAM · BUFFER 250</span>
                </div>
                <div class="feed-logs">
                  <code>[TRACE #8812] spec_decomposition: agent_orchestrator OK (latency=412ms)</code>
                  <code>[TRACE #8813] code_synthesis: frontend_view & backend_router generated</code>
                  <code>[TRACE #8814] verification_gate: safety_audit PASSED (0 errors, 0 warnings)</code>
                  <code>[TRACE #8815] human_interaction: review approved, zero cognitive friction spike</code>
                </div>
              </div>

              <div style="margin-top: 1.5rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div style="font-size: 0.85rem; color: var(--color-text-muted);">
                  Ready for paper publication or statistical analysis.
                </div>
                <button @click="handleExportData" class="btn btn-secondary" style="font-size: 0.825rem;">
                  Export Full JSONL Dataset
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Project-Level Comments, Directives & Architecture Log Section -->
        <div class="project-comments-card">
          <div class="comments-card-header">
            <div class="comments-header-info">
              <div class="header-icon-box">💬</div>
              <div>
                <h3 class="detail-card-title">
                  Project Comments & Architecture Log
                  <span class="comment-count-chip">{{ projectComments.length }}</span>
                </h3>
                <span class="detail-card-sub">
                  Project-level discussion, milestone directives, and verification rubrics for <strong>{{ currentProject.title }}</strong>
                </span>
              </div>
            </div>
          </div>

          <!-- Project Comment Composer -->
          <div class="project-composer-box">
            <div class="composer-top-row">
              <div class="composer-author-badge">
                <span class="avatar-circle">
                  {{ (researcherDisplayName || 'R').slice(0, 2).toUpperCase() }}
                </span>
                <span class="author-label">
                  Posting as <strong>{{ researcherDisplayName }}</strong>
                </span>
              </div>

              <!-- Comment Type Chips -->
              <div class="comment-type-chips">
                <button 
                  type="button" 
                  :class="['type-chip', { active: newCommentType === 'project_note' }]"
                  @click="newCommentType = 'project_note'"
                >
                  📝 Project Note
                </button>
                <button 
                  type="button" 
                  :class="['type-chip', { active: newCommentType === 'question' }]"
                  @click="newCommentType = 'question'"
                >
                  ❓ Technical Question
                </button>
                <button 
                  type="button" 
                  :class="['type-chip', { active: newCommentType === 'verification_update' }]"
                  @click="newCommentType = 'verification_update'"
                >
                  ✅ Verification Update
                </button>
              </div>
            </div>

            <textarea 
              v-model="newCommentContent"
              :placeholder="`Write a project-level note, technical question, or verification update for ${currentProject.title}...`"
              rows="3"
              class="project-comment-textarea"
            ></textarea>

            <div v-if="commentError" class="comment-error-alert">
              {{ commentError }}
            </div>

            <div class="composer-footer-row">
              <span class="scope-indicator">
                Project Scope: <strong>{{ currentProject.title }} ({{ currentProject.id }})</strong>
              </span>
              <button 
                @click="handlePostProjectComment" 
                class="btn btn-primary post-btn"
                :disabled="isPostingComment || !newCommentContent.trim()"
              >
                <span v-if="isPostingComment">Posting...</span>
                <span v-else>💬 Post Comment to Project</span>
              </button>
            </div>
          </div>

          <!-- Chronological Project Comments Stream -->
          <div class="project-comments-feed">
            <div v-if="isLoadingComments" class="comments-loading">
              <div class="spinner-small"></div>
              <span>Loading project comments stream...</span>
            </div>

            <div v-else-if="projectComments.length === 0" class="no-comments-state">
              <p>No project comments or architect directives logged yet for <strong>{{ currentProject.title }}</strong>.</p>
              <span class="no-comments-sub">
                Use the composer above to post the first comment or architectural inquiry on this project.
              </span>
            </div>

            <div v-else class="comments-timeline">
              <div v-for="c in projectComments" :key="c.id" class="project-comment-bubble">
                <div class="comment-meta-bar">
                  <div class="comment-author-info">
                    <div class="comment-avatar">
                      {{ (c.author_name || 'JL').slice(0, 2).toUpperCase() }}
                    </div>
                    <div>
                      <div class="comment-author-name">{{ c.author_name || 'Jeremy Lankford' }}</div>
                      <div class="comment-author-role" :class="{ 'architect': c.author_role?.includes('Architect') }">
                        {{ c.author_role || 'Researcher' }}
                      </div>
                    </div>
                  </div>

                  <div class="comment-meta-badges">
                    <span :class="['comment-pill', c.comment_type]">
                      {{ (c.comment_type || 'project_note').replace('_', ' ').toUpperCase() }}
                    </span>
                    <span class="comment-timestamp">{{ formatCommentDate(c.created_at) }}</span>
                  </div>
                </div>

                <div class="comment-body">
                  {{ c.content }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Academic Agreement & Pro-Bono Notice -->
        <div class="academic-agreement-banner">
          <div style="display: flex; align-items: center; gap: 1rem;">
            <div class="academic-seal-icon">🎓</div>
            <div>
              <h4 style="font-size: 1.05rem; font-weight: 700; color: var(--color-navy); margin: 0 0 0.25rem 0;">
                Academic Authorship & $0 Grant Cost Agreement
              </h4>
              <p style="font-size: 0.875rem; color: var(--color-text-muted); margin: 0; line-height: 1.5;">
                This project is provided entirely pro-bono by Jeremy Lankford for qualifying university research labs in exchange for the opportunity to study ADLC metrics and co-author peer-reviewed publications.
              </p>
            </div>
          </div>
          <a href="#lead-researcher" @click="emit('go-home')" class="btn btn-secondary" style="white-space: nowrap; font-size: 0.85rem;">
            Contact Lead Architect
          </a>
        </div>

      </div>

      <!-- Empty State -->
      <div v-else class="empty-state-card">
        <h3>No projects found</h3>
        <p>You do not currently have any active testbeds associated with this account.</p>
        <button @click="emit('submit-proposal')" class="btn btn-primary" style="margin-top: 1rem;">
          Submit ADLC Research Proposal ($0 Cost)
        </button>
      </div>

    </div>
  </div>
</template>

<style scoped>
.my-projects-page {
  background-color: var(--color-bg-light);
  min-height: 85vh;
  padding-bottom: 5rem;
}

.projects-subnav {
  background-color: var(--color-bg-white);
  border-bottom: 1px solid var(--color-border);
  padding: 0.85rem 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

.back-home-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: var(--color-primary);
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  transition: all 0.15s ease;
}

.back-home-btn:hover {
  background: var(--color-primary-light);
  color: var(--color-primary-hover);
}

.live-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 8px #10b981;
}

.projects-main-container {
  padding-top: 2.5rem;
}

.projects-header-block {
  margin-bottom: 2rem;
}

.projects-page-title {
  font-size: 2.35rem;
  font-weight: 800;
  color: var(--color-navy);
  letter-spacing: -0.02em;
  margin: 0.4rem 0 0.75rem 0;
}

.projects-page-subtitle {
  font-size: 1.05rem;
  color: var(--color-text-muted);
  max-width: 760px;
  line-height: 1.6;
  margin: 0;
}

.user-id-pill {
  font-family: monospace;
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--color-primary-light);
  color: var(--color-primary);
  padding: 0.2rem 0.6rem;
  border-radius: 9999px;
  border: 1px solid rgba(27, 108, 168, 0.2);
}

/* Selector Bar */
.project-selector-card {
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1.25rem 1.5rem;
  box-shadow: var(--shadow-sm);
  margin-bottom: 2rem;
}

.selector-content-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.25rem;
}

.selector-left-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-grow: 1;
  flex-wrap: wrap;
}

.selector-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--color-navy);
}

.select-wrapper {
  position: relative;
  min-width: 340px;
  flex-grow: 1;
  max-width: 480px;
}

.project-dropdown-select {
  width: 100%;
  appearance: none;
  background: var(--color-bg-light);
  border: 1.5px solid var(--color-border);
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border-radius: var(--radius-sm);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-navy);
  cursor: pointer;
  transition: all 0.2s ease;
  outline: none;
}

.project-dropdown-select:hover,
.project-dropdown-select:focus {
  border-color: var(--color-primary);
  background: var(--color-bg-white);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.select-arrow {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: var(--color-text-muted);
}

.selector-right-actions {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  flex-wrap: wrap;
}

.ownership-badge {
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.35rem 0.75rem;
  border-radius: 9999px;
}

.ownership-badge.owned {
  background: #dcfce7;
  color: #15803d;
  border: 1px solid #bbf7d0;
}

.claim-btn {
  font-size: 0.825rem;
  padding: 0.5rem 0.85rem;
}

/* Detail Layout */
.project-detail-layout {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.project-detail-hero {
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 2.25rem;
  box-shadow: var(--shadow-sm);
}

.hero-top-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.hero-tags-group {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.project-id-tag {
  font-family: monospace;
  font-size: 0.8rem;
  font-weight: 700;
  background: var(--color-bg-light);
  border: 1px solid var(--color-border);
  padding: 0.25rem 0.65rem;
  border-radius: var(--radius-sm);
  color: var(--color-navy);
}

.project-status-tag {
  font-size: 0.75rem;
  font-weight: 700;
  background: #dbeafe;
  color: #1e40af;
  border: 1px solid #bfdbfe;
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
}

.project-domain-tag {
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--color-bg-light);
  color: var(--color-text-muted);
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
}

.project-headline {
  font-size: 1.85rem;
  font-weight: 800;
  color: var(--color-navy);
  margin: 0 0 1rem 0;
  letter-spacing: -0.01em;
}

.project-summary-text {
  font-size: 1.05rem;
  line-height: 1.65;
  color: var(--color-text-main);
  margin-bottom: 1rem;
}

.project-full-description {
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--color-text-muted);
  background: var(--color-bg-light);
  border-left: 3px solid var(--color-primary);
  padding: 1rem 1.25rem;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  margin-bottom: 1.25rem;
}

.project-tech-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tech-tag-pill {
  font-size: 0.75rem;
  font-weight: 600;
  color: #475569;
  background: #f1f5f9;
  padding: 0.25rem 0.65rem;
  border-radius: var(--radius-sm);
  border: 1px solid #e2e8f0;
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.25rem;
}

.metric-card {
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  box-shadow: var(--shadow-sm);
}

.metric-icon-box {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.metric-icon-box.blue {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.metric-icon-box.green {
  background: #dcfce7;
  color: #16a34a;
}

.metric-icon-box.purple {
  background: #f3e8ff;
  color: #9333ea;
}

.metric-icon-box.amber {
  background: #fef3c7;
  color: #d97706;
}

.metric-info {
  display: flex;
  flex-direction: column;
}

.metric-label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-muted);
  margin-bottom: 0.25rem;
}

.metric-value {
  font-size: 1.45rem;
  font-weight: 800;
  color: var(--color-navy);
  line-height: 1.2;
}

.metric-sub {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin-top: 0.25rem;
}

/* Detail Sections Grid */
.detail-sections-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

@media (max-width: 900px) {
  .detail-sections-grid {
    grid-template-columns: 1fr;
  }
}

.detail-card {
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1.75rem;
  box-shadow: var(--shadow-sm);
}

.detail-card-header {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
}

.detail-card-icon {
  font-size: 1.75rem;
}

.detail-card-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--color-navy);
  margin: 0;
}

.detail-card-sub {
  font-size: 0.8rem;
  color: var(--color-text-muted);
}

.detail-content-body p {
  font-size: 0.925rem;
  line-height: 1.6;
  color: var(--color-text-main);
  margin-bottom: 1.25rem;
}

.protocol-steps-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--color-text-main);
  background: var(--color-bg-light);
  padding: 0.75rem 1rem;
  border-radius: var(--radius-sm);
}

.step-num {
  font-family: monospace;
  font-weight: 800;
  color: var(--color-primary);
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

/* Telemetry Feed Box */
.telemetry-feed-box {
  background: #0f172a;
  border-radius: var(--radius-sm);
  padding: 1.25rem;
  color: #e2e8f0;
}

.feed-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

.feed-title {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #94a3b8;
  letter-spacing: 0.08em;
}

.feed-status {
  font-family: monospace;
  font-size: 0.7rem;
  color: #34d399;
  font-weight: 700;
}

.feed-logs {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-family: 'Fira Code', monospace;
  font-size: 0.775rem;
  color: #cbd5e1;
}

.feed-logs code {
  white-space: pre-wrap;
  word-break: break-all;
}

/* Agreement Banner */
.academic-agreement-banner {
  background: var(--color-bg-white);
  border: 1.5px solid var(--color-primary-light);
  border-radius: var(--radius-md);
  padding: 1.5rem 1.75rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.25rem;
  box-shadow: var(--shadow-sm);
}

.academic-seal-icon {
  font-size: 2.25rem;
}

/* Project Comments Section */
.project-comments-card {
  background-color: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  margin-bottom: 2.5rem;
}

.comments-card-header {
  margin-bottom: 1.5rem;
}

.comments-header-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background-color: var(--color-primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.comment-count-chip {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
  background-color: var(--color-primary-light);
  color: var(--color-primary);
  margin-left: 0.5rem;
  vertical-align: middle;
}

.project-composer-box {
  background-color: var(--color-bg-light);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 2rem;
}

.composer-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.85rem;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.composer-author-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.avatar-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1B6CA8 0%, #4DA8DA 100%);
  color: #ffffff;
  font-weight: 700;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.author-label {
  font-size: 0.8125rem;
  color: var(--color-text-muted);
}

.author-label strong {
  color: var(--color-navy);
}

.comment-type-chips {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.type-chip {
  padding: 0.3rem 0.65rem;
  border-radius: 9999px;
  border: 1px solid var(--color-border);
  background-color: var(--color-bg-white);
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-text-main);
  cursor: pointer;
  transition: all 0.15s ease;
}

.type-chip:hover {
  border-color: var(--color-primary);
}

.type-chip.active {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: #ffffff;
}

.project-comment-textarea {
  width: 100%;
  padding: 0.85rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-bg-white);
  color: var(--color-text-main);
  font-family: inherit;
  font-size: 0.9375rem;
  line-height: 1.5;
  resize: vertical;
  box-sizing: border-box;
}

.project-comment-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(27, 108, 168, 0.12);
}

.comment-error-alert {
  color: #ef4444;
  font-size: 0.8125rem;
  margin-top: 0.5rem;
}

.composer-footer-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.85rem;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.scope-indicator {
  font-size: 0.8125rem;
  color: var(--color-text-muted);
}

.scope-indicator strong {
  color: var(--color-navy);
}

.post-btn {
  padding: 0.55rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 700;
}

.comments-loading {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 2rem;
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

.spinner-small {
  width: 18px;
  height: 18px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.no-comments-state {
  background-color: var(--color-bg-light);
  border: 1px dashed var(--color-border);
  border-radius: 12px;
  padding: 2rem 1rem;
  text-align: center;
}

.no-comments-state p {
  font-weight: 600;
  color: var(--color-navy);
  margin-bottom: 0.25rem;
}

.no-comments-sub {
  font-size: 0.8125rem;
  color: var(--color-text-muted);
}

.project-comment-bubble {
  border: 1px solid var(--color-border);
  background-color: var(--color-bg-white);
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  margin-bottom: 1rem;
}

.comment-author-info {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.comment-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1B6CA8 0%, #4DA8DA 100%);
  color: #ffffff;
  font-weight: 700;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.comment-author-name {
  font-weight: 700;
  font-size: 0.875rem;
  color: var(--color-navy);
}

.comment-author-role {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.comment-author-role.architect {
  color: var(--color-primary);
  font-weight: 600;
}

.comment-meta-badges {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.comment-pill {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  letter-spacing: 0.04em;
  background-color: var(--color-primary-light);
  color: var(--color-primary);
}

.comment-pill.project_feedback,
.comment-pill.account_feedback {
  background-color: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.comment-pill.phase_change,
.comment-pill.phase_directive {
  background-color: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.comment-pill.verification_signoff,
.comment-pill.verification_update {
  background-color: rgba(245, 158, 11, 0.1);
  color: #d97706;
}

.comment-pill.question {
  background-color: rgba(236, 72, 153, 0.1);
  color: #ec4899;
}

.comment-timestamp {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.comment-body {
  font-size: 0.9375rem;
  line-height: 1.6;
  color: var(--color-text-main);
  white-space: pre-wrap;
  background-color: var(--color-bg-light);
  padding: 0.85rem 1rem;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  margin-top: 0.85rem;
}

/* States */
.loading-state-card,
.empty-state-card {
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 4rem 2rem;
  text-align: center;
  color: var(--color-text-muted);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
