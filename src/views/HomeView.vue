<!-- src/view/HomeView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 pb-20">
    <!-- ヘッダー -->
    <header class="bg-white p-4 shadow-sm">
      <div class="flex justify-between items-center">
        <div class="flex items-center space-x-4">
          <img src="https://custome-tee-designs.s3.ap-northeast-1.amazonaws.com/designs/imges/geneartweaveio-high-resolution-logo-transparent.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAYM7POCGCVWCDNSBN%2F20250127%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20250127T104945Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFMaDmFwLW5vcnRoZWFzdC0xIkcwRQIgXF5iAjIO2Y1VvydDZYeKkg8%2B2iGERfyPA2hM%2BKCC4nwCIQCrSsTv5qCvnuaIVhPP8MOLQfLv7QrDjTj3qiV24Sy8cyrsAghcEAAaDDU3NzYzODM3MTcxNyIMJEIJ68AtsnHlNN5GKskC4mPKpqlT5o8jADuRIfa4XTuOX5ncnLSMQ1M7RuXTBmL0x3jJXTQvYRBocCfCR2xIFeXPn5GfcjOKmK0uYrs7eNtv5EnSOMS%2BKpeltpzCm7D39ijRSz6N2tNoXDz1j%2BgBASWtk0WFx0x%2BThYTn0U99PIu%2BxRZ7FqCx33DpN8zQ1RWKqqi%2Bz0UbORuIvZsRUx2R21gRHUoY79rx0LbBDLKLv5AChkwkFQyqQ46BJ00ba6qi5fhRadRqpMEKV8TSVSOMdwFitRv2v131eATapzpN5XgzC28OMhTsOnaS2cHYt40h6OHoqR3eONrankNPSQcIthnt2TX1eK9Go02hGXuICwhHFmcx2O5MLd34zAViBvYFU2lkMXesFUp%2FFX%2FCHoyuPkSHnwKut9rkFQfiu9nK1jeqzd9EvAC5ORNUDqst1pBgEARvqsIzaYw6cfdvAY6swKhlSv7O4YrcB5ZOkBGcXJTEMBc8Iewj2nrElyycquXwRyYZ6HGMKrbvTR2x3RIDueXWhgtg8db87krghVfQqzkmNvu70tqMHrLLviOT7Ne4eJ2H%2FW%2F7lo%2BhbOkK8lDD6GhIUiweYztfd8PX%2BjAdQrE%2FCxflQvYNoCdxwjVhxJymxlhD2Pe674TUEm4%2BPT9TmmUOYvkwcjQvYMlZ%2Ft%2BfPBimwb7LzQ45l5mVvSkkg%2FEzuY%2Fa9rg3WeNzP8pfXPzv39WXs82Y6oyuVItVTWzVUPOH2SLlQVfyk%2F9tApZqpNCZ0oM1dKs3bzXgzuzzsGkNcKDSjmoGMaVLN3WWhMXZc%2Blv6w%2BPZR1emWgVxhE5f1UrIAXG4gFjZh9yquWPtjjOoFDNlVrHVkRyXP8tg6%2BOCeo6%2BhK&X-Amz-Signature=2438c61382afa887e0595bce03ce96f611601beabea0099d65ee02a986a62607&X-Amz-SignedHeaders=host&response-content-disposition=inline" alt="Logo" class="w-20 h-15" />
        </div>

        <div class="flex items-center space-x-4">
          <LanguageSelector />
          <div v-if="authStore.isAuthenticated" class="flex items-center space-x-4">
            <span class="text-gray-700">{{ authStore.user?.username }}</span>
            <button
              @click="handleLogout"
              class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600"
            >
              {{ $t('common.logout') }}
            </button>
          </div>
          <template v-else>
            <router-link
              to="/login"
              class="text-black px-4 py-2 rounded-md hover:bg-indigo-700"
            >
              {{ $t('common.login') }}
            </router-link>
            <router-link
              to="/register"
              class="bg-indigo-500 text-white px-4 py-2 rounded-md hover:bg-green-600"
            >
              会員登録
            </router-link>
          </template>
        </div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="p-4">
      <div class="max-w-6xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <!-- 左側: テキスト -->
          <div class="space-y-6 text-center md:text-left">
            <h1 class="text-4xl md:text-5xl font-bold text-gray-900">AI T-Shirt Design Generator</h1>
            <p class="text-lg md:text-xl text-gray-600">
              AIであなただけのTシャツデザインを作りましょう！
            </p>
            <p class="text-lg md:text-xl text-gray-600">
              あなたのアイデアを形にし、魅力的なTシャツを一緒に生成しましょう！
            </p>
            <router-link
              to="/create-design"
              class="inline-block bg-indigo-600 text-white px-8 py-3 rounded-lg text-lg hover:bg-indigo-700"
            >
             無料で始める
            </router-link>
          </div>

          <!-- 右側: ビジュアル例 -->
          <div class="grid grid-cols-2 gap-4 mt-8 md:mt-0">
            <div class="bg-white rounded-lg shadow-lg overflow-hidden">
              <img src="https://custome-tee-designs.s3.ap-northeast-1.amazonaws.com/designs/designs/6/c9c05e3e-0c45-4768-ba33-622938ba7094.png" class="w-full h-full object-cover"
              />
            </div>
            <div class="bg-white rounded-lg shadow-lg overflow-hidden">
              <img src="https://custome-tee-designs.s3.ap-northeast-1.amazonaws.com/designs/designs/2/7168bbc6-3989-43e1-ad51-ff59451d0a3d.png" class="w-full h-full object-cover"
              />
            </div>
            <div class="bg-white rounded-lg shadow-lg overflow-hidden">
              <img src="https://custome-tee-designs.s3.ap-northeast-1.amazonaws.com/designs/designs/6/3a29c984-a4b7-4f17-9c55-01162be08a1b.png" class="w-full h-full object-cover"
              />
            </div>
            <div class="bg-white rounded-lg shadow-lg overflow-hidden">
              <img src="https://custome-tee-designs.s3.ap-northeast-1.amazonaws.com/designs/designs/3/fe0beed9-a8c1-4659-b787-35c3f2bd5a44.png" class="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import LanguageSelector from '@/components/LanguageSelector.vue'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>