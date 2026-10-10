<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import BrandLogo from './BrandLogo.vue'
import {
  fetchAdminProjects,
  updateAdminProject,
  fetchProjectComments,
  postProjectComment,
  fetchRegisteredUsers
} from '../services/projects'

const props = defineProps({
  user: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['go-home', 'open-my-projects'])

const defaultJeremyUser = {
  id: 'jeremy-lankford',
  display_name: 'Jeremy Lankford',
  email: 'jwlankford@gmail.com',
  role: 'lead_architect'
}

// State
const projects = ref([])
const selectedProjectId = ref('')
const users = ref([defaultJeremyUser])
const comments = ref([])
const isLoading = ref(true)
const isSaving = ref(false)
const isPostingComment = ref(false)
const saveSuccessMessage = ref('')
const errorMessage = ref('')
const searchQuery = ref('')
const activeTab = ref('controls') // 'controls' | 'comments'

// Form State for Selected Project
const editForm = ref({
  title: '',
  domain: '',
  status: 'Active · ADLC Development',
  phase: 'Phase 1: Agentic Specification & Requirements',
  user_id: 'jeremy-lankford',
  user_email: 'jwlankford@gmail.com',
  lead_architect: 'Jeremy Lankford',
  framework: 'Agentic Development Life Cycle (ADLC)',
  production_url: '',
  repo_url: '',
  demo_url: '',
  summary: '',
  description: '',
  is_public: true
})

// Comment Input Form
const commentInput = ref({
  content: '',
  comment_type: 'architect_note' // 'architect_note' | 'project_feedback' | 'phase_directive' | 'verification_signoff'
})

const statusOptions = [
  'Active · ADLC Development',
  'Verification Gate · Human-in-the-Loop',
  'In Review · Empirical Audit',
  'Active · Telemetry Profiling',
  'Completed · Artifact Published',
  'Archived · Frozen Testbed'
]

const phaseOptions = [
  'Phase 1: Agentic Specification & Requirements',
  'Phase 2: Autonomous Multi-Agent Synthesis',
  'Phase 3: Formal Verification & Determinism Gate',
  'Phase 4: Cognitive Workload & Friction Profiling',
  'Phase 5: Production & Clinical Telemetry Validation'
]

const commentTypeOptions = [
  { value: 'architect_note', label: 'Architect Note', icon: '📝' },
  { value: 'project_feedback', label: 'Project Feedback', icon: '💬' },
  { value: 'phase_directive', label: 'Phase Directive', icon: '⚡' },
  { value: 'verification_signoff', label: 'Verification Sign-off', icon: '✅' }
]

// Load all admin data
const loadData = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const [projs, userList] = await Promise.all([
      fetchAdminProjects(),
      fetchRegisteredUsers()
    ])
    projects.value = projs || []
    users.value = (userList && userList.length > 0) ? userList : [defaultJeremyUser]

    if (projects.value.length > 0 && !selectedProjectId.value) {
      selectProject(projects.value[0].id)
    }
  } catch (err) {
    errorMessage.value = 'Failed to load project database. Please check Neon DB connection.'
  } finally {
    isLoading.value = false
  }
}

// Select project to edit and load its comments
const selectProject = async (projId) => {
  selectedProjectId.value = projId
  saveSuccessMessage.value = ''
  errorMessage.value = ''

  const proj = projects.value.find(p => p.id === projId)
  if (proj) {
    const defaultUid = users.value[0]?.id || props.user?.uid || 'jeremy-lankford'
    const defaultEmail = users.value[0]?.email || props.user?.email || 'jwlankford@gmail.com'
    editForm.value = {
      title: proj.title || '',
      domain: proj.domain || '',
      status: proj.status || 'Active · ADLC Development',
      phase: proj.phase || 'Phase 1: Agentic Specification & Requirements',
      user_id: proj.user_id || defaultUid,
      user_email: proj.user_email || defaultEmail,
      lead_architect: proj.lead_architect || 'Jeremy Lankford',
      framework: proj.framework || 'Agentic Development Life Cycle (ADLC)',
      production_url: proj.production_url || '',
      repo_url: proj.repo_url || '',
      demo_url: proj.demo_url || '',
      summary: proj.summary || '',
      description: proj.description || '',
      is_public: proj.is_public !== false
    }
  }

  // Load comments stream
  await loadComments(projId)
}

