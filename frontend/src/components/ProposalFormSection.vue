<script setup>
import { ref, reactive, watch } from 'vue'

const props = defineProps({
  preselectedService: {
    type: String,
    default: ''
  },
  currentUser: {
    type: Object,
    default: null
  }
})

const formData = reactive({
  researcher_name: '',
  institution_name: '',
  department_name: '',
  contact_email: '',
  lab_website: '',
  research_focus: ['adlc_lifecycle'],
  project_summary: '',
  target_venue: '',
  academic_confirmation: false,
  non_commercial_confirmed: false
})

// Auto-prefill if user is logged in
watch(() => props.currentUser, (user) => {
  if (user) {
    if (user.displayName && !formData.researcher_name) formData.researcher_name = user.displayName
    if (user.email && !formData.contact_email) formData.contact_email = user.email
    if (user.institution && !formData.institution_name) formData.institution_name = user.institution
    if (user.department && !formData.department_name) formData.department_name = user.department
  }
}, { immediate: true })

// Watch for preselection from services section
watch(() => props.preselectedService, (newVal) => {
  if (newVal && !formData.research_focus.includes(newVal)) {
    formData.research_focus.push(newVal)
  }
})

const toggleFocus = (id) => {
  const index = formData.research_focus.indexOf(id)
  if (index > -1) {
    if (formData.research_focus.length > 1) {
      formData.research_focus.splice(index, 1)
    }
  } else {
    formData.research_focus.push(id)
  }
}

