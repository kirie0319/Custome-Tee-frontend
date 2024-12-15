<!-- src/views/OrderCompleteView.vue -->
<template>
  <div class="min-h-screen bg-gray-100">
    <!-- メインコンテンツ -->
    <main class="p-4 pt-12 pb-20">
      <!-- 完了メッセージ -->
      <div class="bg-white rounded-lg shadow p-8 text-center">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-indigo-100 rounded-full mb-4">
          <Check class="w-8 h-8 text-indigo-600" />
        </div>
        <h1 class="text-2xl font-bold mb-2">ご注文ありがとうございます</h1>
        <p class="text-sm text-gray-600">注文番号：{{ orderId }}</p>
      </div>

    <!-- Footer -->
    <MobileFooter />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Check, Box, ChevronRight, ShoppingBag, Home as HomeIcon } from 'lucide-vue-next'
import MobileFooter from '@/components/MobileFooter.vue'

const route = useRoute()
const router = useRouter()

const orderId = computed(() => route.params.orderId)

const goToOrderHistory = () => {
  router.push('/orders')
}

const goToHome = () => {
  router.push('/')
}
</script>