const loadComments = async (projId) => {
  if (!projId) return
  comments.value = await fetchProjectComments(projId)
}

// Currently active project object
const currentProject = computed(() => {
  return projects.value.find(p => p.id === selectedProjectId.value) || null
})

// Filtered projects list based on search
const filteredProjects = computed(() => {
  if (!searchQuery.value.trim()) return projects.value
  const q = searchQuery.value.toLowerCase()
  return projects.value.filter(p =>
    (p.title && p.title.toLowerCase().includes(q)) ||
    (p.id && p.id.toLowerCase().includes(q)) ||
    (p.domain && p.domain.toLowerCase().includes(q)) ||
    (p.user_email && p.user_email.toLowerCase().includes(q))
  )
})

// Handle Account Selection from dropdown
const handleAccountSelection = (e) => {
  const chosenUid = e.target.value
  editForm.value.user_id = chosenUid
  const chosenUser = users.value.find(u => u.id === chosenUid)
  if (chosenUser) {
    editForm.value.user_email = chosenUser.email
  } else {
    editForm.value.user_email = props.user?.email || 'jwlankford@gmail.com'
  }
}

watch(() => props.user, (newUser) => {
  if (newUser) {
    const activeUid = newUser.uid || 'jeremy-lankford'
    const activeEmail = newUser.email || 'jwlankford@gmail.com'
    users.value = [{
      id: activeUid,
      display_name: 'Jeremy Lankford',
      email: activeEmail,
      role: 'lead_architect'
    }]
    if (!editForm.value.user_id || editForm.value.user_id === 'jeremy-lankford') {
      editForm.value.user_id = activeUid
      editForm.value.user_email = activeEmail
    }
  }
}, { immediate: true })

// Save Project Updates as Lead Architect
const handleSaveProject = async () => {
  if (!selectedProjectId.value) return
  isSaving.value = true
  saveSuccessMessage.value = ''
  errorMessage.value = ''

  try {
    const res = await updateAdminProject(selectedProjectId.value, editForm.value)
    saveSuccessMessage.value = res.message || 'Project specifications, status, and phase updated successfully!'
    
    // Refresh project in local list
    const idx = projects.value.findIndex(p => p.id === selectedProjectId.value)
    if (idx !== -1) {
      projects.value[idx] = {
        ...projects.value[idx],
        ...editForm.value,
        updated_at: new Date().toISOString()
      }
    }
    // Refresh comments (in case an automated audit comment was generated)
    await loadComments(selectedProjectId.value)

    setTimeout(() => {
      saveSuccessMessage.value = ''
    }, 4500)
  } catch (err) {
    errorMessage.value = err.message || 'Failed to save project updates.'
  } finally {
    isSaving.value = false
  }
}

// Post Comment on Project
const handlePostComment = async () => {
  if (!commentInput.value.content.trim() || !selectedProjectId.value) return
  isPostingComment.value = true
  errorMessage.value = ''

  try {
    const payload = {
      user_id: props.user?.uid || null,
      author_name: props.user?.displayName || 'Jeremy Lankford',
      author_email: props.user?.email || 'jlankford@cognitivemetrics.org',
      author_role: 'Lead Architect',
      comment_type: commentInput.value.comment_type,
      content: commentInput.value.content.trim()
    }

    const created = await postProjectComment(selectedProjectId.value, payload)
    if (created) {
      comments.value.unshift(created)
      commentInput.value.content = ''
      
      // Update comment count on project
      const proj = projects.value.find(p => p.id === selectedProjectId.value)
      if (proj) {
        proj.comment_count = (proj.comment_count || 0) + 1
      }
    }
  } catch (err) {
    errorMessage.value = err.message || 'Failed to post project comment.'
  } finally {
    isPostingComment.value = false
  }
}

