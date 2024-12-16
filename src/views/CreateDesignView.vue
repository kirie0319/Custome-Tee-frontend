<!-- src/views/CreateDesignView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 pb-20">
    <!-- ヘッダー -->
    <header class="bg-white p-4 shadow-sm sticky top-0 z-10">
      <div class="flex items-center">
        <button @click="router.push('/')" class="p-2 -ml-2">
          <ChevronLeft class="h-6 w-6" />
        </button>
        <h1 class="text-xl font-bold flex-1 text-center">デザインを作成</h1>
        <div class="w-10"></div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="p-4 space-y-6">
      <!-- エラーメッセージ -->
      <div
        v-if="error"
        class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
      >
        {{ error }}
      </div>

      <!-- デザイン作成フォーム -->
      <div class="bg-white rounded-lg shadow p-6">
        <form @submit.prevent="generateDesign" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              デザインの説明（英語でお願いします）
            </label>
            <textarea
              v-model="prompt"
              class="w-full h-32 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="例: 夕暮れの山々を現代的でミニマルなスタイルで"
              required
            />
          </div>

          <button
            type="submit"
            class="w-full bg-indigo-600 text-white py-4 rounded-lg font-bold hover:bg-indigo-700 transition-colors"
            :disabled="isLoading"
            :class="{ 'opacity-50 cursor-not-allowed': isLoading }"
          >
            <div class="flex items-center justify-center">
              <Loader2 v-if="isLoading" class="w-5 h-5 animate-spin mr-2" />
              <span>{{ isLoading ? 'デザインを生成中...' : 'AIでデザインを生成' }}</span>
            </div>
          </button>
        </form>
      </div>

      <!-- デザイン生成結果 -->
      <div v-if="generatedDesign" class="space-y-6">
        <!-- プレビュー -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold mb-4">プレビュー</h3>
          <TShirtPreview
            :design-image="generatedDesign.image_url"
            :initial-config="designConfig"
            @update:designConfig="updateDesignConfig"
          />
        </div>

        <!-- 商品オプション -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold mb-4">オプション</h3>
          <div class="space-y-6">
            <!-- サイズ選択 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2"> サイズ </label>
              <div class="grid grid-cols-4 gap-2">
                <button
                  v-for="s in ['S', 'M', 'L', 'XL']"
                  :key="s"
                  @click="size = s"
                  class="py-2 rounded-md border transition-colors"
                  :class="[
                    size === s
                      ? 'border-indigo-600 bg-indigo-50 text-indigo-600'
                      : 'border-gray-300 hover:border-gray-400',
                  ]"
                >
                  {{ s }}
                </button>
              </div>
            </div>

            <!-- カラー選択 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2"> カラー </label>
              <div class="flex gap-4">
                <button
                  v-for="c in ['White', 'Black']"
                  :key="c"
                  @click="updateColor(c)"
                  class="w-12 h-12 rounded-full border-2 transition-all relative"
                  :class="[
                    color === c
                      ? 'border-indigo-600 ring-2 ring-indigo-200'
                      : 'border-gray-300 hover:border-gray-400',
                  ]"
                  :style="{ backgroundColor: c.toLowerCase() }"
                >
                  <Check
                    v-if="color === c"
                    class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-6 h-6"
                    :class="c === 'White' ? 'text-gray-800' : 'text-white'"
                  />
                </button>
              </div>
            </div>

            <!-- カートに追加ボタン -->
            <button
              @click="addToCart"
              class="w-full bg-indigo-600 text-white py-4 rounded-lg font-bold hover:bg-indigo-700 transition-colors flex items-center justify-center"
              :disabled="isAddingToCart"
              :class="{ 'opacity-50 cursor-not-allowed': isAddingToCart }"
            >
              <Loader2 v-if="isAddingToCart" class="w-5 h-5 animate-spin mr-2" />
              <span>{{ isAddingToCart ? 'カートに追加中...' : 'カートに追加' }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- デザインのヒント -->
      <div class="bg-white rounded-lg shadow p-4">
        <h3 class="font-semibold text-gray-700 mb-2">デザインのヒント</h3>
        <ul class="text-sm text-gray-600 space-y-2">
          <li class="flex items-center">
            <Dot class="w-4 h-4 text-gray-400" />
            できるだけ具体的な説明を書いてみましょう
          </li>
          <li class="flex items-center">
            <Dot class="w-4 h-4 text-gray-400" />
            アートスタイルを指定するとイメージに近づきやすいです
          </li>
          <li class="flex items-center">
            <Dot class="w-4 h-4 text-gray-400" />
            色やテイストについても記述できます
          </li>
        </ul>
      </div>
    </main>

    <!-- Footer -->
    <MobileFooter />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronLeft, Check, Loader2, Dot } from 'lucide-vue-next'
import TShirtPreview from '@/components/TShirtPreview.vue'
import MobileFooter from '@/components/MobileFooter.vue'
import { useCartStore } from '@/stores/cart'
import type { DesignConfig } from '@/types/cart'

// ロジック部分（省略なし）
const router = useRouter()
const cartStore = useCartStore()

const prompt = ref('')
const size = ref('M')
const color = ref('White')
const isLoading = ref(false)
const isAddingToCart = ref(false)
const error = ref('')
const generatedDesign = ref<any>(null)

const designConfig = ref<DesignConfig>({
  color: 'white',
  position: { x: 50, y: 50 },
  scale: 1,
  rotation: 0,
})

const updateColor = (newColor: string) => {
  color.value = newColor
  designConfig.value.color = newColor.toLowerCase()
}

const updateDesignConfig = (config: DesignConfig) => {
  designConfig.value = config
}

const generateDesign = async () => {
  error.value = ''
  try {
    isLoading.value = true
    const response = await cartStore.generateDesign(prompt.value)
    generatedDesign.value = response.design
  } catch (e: any) {
    error.value = e.response?.data?.message || 'デザインの生成に失敗しました'
    console.error('Failed to generate design:', e)
  } finally {
    isLoading.value = false
  }
}

const addToCart = async () => {
  if (!generatedDesign.value) return
  error.value = ''
  try {
    isAddingToCart.value = true
    await cartStore.addToCart({
      design_id: generatedDesign.value.id,
      quantity: 1,
      size: size.value,
      color: color.value,
      design_config: {
        color: designConfig.value.color,
        position: {
          x: designConfig.value.position.x,
          y: designConfig.value.position.y,
        },
        scale: designConfig.value.scale,
        rotation: designConfig.value.rotation,
      },
    })
    await cartStore.fetchCartItems()
    router.push('/cart')
  } catch (e: any) {
    error.value = e.response?.data?.message || 'カートへの追加に失敗しました'
    console.error('Failed to add to cart:', e)
  } finally {
    isAddingToCart.value = false
  }
}
</script>
