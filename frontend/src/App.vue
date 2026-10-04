<script setup>
import { ref } from 'vue'
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

const preselectedService = ref('')

const onSelectService = (serviceId) => {
  preselectedService.value = serviceId
}
</script>

<template>
  <div class="app-layout">
    <!-- Sticky Nav -->
    <Navbar />

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
      <ProposalFormSection :preselected-service="preselectedService" />

      <!-- Signature Dual-Column FAQs with Pink Plus/Minus Toggles -->
      <FaqSection />

      <!-- Guides & Resources Publication -->
      <ResourceGuideSection />
    </main>

    <!-- Comprehensive Nonprofit Footer -->
    <FooterSection />
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
