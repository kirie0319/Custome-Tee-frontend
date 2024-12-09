<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow">
      <div class="text-center">
        <h2 class="text-3xl font-bold">Admin Login Page</h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">
            Admin User Name
          </label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">
            Admin Password
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm"
          />
        </div>

        <div v-if="error" class="text-red-500 text-sm">
          {{ error }}
        </div>

        <button
          type="submit"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
          :disabled="loading"
        >
          <span v-if="loading">Signing in...</span>
          <span v-else>Sign in as Admin</span>
        </button>

        <div class="flex items-center justify-start space-x-2 text-sm">
          <ArrowLeftIcon class="w-4 h-4" />
          <a href="/" class="text-indigo-600 hover:text-indigo-500">
            Return to Home
          </a>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ArrowLeftIcon } from 'lucide-react'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

onMounted(async () => {
  // すでに管理者としてログインしている場合は
  // ダッシュボードにリダイレクト
  if (authStore.isAdmin) {
    router.push('/admin')
  }
})

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  
  try {
    await authStore.login(username.value, password.value)
    
    // ログイン成功後、管理者権限をチェック
    if (authStore.isAdmin) {
      router.push('/admin')
    } else {
      error.value = 'This account does not have administrator privileges.'
      await authStore.logout()
    }
  } catch (e) {
    if (e instanceof Error) {
      error.value = 'Invalid credentials. Please check your username and password.'
    } else {
      error.value = 'An unexpected error occurred. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>