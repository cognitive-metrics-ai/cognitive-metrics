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
        <span>Cognitive Metrics</span>
      </a>

      <!-- Desktop Navigation Menu -->
      <nav class="nav-menu">
        <a href="#how-it-works" class="nav-link">How it works</a>
        <a href="#our-work" class="nav-link">Our work</a>
        <a href="#client-services" class="nav-link">Services</a>
        <a href="#batch-timeline" class="nav-link">Timeline</a>
        <a href="#faqs" class="nav-link">FAQs</a>
      </nav>

      <!-- Desktop CTA Group -->
      <div class="nav-cta-group">
        <a href="#submit-app" class="btn btn-primary">Submit a proposal</a>
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
      <a href="#how-it-works" class="nav-link" @click="closeMobileMenu">How it works</a>
      <a href="#our-work" class="nav-link" @click="closeMobileMenu">Our work</a>
      <a href="#client-services" class="nav-link" @click="closeMobileMenu">Services</a>
      <a href="#batch-timeline" class="nav-link" @click="closeMobileMenu">Timeline</a>
      <a href="#faqs" class="nav-link" @click="closeMobileMenu">FAQs</a>
      <div style="padding-top: 0.5rem;">
        <a href="#submit-app" class="btn btn-primary" style="width: 100%; text-align: center;" @click="closeMobileMenu">Submit a proposal</a>
      </div>
    </div>
  </header>
</template>
