<!-- src/views/HomeView.vue -->
<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-bold">CustomAI Tee</h1>
          </div>
          <div class="flex items-center">
            <div v-if="authStore.isAuthenticated" class="flex items-center">
              <!-- 管理者ダッシュボードリンク -->
              <router-link 
                v-if="authStore.isAdmin"
                to="/admin"
                class="mr-4 flex items-center text-gray-600 hover:text-gray-900"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                </svg>
                <span class="ml-1">Admin Dashboard</span>
              </router-link>
              
              <!-- カートリンク (管理者以外に表示) -->
              <router-link 
                v-if="!authStore.isAdmin"
                to="/cart"
                class="mr-4 flex items-center text-gray-600 hover:text-gray-900"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span class="ml-1">Cart</span>
              </router-link>

              <div class="flex items-center space-x-4">
                <span class="text-gray-700">
                  Welcome, 
                  <span class="font-semibold">
                    {{ authStore.user?.username }}
                    <span v-if="authStore.isAdmin" class="text-indigo-600">(Admin)</span>
                  </span>
                </span>
                <button 
                  @click="handleLogout"
                  class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                >
                  Logout
                </button>
              </div>
            </div>
            <router-link 
              v-else 
              to="/login"
              class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Login
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- 管理者向けコンテンツ -->
      <div v-if="authStore.isAuthenticated && authStore.isAdmin">
        <h2 class="text-2xl font-bold mb-4">Admin Controls</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div class="bg-white p-6 rounded-lg shadow">
            <h3 class="text-lg font-semibold mb-2">Dashboard</h3>
            <p class="text-gray-600">View sales and analytics</p>
            <router-link 
              to="/admin"
              class="mt-4 inline-block bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
            >
              Go to Dashboard
            </router-link>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <h3 class="text-lg font-semibold mb-2">Orders Management</h3>
            <p class="text-gray-600">Manage customer orders</p>
            <router-link 
              to="/admin/orders"
              class="mt-4 inline-block bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
            >
              Manage Orders
            </router-link>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <h3 class="text-lg font-semibold mb-2">User Management</h3>
            <p class="text-gray-600">Manage user accounts</p>
            <router-link 
              to="/admin/users"
              class="mt-4 inline-block bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
            >
              Manage Users
            </router-link>
          </div>
        </div>
      </div>

      <!-- 一般ユーザー向けコンテンツ -->
      <div v-else-if="authStore.isAuthenticated">
        <h2 class="text-2xl font-bold mb-4">Dashboard</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="bg-white p-6 rounded-lg shadow">
            <h3 class="text-lg font-semibold mb-2">Create Design</h3>
            <p class="text-gray-600">Generate custom T-shirt designs with AI</p>
            <router-link 
              to="/create-design"
              class="mt-4 inline-block bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
            >
              Start Creating
            </router-link>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <h3 class="text-lg font-semibold mb-2">My Designs</h3>
            <p class="text-gray-600">View and manage your designs</p>
            <router-link 
              to="/my-designs"
              class="mt-4 inline-block bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
            >
              View Designs
            </router-link>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <h3 class="text-lg font-semibold mb-2">Orders</h3>
            <p class="text-gray-600">View your order history</p>
            <router-link 
              to="/orders"
              class="mt-4 inline-block bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
            >
              View Orders
            </router-link>
          </div>
          <div class="bg-white p-6 rounded-lg shadow">
            <h3 class="text-lg font-semibold mb-2">Shopping Cart</h3>
            <p class="text-gray-600">View and edit your cart items</p>
            <router-link 
              to="/cart"
              class="mt-4 inline-block bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
            >
              View Cart
            </router-link>
          </div>
        </div>
      </div>

      <!-- 未ログインユーザー向けコンテンツ -->
      <div v-else class="text-center py-12">
        <h2 class="text-3xl font-bold mb-4">Welcome to CustomAI Tee</h2>
        <p class="text-xl text-gray-600 mb-8">Create unique T-shirt designs with AI</p>
        <div class="space-y-4">
          <router-link 
            to="/login"
            class="block bg-blue-500 text-white px-6 py-3 rounded-lg text-lg hover:bg-blue-600 w-64 mx-auto"
          >
            Login as User
          </router-link>
          <router-link 
            to="/login?admin=true"
            class="block bg-indigo-500 text-white px-6 py-3 rounded-lg text-lg hover:bg-indigo-600 w-64 mx-auto"
          >
            Login as Admin
          </router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>