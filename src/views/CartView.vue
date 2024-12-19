<!-- src/views/CartView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 pb-20">
    <!-- ヘッダー -->
    <header class="bg-white p-4 shadow-sm">
      <h1 class="text-xl font-bold text-center">ショッピングカート</h1>
    </header>

    <!-- メインコンテンツ -->
    <main class="p-4">
      <!-- カートアイテム -->
      <div v-if="cartItems.length > 0" class="space-y-4 mb-6">
        <div v-for="item in cartItems" :key="item.id" class="bg-white rounded-lg shadow p-4">
          <div class="flex space-x-4">
            <!-- 商品画像 -->
            <img
              :src="item.design.image_url"
              :alt="item.design.prompt"
              class="w-24 h-24 bg-gray-100 rounded-md object-cover"
            />

            <!-- 商品詳細 -->
            <div class="flex-1">
              <p class="text-sm text-gray-600">AI生成デザイン #{{ item.id }}</p>
              <div class="mt-1 space-y-1">
                <p class="text-sm">サイズ: {{ item.size }}</p>
                <p class="text-sm">カラー: {{ item.color }}</p>
                <p class="text-sm">数量: {{ item.quantity }}</p>
              </div>
              <div class="flex items-center mt-2">
                <router-link
                  :to="`/cart/edit/${item.id}`"
                  class="flex items-center text-blue-600 mr-4"
                >
                  <Edit class="w-4 h-4 mr-1" />
                  <span class="text-sm">編集</span>
                </router-link>
                <button @click="removeFromCart(item.id)" class="flex items-center text-red-600">
                  <Trash2 class="w-4 h-4 mr-1" />
                  <span class="text-sm">削除</span>
                </button>
              </div>
            </div>

            <!-- 価格 -->
            <div class="text-right">
              <p class="font-bold">¥{{ 3000 * item.quantity }}</p>
            </div>
          </div>
        </div>

        <!-- 注文サマリー -->
        <div class="bg-white rounded-lg shadow p-4">
          <div class="space-y-2 mb-4">
            <div class="flex justify-between">
              <span class="text-gray-600">小計</span>
              <span>¥{{ totalAmount }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">送料</span>
              <span>¥500</span>
            </div>
            <div class="border-t pt-2 flex justify-between font-bold">
              <span>合計</span>
              <span>¥{{ totalAmount + 500 }}</span>
            </div>
          </div>
          <button
            @click="checkout"
            class="w-full bg-indigo-600 text-white py-3 rounded-md font-medium"
            :disabled="isLoading"
          >
            レジへ進む
          </button>
        </div>
      </div>

      <!-- カートが空の場合 -->
      <div v-else class="bg-white rounded-lg shadow p-8 text-center">
        <p class="text-gray-600 mb-4">カートに商品がありません</p>
        <router-link to="/" class="text-indigo-600 font-medium"> デザインを作成する </router-link>
      </div>
    </main>

    <!-- Footer -->
    <MobileFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Edit, Trash2 } from 'lucide-vue-next'
import MobileFooter from '@/components/MobileFooter.vue'
import { useCartStore } from '@/stores/cart'
import type { CartItem } from '@/types/cart' // 型をインポート

const router = useRouter()
const cartStore = useCartStore()
const isLoading = ref(false)

const cartItems = computed((): CartItem[] => cartStore.items)
const totalAmount = computed(() => {
  return cartItems.value.reduce((total, item) => total + 3000 * item.quantity, 0)
})

const removeFromCart = async (itemId: number) => {
  try {
    await cartStore.removeItem(itemId)
  } catch (error) {
    console.error('Failed to remove item:', error)
  }
}

const checkout = async () => {
  try {
    isLoading.value = true
    await cartStore.initCheckout()
    router.push('/checkout')
  } catch (error) {
    console.error('Checkout failed:', error)
  } finally {
    isLoading.value = false
  }
}
</script>
