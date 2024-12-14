<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold mb-8">{{ $t('register.title') }}</h1>

      <!-- 登録フォーム -->
      <div class="bg-white rounded-lg shadow p-6">
        <form @submit.prevent="handleRegister" class="space-y-6">
          <!-- 基本情報 -->
          <div class="space-y-4">
            <h2 class="text-xl font-semibold mb-4">{{ $t('register.basicInfo.title') }}</h2>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ $t('register.basicInfo.username') }} *
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

            <!-- 他のフィールドも同様に修正... -->
            <!-- Email -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ $t('register.basicInfo.email') }} *
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

            <!-- Password -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ $t('register.basicInfo.password') }} *
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

            <!-- Confirm Password -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ $t('register.basicInfo.confirmPassword') }} *
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

          <!-- 登録ボタン -->
          <button
            type="submit"
            class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 disabled:opacity-50"
            :disabled="isLoading"
          >
            {{ isLoading ? $t('register.submit.loading') : $t('register.submit.default') }}
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
            {{ $t('register.login.text') }}
            <router-link to="/login" class="text-indigo-600 hover:text-indigo-500">
              {{ $t('register.login.link') }}
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
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength, sameAs } from '@vuelidate/validators'

const { t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()
const isLoading = ref(false)
const error = ref('')

// フォームの状態
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

// バリデーションメッセージをi18n対応に
const validationMessages = computed(() => ({
  required: () => t('register.validation.required'),
  minLength: (params: any) => t('register.validation.minLength', { n: params.$params.min }),
  email: () => t('register.validation.email'),
  sameAsPassword: () => t('register.validation.passwordMatch')
}))

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

// const v$ = useVuelidate(rules, form, { $messages: validationMessages.value })
// const v$ = useVuelidate(rules, form, { 
//   globalConfig: { 
//     messages: validationMessages.value 
//   } 
// })
const v$ = useVuelidate(rules, form, { 
  $messages: validationMessages.value 
})

// 登録処理
const handleRegister = async () => {
  error.value = ''

  try {
    const result = await v$.value.$validate()
    if (!result) {
      error.value = t('register.validation.formError')
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

    await authStore.register(registrationData)
    router.push('/login')
  } catch (e: any) {
    error.value = e.response?.data?.error || t('register.error.default')
  } finally {
    isLoading.value = false
  }
}
</script>