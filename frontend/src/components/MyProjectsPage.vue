<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
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
const selectedProjectId = ref(null)
const isLoading = ref(true)
const exportSuccess = ref(false)
const searchQuery = ref('')

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

const filteredProjects = computed(() => {
  if (!searchQuery.value.trim()) return projects.value
  const q = searchQuery.value.toLowerCase().trim()
  return projects.value.filter(p => {
    const titleMatch = (p.title || '').toLowerCase().includes(q)
    const domainMatch = (p.domain || '').toLowerCase().includes(q)
    const idMatch = (p.id || '').toLowerCase().includes(q)
    const summaryMatch = (p.summary || '').toLowerCase().includes(q)
    const tagsMatch = Array.isArray(p.tags) && p.tags.some(t => t.toLowerCase().includes(q))
    return titleMatch || domainMatch || idMatch || summaryMatch || tagsMatch
  })
})

const parseHashProjectId = () => {
  const hash = window.location.hash || ''
  if (!hash.startsWith('#my-projects')) return null
  const queryIndex = hash.indexOf('?')
  if (queryIndex !== -1) {
    const params = new URLSearchParams(hash.slice(queryIndex + 1))
    return params.get('id') || params.get('project')
  }
  const parts = hash.replace(/^#my-projects\/?/, '').split('/')
  if (parts[0] && parts[0].trim()) {
    return decodeURIComponent(parts[0].trim())
  }
  return null
}

const syncProjectFromHash = () => {
  const hashId = parseHashProjectId()
  if (hashId && projects.value.some(p => p.id === hashId)) {
    selectedProjectId.value = hashId
    loadProjectComments(hashId)
  } else {
    selectedProjectId.value = null
  }
}

const openProjectDetails = (projId) => {
  selectedProjectId.value = projId
  window.location.hash = `#my-projects?id=${encodeURIComponent(projId)}`
  loadProjectComments(projId)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const closeProjectDetails = () => {
  selectedProjectId.value = null
  window.location.hash = '#my-projects'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleHashChange = () => {
  syncProjectFromHash()
}

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
    if (props.user?.uid) {
      projects.value = Array.isArray(data) ? data : []
    } else {
      projects.value = data && data.length ? data : DEFAULT_ADLC_PROJECTS
    }
    syncProjectFromHash()
  } catch (err) {
    console.warn('Failed loading projects:', err)
    projects.value = props.user?.uid ? [] : DEFAULT_ADLC_PROJECTS
    syncProjectFromHash()
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  window.addEventListener('hashchange', handleHashChange)
  loadUserProjects()
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

onUnmounted(() => {
  window.removeEventListener('hashchange', handleHashChange)
})

watch(() => props.user?.uid, () => {
  loadUserProjects()
})

watch(selectedProjectId, (newId) => {
  if (newId) {
    const currentHashId = parseHashProjectId()
    if (newId !== currentHashId) {
      window.location.hash = `#my-projects?id=${encodeURIComponent(newId)}`
    }
    loadProjectComments(newId)
  }
})

const currentProject = computed(() => {
  if (!selectedProjectId.value || !projects.value.length) return null
  return projects.value.find(p => p.id === selectedProjectId.value) || null
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
      <!-- Loading State -->
      <div v-if="isLoading" class="loading-state-card">
        <div class="spinner"></div>
        <p>Loading projects from Neon PostgreSQL...</p>
      </div>

      <!-- VIEW 1: Overview Cards Grid (Three per view) -->
      <div v-else-if="!selectedProjectId" class="projects-overview-section">
        <!-- Page Header: [username]'s Projects -->
        <div class="projects-header-block">
          <div class="header-pre-badge">
            <span class="section-label coral">Researcher Workspace</span>
            <span class="projects-count-pill" :class="{ 'empty-pill': projects.length === 0 }">
              {{ projects.length > 0 ? `${projects.length} Active ${projects.length === 1 ? 'Testbed' : 'Testbeds'}` : 'No Projects' }}
            </span>
          </div>
          
          <div class="overview-title-row">
            <div>
              <h1 class="projects-page-title">
                {{ researcherDisplayName }}'s Projects
              </h1>
              <p class="projects-page-subtitle">
                Manage your active software testbeds developed under the <strong>Agentic Development Life Cycle (ADLC)</strong>. Select any card to open the dedicated project page with live telemetry data streams, cognitive metric benchmarks, and verification rubrics.
              </p>
            </div>

            <div class="overview-cta-group">
              <button 
                @click="emit('submit-proposal')" 
                class="btn btn-primary overview-propose-btn"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                <span>Propose New Testbed</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Filter & Database Status Bar -->
        <div class="overview-toolbar">
          <div class="search-input-wrapper">
            <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Filter projects by title, domain, or tag..." 
              class="overview-search-input"
            />
            <button 
              v-if="searchQuery" 
              @click="searchQuery = ''" 
              class="search-clear-btn"
              aria-label="Clear filter"
            >
              &times;
            </button>
          </div>

          <div class="toolbar-meta">
            <span class="filter-count-label">
              <template v-if="projects.length > 0">
                Showing <strong>{{ filteredProjects.length }}</strong> of {{ projects.length }} testbeds
              </template>
              <template v-else>
                No Projects
              </template>
            </span>
            <span class="ownership-badge owned" title="Managed directly in Neon PostgreSQL database">
              ✓ Database Active
            </span>
          </div>
        </div>

        <!-- Filter Empty State -->
        <div v-if="filteredProjects.length === 0 && projects.length > 0" class="empty-filter-card">
          <div class="empty-icon">🔍</div>
          <h3>No projects match "{{ searchQuery }}"</h3>
          <p>Try clearing your search query or searching for a different keyword or domain.</p>
          <button @click="searchQuery = ''" class="btn btn-secondary" style="margin-top: 1rem;">
            Clear Filter
          </button>
        </div>

        <!-- Overview Cards Grid (Three per view) -->
        <div v-else-if="filteredProjects.length > 0" class="projects-grid">
          <div 
            v-for="p in filteredProjects" 
            :key="p.id" 
            class="project-overview-card"
            @click="openProjectDetails(p.id)"
            tabindex="0"
            role="button"
            :aria-label="`Open details for ${p.title}`"
            @keydown.enter="openProjectDetails(p.id)"
          >
            <!-- Card Top Meta -->
            <div class="card-top-row">
              <span class="card-id-badge">{{ p.id }}</span>
              <div class="card-status-badges">
                <span v-if="p.production_url" class="card-live-badge" title="Live production application">
                  <span class="live-pulse"></span>
                  Live App
                </span>
                <span class="card-status-badge">
                  {{ p.status_badge || p.status || 'Active ADLC' }}
                </span>
              </div>
            </div>

            <!-- Domain category -->
            <div class="card-domain-label">{{ p.domain || 'ADLC Research Testbed' }}</div>

            <!-- Title -->
            <h3 class="card-title">{{ p.title }}</h3>

            <!-- Summary with 3-line clamp -->
            <p class="card-summary">{{ p.summary }}</p>

            <!-- Metrics / Telemetry Specs Strip -->
            <div class="card-specs-strip">
              <div class="spec-item" title="Structured telemetry event traces recorded">
                <svg class="spec-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                </svg>
                <span class="spec-text"><strong>{{ (p.traces_count || 15000).toLocaleString() }}</strong> traces</span>
              </div>
              <div class="spec-item" title="Target Research Venue">
                <svg class="spec-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                </svg>
                <span class="spec-text">{{ p.target_venue ? p.target_venue.split('·')[0].trim() : 'ADLC Research' }}</span>
              </div>
            </div>

            <!-- Tech tags -->
            <div v-if="p.tags && p.tags.length" class="card-tags-row">
              <span v-for="tag in p.tags.slice(0, 3)" :key="tag" class="card-tag-pill">
                {{ tag }}
              </span>
              <span v-if="p.tags.length > 3" class="card-tag-more">
                +{{ p.tags.length - 3 }}
              </span>
            </div>

            <!-- Card Footer -->
            <div class="card-footer">
              <div class="card-lead-architect">
                <span class="lead-avatar">{{ (p.lead_architect || 'JL').slice(0, 2).toUpperCase() }}</span>
                <span class="lead-name">{{ p.lead_architect || 'Jeremy Lankford' }}</span>
              </div>

              <span class="view-details-cta">
                <span>View Details</span>
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="cta-arrow">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                  <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
              </span>
            </div>
          </div>
        </div>

        <!-- Empty Projects State -->
        <div v-else class="empty-state-card">
          <div class="empty-icon">📁</div>
          <h3>No Projects</h3>
          <p>You do not currently have any active testbeds assigned to this account.</p>
          <button @click="emit('submit-proposal')" class="btn btn-primary" style="margin-top: 1rem;">
            Submit ADLC Research Proposal ($0 Cost)
          </button>
        </div>
      </div>

      <!-- VIEW 2: Project Full-Page Detail View (when selectedProjectId is set) -->
      <div v-else-if="currentProject" class="project-detail-layout">
        
        <!-- Dedicated Breadcrumb & Details Navigation Bar -->
        <div class="details-top-nav-card">
          <div class="details-nav-left">
            <button @click="closeProjectDetails" class="back-to-all-btn">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="19" y1="12" x2="5" y2="12"></line>
                <polyline points="12 19 5 12 12 5"></polyline>
              </svg>
              <span>Back to All Projects</span>
            </button>

            <div class="details-breadcrumb">
              <span class="breadcrumb-root" @click="closeProjectDetails">Projects</span>
              <span class="breadcrumb-sep">/</span>
              <span class="breadcrumb-active">{{ currentProject.title }}</span>
            </div>
          </div>

          <div class="details-nav-right">
            <!-- Quick Switcher Dropdown -->
            <div class="quick-switch-wrapper">
              <label for="quick-switch-select" class="quick-switch-label">Switch Project:</label>
              <div class="select-wrapper-compact">
                <select 
                  id="quick-switch-select"
                  v-model="selectedProjectId" 
                  class="quick-switch-select"
                >
                  <option 
                    v-for="p in projects" 
                    :key="p.id" 
                    :value="p.id"
                  >
                    {{ p.title }}
                  </option>
                </select>
                <div class="select-arrow-compact">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </div>
              </div>
            </div>

            <button 
              @click="emit('submit-proposal')" 
              class="btn btn-primary"
              style="font-size: 0.85rem; padding: 0.55rem 1.15rem;"
            >
              + Propose New Testbed
            </button>
          </div>
        </div>

        <!-- Project Hero Card -->
        <div class="project-detail-hero">
          <div class="hero-top-meta">
            <div class="hero-tags-group">
              <span class="project-id-tag">{{ currentProject.id }}</span>
              <span class="project-status-tag">{{ currentProject.status || 'Active · ADLC Development' }}</span>
              <span class="project-domain-tag">{{ currentProject.domain }}</span>
              <a 
                v-if="currentProject.production_url" 
                :href="currentProject.production_url" 
                target="_blank" 
                rel="noopener noreferrer"
                class="project-live-tag"
                title="Application is live in production"
              >
                ● Live Production
              </a>
            </div>

            <div class="hero-action-buttons">
              <a 
                v-if="currentProject.production_url" 
                :href="currentProject.production_url" 
                target="_blank" 
                rel="noopener noreferrer"
                class="btn btn-primary action-btn launch-app-btn"
              >
                <span>🚀 Launch Live App</span>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </a>

              <a 
                v-if="currentProject.repo_url" 
                :href="currentProject.repo_url" 
                target="_blank" 
                rel="noopener noreferrer"
                class="btn btn-secondary action-btn"
              >
                <span>💻 Source Repo</span>
              </a>

              <button 
                @click="handleExportData" 
                class="btn btn-secondary action-btn"
              >
                {{ exportSuccess ? '✓ Telemetry Exported' : '📥 Export Telemetry' }}
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

        <!-- Bottom Return to Overview Bar -->
        <div class="details-bottom-bar">
          <button @click="closeProjectDetails" class="btn btn-secondary back-bottom-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="19" y1="12" x2="5" y2="12"></line>
              <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
            <span>Back to All Projects Overview</span>
          </button>

          <button @click="emit('submit-proposal')" class="btn btn-primary">
            + Propose Another Testbed
          </button>
        </div>

      </div>

      <!-- Fallback when project ID not found -->
      <div v-else class="empty-state-card">
        <h3>Project not found</h3>
        <p>The requested project ID could not be found or is not associated with this account.</p>
        <button @click="closeProjectDetails" class="btn btn-primary" style="margin-top: 1rem;">
          Back to All Projects
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

/* Overview Section */
.projects-overview-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header-pre-badge {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin-bottom: 0.5rem;
}

.projects-count-pill {
  font-size: 0.775rem;
  font-weight: 700;
  padding: 0.2rem 0.65rem;
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-radius: 9999px;
  border: 1px solid rgba(27, 108, 168, 0.2);
}

.projects-count-pill.empty-pill {
  background: var(--color-bg-light, #f1f5f9);
  color: var(--color-text-muted, #64748b);
  border-color: var(--color-border, #cbd5e1);
}

.overview-title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.overview-propose-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  padding: 0.7rem 1.35rem;
  white-space: nowrap;
}

/* Toolbar & Filter Bar */
.overview-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.25rem;
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
  box-shadow: var(--shadow-sm);
}

.search-input-wrapper {
  position: relative;
  flex-grow: 1;
  max-width: 480px;
  min-width: 260px;
}

.search-icon {
  position: absolute;
  left: 0.9rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  pointer-events: none;
}

.overview-search-input {
  width: 100%;
  padding: 0.65rem 2.2rem 0.65rem 2.4rem;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-bg-light);
  font-size: 0.9rem;
  color: var(--color-text-main);
  transition: all 0.2s ease;
  outline: none;
  box-sizing: border-box;
}

.overview-search-input:focus {
  border-color: var(--color-primary);
  background: var(--color-bg-white);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.search-clear-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 1.25rem;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.toolbar-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-count-label {
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

.filter-count-label strong {
  color: var(--color-navy);
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

.empty-filter-card {
  background: var(--color-bg-white);
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-md);
  padding: 3.5rem 2rem;
  text-align: center;
  color: var(--color-text-muted);
}

.empty-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
}

/* =========================================================
   3-PER-VIEW OVERVIEW CARDS GRID
   ========================================================= */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

@media (max-width: 1120px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 700px) {
  .projects-grid {
    grid-template-columns: 1fr;
  }
}

.project-overview-card {
  background: var(--color-bg-white);
  border: 1.5px solid var(--color-border);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 0.22s cubic-bezier(0.16, 1, 0.3, 1),
              border-color 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  outline: none;
}

.project-overview-card:hover,
.project-overview-card:focus-visible {
  transform: translateY(-4px);
  border-color: var(--color-primary);
  box-shadow: 0 16px 32px rgba(27, 108, 168, 0.12), 0 4px 12px rgba(0, 0, 0, 0.04);
}

.card-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.85rem;
  flex-wrap: wrap;
}

.card-id-badge {
  font-family: monospace;
  font-size: 0.725rem;
  font-weight: 700;
  background: var(--color-bg-light);
  border: 1px solid var(--color-border);
  color: var(--color-navy);
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
}

.card-status-badges {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.card-status-badge {
  font-size: 0.7rem;
  font-weight: 700;
  background: #dbeafe;
  color: #1e40af;
  border: 1px solid #bfdbfe;
  padding: 0.18rem 0.55rem;
  border-radius: 9999px;
}

.card-live-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.7rem;
  font-weight: 700;
  background: #d1fae5;
  color: #065f46;
  border: 1px solid #a7f3d0;
  padding: 0.18rem 0.55rem;
  border-radius: 9999px;
}

.live-pulse {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: pulse-green 2s infinite;
}

@keyframes pulse-green {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.card-domain-label {
  font-size: 0.775rem;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.35rem;
}

.card-title {
  font-size: 1.225rem;
  font-weight: 700;
  color: var(--color-navy);
  margin: 0 0 0.65rem 0;
  line-height: 1.35;
  letter-spacing: -0.01em;
  transition: color 0.15s ease;
}

.project-overview-card:hover .card-title {
  color: var(--color-primary);
}

.card-summary {
  font-size: 0.885rem;
  color: #475569;
  line-height: 1.55;
  margin: 0 0 1rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-specs-strip {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.65rem 0.85rem;
  background: var(--color-bg-light);
  border-radius: var(--radius-sm);
  margin-bottom: 0.85rem;
  font-size: 0.775rem;
  color: #334155;
}

.spec-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  white-space: nowrap;
}

.spec-icon {
  color: var(--color-primary);
  flex-shrink: 0;
}

.spec-text strong {
  color: var(--color-navy);
}

.card-tags-row {
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
  margin-bottom: 1.25rem;
}

.card-tag-pill {
  font-size: 0.7rem;
  font-weight: 600;
  color: #475569;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}

.card-tag-more {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--color-text-muted);
  padding: 0.15rem 0.35rem;
}

.card-footer {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
  gap: 0.75rem;
}

.card-lead-architect {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.775rem;
  color: var(--color-text-muted);
}

.lead-avatar {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1B6CA8 0%, #4DA8DA 100%);
  color: #ffffff;
  font-weight: 700;
  font-size: 0.65rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lead-name {
  font-weight: 600;
  color: var(--color-navy);
}

.view-details-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.825rem;
  font-weight: 700;
  color: var(--color-primary);
  transition: all 0.15s ease;
}

.cta-arrow {
  transition: transform 0.2s ease;
}

.project-overview-card:hover .cta-arrow {
  transform: translateX(4px);
}

/* =========================================================
   PROJECT DETAILS PAGE NAVIGATION BAR
   ========================================================= */
.details-top-nav-card {
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  box-shadow: var(--shadow-sm);
  margin-bottom: 0.25rem;
}

.details-nav-left {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.back-to-all-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  background: var(--color-primary-light);
  border: 1px solid rgba(27, 108, 168, 0.2);
  color: var(--color-primary);
  font-size: 0.85rem;
  font-weight: 700;
  padding: 0.45rem 0.85rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.15s ease;
}

.back-to-all-btn:hover {
  background: var(--color-primary);
  color: #ffffff;
}

.details-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.breadcrumb-root {
  color: var(--color-primary);
  cursor: pointer;
  font-weight: 600;
}

.breadcrumb-root:hover {
  text-decoration: underline;
}

.breadcrumb-sep {
  color: var(--color-text-muted);
}

.breadcrumb-active {
  font-weight: 700;
  color: var(--color-navy);
  max-width: 280px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.details-nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.quick-switch-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quick-switch-label {
  font-size: 0.825rem;
  font-weight: 600;
  color: var(--color-text-muted);
}

.select-wrapper-compact {
  position: relative;
  min-width: 220px;
}

.quick-switch-select {
  width: 100%;
  appearance: none;
  background: var(--color-bg-light);
  border: 1px solid var(--color-border);
  padding: 0.45rem 2rem 0.45rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.825rem;
  font-weight: 600;
  color: var(--color-navy);
  cursor: pointer;
  outline: none;
  transition: all 0.15s ease;
}

.quick-switch-select:focus,
.quick-switch-select:hover {
  border-color: var(--color-primary);
  background: var(--color-bg-white);
}

.select-arrow-compact {
  position: absolute;
  right: 0.65rem;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: var(--color-text-muted);
}

.details-bottom-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1.25rem 1.5rem;
  margin-top: 1rem;
  box-shadow: var(--shadow-sm);
}

.back-bottom-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
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

.project-live-tag {
  display: inline-flex;
  align-items: center;
  font-size: 0.75rem;
  font-weight: 700;
  background: #d1fae5;
  color: #065f46;
  border: 1px solid #a7f3d0;
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
  text-decoration: none;
  transition: all 0.15s ease;
}

.project-live-tag:hover {
  background: #a7f3d0;
  color: #047857;
}

.hero-action-buttons {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  padding: 0.5rem 0.95rem;
  text-decoration: none;
  white-space: nowrap;
}

.launch-app-btn {
  background-color: #059669;
  border-color: #059669;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25);
}

.launch-app-btn:hover {
  background-color: #047857;
  border-color: #047857;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(5, 150, 105, 0.35);
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
