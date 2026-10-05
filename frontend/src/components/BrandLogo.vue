<script setup>
import { computed } from 'vue'
import { currentTheme } from '../services/theme'

const props = defineProps({
  variant: {
    type: String,
    default: 'auto', // 'auto' | 'light' | 'dark' | 'emblem' | 'emblem-dark' | 'icon'
    validator: (v) => ['auto', 'light', 'dark', 'emblem', 'emblem-light', 'emblem-dark', 'icon'].includes(v)
  },
  height: {
    type: [Number, String],
    default: 40
  },
  alt: {
    type: String,
    default: 'Cognitive Metrics Brand Logo'
  }
})

const logoSrc = computed(() => {
  if (props.variant === 'icon') {
    return '/assets/logo-icon.png'
  }
  if (props.variant === 'emblem-dark') {
    return '/assets/logo-emblem-dark.png'
  }
  if (props.variant === 'emblem-light' || props.variant === 'emblem') {
    return currentTheme.value === 'dark' ? '/assets/logo-emblem-light.png' : '/assets/logo-emblem-light.png'
  }
  if (props.variant === 'dark') {
    return '/assets/logo-dark.png'
  }
  if (props.variant === 'light') {
    return '/assets/logo-light.png'
  }
  // 'auto': In dark mode use bright/vibrant logo-light.png, in light mode use logo-dark.png or logo-light.png
  return currentTheme.value === 'dark' ? '/assets/logo-light.png' : '/assets/logo-dark.png'
})

const heightStyle = computed(() => {
  return typeof props.height === 'number' ? `${props.height}px` : props.height
})
</script>

<template>
  <img 
    :src="logoSrc" 
    :alt="alt" 
    :style="{ height: heightStyle, width: 'auto', objectFit: 'contain' }"
    class="brand-logo-img"
    loading="lazy"
  />
</template>

<style scoped>
.brand-logo-img {
  display: inline-block;
  vertical-align: middle;
  transition: transform 0.2s ease, filter 0.25s ease;
}
</style>
