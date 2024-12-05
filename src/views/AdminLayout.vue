<!-- src/views/AdminLayout.vue -->
<template>
  <div class="min-h-screen bg-gray-100">
    <!-- サイドナビゲーション -->
    <nav class="bg-gray-800 fixed h-full w-64">
      <div class="px-4 py-5">
        <h2 class="text-xl font-bold text-white">CustomAI Tee Admin</h2>
      </div>
      <div class="mt-5 px-2">
        <router-link
          to="/admin"
          class="group flex items-center px-2 py-2 text-base font-medium rounded-md text-gray-300 hover:bg-gray-700 hover:text-white"
          :class="{ 'bg-gray-900 text-white': $route.path === '/admin' }"
        >
          <HomeIcon class="mr-4 h-6 w-6" />
          Dashboard
        </router-link>

        <router-link
          to="/admin/orders"
          class="mt-1 group flex items-center px-2 py-2 text-base font-medium rounded-md text-gray-300 hover:bg-gray-700 hover:text-white"
          :class="{ 'bg-gray-900 text-white': $route.path.startsWith('/admin/orders') }"
        >
          <ShoppingBagIcon class="mr-4 h-6 w-6" />
          Orders
        </router-link>

        <router-link
          to="/admin/users"
          class="mt-1 group flex items-center px-2 py-2 text-base font-medium rounded-md text-gray-300 hover:bg-gray-700 hover:text-white"
          :class="{ 'bg-gray-900 text-white': $route.path.startsWith('/admin/users') }"
        >
          <UsersIcon class="mr-4 h-6 w-6" />
          Users
        </router-link>

        <router-link
          to="/"
          class="mt-8 group flex items-center px-2 py-2 text-base font-medium rounded-md text-gray-300 hover:bg-gray-700 hover:text-white"
        >
          <ArrowLeftIcon class="mr-4 h-6 w-6" />
          Back to Store
        </router-link>
      </div>
    </nav>

    <!-- メインコンテンツ -->
    <div class="pl-64">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { HomeIcon, ShoppingBagIcon, UsersIcon, ArrowLeftIcon } from 'lucide-react'

const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  // 管理者権限チェック
  if (!authStore.isAdmin) {
    router.push('/')
  }
})
</script>