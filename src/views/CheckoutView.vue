<!-- src/views/CheckoutView.vue -->
<template>
 <div class="min-h-screen bg-gray-100 pb-20">
   <!-- ヘッダー -->
   <header class="bg-white p-4 shadow-sm">
     <div class="flex items-center">
       <button @click="router.push('/cart')" class="p-2 -ml-2">
         <ChevronLeft class="h-6 w-6" />
       </button>
       <h1 class="text-xl font-bold flex-1 text-center">チェックアウト</h1>
       <div class="w-10"></div>
     </div>
   </header>

   <!-- メインコンテンツ -->
   <main class="p-4 space-y-4">
     <!-- お届け先 -->
     <div class="bg-white rounded-lg shadow p-4">
       <div class="flex items-center justify-between mb-4">
         <div class="flex items-center space-x-2">
           <MapPin class="w-5 h-5 text-gray-600" />
           <h2 class="font-bold">お届け先</h2>
         </div>
       </div>
       <!-- <div class="text-sm text-gray-600">
         〒{{ shippingAddress.postal_code }}<br />
         {{ shippingAddress.address }}<br />
         {{ shippingAddress.name }}
       </div> -->
       <form class="space-y-4">
        <div class="space-y-2">
          <label for="name" class="block text-sm font-medium text-gray-700">お名前</label>
          <input
            id="name"
            v-model="shippingAddress.name"
            type="text"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            :class="{ 'border-red-300': errors.name }"
            required
          />
          <p v-if="errors.name" class="text-sm text-red-600">{{ errors.name }}</p>
        </div>

        <div class="space-y-2">
          <label for="postal_code" class="block text-sm font-medium text-gray-700">郵便番号</label>
          <input
            id="postal_code"
            v-model="shippingAddress.postal_code"
            type="text"
            placeholder="123-4567"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            :class="{ 'border-red-300': errors.postal_code }"
            required
          />
          <p v-if="errors.postal_code" class="text-sm text-red-600">{{ errors.postal_code }}</p>
        </div>
        <div class="space-y-2">
          <label for="address" class="block text-sm font-medium text-gray-700">住所（建物の名前から部屋番号まで入れてください）</label>
          <input
            id="address"
            v-model="shippingAddress.address"
            type="text"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            :class="{ 'border-red-300': errors.address }"
            required
          />
          <p v-if="errors.address" class="text-sm text-red-600">{{ errors.address }}</p>
        </div>
        <div class="space-y-2">
          <label for="city" class="block text-sm font-medium text-gray-700">市区町村</label>
          <input
            id="city"
            v-model="shippingAddress.city"
            type="text"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            :class="{ 'border-red-300': errors.city }"
            required
          />
          <p v-if="errors.city" class="text-sm text-red-600">{{ errors.city }}</p>
        </div>
       </form>
     </div>

     <!-- 注文内容 -->
     <div class="bg-white rounded-lg shadow p-4">
       <div class="flex items-center space-x-2 mb-4">
         <Box class="w-5 h-5 text-gray-600" />
         <h2 class="font-bold">注文内容</h2>
       </div>
       <div 
         v-for="item in cartItems" 
         :key="item.id" 
         class="flex justify-between py-2 border-b last:border-none"
       >
         <div>
           <p class="text-sm text-gray-600">AI生成デザイン #{{ item.id }}</p>
           <div class="mt-1 space-y-1">
             <p class="text-sm">サイズ: {{ item.size }}</p>
             <p class="text-sm">カラー: {{ item.color }}</p>
             <p class="text-sm">数量: {{ item.quantity }}</p>
           </div>
         </div>
         <p class="font-bold">¥{{ item.price * item.quantity }}</p>
       </div>
     </div>

     <!-- 注文金額 -->
     <div class="bg-white rounded-lg shadow p-4">
       <div class="space-y-2">
         <div class="flex justify-between">
           <span class="text-gray-600">小計</span>
           <span>¥{{ subtotal }}</span>
         </div>
         <div class="flex justify-between">
           <span class="text-gray-600">送料</span>
           <span>¥500</span>
         </div>
         <div class="border-t pt-2 flex justify-between font-bold">
           <span>合計（税込）</span>
           <span>¥{{ total }}</span>
         </div>
       </div>
     </div>
     <!-- お支払い方法 -->
     <div class="bg-white rounded-lg shadow p-4">
       <div class="flex items-center space-x-2 mb-4">
         <CreditCard class="w-5 h-5 text-gray-600" />
         <h2 class="font-bold">お支払い方法</h2>
       </div>
       
       <PaymentForm
         v-if="clientSecret"
         :client-secret="clientSecret"
         :shipping-address="shippingAddress"
         @success="handlePaymentSuccess"
         @error="handlePaymentError"
       />

       <div v-if="paymentError" class="mt-2 text-sm text-red-600">
         {{ paymentError }}
       </div>
     </div>
   </main>
 </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronLeft, MapPin, CreditCard, Box } from 'lucide-vue-next'
import { useCartStore } from '@/stores/cart'
import type { CartItem } from '@/types/cart'  // 型をインポート
import PaymentForm from '@/components/PaymentForm.vue'

const router = useRouter()
const cartStore = useCartStore()
const isProcessing = ref(false)
const clientSecret = ref<string | null>(null)
const paymentError = ref<string | null>(null)

// エラー状態の管理を追加
const errors = ref({
  name: '',
  postal_code: '',
  address: '',
  city: ''
})

// 配送先情報
const shippingAddress = ref({
 name: '',
 postal_code: '',
 address: '',
 city: ''
})

// バリデーション関数を追加
const validateShippingAddress = () => {
  let isValid = true
  errors.value = {
    name: '',
    postal_code: '',
    address: '',
    city: ''
  }

  if (!shippingAddress.value.name) {
    errors.value.name = 'お名前を入力してください'
    isValid = false
  }

  if (!shippingAddress.value.postal_code) {
    errors.value.postal_code = '郵便番号を入力してください'
    isValid = false
  } else if (!/^\d{3}-\d{4}$/.test(shippingAddress.value.postal_code)) {
    errors.value.postal_code = '正しい郵便番号を入力してください（例：123-4567）'
    isValid = false
  }

  if (!shippingAddress.value.address) {
    errors.value.address = '住所を入力してください'
    isValid = false
  }

  if (!shippingAddress.value.city) {
    errors.value.city = '市区町村を入力してください'
    isValid = false
  }

  return isValid
}


const cartItems = computed((): CartItem[] => cartStore.items)
const subtotal = computed(() => 
 cartItems.value.reduce((sum, item) => sum + (2000 * item.quantity), 0)
)
const total = computed(() => subtotal.value + 500)

onMounted(async () => {
 try {
   const { client_secret } = await cartStore.initCheckout()
   clientSecret.value = client_secret
 } catch (error) {
   paymentError.value = '決済の初期化に失敗しました'
 }
})

const handlePaymentSuccess = async (orderId: string) => {
 await router.push(`/order-complete/${orderId}`)
}

const handlePaymentError = (error: string) => {
 paymentError.value = error
}

const handleSubmit = async () => {
  if (!validateShippingAddress()) {
    return
  }

 isProcessing.value = true
 try {
   const { client_secret } = await cartStore.initCheckout()
   clientSecret.value = client_secret
 } catch (error) {
   paymentError.value = '決済の初期化に失敗しました'
 } finally {
   isProcessing.value = false
 }
}
</script>