<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-bold">{{ $t('home.title') }}</h1>
          </div>
          <div class="flex items-center space-x-4">
            <!-- 言語切り替え -->
            <LanguageSelector />

            <div v-if="authStore.isAuthenticated" class="flex items-center">
              <!-- カートリンク -->
              <router-link 
                to="/cart"
                class="mr-4 flex items-center text-gray-600 hover:text-gray-900"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span class="ml-1">{{ $t('common.cart') }}</span>
              </router-link>
              <span class="mr-4">{{ $t('common.welcome') }}, {{ authStore.user?.username }}</span>
              <button 
                @click="handleLogout"
                class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
              >
                {{ $t('common.logout') }}
              </button>
            </div>
            <router-link 
              v-else 
              to="/login"
              class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              {{ $t('common.login') }}
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div v-if="authStore.isAuthenticated">
        <h2 class="text-2xl font-bold mb-4">{{ $t('home.dashboard') }}</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="bg-white p-6 rounded-lg shadow">
            <h3 class="text-lg font-semibold mb-2">{{ $t('home.createDesign') }}</h3>
            <p class="text-gray-600">{{ $t('home.createDesignDesc') }}</p>
            <router-link 
              to="/create-design"
              class="mt-4 inline-block bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
            >
              {{ $t('home.createDesignButton') }}
            </router-link>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <h3 class="text-lg font-semibold mb-2">{{ $t('home.myDesigns') }}</h3>
            <p class="text-gray-600">{{ $t('home.myDesignsDesc') }}</p>
            <router-link 
              to="/my-designs"
              class="mt-4 inline-block bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
            >
              {{ $t('home.myDesignsButton') }}
            </router-link>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <h3 class="text-lg font-semibold mb-2">{{ $t('home.orders') }}</h3>
            <p class="text-gray-600">{{ $t('home.ordersDesc') }}</p>
            <router-link 
              to="/orders"
              class="mt-4 inline-block bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
            >
              {{ $t('home.ordersButton') }}
            </router-link>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <h3 class="text-lg font-semibold mb-2">{{ $t('home.cart') }}</h3>
            <p class="text-gray-600">{{ $t('home.cartDesc') }}</p>
            <router-link 
              to="/cart"
              class="mt-4 inline-block bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
            >
              {{ $t('home.cartButton') }}
            </router-link>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-12">
        <h2 class="text-3xl font-bold mb-4">{{ $t('home.welcome') }}</h2>
        <p class="text-xl text-gray-600 mb-8">{{ $t('home.subtitle') }}</p>
        <router-link 
          to="/login"
          class="bg-blue-500 text-white px-6 py-3 rounded-lg text-lg hover:bg-blue-600"
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
import LanguageSelector from '@/components/LanguageSelector.vue'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
