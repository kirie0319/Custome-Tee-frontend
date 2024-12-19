<!-- src/components/MobileFooter.vue -->
<template>
  <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2 z-50">
    <div class="flex justify-around items-center">
      <!-- Home Button -->
      <router-link 
        to="/" 
        class="flex flex-col items-center min-w-[48px] min-h-[48px] pt-2"
        :class="{ 'text-indigo-600': $route.path === '/' }"
      >
        <HomeIcon class="h-6 w-6" />
        <span class="text-xs mt-1">Home</span>
      </router-link>

      <!-- Cart Button -->
      <router-link 
        to="/cart"
        class="flex flex-col items-center min-w-[48px] min-h-[48px] pt-2"
        :class="{ 'text-indigo-600': $route.path.includes('cart') }"
        @click.native="handleCartClick"
      >
        <ShoppingCartIcon class="h-6 w-6" />
        <span class="text-xs mt-1">Cart</span>
      </router-link>

      <!-- My Page Button -->
      <router-link 
        to="/legal" 
        class="flex flex-col items-center min-w-[48px] min-h-[48px] pt-2"
        :class="{ 'text-indigo-600': $route.path.includes('legal') }"
      >
        <UserIcon class="h-6 w-6" />
        <span class="text-xs mt-1">Legal</span>
      </router-link>

      <!-- Menu Button -->
      <!-- <button 
        @click="toggleMenu"
        class="flex flex-col items-center min-w-[48px] min-h-[48px] pt-2"
        :class="{ 'text-indigo-600': isMenuOpen }"
      >
        <MenuIcon class="h-6 w-6" />
        <span class="text-xs mt-1">Menu</span>
      </button> -->
    </div>

    <!-- Menu Overlay -->
    <!-- <div 
      v-if="isMenuOpen"
      class="fixed inset-0 bg-black bg-opacity-50"
      @click="isMenuOpen = false"
    /> -->

    <!-- Menu Content -->
    <!-- <div 
      v-if="isMenuOpen"
      class="fixed bottom-16 left-0 right-0 bg-white rounded-t-lg shadow-lg p-4"
    >
      <div class="space-y-4">
        <router-link 
          v-for="item in menuItems" 
          :key="item.path"
          :to="item.path"
          class="block px-4 py-2 hover:bg-gray-100 rounded-md"
          @click="isMenuOpen = false"
        >
          {{ item.label }}
        </router-link>
      </div>
    </div> -->
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { HomeIcon, ShoppingCartIcon, UserIcon, MenuIcon } from 'lucide-vue-next'
import { useCartStore } from '@/stores/cart'

const isMenuOpen = ref(false)
const menuItems = [
  { path: '/help', label: 'Help' },
  { path: '/faq', label: 'FAQ' },
  { path: '/contact', label: 'Contact' },
  { path: '/terms', label: 'Terms of Service' },
  { path: '/privacy', label: 'Privacy Policy' }
]

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const cartStore = useCartStore()

const handleCartClick = async () => {
  await cartStore.fetchCartItems()
}
</script>

<style scoped>
/* Add padding to main content to prevent footer overlap */
:deep(main) {
  padding-bottom: 64px; /* Height of footer */
}
</style>