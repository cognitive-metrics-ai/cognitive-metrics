<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

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
        <a href="#lead-researcher" class="nav-link">Jeremy Lankford</a>
        <a href="#how-it-works" class="nav-link">How it works</a>
        <a href="#our-work" class="nav-link">ADLC Studies</a>
        <a href="#client-services" class="nav-link">Free services</a>
        <a href="#batch-timeline" class="nav-link">Research cycle</a>
        <a href="#faqs" class="nav-link">FAQs</a>
        <a href="http://jeremylankford.com" target="_blank" rel="noopener noreferrer" class="nav-link" style="color: #f52c68; font-weight: 600;">
          jeremylankford.com ↗
        </a>
      </nav>

      <!-- Desktop CTA Group -->
      <div class="nav-cta-group">
        <a href="#submit-app" class="btn btn-primary">Submit research proposal</a>
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
      <a href="#lead-researcher" class="nav-link" @click="closeMobileMenu">Jeremy Lankford</a>
      <a href="http://jeremylankford.com" target="_blank" rel="noopener noreferrer" class="nav-link" style="color: #f52c68; font-weight: 600;" @click="closeMobileMenu">jeremylankford.com ↗</a>
      <a href="#how-it-works" class="nav-link" @click="closeMobileMenu">How it works</a>
      <a href="#our-work" class="nav-link" @click="closeMobileMenu">ADLC Studies</a>
      <a href="#client-services" class="nav-link" @click="closeMobileMenu">Free services</a>
      <a href="#batch-timeline" class="nav-link" @click="closeMobileMenu">Research cycle</a>
      <a href="#faqs" class="nav-link" @click="closeMobileMenu">FAQs</a>
      <div style="padding-top: 0.5rem;">
        <a href="#submit-app" class="btn btn-primary" style="width: 100%; text-align: center;" @click="closeMobileMenu">Submit research proposal</a>
      </div>
    </div>
  </header>
</template>
