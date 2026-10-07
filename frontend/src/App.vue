<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Navbar from './components/Navbar.vue'
import HeroSection from './components/HeroSection.vue'
import ResearcherProfileSection from './components/ResearcherProfileSection.vue'
import HowItWorksSection from './components/HowItWorksSection.vue'
import OurWorkSection from './components/OurWorkSection.vue'
import SocialProofSection from './components/SocialProofSection.vue'
import ServicesSection from './components/ServicesSection.vue'
import TimelineSection from './components/TimelineSection.vue'
import ProposalFormSection from './components/ProposalFormSection.vue'
import FaqSection from './components/FaqSection.vue'
import ResourceGuideSection from './components/ResourceGuideSection.vue'
import FooterSection from './components/FooterSection.vue'

// Full-Page Components
import MyProjectsPage from './components/MyProjectsPage.vue'
import AdminConsolePage from './components/AdminConsolePage.vue'

// Auth & Modals
import AuthModal from './components/AuthModal.vue'
import ApprovedProjectsModal from './components/ApprovedProjectsModal.vue'
import PreferencesModal from './components/PreferencesModal.vue'
import { subscribeToAuthChanges, saveLocalUser } from './services/firebase'
import { syncUserWithBackend } from './services/projects'

const currentUser = ref(null)
const preselectedService = ref('')

const resolveCurrentPage = () => {
  const hash = window.location.hash || ''
  if (hash.startsWith('#admin-console')) return 'admin-console'
  if (hash.startsWith('#my-projects')) return 'my-projects'
  return 'home'
}

const currentPage = ref(resolveCurrentPage())

const showAuthModal = ref(false)
const showApprovedProjectsModal = ref(false)
const showPreferencesModal = ref(false)

let unsubscribeAuth = null

const handleHashChange = () => {
  currentPage.value = resolveCurrentPage()
}

onMounted(() => {
  window.addEventListener('hashchange', handleHashChange)
  unsubscribeAuth = subscribeToAuthChanges((user) => {
    currentUser.value = user
    if (user) {
      syncUserWithBackend(user)
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('hashchange', handleHashChange)
  if (unsubscribeAuth) unsubscribeAuth()
})

const navigateToMyProjects = () => {
  currentPage.value = 'my-projects'
  window.location.hash = '#my-projects'
}

const navigateToAdminConsole = () => {
  currentPage.value = 'admin-console'
  window.location.hash = '#admin-console'
}

const navigateToHome = () => {
  currentPage.value = 'home'
  if (window.location.hash.startsWith('#my-projects') || window.location.hash.startsWith('#admin-console')) {
    window.location.hash = ''
  }
}

const onSelectService = (serviceId) => {
  preselectedService.value = serviceId
}

const handleAuthSuccess = (user) => {
  currentUser.value = user
  showAuthModal.value = false
}

const handleLoggedOut = () => {
  currentUser.value = null
  navigateToHome()
}

const handlePreferencesSaved = (updatedUser) => {
  currentUser.value = updatedUser
  saveLocalUser(updatedUser)
}

const scrollToProposal = () => {
  navigateToHome()
  setTimeout(() => {
    const el = document.getElementById('submit-app')
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  }, 100)
}
</script>

<template>
  <div class="app-layout">
    <!-- Sticky Nav with User Account Menu -->
    <Navbar 
      :current-user="currentUser"
      @go-home="navigateToHome"
      @open-auth="showAuthModal = true"
      @open-my-projects="navigateToMyProjects"
      @open-admin-console="navigateToAdminConsole"
      @open-approved-projects="showApprovedProjectsModal = true"
      @open-preferences="showPreferencesModal = true"
      @submit-proposal="scrollToProposal"
      @logged-out="handleLoggedOut"
    />

    <!-- Main Page Content -->
    <main>
      <!-- Dedicated Full-Page View for Lead Architect Console -->
      <AdminConsolePage 
        v-if="currentPage === 'admin-console'"
        :user="currentUser"
        @go-home="navigateToHome"
        @open-my-projects="navigateToMyProjects"
      />

      <!-- Dedicated Full-Page View for My Projects -->
      <MyProjectsPage 
        v-else-if="currentPage === 'my-projects'"
        :user="currentUser"
        @go-home="navigateToHome"
        @submit-proposal="scrollToProposal"
      />

      <!-- Default Home Page Landing View -->
      <template v-else>
        <!-- Hero with Interactive Metric Engine -->
        <HeroSection />

        <!-- Lead Researcher & Architect Profile (Jeremy Lankford) -->
        <ResearcherProfileSection />

        <!-- How Academic Research Collaboration Works (3-step) -->
        <HowItWorksSection />

        <!-- Case Studies & Work with Modals -->
        <OurWorkSection />

        <!-- WHO Testimonial, University Logos & Success Criteria -->
        <SocialProofSection />

        <!-- Menu of Services with $1,000 Flat Fee Notice -->
        <ServicesSection @select-service="onSelectService" />

        <!-- Batch Schedule & Milestones -->
        <TimelineSection />

        <!-- The Core Proposal Application Form (#submit-app) -->
        <ProposalFormSection 
          :preselected-service="preselectedService" 
          :current-user="currentUser" 
        />

        <!-- Signature Dual-Column FAQs with Pink Plus/Minus Toggles -->
        <FaqSection />

        <!-- Guides & Resources Publication -->
        <ResourceGuideSection />
      </template>
    </main>

    <!-- Comprehensive Nonprofit Footer -->
    <FooterSection @open-approved-projects="showApprovedProjectsModal = true" />

    <!-- Modals -->
    <AuthModal 
      v-if="showAuthModal" 
      @close="showAuthModal = false" 
      @auth-success="handleAuthSuccess" 
    />

    <ApprovedProjectsModal 
      v-if="showApprovedProjectsModal" 
      :user="currentUser"
      @close="showApprovedProjectsModal = false" 
      @open-proposal="scrollToProposal" 
    />

    <PreferencesModal 
      v-if="showPreferencesModal" 
      :user="currentUser" 
      @close="showPreferencesModal = false" 
      @saved="handlePreferencesSaved" 
    />
  </div>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex-grow: 1;
}
</style>
