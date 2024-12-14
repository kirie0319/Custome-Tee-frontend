<!-- src/components/PaymentForm.vue -->
<template>
  <div class="space-y-4">
    <div v-if="error" class="bg-red-50 p-4 rounded-lg text-red-600 text-sm">
      {{ error }}
    </div>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div id="payment-element" class="bg-white p-4 rounded-lg border"></div>
      
      <button
        type="submit"
        class="w-full bg-indigo-600 text-white py-4 rounded-lg font-bold disabled:opacity-50"
        :disabled="isLoading"
      >
        {{ isLoading ? '処理中...' : '支払いを確定する' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useCartStore } from '@/stores/cart';
import { stripePromise } from '@/utils/stripe';
import { StripeError } from '@stripe/stripe-js';

const props = defineProps<{
  clientSecret: string;
  shippingAddress: any;
}>();

const emit = defineEmits<{
  (e: 'success', orderId: string): void;
  (e: 'error', error: string): void;
}>();

const cartStore = useCartStore();
const error = ref<string | null>(null);
const isLoading = ref(false);
let elements: any = null;

onMounted(async () => {
  try {
    const stripe = await stripePromise;
    if (!stripe) throw new Error('Stripeの初期化に失敗しました');

    elements = stripe.elements({
      clientSecret: props.clientSecret,
      appearance: {
        theme: 'stripe',
        variables: {
          colorPrimary: '#4F46E5',
        },
      },
    });

    const paymentElement = elements.create('payment');
    paymentElement.mount('#payment-element');
  } catch (e) {
    error.value = '決済フォームの読み込みに失敗しました';
    emit('error', error.value);
  }
});

const handleSubmit = async () => {
  if (!elements) return;
  isLoading.value = true;
  error.value = null;

  try {
    const stripe = await stripePromise;
    if (!stripe) throw new Error('Stripeの初期化に失敗しました');

    const { error: stripeError } = await stripe.confirmPayment({
      elements,
      redirect: 'if_required',
    }) as { error: StripeError | undefined };

    if (stripeError) {
      error.value = stripeError.message || '決済処理に失敗しました';
      emit('error', error.value);
      return;
    }

    // 決済の確認
    const result = await cartStore.confirmPayment(
      stripeError?.payment_intent?.id ?? '',
      props.shippingAddress
    );
    
    emit('success', result.order_id);
  } catch (e) {
    error.value = '決済処理に失敗しました';
    emit('error', error.value);
  } finally {
    isLoading.value = false;
  }
};
</script>