<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import UserMenu from './UserMenu.vue'
import { logoutUser } from '../services/firebase'

const props = defineProps({
  currentUser: {
    type: Object,
    default: null
  }
})

const emit = defineEmits([
  'open-auth',
  'submit-proposal',
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
  } else if (action === 'approved-projects') {
    emit('open-approved-projects')
  } else if (action === 'preferences') {
    emit('open-preferences')
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
  <header class="navbar" :style="{ boxShadow: isScrolled ? '0 4px 20px rgba(0, 0, 0, 0.06)' : 'none' }">
    <div class="container nav-container">
      <!-- Brand Logo -->
      <a href="#" class="brand-link">
        <div class="brand-logo-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"/>
            <path d="M12 6v6l4 2"/>
            <circle cx="12" cy="12" r="3" fill="currentColor"/>
          </svg>
        </div>
        <div style="display: flex; flex-direction: column; line-height: 1.15;">
          <span>Cognitive Metrics</span>
          <span style="font-size: 0.6875rem; font-weight: 700; color: #f52c68; letter-spacing: 0.08em; text-transform: uppercase;">
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
          @open-approved-projects="emit('open-approved-projects')"
          @open-preferences="emit('open-preferences')"
          @logged-out="emit('logged-out')"
        />

        <!-- If Logged Out: Sign In Button -->
        <button 
          v-else 
          @click="emit('open-auth')" 
          class="btn btn-secondary" 
          style="font-size: 0.875rem; padding: 0.55rem 1.25rem;"
        >
          Sign In
        </button>
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
      <div v-if="currentUser" style="padding: 0.75rem 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 0.5rem;">
        <div style="font-weight: 700; color: #0e1b2f;">{{ currentUser.displayName || 'Academic Researcher' }}</div>
        <div style="font-size: 0.8rem; color: #64748b;">{{ currentUser.email }}</div>
      </div>

      <a href="#how-it-works" class="nav-link" @click="closeMobileMenu">How it works</a>
      <a href="#our-work" class="nav-link" @click="closeMobileMenu">ADLC Studies</a>
      <a href="#client-services" class="nav-link" @click="closeMobileMenu">Free services</a>
      <a href="#batch-timeline" class="nav-link" @click="closeMobileMenu">Research cycle</a>
      <a href="#faqs" class="nav-link" @click="closeMobileMenu">FAQs</a>

      <!-- Logged In Mobile Actions -->
      <template v-if="currentUser">
        <div style="height: 1px; background: #e2e8f0; margin: 0.5rem 0;"></div>
        <a href="#submit-app" class="nav-link" @click="handleMobileAction('submit-proposal')">📝 Submit proposal</a>
        <button class="nav-link" style="background: none; border: none; text-align: left; cursor: pointer; width: 100%;" @click="handleMobileAction('approved-projects')">
          🔬 Approved projects
        </button>
        <button class="nav-link" style="background: none; border: none; text-align: left; cursor: pointer; width: 100%;" @click="handleMobileAction('preferences')">
          ⚙️ Preferences
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
