<!-- src/view/HomeView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 pb-20">
    <!-- ヘッダー -->
    <header class="bg-white p-4 shadow-sm">
      <div class="flex justify-between items-center">
        <div class="flex items-center space-x-4">
          <h1 class="text-xl font-bold">Geneartweave</h1>
          <LanguageSelector />
        </div>

        <div class="flex items-center space-x-4">
          <div v-if="authStore.isAuthenticated" class="flex items-center space-x-4">
            <span class="text-gray-700">{{ authStore.user?.username }}</span>
            <button
              @click="handleLogout"
              class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600"
            >
              {{ $t('common.logout') }}
            </button>
          </div>
          <router-link
            v-else
            to="/login"
            class="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
          >
            {{ $t('common.login') }}
          </router-link>
        </div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="p-4 space-y-6">
      <div v-if="authStore.isAuthenticated">
        <!-- デザイン作成セクション -->
        <div class="bg-indigo-600 text-white p-6 rounded-lg shadow-md text-center">
          <h2 class="text-xl font-bold mb-4">AIでオリジナルTシャツを作ろう</h2>
          <router-link
            to="/create-design"
            class="inline-block bg-white text-indigo-600 px-6 py-3 rounded-full font-semibold"
          >
            {{ $t('home.createDesignButton') }}
          </router-link>
        </div>

        <!-- メニューグリッド -->
        <!-- <div class="grid grid-cols-2 gap-4">
          <div class="bg-white p-6 rounded-lg shadow">
            <Heart class="w-8 h-8 text-red-500 mb-2" />
            <h3 class="text-lg font-semibold mb-2">{{ $t('home.myDesigns') }}</h3>
            <p class="text-gray-600 text-sm mb-4">{{ $t('home.myDesignsDesc') }}</p>
            <router-link 
              to="/my-designs"
              class="text-indigo-600 hover:text-indigo-700 text-sm font-medium"
            >
              {{ $t('home.myDesignsButton') }} →
            </router-link>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <ShoppingBag class="w-8 h-8 text-blue-500 mb-2" />
            <h3 class="text-lg font-semibold mb-2">{{ $t('home.orders') }}</h3>
            <p class="text-gray-600 text-sm mb-4">{{ $t('home.ordersDesc') }}</p>
            <router-link 
              to="/orders"
              class="text-indigo-600 hover:text-indigo-700 text-sm font-medium"
            >
              {{ $t('home.ordersButton') }} →
            </router-link>
          </div>
        </div> -->

        <!-- 人気デザイン -->
        <!-- <section>
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center">
              <TrendingUp class="w-5 h-5 mr-2 text-gray-600" />
              <h2 class="text-lg font-semibold">{{ $t('home.popularDesigns') }}</h2>
            </div>
            <button class="text-indigo-600 text-sm font-medium">
              {{ $t('home.viewAll') }} →
            </button>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div 
              v-for="item in [1, 2, 3, 4]" 
              :key="item" 
              class="bg-white rounded-lg shadow overflow-hidden"
            >
              <div class="aspect-square bg-gray-100">
                <img 
                  :src="`/api/placeholder/200/200?text=Design${item}`" 
                  :alt="`Design ${item}`" 
                  class="w-full h-full object-cover" 
                />
              </div>
              <div class="p-3">
                <p class="text-sm text-gray-600">デザイン #{{ item }}</p>
                <p class="text-sm font-bold mt-1">¥2,000</p>
              </div>
            </div>
          </div>
        </section> -->
      </div>

      <!-- 未ログイン時の表示 -->
      <div v-else class="text-center py-12">
        <h2 class="text-3xl font-bold mb-4">{{ $t('home.welcome') }}</h2>
        <p class="text-xl text-gray-600 mb-8">{{ $t('home.subtitle') }}</p>
        <router-link
          to="/login"
          class="bg-indigo-600 text-white px-6 py-3 rounded-lg text-lg hover:bg-indigo-700"
        >
          {{ $t('home.getStarted') }}
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { ShoppingCart, Heart, ShoppingBag, TrendingUp } from 'lucide-vue-next'
import LanguageSelector from '@/components/LanguageSelector.vue'
import MobileFooter from '@/components/MobileFooter.vue'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>
