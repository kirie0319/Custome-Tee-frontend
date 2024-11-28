<!-- src/views/RegisterView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold mb-8">Register</h1>

      <!-- 登録フォーム -->
      <div class="bg-white rounded-lg shadow p-6">
        <form @submit.prevent="handleRegister" class="space-y-6">
          <!-- 基本情報 -->
          <div class="space-y-4">
            <h2 class="text-xl font-semibold mb-4">Basic Information</h2>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Username *
              </label>
              <input
                v-model="form.username"
                type="text"
                required
                class="w-full p-2 border border-gray-300 rounded-md"
                :class="{ 'border-red-500': v$.username.$error }"
              />
              <span v-if="v$.username.$error" class="text-sm text-red-500">
                {{ v$.username.$errors[0].$message }}
              </span>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Email *
              </label>
              <input
                v-model="form.email"
                type="email"
                required
                class="w-full p-2 border border-gray-300 rounded-md"
                :class="{ 'border-red-500': v$.email.$error }"
              />
              <span v-if="v$.email.$error" class="text-sm text-red-500">
                {{ v$.email.$errors[0].$message }}
              </span>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Password *
              </label>
              <input
                v-model="form.password"
                type="password"
                required
                class="w-full p-2 border border-gray-300 rounded-md"
                :class="{ 'border-red-500': v$.password.$error }"
              />
              <span v-if="v$.password.$error" class="text-sm text-red-500">
                {{ v$.password.$errors[0].$message }}
              </span>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Confirm Password *
              </label>
              <input
                v-model="form.confirmPassword"
                type="password"
                required
                class="w-full p-2 border border-gray-300 rounded-md"
                :class="{ 'border-red-500': v$.confirmPassword.$error }"
              />
              <span v-if="v$.confirmPassword.$error" class="text-sm text-red-500">
                {{ v$.confirmPassword.$errors[0].$message }}
              </span>
            </div>
          </div>

          <!-- デフォルトの配送情報 -->
          <div class="space-y-4">
            <h2 class="text-xl font-semibold mb-4">Default Shipping Information (Optional)</h2>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Full Name
              </label>
              <input
                v-model="form.shipping.name"
                type="text"
                class="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Address
              </label>
              <input
                v-model="form.shipping.address"
                type="text"
                class="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                City
              </label>
              <input
                v-model="form.shipping.city"
                type="text"
                class="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Postal Code
              </label>
              <input
                v-model="form.shipping.postalCode"
                type="text"
                class="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Country
              </label>
              <input
                v-model="form.shipping.country"
                type="text"
                class="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>
          </div>

          <!-- 登録ボタン -->
          <button
            type="submit"
            class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 disabled:opacity-50"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Registering...' : 'Register' }}
          </button>

          <!-- エラーメッセージ -->
          <div
            v-if="error"
            class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
          >
            {{ error }}
          </div>
        </form>

        <!-- ログインへのリンク -->
        <div class="mt-4 text-center">
          <p class="text-sm text-gray-600">
            Already have an account?
            <router-link to="/login" class="text-indigo-600 hover:text-indigo-500">
              Login here
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength, sameAs } from '@vuelidate/validators'

const router = useRouter()
const authStore = useAuthStore()
const isLoading = ref(false)
const error = ref('')

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  shipping: {
    name: '',
    address: '',
    city: '',
    postalCode: '',
    country: ''
  }
})

// バリデーションルール
const rules = computed(() => ({
  username: { required, minLength: minLength(3) },
  email: { required, email },
  password: { required, minLength: minLength(8) },
  confirmPassword: { 
    required,
    sameAsPassword: sameAs(form.password)
  }
}))

const v$ = useVuelidate(rules, form)

const handleRegister = async () => {
  error.value = ''

  try {
    // バリデーションチェック
    const result = await v$.value.$validate()
    if (!result) {
      error.value = 'Please check the form for errors'
      return
    }

    isLoading.value = true
    const registrationData = {
      username: form.username,
      email: form.email,
      password: form.password,
      default_shipping_info: Object.values(form.shipping).some(value => value)
        ? {
            name: form.shipping.name,
            address: form.shipping.address,
            city: form.shipping.city,
            postal_code: form.shipping.postalCode,
            country: form.shipping.country
          }
        : null
    }

    console.log('Registering with data:', registrationData)  // デバッグ用
    await authStore.register(registrationData)
    router.push('/login')
  } catch (e: any) {
    console.error('Registration error:', e)  // デバッグ用
    error.value = e.response?.data?.error || 'Registration failed'
  } finally {
    isLoading.value = false
  }
}
</script>