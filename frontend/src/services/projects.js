/**
 * Projects Service
 * Interacts with the Cognitive Metrics Backend & Neon PostgreSQL Database.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Default registered Lead Architect user
export const DEFAULT_REGISTERED_USERS = [
  {
    id: 'Jq4WTmNLN9XbtDqZsbIesLWCTTn1',
    email: 'jwlankford@gmail.com',
    display_name: 'Jeremy Lankford',
    role: 'lead_architect',
    institution: 'Cognitive Metrics Research Lab',
    department: 'AI & Systems Architecture'
  }
]

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
    user_id: 'Jq4WTmNLN9XbtDqZsbIesLWCTTn1',
    user_email: 'jwlankford@gmail.com',
    traces_count: 22400,
    target_venue: 'Clinical Fluid Monitoring · ADLC Research',
    tags: ['Clinical Telemetry', 'Agentic Synthesis', 'Safety Verification', 'Trace Logging'],
    repo_url: 'https://github.com/cognitive-metrics-ai/fluid-guardian',
    demo_url: null,
    production_url: 'https://fluid-guardian.cognitivemetrics.app/'
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
    user_id: 'Jq4WTmNLN9XbtDqZsbIesLWCTTn1',
    user_email: 'jwlankford@gmail.com',
    traces_count: 16850,
    target_venue: 'Enterprise Systems · ADLC Architecture',
    tags: ['Enterprise Architecture', 'Multi-Agent Orchestration', 'Cognitive Profiling', 'ADLC Telemetry'],
    repo_url: 'https://github.com/cognitive-metrics-ai/epms',
    demo_url: null,
    production_url: null
  }
]

const LOCAL_PROJECTS_KEY = 'cognitive_metrics_adlc_projects'

/**
 * Retrieve cached projects from localStorage with fallback to default projects.
 */
export function getLocalProjects() {
  try {
    const raw = typeof localStorage !== 'undefined' ? localStorage.getItem(LOCAL_PROJECTS_KEY) : null
    if (raw) {
      const parsed = JSON.parse(raw)
      if (Array.isArray(parsed) && parsed.length > 0) {
        // Strip any legacy placeholder/fake projects
        const cleaned = parsed.filter(p => p.id !== 'PROP-ADLC-9042' && p.id !== 'PROP-ADLC-8411')
        if (cleaned.length !== parsed.length) {
          saveLocalProjects(cleaned)
        }
        return cleaned.length > 0 ? cleaned : DEFAULT_ADLC_PROJECTS
      }
    }
  } catch (e) {
    // Ignore storage parse error
  }
  return DEFAULT_ADLC_PROJECTS
}

/**
 * Persist projects list to localStorage.
 */
export function saveLocalProjects(projects) {
  try {
    if (typeof localStorage !== 'undefined' && Array.isArray(projects)) {
      localStorage.setItem(LOCAL_PROJECTS_KEY, JSON.stringify(projects))
    }
  } catch (e) {
    // Ignore storage quota error
  }
}

/**
 * Update a project in the local cache and DEFAULT_ADLC_PROJECTS.
 */
export function updateLocalProject(projectId, updateData) {
  const current = getLocalProjects()
  const idx = current.findIndex(p => p.id === projectId || p.slug === projectId)
  let updatedItem

  const sanitizedUpdate = { ...updateData }
  if (sanitizedUpdate.user_id === '' || sanitizedUpdate.user_id === 'unassigned') {
    sanitizedUpdate.user_id = null
  }
  if (sanitizedUpdate.user_email === '') {
    sanitizedUpdate.user_email = null
  }

  if (idx !== -1) {
    current[idx] = { ...current[idx], ...sanitizedUpdate, updated_at: new Date().toISOString() }
    updatedItem = current[idx]
  } else {
    updatedItem = { id: projectId, ...sanitizedUpdate, updated_at: new Date().toISOString() }
    current.push(updatedItem)
  }
  saveLocalProjects(current)

  // Also sync in-memory DEFAULT_ADLC_PROJECTS
  const defIdx = DEFAULT_ADLC_PROJECTS.findIndex(p => p.id === projectId || p.slug === projectId)
  if (defIdx !== -1) {
    DEFAULT_ADLC_PROJECTS[defIdx] = { ...DEFAULT_ADLC_PROJECTS[defIdx], ...sanitizedUpdate }
  }
  return updatedItem
}

/**
 * Determine if a project belongs to a user (matching user ID or user email).
 * An unassigned project (no user_id and no user_email) belongs to no one and must never match.
 */
export function filterUserProjects(projectsList, user) {
  if (!user) return []
  const uid = typeof user === 'string' ? user : (user.uid || user.id || '')
  const email = (typeof user === 'object' && user.email ? user.email : (uid.includes('@') ? uid : '')).trim().toLowerCase()
  const isJeremy = email === 'jwlankford@gmail.com' || uid === 'Jq4WTmNLN9XbtDqZsbIesLWCTTn1'

  return (projectsList || []).filter(p => {
    // Unassigned check: if neither user_id nor user_email is set, project belongs to NO ONE
    const hasUserId = p.user_id && p.user_id !== 'unassigned' && p.user_id !== 'null'
    const hasUserEmail = p.user_email && p.user_email !== 'null'
    if (!hasUserId && !hasUserEmail) return false

    // 1. Direct match on user_id
    if (uid && p.user_id && p.user_id === uid) return true
    // 2. Direct match on user_email
    if (email && p.user_email && p.user_email.trim().toLowerCase() === email) return true
    // 3. Lead Architect Jeremy Lankford matching
    if (isJeremy) {
      if (p.user_id === 'Jq4WTmNLN9XbtDqZsbIesLWCTTn1') return true
      if (p.user_email && p.user_email.trim().toLowerCase() === 'jwlankford@gmail.com') return true
    }
    return false
  })
}

