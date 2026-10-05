<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { logoutUser } from '../services/firebase'
import { currentTheme, toggleTheme } from '../services/theme'

const props = defineProps({
  user: {
    type: Object,
    required: true
  }
})

const emit = defineEmits([
  'submit-proposal',
  'open-my-projects',
  'open-admin-console',
  'open-approved-projects',
  'open-preferences',
  'logged-out'
])

const menuOpen = ref(false)
const menuRef = ref(null)

const userInitials = computed(() => {
  if (!props.user) return 'AR'
  const name = props.user.displayName || props.user.email || 'Researcher'
  const parts = name.trim().split(/\s+/)
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.slice(0, 2).toUpperCase()
})

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
  menuOpen.value = false
}

const handleClickOutside = (e) => {
  if (menuRef.value && !menuRef.value.contains(e.target)) {
    closeMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const handleAction = (action) => {
  closeMenu()
  if (action === 'submit-proposal') {
    emit('submit-proposal')
    const el = document.getElementById('submit-app')
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' })
    }
  } else if (action === 'my-projects') {
    emit('open-my-projects')
  } else if (action === 'admin-console') {
    emit('open-admin-console')
  } else if (action === 'approved-projects') {
    emit('open-approved-projects')
  } else if (action === 'preferences') {
    emit('open-preferences')
  } else if (action === 'theme') {
    toggleTheme()
  } else if (action === 'logout') {
    logoutUser()
    emit('logged-out')
  }
}
</script>

<template>
  <div class="user-menu-container" ref="menuRef" style="position: relative;">
    <!-- Avatar Trigger Button -->
    <button 
      @click="toggleMenu" 
      aria-label="User account menu"
      style="display: flex; align-items: center; gap: 0.5rem; background: none; border: none; cursor: pointer; padding: 2px;"
    >
      <div style="position: relative;">
        <!-- Avatar Circle -->
        <div 
          v-if="user.photoURL" 
          style="width: 40px; height: 40px; border-radius: 50%; overflow: hidden; border: 2px solid #e2e8f0;"
        >
          <img :src="user.photoURL" alt="User avatar" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
        <div 
          v-else 
          style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #1B6CA8 0%, #4DA8DA 100%); color: #ffffff; font-weight: 700; font-size: 0.95rem; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(27, 108, 168, 0.25);"
        >
          {{ userInitials }}
        </div>

        <!-- Online Status Dot -->
        <span style="position: absolute; bottom: 0; right: 0; width: 10px; height: 10px; border-radius: 50%; background: #10b981; border: 2px solid #ffffff;"></span>
      </div>

      <!-- Down Arrow Indicator -->
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2.5" :style="{ transform: menuOpen ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s ease' }">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </button>

    <!-- Dropdown Menu -->
    <div 
      v-if="menuOpen" 
      class="user-dropdown-menu"
      style="position: absolute; top: calc(100% + 12px); right: 0; width: 260px; background: var(--color-bg-white); border-radius: 14px; box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.3), 0 5px 15px rgba(0, 0, 0, 0.1); border: 1px solid var(--color-border); overflow: hidden; z-index: 1000; animation: fadeIn 0.15s ease;"
    >
      <!-- User Info Header -->
      <div style="padding: 1.15rem 1.25rem; background: var(--color-bg-light); border-bottom: 1px solid var(--color-border);">
        <div style="font-weight: 700; color: var(--color-navy); font-size: 0.95rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
          {{ user.displayName || 'Academic Researcher' }}
        </div>
        <div style="font-size: 0.8rem; color: var(--color-text-muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin-bottom: 0.4rem;">
          {{ user.email }}
        </div>
        <span style="display: inline-block; font-size: 0.7rem; font-weight: 700; color: var(--color-primary); background: var(--color-primary-light); padding: 0.15rem 0.5rem; border-radius: 9999px;">
          Verified Researcher
        </span>
      </div>

      <!-- Menu Items List -->
      <div style="padding: 0.5rem;">
        <!-- 1. Submit proposal -->
        <button 
          @click="handleAction('submit-proposal')"
          class="dropdown-item"
        >
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
          <span>Submit proposal</span>
        </button>

        <!-- 2. My Projects -->
        <button 
          @click="handleAction('my-projects')"
          class="dropdown-item"
        >
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
            <polyline points="9 13 12 16 17 11"></polyline>
          </svg>
          <span style="font-weight: 600;">My Projects</span>
        </button>

        <!-- 3. Lead Architect Console -->
        <button 
          @click="handleAction('admin-console')"
          class="dropdown-item"
          style="background-color: rgba(139, 92, 246, 0.06);"
        >
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" stroke-width="2">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
          </svg>
          <span style="font-weight: 700; color: #8b5cf6;">Lead Architect Console</span>
        </button>

        <!-- 4. Preferences -->
        <button 
          @click="handleAction('preferences')"
          class="dropdown-item"
        >
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
          <span>Preferences</span>
        </button>

        <!-- 4. Quick Theme Toggle -->
        <button 
          @click="handleAction('theme')"
          class="dropdown-item"
        >
          <svg v-if="currentTheme === 'dark'" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
          </svg>
          <svg v-else width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
          <span style="flex-grow: 1;">Mode</span>
          <span style="font-size: 0.75rem; color: var(--color-primary); font-weight: 700; text-transform: capitalize;">
            {{ currentTheme }}
          </span>
        </button>

        <div style="height: 1px; background: var(--color-border); margin: 0.4rem 0;"></div>

        <!-- 5. Logout -->
        <button 
          @click="handleAction('logout')"
          class="dropdown-item logout"
        >
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          <span>Logout</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 0.85rem;
  border-radius: 8px;
  background: transparent;
  border: none;
  font-size: 0.875rem;
  font-weight: 500;
  color: #334155;
  cursor: pointer;
  text-align: left;
  transition: all 0.15s ease;
}

.dropdown-item:hover {
  background: #f1f5f9;
  color: var(--color-navy);
}

.dropdown-item.logout {
  color: #dc2626;
}

.dropdown-item.logout:hover {
  background: #fef2f2;
  color: #b91c1c;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
