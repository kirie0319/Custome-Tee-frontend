<!-- TShirtPreview.vue -->
<template>
  <div class="relative w-full max-w-2xl mx-auto bg-white p-4">
    <!-- Tシャツ背景画像 -->
    <div class="relative aspect-[3/4] bg-gray-50 rounded-lg overflow-hidden shadow-sm">
      <img 
        :src="tshirtImageUrl" 
        alt="T-shirt base" 
        class="w-full h-full object-contain"
      />
      
      <!-- デザイン画像 -->
      <div
        class="absolute"
        :style="designStyle"
      >
        <img 
          :src="props.designImage" 
          :alt="$t('createDesign.preview')" 
          class="w-full h-full object-contain"
        />
      </div>
    </div>

    <!-- 位置・サイズ・回転調整 -->
    <div class="mt-6 space-y-6">
      <!-- 位置調整 -->
      <div class="space-y-4">
        <h3 class="text-sm font-medium text-gray-700">{{ $t('tshirtEdit.position.horizontal') }}</h3>
        <input
          type="range"
          v-model="position.x"
          min="20"
          max="80"
          step="1"
          class="w-full"
          @input="emitUpdate"
        />
        <h3 class="text-sm font-medium text-gray-700">{{ $t('tshirtEdit.position.vertical') }}</h3>
        <input
          type="range"
          v-model="position.y"
          min="20"
          max="80"
          step="1"
          class="w-full"
          @input="emitUpdate"
        />
      </div>

      <!-- サイズ調整 -->
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('tshirtEdit.size') }}</label>
        <input
          type="range"
          v-model="scale"
          min="0.5"
          max="2"
          step="0.1"
          class="w-full"
          @input="emitUpdate"
        />
      </div>

      <!-- 回転調整 -->
      <div>
        <label class="block text-sm font-medium text-gray-700">{{ $t('tshirtEdit.rotation') }}</label>
        <input
          type="range"
          v-model="rotation"
          min="-180"
          max="180"
          step="1"
          class="w-full"
          @input="emitUpdate"
        />
      </div>

      <!-- リセットボタン -->
      <button
        @click="resetDesign"
        class="w-full py-2 px-4 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200"
      >
        {{ $t('tshirtEdit.reset') }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import type { DesignConfig } from '@/types/design'
import { DEFAULT_DESIGN_CONFIG } from '@/types/design'

const { t } = useI18n()

// // Props の定義
// const props = defineProps<{
//   designImage: string
//   initialConfig: {
//     color: string
//     position: { x: number, y: number }
//     scale: number
//     rotation: number
//   }
// }>()
// Props の型定義を修正
const props = defineProps<{
  designImage: string
  initialConfig: DesignConfig
}>()

// const emit = defineEmits<{
//   'update:designConfig': [config: typeof props.initialConfig]
// }>()

// Emitの型定義を明確に
const emit = defineEmits<{
  'update:designConfig': [config: DesignConfig]
}>()

// // 状態管理
// const selectedColor = ref(props.initialConfig.color)
// const position = ref({ ...props.initialConfig.position })
// const scale = ref(props.initialConfig.scale)
// const rotation = ref(props.initialConfig.rotation)

// 状態管理の型付け
const selectedColor = ref<string>(props.initialConfig.color)
const position = ref<{ x: number, y: number }>(props.initialConfig.position)
const scale = ref<number>(props.initialConfig.scale)
const rotation = ref<number>(props.initialConfig.rotation)

// Tシャツ画像のURL
const tshirtImageUrl = computed(() => {
  return `/images/tshirt-${selectedColor.value.toLowerCase()}.png`
})

// デザイン画像のスタイル
const designStyle = computed(() => {
  return {
    left: `${position.value.x}%`,
    top: `${position.value.y}%`,
    transform: `translate(-50%, -50%) scale(${scale.value}) rotate(${rotation.value}deg)`,
    width: '200px'
  }
})

// カラー変更
const updateColor = (color: string) => {
  selectedColor.value = color
  emitUpdate()
}

// // 設定変更通知
// const emitUpdate = () => {
//   emit('update:designConfig', {
//     color: selectedColor.value,
//     position: position.value,
//     scale: scale.value,
//     rotation: rotation.value
//   })
// }

// 設定変更通知の型安全性を確保
const emitUpdate = () => {
  const config: DesignConfig = {
    color: selectedColor.value,
    position: position.value,
    scale: scale.value,
    rotation: rotation.value
  }
  emit('update:designConfig', config)
}

// // リセット機能
// const resetDesign = () => {
//   position.value = { x: 50, y: 50 }
//   scale.value = 1
//   rotation.value = 0
//   selectedColor.value = props.initialConfig.color
//   emitUpdate()
// }

// リセット機能を修正
const resetDesign = () => {
  const defaultConfig = { ...DEFAULT_DESIGN_CONFIG }
  position.value = defaultConfig.position
  scale.value = defaultConfig.scale
  rotation.value = defaultConfig.rotation
  selectedColor.value = defaultConfig.color
  emitUpdate()
}

// // 親からの設定更新を監視
// watch(
//   () => props.initialConfig,
//   (newConfig) => {
//     selectedColor.value = newConfig.color
//     position.value = { ...newConfig.position }
//     scale.value = newConfig.scale
//     rotation.value = newConfig.rotation
//   },
//   { deep: true }
// )

// watchの型安全性を向上
watch(
  () => props.initialConfig,
  (newConfig: DesignConfig) => {
    selectedColor.value = newConfig.color
    position.value = { ...newConfig.position }
    scale.value = newConfig.scale
    rotation.value = newConfig.rotation
  },
  { deep: true }
)
</script>