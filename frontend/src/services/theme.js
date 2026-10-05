import { ref } from 'vue'

const THEME_STORAGE_KEY = 'cognitive_metrics_theme'

export const currentTheme = ref('light')

export const applyTheme = (theme) => {
  const targetTheme = theme === 'dark' ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', targetTheme)
  if (targetTheme === 'dark') {
    document.documentElement.classList.add('dark-theme')
  } else {
    document.documentElement.classList.remove('dark-theme')
  }
}

export const initTheme = () => {
  const saved = typeof localStorage !== 'undefined' ? localStorage.getItem(THEME_STORAGE_KEY) : null
  if (saved === 'dark' || saved === 'light') {
    currentTheme.value = saved
  } else if (typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    currentTheme.value = 'dark'
  } else {
    currentTheme.value = 'light'
  }
  applyTheme(currentTheme.value)
}

export const setTheme = (theme) => {
  const validTheme = theme === 'dark' ? 'dark' : 'light'
  currentTheme.value = validTheme
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem(THEME_STORAGE_KEY, validTheme)
  }
  applyTheme(validTheme)
}

export const toggleTheme = () => {
  const next = currentTheme.value === 'dark' ? 'light' : 'dark'
  setTheme(next)
  return next
}
