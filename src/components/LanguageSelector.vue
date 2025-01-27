<!-- src/components/LanguageSelector.vue -->
<template>
  <div class="relative inline-block text-left language-selector">
    <button 
      @click="isOpen = !isOpen"
      class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
    >
      <span class="mr-1"><img src="https://custome-tee-designs.s3.ap-northeast-1.amazonaws.com/designs/imges/language_translation.png" class="w-10 h-10" alt="language_translation_logo"></span>
      <ChevronDown class="h-4 w-4" />
    </button>

    <!-- ドロップダウンメニュー -->
    <div 
      v-if="isOpen" 
      class="origin-top-right absolute right-0 mt-2 w-28 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50"
    >
      <div class="py-1">
        <button
          v-for="(label, lang) in languages"
          :key="lang"
          @click="changeLanguage(lang)"
          class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
          :class="{ 'bg-gray-100': currentLocale === lang }"
        >
          {{ label }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { ChevronDown } from 'lucide-vue-next'

const { locale } = useI18n()
const isOpen = ref(false)

const languages = {
  'ja': '日本語',
  'en': 'English'
}

const currentLocale = computed(() => locale.value)
const currentLanguageLabel = computed(() => languages[locale.value as keyof typeof languages])

const changeLanguage = (lang: string) => {
  locale.value = lang
  isOpen.value = false
}

// クリックイベントのハンドラーを追加して、外部クリックでドロップダウンを閉じる
const handleClickOutside = (event: MouseEvent) => {
  if (!event.target) return
  
  const target = event.target as HTMLElement
  if (!target.closest('.language-selector')) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>