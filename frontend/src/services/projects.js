/**
 * Projects Service
 * Interacts with the Cognitive Metrics Backend & Neon PostgreSQL Database.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Default fallback projects for offline / standalone preview
export const DEFAULT_ADLC_PROJECTS = [
  {
    id: 'fluid-guardian',
    title: 'fluid-guardian application',
    slug: 'fluid-guardian',
    domain: 'Clinical Fluid Monitoring & Telemetry',
    status: 'Active · ADLC Development',
    status_badge: 'ADLC Development',
    summary: 'Safety-critical clinical fluid monitoring and volume telemetry application developed using autonomous agent workflows with human-in-the-loop verification under the ADLC protocol.',
    framework: 'Agentic Development Life Cycle (ADLC)',
    lead_architect: 'Jeremy Lankford',
    traces_count: 22400,
    target_venue: 'Clinical Fluid Monitoring · ADLC Research',
    tags: ['Clinical Telemetry', 'Agentic Synthesis', 'Safety Verification', 'Trace Logging']
  },
  {
    id: 'employee-performance-management',
    title: 'Employee Performance Management System',
    slug: 'employee-performance-management',
    domain: 'Enterprise Evaluation & Workflow Suite',
    status: 'Active · ADLC Development',
    status_badge: 'ADLC Development',
    summary: 'Full-lifecycle workforce evaluation, goal tracking, and review platform engineered utilizing multi-agent ADLC orchestration and empirical cognitive friction profiling.',
    framework: 'Agentic Development Life Cycle (ADLC)',
    lead_architect: 'Jeremy Lankford',
    traces_count: 16850,
    target_venue: 'Enterprise Systems · ADLC Architecture',
    tags: ['Enterprise Architecture', 'Multi-Agent Orchestration', 'Cognitive Profiling', 'ADLC Telemetry']
  }
]

/**
 * Fetch projects from Neon DB via backend API.
 * If userId is provided, queries projects tied directly to this user ID.
 */
export async function fetchProjects(userId = null) {
  try {
    const url = userId 
      ? `${API_BASE_URL}/api/users/${encodeURIComponent(userId)}/projects`
      : `${API_BASE_URL}/api/projects`
      
    const res = await fetch(url, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      const data = await res.json()
      if (Array.isArray(data) && data.length > 0) {
        return data
      }
    }
  } catch (err) {
    console.info('Backend API offline or unreachable; using local ADLC projects cache.')
  }
  return DEFAULT_ADLC_PROJECTS
}

/**
 * Tie a project to a signed user ID in Neon DB.
 */
export async function assignProjectToUser(projectId, userId, userEmail = '') {
  try {
    const params = new URLSearchParams({ user_id: userId })
    if (userEmail) params.append('user_email', userEmail)

    const res = await fetch(`${API_BASE_URL}/api/projects/${encodeURIComponent(projectId)}/assign?${params.toString()}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      return await res.json()
    }
  } catch (err) {
    console.warn('Failed to assign project to user in backend:', err)
  }
  return null
}

/**
 * Fetch proposals submitted by a signed user ID.
 */
export async function fetchUserProposals(userId) {
  if (!userId) return []
  try {
    const res = await fetch(`${API_BASE_URL}/api/users/${encodeURIComponent(userId)}/proposals`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      return await res.json()
    }
  } catch (err) {
    console.warn('Failed to fetch user proposals:', err)
  }
  return []
}

/**
 * Synchronize user profile into Neon PostgreSQL users table automatically.
 */
export async function syncUserWithBackend(user) {
  if (!user || !user.uid) return null
  try {
    const res = await fetch(`${API_BASE_URL}/api/users/sync`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: user.uid,
        email: user.email || `${user.uid}@researcher.local`,
        display_name: user.displayName || '',
        institution: user.institution || '',
        department: user.department || ''
      })
    })
    if (res.ok) {
      return await res.json()
    }
  } catch (err) {
    console.info('Backend unreachable for user sync; proceeding offline.')
  }
  return null
}

/**
 * Lead Architect: Fetch all projects with admin stats and comment counts.
 */
export async function fetchAdminProjects() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/admin/projects`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      return await res.json()
    }
  } catch (err) {
    console.warn('Failed to fetch admin projects:', err)
  }
  return DEFAULT_ADLC_PROJECTS
}

/**
 * Lead Architect: Update project status, phase, assignment, and specs.
 */
export async function updateAdminProject(projectId, updateData) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/admin/projects/${encodeURIComponent(projectId)}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updateData)
    })
    if (res.ok) {
      return await res.json()
    }
    const errData = await res.json().catch(() => ({}))
    throw new Error(errData.detail || 'Failed to update project.')
  } catch (err) {
    console.error('Error updating project:', err)
    throw err
  }
}

/**
 * Retrieve comments and architect notes for a project.
 */
export async function fetchProjectComments(projectId) {
  if (!projectId) return []
  try {
    const res = await fetch(`${API_BASE_URL}/api/projects/${encodeURIComponent(projectId)}/comments`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      return await res.json()
    }
  } catch (err) {
    console.warn('Failed to fetch project comments:', err)
  }
  return []
}

/**
 * Post a comment, audit note, directive, or feedback on a project.
 */
export async function postProjectComment(projectId, commentData) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/projects/${encodeURIComponent(projectId)}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(commentData)
    })
    if (res.ok) {
      return await res.json()
    }
    const errData = await res.json().catch(() => ({}))
    throw new Error(errData.detail || 'Failed to post comment.')
  } catch (err) {
    console.error('Error posting comment:', err)
    throw err
  }
}

/**
 * Lead Architect: Fetch registered users for project assignment dropdown.
 */
export async function fetchRegisteredUsers() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/admin/users`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      return await res.json()
    }
  } catch (err) {
    console.warn('Failed to fetch registered users:', err)
  }
  return []
}