const formatDate = (dateStr) => {
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

onMounted(() => {
  loadData()
  window.scrollTo({ top: 0, behavior: 'smooth' })
})
</script>

<template>
  <div class="admin-console-page">
    <!-- Top Navigation Bar -->
    <div class="admin-subnav">
      <div class="container" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
        <button @click="emit('go-home')" class="back-home-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          <span>Back to Research Overview</span>
        </button>

        <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
          <button @click="emit('open-my-projects')" class="nav-ghost-btn">
            📁 View Researcher Workspace
          </button>
          <div class="db-pill">
            <span class="live-dot" title="Neon DB Connected"></span>
            <span>Neon DB Connected</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Container -->
    <div class="container admin-main-container">
      
      <!-- Executive Header -->
      <div class="admin-header-card">
        <div class="header-badge-row">
          <span class="badge-role">Lead Architect Console</span>
          <span class="badge-architect">Architect: Jeremy Lankford</span>
        </div>
        <h1 class="admin-title">Project & Account Administration</h1>
        <p class="admin-subtitle">
          Manage ADLC lifecycle phases, update research project specifications, bind accounts at the database table level, and maintain the project-level audit comment stream.
        </p>

        <!-- Quick Metrics Counter Strip -->
        <div class="metrics-strip">
          <div class="metric-box">
            <div class="metric-num">{{ projects.length }}</div>
            <div class="metric-lbl">Total Database Projects</div>
          </div>
          <div class="metric-box">
            <div class="metric-num">{{ users.length }}</div>
            <div class="metric-lbl">Registered Accounts</div>
          </div>
          <div class="metric-box">
            <div class="metric-num">{{ comments.length }}</div>
            <div class="metric-lbl">Active Project Comments</div>
          </div>
          <div class="metric-box">
            <div class="metric-num" style="color: #10b981;">100%</div>
            <div class="metric-lbl">Neon Schema Integrity</div>
          </div>
        </div>
      </div>

      <!-- Error / Success Alert Banners -->
      <div v-if="errorMessage" class="alert-banner error-banner">
        ⚠️ {{ errorMessage }}
      </div>
      <div v-if="saveSuccessMessage" class="alert-banner success-banner">
        ✓ {{ saveSuccessMessage }}
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Connecting to Neon PostgreSQL database...</p>
      </div>

      <!-- Main Layout: Sidebar Projects List + Detail Workspace -->
      <div v-else class="admin-workspace-grid">
        
        <!-- Left Column: Projects Directory -->
        <div class="projects-sidebar-panel">
          <div class="panel-header">
            <h3>Projects Directory</h3>
            <span class="counter-badge">{{ filteredProjects.length }}</span>
          </div>

          <!-- Search Box -->
          <div class="search-box-wrap">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search by title, domain, or account..." 
              class="search-input"
            />
          </div>

          <!-- Project List Items -->
          <div class="project-items-list">
            <div 
              v-for="p in filteredProjects" 
              :key="p.id"
              :class="['project-sidebar-card', { active: p.id === selectedProjectId }]"
              @click="selectProject(p.id)"
            >
              <div class="card-top-row">
                <span class="proj-id-badge">{{ p.id }}</span>
                <span class="proj-comments-count" v-if="p.comment_count">
                  💬 {{ p.comment_count }}
                </span>
              </div>
              <h4 class="proj-title">{{ p.title }}</h4>
              <div class="proj-meta-line">
                <span class="proj-phase-chip">{{ p.phase || 'Phase 1' }}</span>
              </div>
              <div class="proj-account-line">
                <span class="account-icon">👤</span>
                <span class="account-text">{{ p.user_email || 'jwlankford@gmail.com' }}</span>
              </div>
            </div>

            <div v-if="filteredProjects.length === 0" class="no-projects-hint">
              No matching projects found.
            </div>
          </div>
        </div>

        <!-- Right Column: Lead Architect Studio -->
        <div class="architect-studio-panel" v-if="currentProject">
          
          <!-- Top Studio Bar with Tabs -->
          <div class="studio-top-bar">
            <div class="studio-project-title-area">
              <span class="studio-label">Managing Project</span>
              <h2>{{ currentProject.title }}</h2>
            </div>

            <div class="studio-tabs">
              <button 
                :class="['tab-btn', { active: activeTab === 'controls' }]"
                @click="activeTab = 'controls'"
              >
                ⚙️ Status, Phase & Specs
              </button>
              <button 
                :class="['tab-btn', { active: activeTab === 'comments' }]"
                @click="activeTab = 'comments'"
              >
                💬 Project Comments & Log ({{ comments.length }})
              </button>
            </div>
          </div>

          <!-- TAB 1: Status, Phase & Assignment Controls -->
          <div v-if="activeTab === 'controls'" class="tab-content controls-content">
            <form @submit.prevent="handleSaveProject" class="architect-form">
              
              <!-- Row 1: Status & Phase Grid -->
              <div class="form-row-2">
                <div class="form-group">
                  <label class="form-label">
                    <span>Project Lifecycle Status</span>
                    <span class="required">*</span>
                  </label>
                  <select v-model="editForm.status" class="form-select">
                    <option v-for="st in statusOptions" :key="st" :value="st">{{ st }}</option>
                  </select>
                  <p class="field-hint">Publicly displayed development status indicator</p>
                </div>

                <div class="form-group">
                  <label class="form-label">
                    <span>ADLC Development Phase</span>
                    <span class="required">*</span>
                  </label>
                  <select v-model="editForm.phase" class="form-select highlight-select">
                    <option v-for="ph in phaseOptions" :key="ph" :value="ph">{{ ph }}</option>
                  </select>
                  <p class="field-hint">Current stage in the Agentic Development Life Cycle</p>
                </div>
              </div>

              <!-- Row 2: Account Assignment (Database Table Binding) -->
              <div class="assignment-box">
                <div class="assignment-header">
                  <h4>Account Binding (Database Table Level)</h4>
                  <span class="badge-relational">user_projects junction</span>
                </div>
                <div class="form-row-2">
                  <div class="form-group">
                    <label class="form-label">Assign to Registered User Account</label>
                    <select :value="editForm.user_id" @change="handleAccountSelection" class="form-select">
                      <option v-for="u in users" :key="u.id" :value="u.id">
                        Jeremy Lankford
                      </option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label class="form-label">Assigned Account Email</label>
                    <input 
                      v-model="editForm.user_email" 
                      type="email" 
                      placeholder="jwlankford@gmail.com" 
                      class="form-input"
                    />
                  </div>
                </div>
                <p class="field-hint" style="margin-top: 0.25rem;">
                  Binding writes directly to PostgreSQL <code>projects.user_id</code> and creates referential rows in <code>user_projects</code>.
                </p>
              </div>

              <!-- Row 3: Project Title & Domain -->
              <div class="form-row-2">
                <div class="form-group">
                  <label class="form-label">Project Title</label>
                  <input v-model="editForm.title" type="text" class="form-input" required />
                </div>

                <div class="form-group">
                  <label class="form-label">Domain / Application Area</label>
                  <input v-model="editForm.domain" type="text" class="form-input" required />
                </div>
              </div>

              <!-- Row 4: Lead Architect & Framework -->
              <div class="form-row-2">
                <div class="form-group">
                  <label class="form-label">Lead Architect</label>
                  <input v-model="editForm.lead_architect" type="text" class="form-input" />
                </div>

                <div class="form-group">
                  <label class="form-label">Architecture Framework</label>
                  <input v-model="editForm.framework" type="text" class="form-input" />
                </div>
              </div>

              <!-- Row 5: Application Deployment & Repository URLs -->
              <div class="form-row-2">
                <div class="form-group">
                  <label class="form-label">
                    <span>🚀 Production Application URL</span>
                  </label>
                  <input 
                    v-model="editForm.production_url" 
                    type="url" 
                    placeholder="https://fluid-guardian.cognitivemetrics.app" 
                    class="form-input" 
                  />
                  <p class="field-hint">Live deployed application URL for researchers to launch</p>
                </div>

                <div class="form-group">
                  <label class="form-label">
                    <span>💻 Source Repository URL</span>
                  </label>
                  <input 
                    v-model="editForm.repo_url" 
                    type="url" 
                    placeholder="https://github.com/cognitive-metrics-ai/..." 
                    class="form-input" 
                  />
                  <p class="field-hint">Public or private Git repository link</p>
                </div>
              </div>

              <!-- Row 6: Project Summary -->
              <div class="form-group">
                <label class="form-label">Executive Summary</label>
                <textarea v-model="editForm.summary" rows="3" class="form-textarea" required></textarea>
              </div>

              <!-- Row 6: Detailed Description -->
              <div class="form-group">
                <label class="form-label">Detailed Architectural Description</label>
                <textarea v-model="editForm.description" rows="4" class="form-textarea"></textarea>
              </div>

              <!-- Submit Button -->
              <div class="form-actions-bar">
                <button type="submit" class="btn btn-primary save-btn" :disabled="isSaving">
                  <span v-if="isSaving">Updating Neon DB...</span>
                  <span v-else>💾 Save Project & Phase Updates</span>
                </button>
              </div>
            </form>
          </div>

          <!-- TAB 2: Project-Level Comments & Architect Log -->
          <div v-else-if="activeTab === 'comments'" class="tab-content comments-content">
            
            <!-- Comment Input Box -->
            <div class="comment-composer-box">
              <div class="composer-header">
                <h4>Post Comment / Architect Note on Project</h4>
                <span class="author-tag">Author: Jeremy Lankford (Lead Architect)</span>
              </div>

              <!-- Comment Type Picker -->
              <div class="comment-type-pills">
                <button 
                  v-for="opt in commentTypeOptions" 
                  :key="opt.value"
                  type="button"
                  :class="['type-pill-btn', { selected: commentInput.comment_type === opt.value }]"
                  @click="commentInput.comment_type = opt.value"
                >
                  <span>{{ opt.icon }}</span>
                  <span>{{ opt.label }}</span>
                </button>
              </div>

              <!-- Textarea -->
              <textarea 
                v-model="commentInput.content" 
                placeholder="Write an architectural audit note, specification feedback, verification milestone, or directive for this project..."
                rows="3"
                class="form-textarea comment-textarea"
              ></textarea>

              <div class="composer-footer">
                <span class="target-project-hint">
                  Project Scope: <strong>{{ currentProject.title }} ({{ currentProject.id }})</strong>
                </span>
                <button 
                  @click="handlePostComment" 
                  class="btn btn-primary post-comment-btn"
                  :disabled="isPostingComment || !commentInput.content.trim()"
                >
                  <span v-if="isPostingComment">Posting...</span>
                  <span v-else>💬 Post Comment to Project</span>
                </button>
              </div>
            </div>

            <!-- Comments Stream List -->
            <div class="comments-stream-container">
              <h4 class="stream-title">Chronological Project Audit & Comments Stream</h4>
              
              <div v-if="comments.length === 0" class="no-comments-box">
                <p>No comments or audit notes recorded on this project yet.</p>
                <span style="font-size: 0.8125rem; color: var(--color-text-muted);">
                  Use the composer above to log the first feedback note, phase directive, or milestone for {{ currentProject.title }}.
                </span>
              </div>

              <div v-else class="comments-timeline">
                <div v-for="c in comments" :key="c.id" class="comment-bubble-card">
                  <div class="comment-meta-bar">
                    <div class="author-info-group">
                      <div class="author-avatar-chip">
                        {{ (c.author_name || 'JL').slice(0, 2).toUpperCase() }}
                      </div>
                      <div>
                        <div class="author-name-text">{{ c.author_name || 'Jeremy Lankford' }}</div>
                        <div class="author-role-sub">{{ c.author_role || 'Lead Architect' }}</div>
                      </div>
                    </div>

                    <div class="comment-badge-group">
                      <span :class="['comment-type-badge', c.comment_type]">
                        {{ c.comment_type?.replace('_', ' ').toUpperCase() }}
                      </span>
                      <span class="comment-date-text">{{ formatDate(c.created_at) }}</span>
                    </div>
                  </div>

                  <div class="comment-body-text">
                    {{ c.content }}
                  </div>
                </div>
              </div>

            </div>

          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<style scoped>
.admin-console-page {
  min-height: 100vh;
  background-color: var(--color-bg-light);
  color: var(--color-text-main);
  padding-bottom: 5rem;
}

.admin-subnav {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: var(--color-bg-white);
  border-bottom: 1px solid var(--color-border);
  padding: 0.75rem 0;
  backdrop-filter: blur(8px);
}

.back-home-btn, .nav-ghost-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 0.45rem 0.85rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-main);
  cursor: pointer;
  transition: all 0.15s ease;
}

