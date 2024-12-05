<!-- src/App.vue -->
<template>
  <div class="min-h-screen bg-gray-100">
    <router-view />
    <MobileFooter v-if="shouldShowFooter" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import MobileFooter from '@/components/MobileFooter.vue'

const route = useRoute()

// フッターを非表示にするルートのリスト
const footerExcludedRoutes = [
  '/checkout',
  '/onboarding',
  '/login',
  '/register'
]

const shouldShowFooter = computed(() => 
  !footerExcludedRoutes.some(path => route.path.startsWith(path))
)
</script>