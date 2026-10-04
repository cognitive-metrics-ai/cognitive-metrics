<script setup>
import { ref, reactive } from 'vue'
import {
  signInWithGoogle,
  signInWithEmail,
  signUpWithEmail,
  isFirebaseConfigured
} from '../services/firebase'

const emit = defineEmits(['close', 'auth-success'])

const isSignUp = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

const form = reactive({
  displayName: '',
  institution: '',
  email: '',
  password: ''
})

const handleGoogleSignIn = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const user = await signInWithGoogle()
    emit('auth-success', user)
    emit('close')
  } catch (err) {
    console.error('Google Sign-In Error:', err)
    errorMessage.value = err.message || 'Google Sign-In failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const handleSubmit = async () => {
  if (!form.email || !form.password) {
    errorMessage.value = 'Please provide an email and password.'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    let user
    if (isSignUp.value) {
      if (!form.displayName) {
        errorMessage.value = 'Please enter your full name.'
        isLoading.value = false
        return
      }
      user = await signUpWithEmail(form.email, form.password, form.displayName, form.institution)
    } else {
      user = await signInWithEmail(form.email, form.password)
    }
    emit('auth-success', user)
    emit('close')
  } catch (err) {
    console.error('Email Auth Error:', err)
    errorMessage.value = err.message || 'Authentication failed. Please verify your credentials.'
  } finally {
    isLoading.value = false
  }
}

// 1-Click demo sign-in for testing
const handleDemoSignIn = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const demoUser = await signInWithEmail('dr.vance@stanford.edu', 'academicdemo123')
    emit('auth-success', demoUser)
    emit('close')
  } catch (err) {
    errorMessage.value = 'Demo login failed.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="modal-backdrop" @click.self="emit('close')" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(14, 27, 47, 0.75); backdrop-filter: blur(5px); z-index: 999; display: flex; align-items: center; justify-content: center; padding: 1.5rem;">
    <div class="modal-content" style="background: #ffffff; border-radius: 18px; max-width: 480px; width: 100%; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); padding: 2.5rem; position: relative;">
      <!-- Close Button -->
      <button @click="emit('close')" style="position: absolute; top: 1.25rem; right: 1.25rem; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #94a3b8;">
        &times;
      </button>

      <div style="text-align: center; margin-bottom: 2rem;">
        <span class="section-label coral">Researcher Portal</span>
        <h2 style="font-size: 1.75rem; margin-top: 0.25rem;">
          {{ isSignUp ? 'Create Researcher Account' : 'Sign In to Cognitive Metrics' }}
        </h2>
        <p style="font-size: 0.9rem; margin-top: 0.35rem;">
          Access your approved ADLC testbeds, telemetry data, and research proposals.
        </p>
      </div>

      <!-- Error Box -->
      <div v-if="errorMessage" style="background: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 1.25rem; font-size: 0.875rem;">
        {{ errorMessage }}
      </div>

      <!-- Google Sign In Button -->
      <button 
        type="button" 
        @click="handleGoogleSignIn" 
        :disabled="isLoading"
        style="width: 100%; display: flex; align-items: center; justify-content: center; gap: 0.75rem; padding: 0.75rem 1rem; border-radius: 9999px; border: 1px solid #cbd5e1; background: #ffffff; color: #1e293b; font-weight: 600; font-size: 0.95rem; cursor: pointer; transition: all 0.2s ease; margin-bottom: 1.25rem;"
        @mouseenter="$event.currentTarget.style.borderColor = '#94a3b8'; $event.currentTarget.style.background = '#f8fafc'"
        @mouseleave="$event.currentTarget.style.borderColor = '#cbd5e1'; $event.currentTarget.style.background = '#ffffff'"
      >
        <svg width="20" height="20" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span>Continue with Google</span>
      </button>

      <div style="display: flex; align-items: center; margin: 1.25rem 0; color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em;">
        <div style="flex-grow: 1; height: 1px; background: #e2e8f0;"></div>
        <span style="padding: 0 0.75rem;">Or with institutional email</span>
        <div style="flex-grow: 1; height: 1px; background: #e2e8f0;"></div>
      </div>

      <!-- Email/Password Form -->
      <form @submit.prevent="handleSubmit">
        <div v-if="isSignUp" class="form-group">
          <label class="form-label">Full Name & Title</label>
          <input 
            type="text" 
            v-model="form.displayName" 
            class="form-input" 
            placeholder="e.g. Dr. Jane Smith" 
            required 
          />
        </div>

        <div v-if="isSignUp" class="form-group">
          <label class="form-label">University / Institution</label>
          <input 
            type="text" 
            v-model="form.institution" 
            class="form-input" 
            placeholder="e.g. Stanford University" 
          />
        </div>

        <div class="form-group">
          <label class="form-label">Institutional Email</label>
          <input 
            type="email" 
            v-model="form.email" 
            class="form-input" 
            placeholder="researcher@university.edu" 
            required 
          />
        </div>

        <div class="form-group">
          <label class="form-label">Password</label>
          <input 
            type="password" 
            v-model="form.password" 
            class="form-input" 
            placeholder="••••••••" 
            required 
            minlength="6"
          />
        </div>

        <button 
          type="submit" 
          class="btn btn-primary" 
          style="width: 100%; margin-top: 1rem; padding: 0.85rem;"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Authenticating...' : (isSignUp ? 'Create Researcher Account' : 'Sign In') }}
        </button>
      </form>

      <!-- Toggle Sign In / Sign Up -->
      <div style="text-align: center; margin-top: 1.25rem; font-size: 0.875rem; color: #64748b;">
        <span>{{ isSignUp ? 'Already have an academic account?' : "Don't have an account?" }}</span>
        <button 
          type="button" 
          @click="isSignUp = !isSignUp" 
          style="background: none; border: none; color: var(--color-primary); font-weight: 700; cursor: pointer; margin-left: 0.35rem;"
        >
          {{ isSignUp ? 'Sign In' : 'Sign Up' }}
        </button>
      </div>

      <!-- Quick 1-Click Demo Sign-In -->
      <div v-if="!isFirebaseConfigured" style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px dashed #cbd5e1; text-align: center;">
        <span style="font-size: 0.75rem; color: #64748b; display: block; margin-bottom: 0.5rem;">
          Firebase in local demo mode. Try 1-click preview:
        </span>
        <button 
          type="button" 
          @click="handleDemoSignIn"
          class="btn btn-secondary"
          style="font-size: 0.8rem; padding: 0.4rem 0.9rem;"
        >
          ⚡ Instant Demo Sign-In (Dr. Marcus Vance)
        </button>
      </div>
    </div>
  </div>
</template>
