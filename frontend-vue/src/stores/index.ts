// Store统一导出
export { useUserStore } from './user'
export { useThemeStore } from './theme'
export { useProjectStore } from './project'
export { useTaskStore } from './task'
export { useCounterStore } from './counter'
export { useLanguageStore } from './language'

// Store初始化函数
import { useUserStore } from './user'
import { useThemeStore } from './theme'
import { useLanguageStore } from './language'

/**
 * 初始化所有stores
 */
export const initializeStores = async () => {
  const themeStore = useThemeStore()
  const userStore = useUserStore()
  const languageStore = useLanguageStore()

  // 初始化主题
  themeStore.initializeTheme()

  // 初始化语言设置
  languageStore.initializeLanguage()

  // 初始化用户认证状态
  await userStore.initializeAuth()
}