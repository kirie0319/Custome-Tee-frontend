<!-- src/views/CheckoutView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold mb-8">{{ $t('checkout.title') }}</h1>

      <!-- 注文サマリー -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('checkout.orderSummary') }}</h2>
        <div class="flex justify-between mb-4">
          <span>{{ $t('cart.total') }}</span>
          <span class="font-semibold">¥{{ amount }}</span>
        </div>
      </div>

      <!-- 配送先情報フォーム -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('checkout.shippingInfo') }}</h2>
        <form @submit.prevent="confirmPayment" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ $t('checkout.form.name') }}
            </label>
            <input
              v-model="shippingAddress.name"
              type="text"
              required
              class="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ $t('checkout.form.address') }}
            </label>
            <input
              v-model="shippingAddress.address"
              type="text"
              required
              class="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ $t('checkout.form.city') }}
            </label>
            <input
              v-model="shippingAddress.city"
              type="text"
              required
              class="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ $t('checkout.form.postalCode') }}
            </label>
            <input
              v-model="shippingAddress.postal_code"
              type="text"
              required
              class="w-full p-2 border border-gray-300 rounded-md"
              pattern="\d{3}-?\d{4}"
              title="{{ $t('checkout.form.postalCodeFormat') }}"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ $t('checkout.form.country') }}
            </label>
            <input
              v-model="shippingAddress.country"
              type="text"
              required
              class="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>

          <!-- 支払い確認ボタン -->
          <button
            type="submit"
            class="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 disabled:opacity-50"
            :disabled="isLoading || !isValidPaymentIntent"
          >
            {{ isLoading ? $t('common.processing') : $t('checkout.confirmOrder') }}
          </button>
        </form>
      </div>

      <!-- エラーメッセージ -->
      <div
        v-if="error"
        class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-4"
      >
        {{ $t(`checkout.errors.${error}`) }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// State
const amount = ref(route.query.amount || 0)
const isLoading = ref(false)
const error = ref('')

// Payment Intent
const paymentIntentId = computed(() => route.query.payment_intent as string)
const isValidPaymentIntent = computed(() => Boolean(paymentIntentId.value))

// Form data
const shippingAddress = ref({
  name: '',
  address: '',
  city: '',
  postal_code: '',
  country: 'Japan'
})

// Payment confirmation handler
const confirmPayment = async () => {
  if (!isValidPaymentIntent.value) {
    error.value = 'Invalid payment session. Please try again.'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    // Debug logging
    console.log('Auth token:', authStore.token ? 'Present' : 'Missing')
    
    const requestData = {
      payment_intent_id: paymentIntentId.value,
      shipping_address: shippingAddress.value
    }
    
    console.log('Sending payment confirmation:', requestData)

    // API request
    const response = await axios.post(
      'http://localhost:5000/api/payment/confirm-payment',
      requestData,
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    console.log('Payment confirmation response:', response.data)

    // Redirect to order complete page
    router.push({
      name: 'order-complete',
      params: { orderId: response.data.order_id }
    })
  } catch (e: any) {
    // Enhanced error handling
    console.error('Payment error:', {
      status: e.response?.status,
      data: e.response?.data,
      message: e.message
    })
    
    error.value = e.response?.data?.error || 
                  'Failed to process payment. Please try again.'
  } finally {
    isLoading.value = false
  }
}

// Initialization
onMounted(() => {
  console.log('CheckoutView mounted', {
    amount: amount.value,
    paymentIntentId: paymentIntentId.value,
    token: authStore.token ? 'Present' : 'Missing'
  })

  if (!isValidPaymentIntent.value) {
    error.value = 'Invalid payment session. Please try again.'
    console.error('No payment_intent_id found in URL')
  }
})
</script>