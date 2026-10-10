<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import UserMenu from './UserMenu.vue'
import BrandLogo from './BrandLogo.vue'
import { logoutUser } from '../services/firebase'
import { currentTheme, toggleTheme } from '../services/theme'

const props = defineProps({
  currentUser: {
    type: Object,
    default: null
  }
})

const emit = defineEmits([
  'go-home',
  'open-auth',
  'submit-proposal',
  'open-my-projects',
  'open-admin-console',
  'open-approved-projects',
  'open-preferences',
  'logged-out'
])

const isScrolled = ref(false)
const mobileMenuOpen = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const handleMobileAction = (action) => {
  closeMobileMenu()
  if (action === 'auth') {
    emit('open-auth')
  } else if (action === 'submit-proposal') {
    emit('submit-proposal')
    const el = document.getElementById('submit-app')
    if (el) el.scrollIntoView({ behavior: 'smooth' })
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

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <header class="navbar" :style="{ boxShadow: isScrolled ? '0 4px 20px rgba(0, 0, 0, 0.12)' : 'none' }">
    <div class="container nav-container">
      <!-- Core Brand Logo -->
      <a href="#" class="brand-link" @click.prevent="emit('go-home')" aria-label="Cognitive Metrics Home">
        <div class="brand-logo-icon">
          <BrandLogo variant="emblem" :height="38" alt="Cognitive Metrics Emblem" />
        </div>
        <div style="display: flex; flex-direction: column; line-height: 1.15;">
          <span>Cognitive Metrics</span>
          <span style="font-size: 0.6875rem; font-weight: 700; color: var(--color-primary); letter-spacing: 0.08em; text-transform: uppercase;">
            Academic ADLC Research
          </span>
        </div>
      </a>

      <!-- Desktop Navigation Menu -->
      <nav class="nav-menu">
        <a href="#how-it-works" class="nav-link">How it works</a>
        <a href="#our-work" class="nav-link">ADLC Studies</a>
        <a href="#client-services" class="nav-link">Free services</a>
        <a href="#batch-timeline" class="nav-link">Research cycle</a>
        <a href="#faqs" class="nav-link">FAQs</a>
      </nav>

      <!-- Desktop CTA & User Account Group -->
      <div class="nav-cta-group">
        <a href="#submit-app" class="btn btn-primary">Submit proposal</a>

        <!-- If User Logged In: Avatar with User Menu -->
        <UserMenu 
          v-if="currentUser" 
          :user="currentUser" 
          @submit-proposal="emit('submit-proposal')"
          @open-my-projects="emit('open-my-projects')"
          @open-admin-console="emit('open-admin-console')"
          @open-approved-projects="emit('open-approved-projects')"
          @open-preferences="emit('open-preferences')"
          @logged-out="emit('logged-out')"
        />

        <!-- If Logged Out: Preferences & Sign In Buttons -->
        <div v-else style="display: flex; align-items: center; gap: 0.5rem;">
          <button 
            @click="emit('open-preferences')" 
            class="btn btn-secondary" 
            style="font-size: 0.875rem; padding: 0.55rem 0.9rem;"
            title="Researcher Settings & Preferences"
            aria-label="Researcher Settings & Preferences"
          >
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
          </button>
          <button 
            @click="emit('open-auth')" 
            class="btn btn-secondary" 
            style="font-size: 0.875rem; padding: 0.55rem 1.25rem;"
          >
            Sign In
          </button>
        </div>
      </div>

      <!-- Mobile Hamburger Button -->
      <button class="mobile-menu-btn" @click="toggleMobileMenu" aria-label="Toggle navigation menu">
        <svg v-if="!mobileMenuOpen" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg v-else width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <!-- Mobile Drawer -->
    <div v-if="mobileMenuOpen" class="mobile-nav-drawer">
      <!-- User Profile Header in Mobile Drawer -->
      <div v-if="currentUser" style="padding: 0.75rem 0; border-bottom: 1px solid var(--color-border); margin-bottom: 0.5rem;">
        <div style="font-weight: 700; color: var(--color-navy);">{{ currentUser.displayName || 'Academic Researcher' }}</div>
        <div style="font-size: 0.8rem; color: var(--color-text-muted);">{{ currentUser.email }}</div>
      </div>

      <!-- Quick Theme Switcher in Mobile Drawer -->
      <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.65rem 0; border-bottom: 1px solid var(--color-border);">
        <span style="font-size: 0.9rem; font-weight: 600; color: var(--color-navy);">Theme</span>
        <button 
          @click="handleMobileAction('theme')" 
          class="theme-toggle-nav-btn" 
          style="display: inline-flex;"
          :aria-label="currentTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
        >
          <span style="font-size: 0.8rem; margin-right: 0.4rem; font-weight: 600; color: var(--color-text-main);">
            {{ currentTheme === 'dark' ? 'Dark' : 'Light' }}
          </span>
          <svg v-if="currentTheme === 'dark'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        </button>
      </div>

      <a href="#how-it-works" class="nav-link" @click="closeMobileMenu">How it works</a>
      <a href="#our-work" class="nav-link" @click="closeMobileMenu">ADLC Studies</a>
      <a href="#client-services" class="nav-link" @click="closeMobileMenu">Free services</a>
      <a href="#batch-timeline" class="nav-link" @click="closeMobileMenu">Research cycle</a>
      <a href="#faqs" class="nav-link" @click="closeMobileMenu">FAQs</a>

      <!-- Quick Preferences Button (Always Available) -->
      <button class="nav-link" style="background: none; border: none; text-align: left; cursor: pointer; width: 100%; display: flex; align-items: center; gap: 0.5rem;" @click="handleMobileAction('preferences')">
        ⚙️ Preferences & Theme
      </button>

      <!-- Logged In Mobile Actions -->
      <template v-if="currentUser">
        <div style="height: 1px; background: var(--color-border); margin: 0.5rem 0;"></div>
        <button class="nav-link" style="background: none; border: none; text-align: left; cursor: pointer; width: 100%; font-weight: 600;" @click="handleMobileAction('my-projects')">
          📂 My Projects
        </button>
        <button class="nav-link" style="background: none; border: none; text-align: left; cursor: pointer; width: 100%; font-weight: 700; color: #8b5cf6;" @click="handleMobileAction('admin-console')">
          ⚡ Lead Architect Console
        </button>
        <button class="nav-link" style="background: none; border: none; text-align: left; cursor: pointer; color: #dc2626; width: 100%;" @click="handleMobileAction('logout')">
          🚪 Logout
        </button>
      </template>

      <!-- Logged Out Mobile Actions -->
      <div v-else style="padding-top: 0.5rem; display: flex; flex-direction: column; gap: 0.5rem;">
        <button @click="handleMobileAction('auth')" class="btn btn-secondary" style="width: 100%;">Sign In / Sign Up</button>
        <a href="#submit-app" class="btn btn-primary" style="width: 100%; text-align: center;" @click="closeMobileMenu">Submit proposal</a>
      </div>
    </div>
  </header>
</template>

<style scoped>
.theme-toggle-nav-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background: var(--color-bg-white);
  color: var(--color-text-main);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-toggle-nav-btn:hover {
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-color: var(--color-primary);
  transform: rotate(15deg);
}
</style>
