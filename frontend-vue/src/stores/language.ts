import { defineStore } from 'pinia'
import { ref } from 'vue'

export type Language = 'zh' | 'en'

export const useLanguageStore = defineStore('language', () => {
  // State
  const currentLanguage = ref<Language>('zh')

  // Actions
  /**
   * 切换语言
   * @param language 目标语言
   */
  const setLanguage = (language: Language) => {
    currentLanguage.value = language
    localStorage.setItem('language', language)
  }

  /**
   * 初始化语言设置
   */
  const initializeLanguage = () => {
    const savedLanguage = localStorage.getItem('language') as Language
    if (savedLanguage && ['zh', 'en'].includes(savedLanguage)) {
      currentLanguage.value = savedLanguage
    }
  }

  return {
    // State
    currentLanguage,
    // Actions
    setLanguage,
    initializeLanguage
  }
})