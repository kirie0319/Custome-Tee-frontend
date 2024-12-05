<!-- src/views/CartItemEditView.vue -->
<template>
  <div :key="componentKey" class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-6xl mx-auto">
      <!-- ヘッダー -->
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-bold">{{ $t('cart_edit.title') }}</h1>
        <button
          @click="router.push('/cart')"
          class="text-gray-600 hover:text-gray-800 flex items-center"
        >
          <span class="mr-2">&larr;</span> {{ $t('cart_edit.backToCart') }}
        </button>
      </div>

      <!-- ローディング表示 -->
      <div v-if="cartStore.loading" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
      </div>

      <!-- エラー表示 -->
      <div
        v-else-if="cartStore.error"
        class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
      >
        {{ cartStore.error }}
      </div>

      <!-- メインコンテンツ -->
      <div v-else-if="cartItem" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 左側: プレビューと位置調整 -->
        <div class="space-y-6">
          <div class="bg-white rounded-lg shadow p-6">
            <TShirtPreview
              :design-image="cartItem.design.image_url"
              :initial-config="designConfig"
              @update:designConfig="updateDesignConfig"
            />
          </div>
        </div>

        <!-- 右側: 商品情報とオプション -->
        <div class="space-y-6">
          <!-- 商品詳細 -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold mb-4">{{ $t('cart_edit.productDetails') }}</h2>
            <p class="text-gray-600 mb-6">{{ cartItem.design.prompt }}</p>

            <!-- オプション選択 -->
            <div class="space-y-6">
              <!-- サイズ選択 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ $t('cart_edit.size') }}
                </label>
                <select
                  v-model="editedItem.size"
                  class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="S">{{ $t('cart_edit.sizes.small') }}</option>
                  <option value="M">{{ $t('cart_edit.sizes.medium') }}</option>
                  <option value="L">{{ $t('cart_edit.sizes.large') }}</option>
                  <option value="XL">{{ $t('cart_edit.sizes.extraLarge') }}</option>
                </select>
              </div>

              <!-- 数量選択 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ $t('cart_edit.quantity') }}
                </label>
                <select
                  v-model="editedItem.quantity"
                  class="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
                </select>
              </div>

              <!-- カラー選択 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ $t('cart_edit.color') }}
                </label>
                <div class="flex gap-4">
                  <button
                    v-for="color in ['White', 'Black']"
                    :key="color"
                    @click="updateColor(color)"
                    :class="[
                      'w-12 h-12 rounded-full border-2 transition-all',
                      editedItem.color === color ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-300'
                    ]"
                    :style="{
                      backgroundColor: color.toLowerCase(),
                      color: color === 'White' ? 'black' : 'white'
                    }"
                  ></button>
                </div>
              </div>
            </div>
          </div>

          <!-- 価格表示 -->
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex justify-between items-center">
              <span class="text-lg font-medium">{{ $t('cart_edit.price') }}:</span>
              <span class="text-2xl font-bold">¥{{ 2000 * editedItem.quantity }}</span>
            </div>
          </div>

          <!-- アクションボタン -->
          <div class="flex gap-4">
            <button
              @click="saveChanges"
              class="flex-1 bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="isSaving || !hasChanges"
            >
              {{ isSaving ? $t('cart_edit.actions.saving') : $t('cart_edit.actions.save') }}
            </button>
            <button
              @click="router.push('/cart')"
              class="flex-1 bg-gray-200 text-gray-700 py-3 px-4 rounded-md hover:bg-gray-300"
              :disabled="isSaving"
            >
              {{ $t('cart_edit.actions.cancel') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import TShirtPreview from '@/components/TShirtPreview.vue'
import type { DesignConfig } from '@/types/cart'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const componentKey = ref(0)
const cartItem = ref<any>(null)
const editedItem = ref<any>(null)
const designConfig = ref<DesignConfig | null>(null)
const isSaving = ref(false)

// Tシャツの色が変更された時の処理
const updateColor = async (color: string) => {
  editedItem.value.color = color
  designConfig.value = {
    ...designConfig.value,
    color: color.toLowerCase()
  }
  componentKey.value++
}

// 初期データの取得
const fetchCartItem = async () => {
  try {
    const data = await cartStore.getCartItem(Number(route.params.id))
    cartItem.value = data
    editedItem.value = {
      size: data.size,
      quantity: data.quantity,
      color: data.color
    }
    designConfig.value = {
      color: data.color.toLowerCase(),
      position: data.design_config?.position || { x: 50, y: 50 },
      scale: Number(data.design_config?.scale || 1),
      rotation: Number(data.design_config?.rotation || 0)
    }
    componentKey.value++
  } catch (error) {
    console.error('Error:', error)
  }
}

// デザイン設定の更新
const updateDesignConfig = (config: DesignConfig) => {
  designConfig.value = {
    ...config,
    color: editedItem.value.color.toLowerCase()
  }
  componentKey.value++
}

// 保存処理
const saveChanges = async () => {
  if (!hasChanges.value) return
  isSaving.value = true
  try {
    await cartStore.updateCartItem(Number(route.params.id), {
      size: editedItem.value.size,
      quantity: editedItem.value.quantity,
      color: editedItem.value.color,
      design_config: designConfig.value
    })
    router.push('/cart')
  } catch (error) {
    console.error('Error saving changes:', error)
  } finally {
    isSaving.value = false
  }
}

// 変更の検知
const hasChanges = computed(() => {
  if (!cartItem.value || !editedItem.value) return false
  return (
    JSON.stringify(designConfig.value) !== JSON.stringify(cartItem.value.design_config) ||
    editedItem.value.size !== cartItem.value.size ||
    editedItem.value.quantity !== cartItem.value.quantity ||
    editedItem.value.color !== cartItem.value.color
  )
})

// 初期化
onMounted(() => {
  fetchCartItem()
})
</script>
