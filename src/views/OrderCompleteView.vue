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

      <!-- お届け予定 -->
      <div class="bg-white rounded-lg shadow p-4 mt-4">
        <div class="flex items-center space-x-2 mb-4">
          <Box class="w-5 h-5 text-gray-600" />
          <h2 class="font-bold">お届け予定</h2>
        </div>
        <p class="text-sm text-gray-600">
          発送まで2〜3営業日程度お時間をいただきます。<br />
          発送後、メールにてお知らせいたします。
        </p>
      </div>

      <!-- アクションボタン -->
      <div class="space-y-4 mt-6">
        <button class="w-full bg-indigo-600 text-white py-4 rounded-lg font-bold flex items-center justify-center">
          <ShoppingBag class="w-5 h-5 mr-2" />
          注文履歴を確認（まだ実装されていません）
        </button>
        
        <button class="w-full bg-white text-gray-900 py-4 rounded-lg font-bold border border-gray-200 flex items-center justify-center">
          <HomeIcon class="w-5 h-5 mr-2" />
          ホームに戻る（まだ実装されていません）
        </button>
      </div>
    </main>

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