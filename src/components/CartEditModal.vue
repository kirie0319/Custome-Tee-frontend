<!-- src/components/CartEditModal.vue -->
<template>
  <div v-if="modelValue" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
    <div class="bg-white rounded-lg p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-bold">デザインの編集</h2>
        <button @click="$emit('update:modelValue', false)" class="text-gray-500 hover:text-gray-700">
          <span class="text-2xl">&times;</span>
        </button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- プレビュー -->
        <div>
          <TShirtPreview
            :design-image="item.design.image_url"
            :initial-config="item.design_config"
            @update:designConfig="updateDesignConfig"
          />
        </div>

        <!-- 注文オプション -->
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              サイズ
            </label>
            <select
              v-model="editedItem.size"
              class="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="S">Small</option>
              <option value="M">Medium</option>
              <option value="L">Large</option>
              <option value="XL">Extra Large</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              数量
            </label>
            <input
              type="number"
              v-model="editedItem.quantity"
              min="1"
              class="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>

          <div class="flex space-x-4">
            <button
              @click="saveChanges"
              class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
            >
              変更を保存
            </button>
            <button
              @click="$emit('update:modelValue', false)"
              class="flex-1 bg-gray-200 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-300"
            >
              キャンセル
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import TShirtPreview from './TShirtPreview.vue'
import type { DesignConfig } from '@/types/cart'
import { useCartStore } from '@/stores/cart'

const props = defineProps<{
  modelValue: boolean
  item: any
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'item-updated': [itemId: number]
}>()

const cartStore = useCartStore()
const editedItem = ref({ ...props.item })
const designConfig = ref<DesignConfig | null>(null)

onMounted(() => {
  if (props.item.design_config) {
    designConfig.value = props.item.design_config
  }
})

const updateDesignConfig = (config: DesignConfig) => {
  designConfig.value = config
}

const saveChanges = async () => {
  try {
    await cartStore.updateCartItem(props.item.id, {
      quantity: editedItem.value.quantity,
      size: editedItem.value.size,
      color: designConfig.value?.color || editedItem.value.color,
      design_config: designConfig.value
    })

    emit('item-updated', props.item.id)
    emit('update:modelValue', false)
  } catch (error) {
    console.error('Failed to update cart item:', error)
  }
}
</script>