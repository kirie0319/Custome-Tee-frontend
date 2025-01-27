<!-- src/components/LanguageSelector.vue -->
<template>
  <div class="relative inline-block text-left language-selector">
    <button 
      @click="isOpen = !isOpen"
      class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
    >
      <span class="mr-1"><img src="https://custome-tee-designs.s3.ap-northeast-1.amazonaws.com/designs/imges/language_translation.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAYM7POCGCVZUEEMZN%2F20250127%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20250127T105027Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFMaDmFwLW5vcnRoZWFzdC0xIkcwRQIgcDUi45nyHXtVmH%2FvenXPPDuclwWAsmHXXkm%2FXgBuPwECIQDwFGJyH9hRRQC4M9sDjr2yIprJtlj15m5BJKBD8KUjDyrsAghcEAAaDDU3NzYzODM3MTcxNyIMan6padfiHw0CFwbgKskCO1CHdgOEMLgGF%2BNEO4BXksPi%2Bc1q1eQ1JtwhlPcE%2F12jInffKBpVB9pzsTXVWAmVAEdcCWuG4jNl7p93xBwtQlFbVdLdvNBElcWjw%2BoEehoI6FatGAoWLyyXv32jwrxyz0Q41NdzLvKyH2j3Q7kUWvHNlV3sBGLkXtchJsswxD%2BFwUv5at8YIuT0AyilRpcK0ywPOeBJzoZ2rwjHBBBQtWHxdZ108G2Bs7%2Bleolks5VkrbPAkS%2Bg%2BLY4BeFiXv1chM89FZVD7S2kum8LkSx3bYbU%2FNWxTfxWtgXiWg8NCNlVIcxMbbDWpUO7U7BXx0K5WGot07015VXbx0BF0KMu3Mz5pMrsQQIvhbbk722FSUYOzHGk2h4bhIBS2Yy%2BJpcMcpBGByhh01a7Jn6rkRR5QLMjZTkTsGvGRKN%2BAu%2Bf7s5J8bmobL0csZsw6cfdvAY6swKB%2FHSbWCq7%2F4FdOTMI4abNx2KhQ1bttsjBzD0PQy%2FNOkasVn%2BDjCd0oS6N1RUfUGl8Cec08n0fNwdz1wpsNMTNob7q8eNNfi2O9b%2B5il3DzuRlEMnDZQRwlLxq5kOYFLTbk0gNUe0F%2BW83HZsCaYffKFh6ekcCH5qfFz4FuTkoQEL8t1rdvFkO4ue%2Bf2z5F0pV3lZ9hPWxS1mX2vK9z%2BZ%2Bg5ErpdPIT6pAG2N71BAL0EsvimJqezM5rmMqTVWhD88xdUmG8EIJS684XDgZXFdgzqB%2BM0o1ux85Oo5mNozuM2D9CjfgZszrlnKHmKcPgXwxa1kdO6xMQM5LELy0BYJt4cXDSyfyX9Yn75XXxiAkSUnaWN%2BPz8JOlpfJ8cbSo6z8u39Y4uOC%2F8Dmi31QAc5JP0ow&X-Amz-Signature=550ab85a3a9340880771240d99c8634b58ee4b5b231da6b0967eb5020555fb95&X-Amz-SignedHeaders=host&response-content-disposition=inline" class="w-10 h-10" alt="language_translation_logo"></span>
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