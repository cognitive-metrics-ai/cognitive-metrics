<script setup>
import { ref, reactive } from 'vue'

const props = defineProps({
  user: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['close', 'saved'])

const saved = ref(false)

const settings = reactive({
  displayName: props.user?.displayName || 'Academic Researcher',
  email: props.user?.email || 'researcher@university.edu',
  institution: props.user?.institution || 'Stanford University',
  department: props.user?.department || 'Department of Computer Science',
  anonymizeSubjects: true,
  logMicroLatencies: true,
  autoExportTelemetry: true,
  notifyMilestones: true,
  notifyPapers: false
})

const handleSave = () => {
  saved.value = true
  emit('saved', { ...props.user, ...settings })
  setTimeout(() => {
    saved.value = false
    emit('close')
  }, 1200)
}
</script>

<template>
  <div class="modal-backdrop" @click.self="emit('close')" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(14, 27, 47, 0.75); backdrop-filter: blur(5px); z-index: 999; display: flex; align-items: center; justify-content: center; padding: 1.5rem;">
    <div class="modal-content" style="background: #ffffff; border-radius: 18px; max-width: 580px; width: 100%; max-height: 90vh; overflow-y: auto; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); padding: 2.5rem; position: relative;">
      <!-- Close Button -->
      <button @click="emit('close')" style="position: absolute; top: 1.25rem; right: 1.25rem; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #94a3b8;">
        &times;
      </button>

      <div style="margin-bottom: 2rem;">
        <span class="section-label coral">Account Settings</span>
        <h2 style="font-size: 1.75rem; margin-top: 0.25rem;">Researcher Preferences</h2>
        <p style="font-size: 0.95rem; color: #64748b; margin-top: 0.35rem;">
          Configure your academic affiliation, telemetry logging schema, and notification preferences.
        </p>
      </div>

      <div v-if="saved" style="background: #f0fdf4; border: 1px solid #bbf7d0; color: #15803d; padding: 0.85rem 1.25rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.95rem; font-weight: 600; text-align: center;">
        ✓ Preferences saved successfully!
      </div>

      <form @submit.prevent="handleSave">
        <!-- Profile Info -->
        <div style="margin-bottom: 1.5rem;">
          <h4 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--color-navy); border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem;">
            Academic Identity
          </h4>

          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Full Name & Title</label>
              <input type="text" v-model="settings.displayName" class="form-input" required />
            </div>

            <div class="form-group">
              <label class="form-label">Institutional Email</label>
              <input type="email" v-model="settings.email" class="form-input" disabled style="background: #f8fafc; color: #64748b;" />
            </div>

            <div class="form-group">
              <label class="form-label">University / Institution</label>
              <input type="text" v-model="settings.institution" class="form-input" />
            </div>

            <div class="form-group">
              <label class="form-label">Department / Lab</label>
              <input type="text" v-model="settings.department" class="form-input" />
            </div>
          </div>
        </div>

        <!-- Telemetry & Privacy -->
        <div style="margin-bottom: 1.5rem;">
          <h4 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--color-navy); border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem;">
            ADLC Telemetry & IRB Privacy Defaults
          </h4>

          <div style="display: flex; flex-direction: column; gap: 0.85rem; font-size: 0.9rem;">
            <label style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer;">
              <input type="checkbox" v-model="settings.anonymizeSubjects" style="width: 18px; height: 18px; accent-color: var(--color-primary);" />
              <span>Automatically anonymize and hash human participant IDs in telemetry logs</span>
            </label>

            <label style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer;">
              <input type="checkbox" v-model="settings.logMicroLatencies" style="width: 18px; height: 18px; accent-color: var(--color-primary);" />
              <span>Record millisecond-level cognitive pauses & prompt-edit latencies</span>
            </label>

            <label style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer;">
              <input type="checkbox" v-model="settings.autoExportTelemetry" style="width: 18px; height: 18px; accent-color: var(--color-primary);" />
              <span>Auto-generate JSONL and Parquet exports upon study trial completion</span>
            </label>
          </div>
        </div>

        <!-- Notifications -->
        <div style="margin-bottom: 2rem;">
          <h4 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--color-navy); border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem;">
            Notifications
          </h4>

          <div style="display: flex; flex-direction: column; gap: 0.85rem; font-size: 0.9rem;">
            <label style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer;">
              <input type="checkbox" v-model="settings.notifyMilestones" style="width: 18px; height: 18px; accent-color: var(--color-primary);" />
              <span>Email notifications when testbed milestones or PRD reviews complete</span>
            </label>

            <label style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer;">
              <input type="checkbox" v-model="settings.notifyPapers" style="width: 18px; height: 18px; accent-color: var(--color-primary);" />
              <span>Receive pre-print announcements and new open-source ADLC benchmark releases</span>
            </label>
          </div>
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 1rem; border-top: 1px solid #e2e8f0; padding-top: 1.25rem;">
          <button type="button" @click="emit('close')" class="btn btn-secondary">Cancel</button>
          <button type="submit" class="btn btn-primary">Save Preferences</button>
        </div>
      </form>
    </div>
  </div>
</template>
