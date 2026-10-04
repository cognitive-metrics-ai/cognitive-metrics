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

// Auth & Modals
import AuthModal from './components/AuthModal.vue'
import ApprovedProjectsModal from './components/ApprovedProjectsModal.vue'
import PreferencesModal from './components/PreferencesModal.vue'
import { subscribeToAuthChanges, saveLocalUser } from './services/firebase'

const currentUser = ref(null)
const preselectedService = ref('')

const showAuthModal = ref(false)
const showApprovedProjectsModal = ref(false)
const showPreferencesModal = ref(false)

let unsubscribeAuth = null

onMounted(() => {
  unsubscribeAuth = subscribeToAuthChanges((user) => {
    currentUser.value = user
  })
})

onUnmounted(() => {
  if (unsubscribeAuth) unsubscribeAuth()
})

const onSelectService = (serviceId) => {
  preselectedService.value = serviceId
}

const handleAuthSuccess = (user) => {
  currentUser.value = user
  showAuthModal.value = false
}

const handleLoggedOut = () => {
  currentUser.value = null
}

const handlePreferencesSaved = (updatedUser) => {
  currentUser.value = updatedUser
  saveLocalUser(updatedUser)
}

const scrollToProposal = () => {
  const el = document.getElementById('submit-app')
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <div class="app-layout">
    <!-- Sticky Nav with User Account Menu -->
    <Navbar 
      :current-user="currentUser"
      @open-auth="showAuthModal = true"
      @open-approved-projects="showApprovedProjectsModal = true"
      @open-preferences="showPreferencesModal = true"
      @submit-proposal="scrollToProposal"
      @logged-out="handleLoggedOut"
    />

    <!-- Main Page Sections -->
    <main>
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
    </main>

    <!-- Comprehensive Nonprofit Footer -->
    <FooterSection />

    <!-- Modals -->
    <AuthModal 
      v-if="showAuthModal" 
      @close="showAuthModal = false" 
      @auth-success="handleAuthSuccess" 
    />

    <ApprovedProjectsModal 
      v-if="showApprovedProjectsModal" 
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