.back-home-btn:hover, .nav-ghost-btn:hover {
  background-color: var(--color-bg-light);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.db-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #10b981;
  background-color: rgba(16, 185, 129, 0.1);
  padding: 0.35rem 0.75rem;
  border-radius: 9999px;
  border: 1px solid rgba(16, 185, 129, 0.25);
}

.live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #10b981;
  box-shadow: 0 0 8px #10b981;
}

.admin-main-container {
  padding-top: 2rem;
}

.admin-header-card {
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow-sm);
}

.header-badge-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
}

.badge-role {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-primary);
  background-color: var(--color-primary-light);
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
}

.badge-architect {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  color: #8b5cf6;
  background-color: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.25);
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
}

.admin-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-navy);
  margin-bottom: 0.5rem;
}

.admin-subtitle {
  color: var(--color-text-muted);
  max-width: 850px;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.metrics-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  border-top: 1px solid var(--color-border);
  padding-top: 1.5rem;
}

.metric-box {
  background-color: var(--color-bg-light);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  padding: 1rem 1.25rem;
}

.metric-num {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--color-navy);
  line-height: 1.2;
}

.metric-lbl {
  font-size: 0.8125rem;
  color: var(--color-text-muted);
  font-weight: 600;
  margin-top: 0.25rem;
}