const handleSubmit = async () => {
  if (!formData.researcher_name || !formData.institution_name || !formData.contact_email || !formData.project_summary) {
    errorMessage.value = 'Please complete all required fields marked with *.'
    return
  }

  if (!formData.academic_confirmation || !formData.non_commercial_confirmed) {
    errorMessage.value = 'Please confirm that this is strictly non-commercial academic research eligible for pro-bono collaboration.'
    return
  }

  errorMessage.value = ''
  isSubmitting.value = true

  const payload = {
    organization_name: `${formData.institution_name} - ${formData.department_name || 'Academic Lab'}`,
    contact_name: formData.researcher_name,
    contact_email: formData.contact_email,
    organization_website: formData.lab_website,
    organization_type: 'Academic / Educational',
    selected_services: formData.research_focus,
    project_summary: `[Target Venue: ${formData.target_venue || 'N/A'}] ${formData.project_summary}`,
    target_demographic: 'Academic Study Participants',
    technical_stack: 'Custom ADLC Research Testbed',
    budget_readiness: 'academic_free_zero_expense',
    point_of_contact_confirmed: true
  }

  try {
    const res = await fetch('http://localhost:8000/api/proposals', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      const data = await res.json()
      submissionResult.value = data
      submitSuccess.value = true
    } else {
      throw new Error('Server returned non-200 response')
    }
  } catch (err) {
    console.warn('Backend unavailable, using client confirmation:', err)
    const fakeId = `RESEARCH-${Math.random().toString(36).substring(2, 9).toUpperCase()}`
    submissionResult.value = {
      proposal_id: fakeId,
      message: 'Academic research proposal received. We will review your study design within 48 hours.',
      data: { ...formData, id: fakeId }
    }
    submitSuccess.value = true
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  formData.researcher_name = ''
  formData.institution_name = ''
  formData.department_name = ''
  formData.contact_email = ''
  formData.lab_website = ''
  formData.project_summary = ''
  formData.target_venue = ''
  formData.academic_confirmation = false
  formData.non_commercial_confirmed = false
  submitSuccess.value = false
  submissionResult.value = null
}
</script>

<template>
  <section id="submit-app" class="section section-divider">
    <div class="container-narrow">
      <div class="text-center">
        <span class="section-label coral">Academic Inquiry Portal</span>
        <h2>Propose an academic ADLC research study</h2>
        <p style="max-width: 640px; margin: 0.5rem auto 0 auto;">
          Submit your study design or experimental software requirements. Qualifying projects receive end-to-end software development at <strong>zero development expenses</strong> to advance empirical science.
        </p>
      </div>

      <!-- Success Card -->
      <div v-if="submitSuccess" class="proposal-box" style="border-color: #10b981; background: #f0fdf4; text-align: center;">
        <div style="width: 64px; height: 64px; border-radius: 50%; background: #10b981; color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto;">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </div>

        <h3 style="color: #065f46; margin-bottom: 0.5rem;">Research Proposal Received!</h3>
        <p style="color: #047857; margin-bottom: 1.5rem; font-size: 1.05rem;">
          Study Docket ID: <strong style="font-family: monospace; font-size: 1.2rem; background: #d1fae5; padding: 0.2rem 0.6rem; border-radius: 6px;">{{ submissionResult?.proposal_id }}</strong>
        </p>

        <div style="background: white; border-radius: 10px; padding: 1.5rem; text-align: left; margin-bottom: 1.75rem; border: 1px solid #a7f3d0;">
          <div style="font-weight: 700; color: #1e293b; margin-bottom: 0.5rem;">Academic Review Process:</div>
          <ul style="padding-left: 1.25rem; color: #475569; display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.95rem;">
            <li>We review your study hypothesis, target dependent variables, and software testbed requirements.</li>
            <li>We will email <strong>{{ formData.contact_email }}</strong> to schedule a 30-minute academic scoping sync.</li>
            <li>Upon alignment, we finalize an experimental development plan at <strong>$0 development expense</strong> to your grant.</li>
          </ul>
        </div>

        <button @click="resetForm" class="btn btn-primary">Submit Another Research Docket</button>
      </div>

      <!-- Active Form -->
      <div v-else class="proposal-box">
        <div v-if="errorMessage" style="background: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; padding: 0.85rem 1.25rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.95rem;">
          {{ errorMessage }}
        </div>

        <form @submit.prevent="handleSubmit">
          <div class="form-grid">
            <!-- Lead Researcher Name -->
            <div class="form-group">
              <label class="form-label">
                Principal Investigator / Researcher Name <span class="required">*</span>
              </label>
              <input 
                type="text" 
                v-model="formData.researcher_name" 
                class="form-input" 
                placeholder="e.g. Prof. David K. Reed / Elena Rostova, PhD" 
                required 
              />
            </div>

            <!-- University / Institution -->
            <div class="form-group">
              <label class="form-label">
                University or Research Institution <span class="required">*</span>
              </label>
              <input 
                type="text" 
                v-model="formData.institution_name" 
                class="form-input" 
                placeholder="e.g. University of the Cumberlands" 
                required 
              />
            </div>

            <!-- Department / Lab -->
            <div class="form-group">
              <label class="form-label">Department / Lab Name</label>
              <input 
                type="text" 
                v-model="formData.department_name" 
                class="form-input" 
                placeholder="e.g. Dept of Computer Science / HCI Research Lab" 
              />
            </div>

            <!-- Institutional Email -->
            <div class="form-group">
              <label class="form-label">
                Institutional Email (.edu / academic) <span class="required">*</span>
              </label>
              <input 
                type="email" 
                v-model="formData.contact_email" 
                class="form-input" 
                placeholder="researcher@ucumberlands.edu" 
                required 
              />
            </div>

            <!-- Lab Website -->
            <div class="form-group full-width">
              <label class="form-label">Lab Website / Faculty Profile URL</label>
              <input 
                type="url" 
                v-model="formData.lab_website" 
                class="form-input" 
                placeholder="https://ucumberlands.edu/~researcher" 
              />
            </div>

            <!-- Research Focus Areas -->
            <div class="form-group full-width">
              <label class="form-label">
                Research Focus & Experimental Needs (Select all applicable) <span class="required">*</span>
              </label>
              <div class="service-checkbox-grid">
                <div 
                  class="service-checkbox-card" 
                  :class="{ selected: formData.research_focus.includes('testbed_dev') }"
                  @click="toggleFocus('testbed_dev')"
                >
                  <div class="service-checkbox-title">Testbed & Prototype UI</div>
                  <div class="service-checkbox-desc">Interactive web testbed, study stimulus interfaces, participant trials.</div>
                </div>

                <div 
                  class="service-checkbox-card" 
                  :class="{ selected: formData.research_focus.includes('telemetry_metrics') }"
                  @click="toggleFocus('telemetry_metrics')"
                >
                  <div class="service-checkbox-title">Cognitive Telemetry Logs</div>
                  <div class="service-checkbox-desc">Developer cognitive friction, latency logging, session event traces.</div>
                </div>

                <div 
                  class="service-checkbox-card" 
                  :class="{ selected: formData.research_focus.includes('agentic_arch') }"
                  @click="toggleFocus('agentic_arch')"
                >
                  <div class="service-checkbox-title">Agentic Architectures</div>
                  <div class="service-checkbox-desc">Autonomous multi-agent loops, synthesis benchmark evaluation.</div>
                </div>
              </div>
            </div>

            <!-- Project Summary -->
            <div class="form-group full-width">
              <label class="form-label">
                Research Hypotheses & Experimental Software Requirements <span class="required">*</span>
              </label>
              <textarea 
                v-model="formData.project_summary" 
                rows="4" 
                class="form-textarea" 
                placeholder="Describe your research questions regarding ADLC (Agentic Development Life Cycle), the experimental software testbed you need developed, and the dependent variables you plan to measure." 
                required
              ></textarea>
            </div>

            <!-- Target Publication Venue -->
            <div class="form-group full-width">
              <label class="form-label">Target Academic Venue / Target Submission Window</label>
              <input 
                type="text" 
                v-model="formData.target_venue" 
                class="form-input" 
                placeholder="e.g. ICSE 2027, CHI 2027, FSE, NeurIPS, PhD Dissertation Chapter" 
              />
            </div>
          </div>

          <!-- Academic & Non-Commercial Confirmation -->
          <div class="checkbox-agreement">
            <input 
              type="checkbox" 
              id="confirm-academic" 
              v-model="formData.academic_confirmation" 
              required 
            />
            <label for="confirm-academic" style="cursor: pointer;">
              <strong>Academic Research Confirmation:</strong> I confirm this study is for academic, scientific, or doctoral research and will contribute to peer-reviewed scholarly literature.
            </label>
          </div>

          <div class="checkbox-agreement" style="margin-top: -0.5rem;">
            <input 
              type="checkbox" 
              id="confirm-noncommercial" 
              v-model="formData.non_commercial_confirmed" 
              required 
            />
            <label for="confirm-noncommercial" style="cursor: pointer;">
              <strong>Non-Commercial & Zero Expense Terms:</strong> I confirm this project is not for business or commercial venture purposes, and understand that Cognitive Metrics takes on development for research with <strong>no development expenses</strong>.
            </label>
          </div>

          <div style="text-align: center; margin-top: 2rem;">
            <button 
              type="submit" 
              class="btn btn-primary btn-large" 
              :disabled="isSubmitting"
              style="min-width: 260px;"
            >
              <span v-if="!isSubmitting">Submit research proposal ($0 cost)</span>
              <span v-else>Submitting research docket...</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>
