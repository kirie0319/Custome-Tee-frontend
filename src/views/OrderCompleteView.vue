<!-- src/views/OrderCompleteView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-2xl mx-auto text-center">
      <div class="bg-white rounded-lg shadow p-8">
        <h1 class="text-3xl font-bold text-green-600 mb-4">
          Thank You for Your Order!
        </h1>
        <p class="text-gray-600 mb-6">
          Your order has been successfully placed.
        </p>
        <p class="text-gray-800 mb-8">
          Order ID: {{ $route.params.orderId }}
        </p>
        <div class="space-x-4">
          <router-link
            to="/"
            class="inline-block bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700"
          >
            Back to Home
          </router-link>
          <router-link
            :to="`/orders/${$route.params.orderId}`"
            class="inline-block bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700"
          >
            View Order Details
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>