// src/i18n/index.ts
import { createI18n } from 'vue-i18n'
import ja from '@/locales/ja.json'
import en from '@/locales/en.json'

export default createI18n({
  legacy: false, // Vue 3の Composition API を使用
  locale: 'ja',
  fallbackLocale: 'en',
  messages: {
    ja,
    en
  }
})