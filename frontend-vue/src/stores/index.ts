// Store统一导出
export { useUserStore } from './user'
export { useThemeStore } from './theme'
export { useProjectStore } from './project'
export { useTaskStore } from './task'
export { useCounterStore } from './counter'

// Store初始化函数
import { useUserStore } from './user'
import { useThemeStore } from './theme'

/**
 * 初始化所有store
 */
export const initializeStores = async () => {
  const userStore = useUserStore()
  const themeStore = useThemeStore()
  
  // 初始化主题
  themeStore.initializeTheme()
  
  // 初始化用户认证状态
  await userStore.initializeAuth()
}