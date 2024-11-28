<!-- src/components/TShirtPreview.vue -->
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
          alt="Design" 
          class="w-full h-full object-contain"
        />
      </div>
    </div>

    <!-- 位置・サイズ・回転調整 -->
    <div class="mt-6 space-y-6">
      <!-- 位置調整 -->
      <div class="space-y-4">
        <h3 class="text-sm font-medium text-gray-700">左右位置調整</h3>
        <input
          type="range"
          v-model="position.x"
          min="20"
          max="80"
          step="1"
          class="w-full"
          @input="emitUpdate"
        />
        <h3 class="text-sm font-medium text-gray-700">上下位置調整</h3>
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
        <label class="block text-sm font-medium text-gray-700">デザインサイズ</label>
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
        <label class="block text-sm font-medium text-gray-700">回転</label>
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
        デザインをリセット
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'

// Props の定義
const props = defineProps<{
  designImage: string
  initialConfig: {
    color: string
    position: { x: number, y: number }
    scale: number
    rotation: number
  }
}>()

const emit = defineEmits<{
  'update:designConfig': [config: typeof props.initialConfig]
}>()

// 状態管理
const selectedColor = ref(props.initialConfig.color)
const position = ref({ ...props.initialConfig.position })
const scale = ref(props.initialConfig.scale)
const rotation = ref(props.initialConfig.rotation)

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

// 設定変更通知
const emitUpdate = () => {
  emit('update:designConfig', {
    color: selectedColor.value,
    position: position.value,
    scale: scale.value,
    rotation: rotation.value
  })
}

// リセット機能
const resetDesign = () => {
  position.value = { x: 50, y: 50 } // 中央に配置
  scale.value = 1 // デフォルトサイズ
  rotation.value = 0 // 回転なし
  selectedColor.value = props.initialConfig.color // 初期カラーに戻す
  emitUpdate() // 変更を親コンポーネントに通知
}

// 親からの設定更新を監視
watch(
  () => props.initialConfig,
  (newConfig) => {
    selectedColor.value = newConfig.color
    position.value = { ...newConfig.position }
    scale.value = newConfig.scale
    rotation.value = newConfig.rotation
  },
  { deep: true }
)
</script>
