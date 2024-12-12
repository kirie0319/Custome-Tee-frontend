<!-- src/views/AdminOrders.vue -->
<template>
  <div class="min-h-screen p-6">
    <div class="max-w-7xl mx-auto">
      <div class="mb-6">
        <h1 class="text-3xl font-bold">Orders Management</h1>
      </div>

      <!-- 検索フィルター -->
      <div class="bg-white p-4 rounded-lg shadow mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Order Status
            </label>
            <select 
              v-model="filters.status"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500"
            >
              <option value="">All</option>
              <option value="paid">Paid</option>
              <option value="processing">Processing</option>
              <option value="shipped">Shipped</option>
              <option value="delivered">Delivered</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Search
            </label>
            <input 
              type="text"
              v-model="filters.query"
              placeholder="Order ID or customer email"
              class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500"
            >
          </div>
          <div class="flex items-end">
            <button
              @click="fetchOrders"
              class="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
            >
              Search
            </button>
          </div>
        </div>
      </div>

      <!-- 注文一覧テーブル -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Order ID
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Customer
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Items
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Total
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="order in orders" :key="order.id">
              <td class="px-6 py-4 whitespace-nowrap">
                #{{ order.id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {{ order.items }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {{ order.items_count }} items
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                ¥{{ order.total_amount.toLocaleString() }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <select 
                  v-model="order.status"
                  @change="updateOrderStatus(order)"
                  class="rounded-md border-gray-300 shadow-sm focus:border-indigo-500"
                >
                  <option value="paid">Paid</option>
                  <option value="processing">Processing</option>
                  <option value="shipped">Shipped</option>
                  <option value="delivered">Delivered</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <button
                  @click="viewOrderDetails(order)"
                  class="text-indigo-600 hover:text-indigo-900"
                >
                  View Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- <div>
        <h1>Order #{{ order.id }}</h1>
        <div v-for="item in order.items" :key="item.id">
          <p>Design: {{ item.design.prompt }}</p>
          <img :src="item.design.image_url" alt="Design Preview" />
        </div>
      </div> -->

      <!-- ページネーション -->
      <div class="mt-4 flex justify-between items-center">
        <div class="text-sm text-gray-700">
          Showing {{ (currentPage - 1) * perPage + 1 }} to {{ Math.min(currentPage * perPage, totalItems) }} of {{ totalItems }} orders
        </div>
        <div class="flex space-x-2">
          <button 
            @click="prevPage" 
            :disabled="currentPage === 1"
            class="px-3 py-1 border rounded-md hover:bg-gray-100 disabled:opacity-50"
          >
            Previous
          </button>
          <button
            @click="nextPage"
            :disabled="currentPage >= totalPages"
            class="px-3 py-1 border rounded-md hover:bg-gray-100 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- 注文詳細モーダル -->
<div v-if="selectedOrder" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center overflow-y-auto">
  <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 my-8 relative">
    <!-- ヘッダー部分 -->
    <div class="flex justify-between items-start mb-4">
      <h2 class="text-xl font-bold">Order Details #{{ selectedOrder.id }}</h2>
      <button 
        @click="selectedOrder = null" 
        class="text-gray-400 hover:text-gray-500 text-2xl"
      >
        ×
      </button>
    </div>

    <!-- スクロール可能なコンテンツエリア -->
    <div class="max-h-[70vh] overflow-y-auto pr-2">
      <!-- 顧客情報と配送先情報 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div class="bg-gray-50 p-4 rounded">
          <h3 class="font-semibold text-gray-700 mb-2">Customer Information</h3>
          <p>{{ selectedOrder.user?.email }}</p>
        </div>
        <div class="bg-gray-50 p-4 rounded">
          <h3 class="font-semibold text-gray-700 mb-2">Shipping Address</h3>
          <p>{{ selectedOrder.shipping_address?.name }}</p>
          <p>{{ selectedOrder.shipping_address?.address1 }}</p>
          <p>{{ selectedOrder.shipping_address?.city }}, {{ selectedOrder.shipping_address?.prefecture }}</p>
          <p>{{ selectedOrder.shipping_address?.postal_code }}</p>
        </div>
      </div>

      <!-- 注文アイテム -->
      <div class="bg-white">
        <h3 class="font-semibold text-gray-700 mb-4">Order Items</h3>
        <div class="space-y-4">
          <div 
            v-for="item in selectedOrder.items" 
            :key="item.id" 
            class="border rounded-lg p-4"
          >
            <div class="flex flex-col md:flex-row md:justify-between md:items-center gap-4">
              <div class="flex flex-col md:flex-row gap-4">
                <!-- 画像 -->
                <div class="w-32 h-32 flex-shrink-0">
                  <img 
                    :src="item.design.image_url" 
                    :alt="item.design.prompt"
                    class="w-full h-full object-cover rounded-lg border"
                    @error="handleImageError"
                  />
                </div>
                <!-- 商品詳細 -->
                <div>
                  <p class="font-medium">{{ item.design.prompt }}</p>
                  <p class="text-sm text-gray-600 mt-1">
                    Size: {{ item.size }}, Color: {{ item.color }}
                  </p>
                </div>
              </div>
              <!-- 価格情報 -->
              <div class="text-right">
                <p class="font-medium">{{ item.quantity }} x ¥{{ item.price?.toLocaleString() ?? '2,000' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 合計金額 -->
      <div class="mt-6 border-t pt-4">
        <p class="text-right font-semibold text-lg">
          Total: ¥{{ selectedOrder.total_amount.toLocaleString() }}
        </p>
      </div>
    </div>
  </div>
</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
// 修正箇所
import type { Order, OrderStatus, PaginatedResponse } from '@/types/admin'

const authStore = useAuthStore()
// const orders = ref([])
// const selectedOrder = ref(null)
const orders = ref<Order[]>([])
const selectedOrder = ref<Order | null>(null)
const currentPage = ref(1)
const perPage = ref(10)
const totalItems = ref(0)
const totalPages = ref(1)

const filters = ref({
  // status: '',
  status: '' as OrderStatus | '',
  query: ''
})

// const fetchOrders = async () => {
//   try {
//     const response = await axios.get('http://localhost:5000/api/admin/orders/search', {
//       headers: { Authorization: `Bearer ${authStore.token}` },
//       params: {
//         page: currentPage.value,
//         per_page: perPage.value,
//         status: filters.value.status,
//         query: filters.value.query
//       }
//     })
    
//     orders.value = response.data.orders
//     totalItems.value = response.data.total
//     totalPages.value = response.data.pages
//   } catch (error) {
//     console.error('Failed to fetch orders:', error)
//   }
// }

interface PaginatedResponse<T> {
    orders: T[];  // dataではなくordersとして定義
    total: number;
    pages: number;
}

// 修正箇所
const fetchOrders = async () => {
    try {
        const response = await axios.get<PaginatedResponse<Order>>('http://localhost:5000/api/admin/orders/search', {
            headers: { Authorization: `Bearer ${authStore.token}` },
            params: {
                page: currentPage.value,
                per_page: perPage.value,
                status: filters.value.status,
                query: filters.value.query
            }
        })
        
        orders.value = response.data.orders
        totalItems.value = response.data.total
        totalPages.value = response.data.pages
    } catch (error) {
        console.error('Failed to fetch orders:', error)
    }
}

// const updateOrderStatus = async (order) => {
//   try {
//     await axios.put(
//       `http://localhost:5000/api/admin/orders/${order.id}/status`,
//       { status: order.status },
//       { headers: { Authorization: `Bearer ${authStore.token}` } }
//     )
//   } catch (error) {
//     console.error('Failed to update order status:', error)
//   }
// }

// 修正箇所
const updateOrderStatus = async (order: Order) => {
    try {
        await axios.put(
            `http://localhost:5000/api/admin/orders/${order.id}/status`,
            { status: order.status },
            { headers: { Authorization: `Bearer ${authStore.token}` } }
        )
    } catch (error) {
        console.error('Failed to update order status:', error)
    }
}

const viewOrderDetails = async (order: Order) => {
  try {
    const response = await axios.get<Order>(
      `http://localhost:5000/api/admin/orders/${order.id}`,
      { headers: { Authorization: `Bearer ${authStore.token}` } }
    )
    selectedOrder.value = response.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Failed to fetch order details:', error.response?.data)
    } else {
      console.error('An unexpected error occurred:', error)
    }
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchOrders()
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchOrders()
  }
}

const handleImageError = (e: Event) => {
  const target = e.target as HTMLImageElement;
  target.src = '/placeholder-image.png' // プレースホルダー画像のパスに変更してください
  console.error('Image failed to load:', target.src)
}

onMounted(() => {
  fetchOrders()
})
</script>