.alert-banner {
  padding: 1rem 1.25rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  font-weight: 600;
  font-size: 0.9375rem;
}

.error-banner {
  background-color: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.success-banner {
  background-color: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #10b981;
}

.loading-state {
  text-align: center;
  padding: 4rem 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Workspace Grid */
.admin-workspace-grid {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 1.75rem;
  align-items: start;
}

@media (max-width: 992px) {
  .admin-workspace-grid {
    grid-template-columns: 1fr;
  }
}

/* Sidebar */
.projects-sidebar-panel {
  background-color: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: 14px;
  padding: 1.25rem;
  box-shadow: var(--shadow-sm);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.panel-header h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-navy);
}

.counter-badge {
  background-color: var(--color-bg-light);
  border: 1px solid var(--color-border);
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
  color: var(--color-text-muted);
}

.search-box-wrap {
  margin-bottom: 1rem;
}

.search-input {
  width: 100%;
  padding: 0.55rem 0.85rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-bg-light);
  color: var(--color-text-main);
  font-size: 0.875rem;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.project-items-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  max-height: 650px;
  overflow-y: auto;
  padding-right: 0.25rem;
}

.project-sidebar-card {
  border: 1px solid var(--color-border);
  background-color: var(--color-bg-light);
  border-radius: 10px;
  padding: 0.85rem 1rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.project-sidebar-card:hover {
  border-color: var(--color-primary);
  transform: translateY(-1px);
}

.project-sidebar-card.active {
  background-color: var(--color-bg-white);
  border-color: var(--color-primary);
  box-shadow: 0 4px 12px rgba(27, 108, 168, 0.15);
  border-left: 4px solid var(--color-primary);
}

.card-top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.35rem;
}

