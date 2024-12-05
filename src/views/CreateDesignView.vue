<!-- src/views/CreateDesignView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-3xl font-bold mb-8">{{ $t('createDesign.title') }}</h1>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 左側: デザイン生成フォーム -->
        <div class="space-y-6">
          <!-- デザイン生成フォーム -->
          <div class="bg-white rounded-lg shadow p-6">
            <form @submit.prevent="generateDesign" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ $t('createDesign.describeDesign') }}
                </label>
                <textarea
                  v-model="prompt"
                  class="w-full h-32 p-3 border border-gray-300 rounded-md"
                  :placeholder="$t('createDesign.placeholder')"
                  required
                ></textarea>
              </div>
              
              <button
                type="submit"
                class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 disabled:opacity-50"
                :disabled="isLoading"
              >
                {{ isLoading ? $t('createDesign.generating') : $t('createDesign.generate') }}
              </button>
            </form>
          </div>

          <!-- 生成されたデザイン（オリジナル） -->
          <div v-if="generatedDesign" class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold mb-4">{{ $t('createDesign.originalDesign') }}</h2>
            <div class="relative aspect-square mb-4">
              <img
                :src="generatedDesign.image_url"
                :alt="$t('createDesign.originalDesign')"
                class="w-full h-full object-contain rounded-md"
              />
            </div>
          </div>

          <!-- エラーメッセージ -->
          <div
            v-if="error"
            class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
          >
            {{ error }}
          </div>
        </div>

        <!-- 右側: プレビューとカスタマイズ -->
        <div v-if="generatedDesign" class="space-y-6">
          <!-- Tシャツプレビュー -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold mb-4">{{ $t('createDesign.preview') }}</h2>
            <TShirtPreview
              :design-image="generatedDesign.image_url"
              :initial-config="designConfig"
              @update:designConfig="updateDesignConfig"
            />
          </div>

          <!-- 注文オプション -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold mb-4">{{ $t('createDesign.orderOptions') }}</h2>
            <div class="space-y-4">
              <!-- サイズ選択 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ $t('createDesign.size') }}
                </label>
                <select
                  v-model="size"
                  class="w-full p-2 border border-gray-300 rounded-md"
                >
                  <option value="S">Small</option>
                  <option value="M">Medium</option>
                  <option value="L">Large</option>
                  <option value="XL">Extra Large</option>
                </select>
              </div>

              <!-- カラー選択 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ $t('createDesign.color') }}
                </label>
                <div class="flex gap-4">
                  <button
                    v-for="c in ['White', 'Black']"
                    :key="c"
                    @click="color = c"
                    :class="[
                      'w-12 h-12 rounded-full border-2 transition-all',
                      color === c ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-300'
                    ]"
                    :style="{
                      backgroundColor: c.toLowerCase(),
                      color: c === 'White' ? 'black' : 'white'
                    }"
                  />
                </div>
              </div>

              <button
                @click="addToCart"
                class="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700"
              >
                {{ $t('createDesign.addToCart') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import TShirtPreview from '@/components/TShirtPreview.vue'
import type { DesignConfig } from '@/types/cart'

const { t } = useI18n()
const authStore = useAuthStore()
const router = useRouter()

// フォームの状態
const prompt = ref('')
const size = ref('M')
const color = ref('White')
const isLoading = ref(false)
const error = ref('')
const generatedDesign = ref<any>(null)

// デザイン設定
const designConfig = ref<DesignConfig>({
  color: 'white',
  position: { x: 50, y: 50 },
  scale: 1,
  rotation: 0
})

// デザイン生成
const generateDesign = async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    const response = await axios.post('http://localhost:5000/api/designs/generate', {
      prompt: prompt.value
    }, {
      headers: {
        Authorization: `Bearer ${authStore.token}`
      }
    })
    
    generatedDesign.value = response.data.design
  } catch (e) {
    error.value = 'Failed to generate design. Please try again.'
    console.error('Error generating design:', e)
  } finally {
    isLoading.value = false
  }
}

// デザイン設定の更新
const updateDesignConfig = (config: DesignConfig) => {
  designConfig.value = config
  color.value = config.color === 'white' ? 'White' : 'Black'
}

// カートに追加する際のデータ形式を修正
const addToCart = async () => {
  if (!generatedDesign.value) return

  try {
    const cartData = {
      design_id: generatedDesign.value.id,
      quantity: 1,
      size: size.value,
      color: color.value,
      design_config: {
        position: {
          x: designConfig.value.position.x,
          y: designConfig.value.position.y
        },
        scale: designConfig.value.scale,
        rotation: designConfig.value.rotation
      }
    }

    console.log('Adding to cart with config:', cartData)

    await axios.post(
      'http://localhost:5000/api/cart/add',
      cartData,
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`
        }
      }
    )
    
    router.push('/cart')
  } catch (e) {
    error.value = 'Failed to add item to cart. Please try again.'
    console.error('Error adding to cart:', e)
  }
}
</script>
