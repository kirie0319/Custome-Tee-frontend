<!-- src/views/LoginView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow">
      <div class="text-center">
        <h2 class="text-3xl font-bold">{{ $t('login.title') }}</h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">
            {{ $t('login.username') }}
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
            {{ $t('login.password') }}
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
          {{ $t(`login.error.${error}`) }}
        </div>

        <button
          type="submit"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
          :disabled="loading"
        >
          {{ loading ? $t('common.processing') : $t('login.submit') }}
        </button>
      </form>

      <div class="text-center">
        <router-link
          to="/register"
          class="text-sm text-indigo-600 hover:text-indigo-500"
        >
          {{ $t('login.registerLink') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const success = await authStore.login(username.value, password.value)
    if (success) {
      router.push('/')
    } else {
      error.value = 'Invalid username or password'
    }
  } catch (e) {
    error.value = 'An error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>