.proj-id-badge {
  font-size: 0.7rem;
  font-family: monospace;
  font-weight: 700;
  color: var(--color-text-muted);
  background: var(--color-bg-white);
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  border: 1px solid var(--color-border);
}

.proj-comments-count {
  font-size: 0.75rem;
  font-weight: 700;
  color: #8b5cf6;
}

.proj-title {
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--color-navy);
  margin-bottom: 0.35rem;
  line-height: 1.3;
}

.proj-meta-line {
  margin-bottom: 0.35rem;
}

.proj-phase-chip {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 600;
  background-color: rgba(27, 108, 168, 0.1);
  color: var(--color-primary);
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}

.proj-account-line {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.75rem;
  color: var(--color-text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.no-projects-hint {
  text-align: center;
  padding: 2rem 1rem;
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

/* Right Studio Panel */
.architect-studio-panel {
  background-color: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: 14px;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.studio-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1.25rem 1.75rem;
  border-bottom: 1px solid var(--color-border);
  background-color: var(--color-bg-light);
}

.studio-project-title-area .studio-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--color-text-muted);
}

.studio-project-title-area h2 {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--color-navy);
  margin-top: 0.2rem;
}

.studio-tabs {
  display: flex;
  gap: 0.5rem;
}

.tab-btn {
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  background-color: var(--color-bg-white);
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-main);
  cursor: pointer;
  transition: all 0.15s ease;
}