/**
 * Fetch projects from Neon DB via backend API or local cache.
 * Accepts a user object ({ uid, email }) or user ID string.
 */
export async function fetchProjects(userOrId = null, userEmail = null) {
  let userId = null
  let email = userEmail

  if (typeof userOrId === 'object' && userOrId !== null) {
    userId = userOrId.uid || userOrId.id || null
    email = email || userOrId.email || null
  } else if (typeof userOrId === 'string' && userOrId.trim()) {
    userId = userOrId.trim()
    if (userId.includes('@') && !email) {
      email = userId
    }
  }

  const isUserQuery = !!(userId || email)

  try {
    const queryParams = new URLSearchParams()
    if (email) queryParams.append('email', email)
    const qs = queryParams.toString() ? `?${queryParams.toString()}` : ''

    const url = userId 
      ? `${API_BASE_URL}/api/users/${encodeURIComponent(userId)}/projects${qs}`
      : (email ? `${API_BASE_URL}/api/users/${encodeURIComponent(email)}/projects${qs}` : `${API_BASE_URL}/api/projects`)
      
    const res = await fetch(url, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      const data = await res.json()
      if (Array.isArray(data)) {
        if (!isUserQuery && data.length > 0) {
          saveLocalProjects(data)
        }
        if (isUserQuery) {
          return data
        }
        if (data.length > 0) {
          return data
        }
      }
    }
  } catch (err) {
    console.info('Backend API offline or unreachable; using local ADLC projects cache.')
  }

  // Offline / Fallback resolution
  const localProjects = getLocalProjects()
  if (isUserQuery) {
    return filterUserProjects(localProjects, { uid: userId, email })
  }
  return localProjects && localProjects.length ? localProjects : DEFAULT_ADLC_PROJECTS
}

/**
 * Tie a project to a signed user ID in Neon DB and local cache.
 */
export async function assignProjectToUser(projectId, userId, userEmail = '') {
  // Update local storage first
  updateLocalProject(projectId, { user_id: userId, user_email: userEmail })

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
  return { id: projectId, user_id: userId, user_email: userEmail }
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
    const displayName = user.displayName || (user.email ? user.email.split('@')[0] : '')
    const res = await fetch(`${API_BASE_URL}/api/users/sync`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: user.uid,
        email: user.email || `${user.uid}@researcher.local`,
        display_name: displayName,
        institution: user.institution || '',
        department: user.department || ''
      })
    })
    if (res.ok) {
      const data = await res.json()
      console.info('User successfully synced with backend PostgreSQL users table:', data.email)
      return data
    } else {
      const errText = await res.text().catch(() => '')
      console.warn('Backend user sync returned error:', res.status, errText)
    }
  } catch (err) {
    console.warn('Backend unreachable for user sync:', err)
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
      const data = await res.json()
      if (Array.isArray(data) && data.length > 0) {
        saveLocalProjects(data)
        return data
      }
    }
  } catch (err) {
    console.warn('Failed to fetch admin projects:', err)
  }
  return getLocalProjects()
}

/**
 * Lead Architect: Update project status, phase, assignment, and specs.
 */
export async function updateAdminProject(projectId, updateData) {
  // Always update local storage and in-memory projects first so changes take effect immediately
  const localUpdated = updateLocalProject(projectId, updateData)

  try {
    const res = await fetch(`${API_BASE_URL}/api/admin/projects/${encodeURIComponent(projectId)}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updateData)
    })
    if (res.ok) {
      const data = await res.json()
      if (data && data.project) {
        updateLocalProject(projectId, data.project)
      }
      return data
    }
    const errData = await res.json().catch(() => ({}))
    throw new Error(errData.detail || 'Failed to update project.')
  } catch (err) {
    console.error('Error updating project in backend:', err)
    if (err.message && (err.message.includes('Failed to fetch') || err.message.includes('NetworkError'))) {
      // Gracefully fall back to local persistence
      return {
        success: true,
        message: 'Project specifications, status, and assignment saved locally.',
        project: localUpdated
      }
    }
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
      const data = await res.json()
      if (Array.isArray(data) && data.length > 0) {
        const hasJeremy = data.some(u => u.email === 'jwlankford@gmail.com' || u.id === 'Jq4WTmNLN9XbtDqZsbIesLWCTTn1')
        if (!hasJeremy) {
          data.unshift(DEFAULT_REGISTERED_USERS[0])
        }
        return data
      }
    }
  } catch (err) {
    console.warn('Failed to fetch registered users; using fallback.')
  }
  return DEFAULT_REGISTERED_USERS
}
