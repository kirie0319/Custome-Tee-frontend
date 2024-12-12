<!-- src/views/AdminDashboard.vue -->
<template>
  <div class="min-h-screen bg-gray-100">
    <!-- ヘッダー -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
      </div>
    </header>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- 統計サマリー -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <DollarSignIcon class="h-6 w-6 text-gray-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dt class="text-sm font-medium text-gray-500 truncate">
                  Total Sales
                </dt>
                <dd class="text-lg font-medium text-gray-900">
                  ¥{{ stats.total_sales.toLocaleString() }}
                </dd>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <ShoppingBagIcon class="h-6 w-6 text-gray-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dt class="text-sm font-medium text-gray-500 truncate">
                  Total Orders
                </dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ stats.total_orders }}
                </dd>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <UsersIcon class="h-6 w-6 text-gray-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dt class="text-sm font-medium text-gray-500 truncate">
                  Total Users
                </dt>
                <dd class="text-lg font-medium text-gray-900">
                  {{ stats.total_users }}
                </dd>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 最近の注文 -->
      <div class="mt-8">
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
            <h2 class="text-lg font-medium text-gray-900">Recent Orders</h2>
            <router-link
              to="/admin/orders"
              class="text-sm text-blue-600 hover:text-blue-500"
            >
              View all
            </router-link>
          </div>
          <div class="border-t border-gray-200">
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
                    Amount
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="order in stats.recent_orders" :key="order.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    #{{ order.id }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ order.user?.email }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ¥{{ order.total_amount.toLocaleString() }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" 
                      :class="getStatusClass(order.status)">
                      {{ order.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ new Date(order.created_at).toLocaleDateString() }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import { DollarSignIcon, ShoppingBagIcon, UsersIcon } from 'lucide-react'
import type { Order, OrderStatus } from '@/types/order'

const router = useRouter()
const authStore = useAuthStore()
interface DashboardStats {
    total_sales: number
    total_orders: number
    total_users: number
    recent_orders: Order[]
}

const stats = ref<DashboardStats>({
    total_sales: 0,
    total_orders: 0,
    total_users: 0,
    recent_orders: []
})

// ステータスに応じたクラスを返す
const getStatusClass = (status: OrderStatus) => {
  const classes = {
    paid: 'bg-blue-100 text-blue-800',
    processing: 'bg-yellow-100 text-yellow-800',
    shipped: 'bg-green-100 text-green-800',
    delivered: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800'
  } as const
  return classes[status] || 'bg-gray-100 text-gray-800'
}

// 統計データの取得
const fetchStats = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/admin/stats', {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    stats.value = response.data
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
}

onMounted(() => {
  if (!authStore.isAdmin) {
    router.push('/')
    return
  }
  fetchStats()
})
</script>