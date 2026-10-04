import { initializeApp, getApps, getApp } from 'firebase/app'
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  updateProfile,
  signOut,
  onAuthStateChanged
} from 'firebase/auth'

// Firebase configuration loaded from environment variables
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || '',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || '',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || '',
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || '',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || ''
}

// Check if valid Firebase configuration is present
export const isFirebaseConfigured = Boolean(
  firebaseConfig.apiKey &&
  firebaseConfig.apiKey !== 'YOUR_FIREBASE_API_KEY' &&
  firebaseConfig.projectId
)

let app = null
let auth = null
let googleProvider = null

if (isFirebaseConfigured) {
  try {
    app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp()
    auth = getAuth(app)
    googleProvider = new GoogleAuthProvider()
  } catch (err) {
    console.warn('Firebase initialization error, using local auth fallback:', err)
  }
}

// Local mock storage key for development/demo mode
const LOCAL_USER_KEY = 'cm_academic_user_session'

export const getSavedLocalUser = () => {
  try {
    const raw = localStorage.getItem(LOCAL_USER_KEY)
    return raw ? JSON.parse(raw) : null
  } catch (e) {
    return null
  }
}

export const saveLocalUser = (user) => {
  if (user) {
    localStorage.setItem(LOCAL_USER_KEY, JSON.stringify(user))
  } else {
    localStorage.removeItem(LOCAL_USER_KEY)
  }
}

// Auth API Methods
export const signInWithGoogle = async () => {
  if (isFirebaseConfigured && auth && googleProvider) {
    const result = await signInWithPopup(auth, googleProvider)
    return result.user
  }
  
  // Demo Mode Google Simulation
  const mockUser = {
    uid: 'google-demo-user-123',
    displayName: 'Academic Researcher',
    email: 'researcher@university.edu',
    photoURL: null,
    institution: 'Research University',
    department: 'Computer Science & AI Lab'
  }
  saveLocalUser(mockUser)
  return mockUser
}

export const signInWithEmail = async (email, password) => {
  if (isFirebaseConfigured && auth) {
    const result = await signInWithEmailAndPassword(auth, email, password)
    return result.user
  }
  
  // Demo Mode Simulation
  const mockUser = {
    uid: `local-${Date.now()}`,
    displayName: email.split('@')[0],
    email: email,
    photoURL: null,
    institution: 'Academic Institution',
    department: 'ADLC Research Group'
  }
  saveLocalUser(mockUser)
  return mockUser
}

export const signUpWithEmail = async (email, password, displayName, institution = '') => {
  if (isFirebaseConfigured && auth) {
    const result = await createUserWithEmailAndPassword(auth, email, password)
    if (displayName) {
      await updateProfile(result.user, { displayName })
    }
    return result.user
  }
  
  // Demo Mode Simulation
  const mockUser = {
    uid: `local-${Date.now()}`,
    displayName: displayName || email.split('@')[0],
    email: email,
    photoURL: null,
    institution: institution || 'Academic Institution',
    department: 'Cognitive Systems Lab'
  }
  saveLocalUser(mockUser)
  return mockUser
}

export const logoutUser = async () => {
  saveLocalUser(null)
  if (isFirebaseConfigured && auth) {
    await signOut(auth)
  }
}

export const subscribeToAuthChanges = (callback) => {
  if (isFirebaseConfigured && auth) {
    return onAuthStateChanged(auth, (user) => {
      if (user) {
        callback(user)
      } else {
        callback(getSavedLocalUser())
      }
    })
  }

  // Local state listener
  const user = getSavedLocalUser()
  callback(user)
  return () => {}
}

export { auth }
