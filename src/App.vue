<!-- src/App.vue -->
<template>
  <div class="min-h-screen bg-gray-100">
    <router-view />
    <!-- <MobileFooter v-if="shouldShowFooter" /> -->
    <MobileFooter v-if="shouldShowFooter && authStore.isAuthenticated"/>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import MobileFooter from '@/components/MobileFooter.vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()

const footerExcludedRouteNames = ['checkout', 'onboarding', 'login', 'register', 'cart-item-edit', 'admin-orders']

const shouldShowFooter = computed(() => !footerExcludedRouteNames.includes(route.name as string))


const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>