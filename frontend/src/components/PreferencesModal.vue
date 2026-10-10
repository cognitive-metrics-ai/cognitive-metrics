<script setup>
import { ref, reactive, onMounted } from 'vue'
import { currentTheme, setTheme } from '../services/theme'
import BrandLogo from './BrandLogo.vue'

const props = defineProps({
  user: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['close', 'saved', 'open-auth'])

const handleSignInClick = () => {
  emit('close')
  emit('open-auth')
}

const saved = ref(false)

const settings = reactive({
  displayName: props.user?.displayName || 'Academic Researcher',
  email: props.user?.email || 'researcher@university.edu',
  institution: props.user?.institution || 'University of the Cumberlands',
  department: props.user?.department || 'Department of Computer Science',
  theme: props.user?.theme || currentTheme.value || 'light',
  anonymizeSubjects: true,
  logMicroLatencies: true,
  autoExportTelemetry: true,
  notifyMilestones: true,
  notifyPapers: false
})

onMounted(() => {
  if (props.user?.theme) {
    settings.theme = props.user.theme
  } else {
    settings.theme = currentTheme.value
  }
})

const selectTheme = (newTheme) => {
  settings.theme = newTheme
  setTheme(newTheme)
}

const handleSave = () => {
  setTheme(settings.theme)
  saved.value = true
  emit('saved', { ...props.user, ...settings })
  setTimeout(() => {
    saved.value = false
    emit('close')
  }, 1200)
}
</script>

<template>
  <Teleport to="body">
    <div class="modal-backdrop" @click.self="emit('close')">
      <div class="modal-content" style="max-width: 600px;">
        <!-- Close Button -->
        <button @click="emit('close')" style="position: absolute; top: 1.25rem; right: 1.25rem; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--color-text-muted);" aria-label="Close preferences">
          &times;
        </button>

      <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
        <BrandLogo variant="icon" :height="48" alt="Cognitive Metrics Logo" style="border-radius: 12px; box-shadow: var(--shadow-md);" />
        <div>
          <span class="section-label coral">Account & System Settings</span>
          <h2 style="font-size: 1.65rem; margin-top: 0.15rem; color: var(--color-navy);">Researcher Preferences</h2>
          <p style="font-size: 0.9rem; color: var(--color-text-muted); margin-top: 0.2rem;">
            Configure interface appearance, academic identity, and ADLC telemetry schema.
          </p>
        </div>
      </div>

      <div v-if="saved" style="background: rgba(16, 185, 129, 0.12); border: 1px solid var(--color-accent-green); color: var(--color-accent-green); padding: 0.85rem 1.25rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.95rem; font-weight: 600; text-align: center;">
        ✓ Preferences saved successfully!
      </div>

      <form @submit.prevent="handleSave">
        <!-- Appearance & Theme Selector -->
        <div style="margin-bottom: 2rem;">
          <h4 style="font-size: 1.05rem; margin-bottom: 0.75rem; color: var(--color-navy); border-bottom: 1px solid var(--color-border); padding-bottom: 0.5rem; display: flex; align-items: center; justify-content: space-between;">
            <span>Interface Appearance</span>
            <span style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--color-primary); letter-spacing: 0.05em;">
              Current: {{ settings.theme === 'dark' ? 'Dark Mode' : 'Light Mode' }}
            </span>
          </h4>
          
          <p style="font-size: 0.85rem; color: var(--color-text-muted); margin-bottom: 1rem;">
            Toggle between light and dark display modes for telemetry dashboards and data logs.
          </p>

          <div class="theme-toggle-grid">
            <!-- Light Mode Option -->
            <button 
              type="button" 
              class="theme-card-btn" 
              :class="{ active: settings.theme === 'light' }"
              @click="selectTheme('light')"
            >
              <div class="theme-icon-circle light">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
              </div>
              <div class="theme-card-info">
                <div class="theme-card-title">Light Mode</div>
                <div class="theme-card-desc">Day reading & high contrast</div>
              </div>
              <span v-if="settings.theme === 'light'" class="theme-pill active">Active</span>
            </button>

            <!-- Dark Mode Option -->
            <button 
              type="button" 
              class="theme-card-btn" 
              :class="{ active: settings.theme === 'dark' }"
              @click="selectTheme('dark')"
            >
              <div class="theme-icon-circle dark">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
              </div>
              <div class="theme-card-info">
                <div class="theme-card-title">Dark Mode</div>
                <div class="theme-card-desc">Low-light laboratory telemetry</div>
              </div>
              <span v-if="settings.theme === 'dark'" class="theme-pill active">Active</span>
            </button>
          </div>
        </div>

        <!-- Academic Identity -->
        <div style="margin-bottom: 1.75rem;">
          <h4 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--color-navy); border-bottom: 1px solid var(--color-border); padding-bottom: 0.5rem; display: flex; align-items: center; justify-content: space-between;">
            <span>Academic Identity</span>
            <span v-if="props.user?.uid" style="font-size: 0.75rem; color: var(--color-accent-green); font-weight: 700;">
              ✓ Signed In
            </span>
            <span v-else style="font-size: 0.75rem; color: var(--color-primary); font-weight: 700;">
              Guest Session
            </span>
          </h4>

          <!-- Account Sign-In Callout if Logged Out -->
          <div v-if="!props.user?.uid" style="background: var(--color-primary-light); border: 1px solid rgba(27, 108, 168, 0.25); border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
            <div>
              <div style="font-weight: 700; color: var(--color-navy); font-size: 0.95rem; margin-bottom: 0.2rem;">
                Sign In to Researcher Account
              </div>
              <div style="font-size: 0.85rem; color: var(--color-text-muted);">
                Sign in to link research proposals, custom telemetry schemas, and approved testbeds to your institutional email.
              </div>
            </div>
            <button 
              type="button" 
              class="btn btn-primary" 
              style="font-size: 0.875rem; padding: 0.55rem 1.15rem; white-space: nowrap;"
              @click="handleSignInClick"
            >
              Sign In Now
            </button>
          </div>

          <!-- Authenticated Account Details -->
          <div v-else style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 10px; padding: 0.65rem 1rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between; font-size: 0.85rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--color-accent-green);"></span>
              <span style="font-weight: 700; color: var(--color-navy);">Signed In Account:</span>
              <span style="color: var(--color-primary); font-weight: 600;">{{ props.user.email }}</span>
            </div>
            <span style="font-size: 0.75rem; font-weight: 700; color: var(--color-accent-green); background: rgba(16, 185, 129, 0.15); padding: 0.15rem 0.55rem; border-radius: 9999px;">
              Active
            </span>
          </div>

          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Full Name & Title</label>
              <input type="text" v-model="settings.displayName" class="form-input" required />
            </div>

            <div class="form-group">
              <label class="form-label">Institutional Email</label>
              <input type="email" v-model="settings.email" class="form-input" disabled style="background: var(--color-bg-light); color: var(--color-text-muted);" />
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
        <div style="margin-bottom: 1.75rem;">
          <h4 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--color-navy); border-bottom: 1px solid var(--color-border); padding-bottom: 0.5rem;">
            ADLC Telemetry & IRB Privacy Defaults
          </h4>

          <div style="display: flex; flex-direction: column; gap: 0.85rem; font-size: 0.9rem;">
            <label style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer; color: var(--color-text-main);">
              <input type="checkbox" v-model="settings.anonymizeSubjects" style="width: 18px; height: 18px; accent-color: var(--color-primary);" />
              <span>Automatically anonymize and hash human participant IDs in telemetry logs</span>
            </label>

            <label style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer; color: var(--color-text-main);">
              <input type="checkbox" v-model="settings.logMicroLatencies" style="width: 18px; height: 18px; accent-color: var(--color-primary);" />
              <span>Record millisecond-level cognitive pauses & prompt-edit latencies</span>
            </label>

            <label style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer; color: var(--color-text-main);">
              <input type="checkbox" v-model="settings.autoExportTelemetry" style="width: 18px; height: 18px; accent-color: var(--color-primary);" />
              <span>Auto-generate JSONL and Parquet exports upon study trial completion</span>
            </label>
          </div>
        </div>

        <!-- Notifications -->
        <div style="margin-bottom: 2rem;">
          <h4 style="font-size: 1.05rem; margin-bottom: 1rem; color: var(--color-navy); border-bottom: 1px solid var(--color-border); padding-bottom: 0.5rem;">
            Notifications
          </h4>

          <div style="display: flex; flex-direction: column; gap: 0.85rem; font-size: 0.9rem;">
            <label style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer; color: var(--color-text-main);">
              <input type="checkbox" v-model="settings.notifyMilestones" style="width: 18px; height: 18px; accent-color: var(--color-primary);" />
              <span>Email notifications when testbed milestones or PRD reviews complete</span>
            </label>

            <label style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer; color: var(--color-text-main);">
              <input type="checkbox" v-model="settings.notifyPapers" style="width: 18px; height: 18px; accent-color: var(--color-primary);" />
              <span>Receive pre-print announcements and new open-source ADLC benchmark releases</span>
            </label>
          </div>
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 1rem; border-top: 1px solid var(--color-border); padding-top: 1.25rem;">
          <button type="button" @click="emit('close')" class="btn btn-secondary">Cancel</button>
          <button type="submit" class="btn btn-primary">Save Preferences</button>
        </div>
      </form>
    </div>
  </div>
  </Teleport>
