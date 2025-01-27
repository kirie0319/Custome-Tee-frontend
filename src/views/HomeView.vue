<!-- src/view/HomeView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 pb-20">
    <!-- ヘッダー -->
    <header class="bg-white p-4 shadow-sm">
      <div class="flex justify-between items-center">
        <div class="flex items-center space-x-4">
          <img src="https://custome-tee-designs.s3.ap-northeast-1.amazonaws.com/designs/imges/geneartweaveio-high-resolution-logo-transparent.png" alt="Logo" class="w-20 h-15" />
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