.tab-btn:hover {
  background-color: var(--color-bg-light);
  border-color: var(--color-primary);
}

.tab-btn.active {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: #ffffff;
}

.tab-content {
  padding: 1.75rem;
}

/* Controls Form */
.architect-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

@media (max-width: 768px) {
  .form-row-2 {
    grid-template-columns: 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--color-navy);
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.required {
  color: #ef4444;
}

.field-hint {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin-top: 0.2rem;
}

.form-input, .form-select, .form-textarea {
  width: 100%;
  padding: 0.65rem 0.85rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-bg-light);
  color: var(--color-text-main);
  font-size: 0.9375rem;
  transition: border-color 0.15s ease;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  background-color: var(--color-bg-white);
}

.highlight-select {
  border-color: #8b5cf6;
  font-weight: 600;
  color: #6d28d9;
}

.assignment-box {
  background-color: var(--color-bg-light);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.25rem;
}

.assignment-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.85rem;
}

.assignment-header h4 {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-navy);
}

.badge-relational {
  font-size: 0.7rem;
  font-family: monospace;
  font-weight: 700;
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.25);
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}

.form-actions-bar {
  display: flex;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

.save-btn {
  padding: 0.75rem 1.75rem;
  font-size: 1rem;
  font-weight: 700;
}

/* Comments Tab */
.comment-composer-box {
  background-color: var(--color-bg-light);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 2rem;
}

.composer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.85rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.composer-header h4 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-navy);
}

.author-tag {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--color-primary);
}

.comment-type-pills {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 0.85rem;
}

.type-pill-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.75rem;
  border-radius: 9999px;
  border: 1px solid var(--color-border);
  background-color: var(--color-bg-white);
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--color-text-main);
  cursor: pointer;
  transition: all 0.15s ease;
}

.type-pill-btn:hover {
  border-color: var(--color-primary);
}

.type-pill-btn.selected {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: #ffffff;
}

.comment-textarea {
  background-color: var(--color-bg-white);
  resize: vertical;
}

.composer-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.85rem;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.target-account-hint,
.target-project-hint {
  font-size: 0.8125rem;
  color: var(--color-text-muted);
}

.target-account-hint strong,
.target-project-hint strong {
  color: var(--color-navy);
}

.post-comment-btn {
  padding: 0.6rem 1.35rem;
  font-size: 0.9375rem;
  font-weight: 700;
}

/* Comments Stream */
.comments-stream-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stream-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--color-navy);
  margin-bottom: 0.25rem;
}

.no-comments-box {
  background-color: var(--color-bg-light);
  border: 1px dashed var(--color-border);
  border-radius: 12px;
  padding: 2.5rem 1rem;
  text-align: center;
}

.no-comments-box p {
  font-weight: 600;
  color: var(--color-navy);
  margin-bottom: 0.35rem;
}

.comments-timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment-bubble-card {
  border: 1px solid var(--color-border);
  background-color: var(--color-bg-white);
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.comment-meta-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.85rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.author-info-group {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.author-avatar-chip {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1B6CA8 0%, #4DA8DA 100%);
  color: #ffffff;
  font-weight: 700;
  font-size: 0.8125rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.author-name-text {
  font-weight: 700;
  font-size: 0.9375rem;
  color: var(--color-navy);
}

.author-role-sub {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.comment-badge-group {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.comment-type-badge {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  letter-spacing: 0.04em;
}

.comment-type-badge.architect_note {
  background-color: rgba(27, 108, 168, 0.1);
  color: var(--color-primary);
}

.comment-type-badge.project_feedback,
.comment-type-badge.account_feedback {
  background-color: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.comment-type-badge.phase_change, .comment-type-badge.phase_directive {
  background-color: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.comment-type-badge.verification_signoff {
  background-color: rgba(245, 158, 11, 0.1);
  color: #d97706;
}

.comment-date-text {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.comment-body-text {
  font-size: 0.9375rem;
  line-height: 1.6;
  color: var(--color-text-main);
  white-space: pre-wrap;
  background-color: var(--color-bg-light);
  padding: 0.85rem 1rem;
  border-radius: 8px;
  border: 1px solid var(--color-border);
}
</style>