</template>

<style scoped>
.theme-toggle-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.theme-card-btn {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 1rem;
  border-radius: var(--radius-md);
  border: 2px solid var(--color-border);
  background: var(--color-bg-white);
  cursor: pointer;
  text-align: left;
  transition: all 0.2s ease;
  position: relative;
  color: var(--color-text-main);
}

.theme-card-btn:hover {
  border-color: var(--color-border-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.theme-card-btn.active {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
}

.theme-icon-circle {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.theme-icon-circle.light {
  background: #fef3c7;
  color: #d97706;
}

.theme-icon-circle.dark {
  background: #1e293b;
  color: #38bdf8;
}

.theme-card-btn.active .theme-icon-circle.light {
  background: #f59e0b;
  color: #ffffff;
}

.theme-card-btn.active .theme-icon-circle.dark {
  background: #0284c7;
  color: #ffffff;
}

.theme-card-info {
  flex-grow: 1;
}

.theme-card-title {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--color-navy);
}

.theme-card-desc {
  font-size: 0.78rem;
  color: var(--color-text-muted);
  line-height: 1.3;
}

.theme-pill {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: 9999px;
  background: var(--color-primary);
  color: #ffffff;
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
}

@media (max-width: 520px) {
  .theme-toggle-grid {
    grid-template-columns: 1fr;
  }
}
</style>
