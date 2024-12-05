<!-- src/views/CartView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold mb-8">{{ $t('cart.title') }}</h1>

      <!-- カートが空の場合 -->
      <div v-if="!cartItems.length" class="bg-white rounded-lg shadow p-6 text-center">
        <p class="text-gray-600 mb-4">{{ $t('cart.empty') }}</p>
        <router-link
          to="/create-design"
          class="inline-block bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700"
        >
          {{ $t('cart.backToDesign') }}
        </router-link>
      </div>

      <!-- カートアイテム一覧 -->
      <div v-else class="space-y-4">
        <div v-for="item in cartItems" :key="item.id" class="bg-white rounded-lg shadow p-6">
          <div class="flex items-start space-x-4">
            <!-- デザイン画像 -->
            <img
              :src="item.design.image_url"
              :alt="item.design.prompt"
              class="w-32 h-32 object-cover rounded-md"
            />
            
            <!-- 商品情報 -->
            <div class="flex-grow">
              <p class="text-sm text-gray-600">{{ item.design.prompt }}</p>
              <div class="mt-2">
                <p class="text-sm text-gray-600">{{ $t('createDesign.size') }}: {{ item.size }}</p>
                <p class="text-sm text-gray-600">{{ $t('createDesign.color') }}: {{ item.color }}</p>
                <p class="text-sm text-gray-600">{{ $t('cart.quantity') }}: {{ item.quantity }}</p>
              </div>
              <div class="mt-4 space-x-4">
                <router-link
                  :to="{ name: 'cart-item-edit', params: { id: item.id }}"
                  class="text-blue-600 hover:text-blue-800"
                >
                  {{ $t('cart.editDesign') }}
                </router-link>
                <button
                  @click="removeFromCart(item.id)"
                  class="text-red-600 hover:text-red-800"
                >
                  {{ $t('common.remove') }}
                </button>
              </div>
            </div>

            <!-- 価格 -->
            <div class="text-right">
              <p class="text-lg font-semibold">¥{{ 2000 * item.quantity }}</p>
            </div>
          </div>
        </div>

        <!-- 注文サマリー -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex justify-between mb-4">
            <span class="font-semibold">{{ $t('cart.total') }}</span>
            <span class="font-semibold">¥{{ totalAmount }}</span>
          </div>
          <button
            @click="checkout"
            class="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700"
            :disabled="isLoading"
          >
            {{ isLoading ? $t('common.processing') : $t('cart.checkout') }}
          </button>
        </div>
      </div>

      <!-- エラーメッセージ -->
      <div
        v-if="error"
        class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-4"
      >
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const authStore = useAuthStore()
const router = useRouter()

const cartItems = ref([])
const isLoading = ref(false)
const error = ref('')

const totalAmount = computed(() => {
  return cartItems.value.reduce((total, item) => total + (2000 * item.quantity), 0)
})

const fetchCartItems = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/cart/items', {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    cartItems.value = response.data.cart_items
  } catch (e) {
    error.value = 'Failed to load cart items'
    console.error('Error loading cart:', e)
  }
}

const removeFromCart = async (itemId) => {
  try {
    await axios.delete(`http://localhost:5000/api/cart/items/${itemId}`, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    await fetchCartItems()
  } catch (e) {
    error.value = 'Failed to remove item from cart'
    console.error('Error removing item:', e)
  }
}

const checkout = async () => {
  isLoading.value = true
  error.value = ''

  try {
    const response = await axios.post('http://localhost:5000/api/payment/create-payment', {}, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })

    router.push({
      name: 'checkout',
      query: { 
        payment_intent: response.data.payment_intent_id,
        amount: response.data.amount
      }
    })
  } catch (e) {
    error.value = 'Failed to initiate checkout'
    console.error('Error during checkout:', e)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchCartItems()
})
</script>