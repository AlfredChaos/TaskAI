import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { ThemeConfig } from '@/types'

/**
 * 主题状态管理
 */
export const useThemeStore = defineStore('theme', () => {
  // 状态
  const mode = ref<'light' | 'dark'>('light')
  const primaryColor = ref('#409EFF')
  const sidebarCollapsed = ref(false)
  const isLoading = ref(false)

  // 计算属性
  const isDark = computed(() => mode.value === 'dark')
  const isLight = computed(() => mode.value === 'light')
  const themeConfig = computed<ThemeConfig>(() => ({
    mode: mode.value,
    primaryColor: primaryColor.value,
    sidebarCollapsed: sidebarCollapsed.value
  }))

  /**
   * 切换主题模式
   */
  const toggleMode = () => {
    mode.value = mode.value === 'light' ? 'dark' : 'light'
    applyTheme()
    saveToStorage()
  }

  /**
   * 设置主题模式
   */
  const setMode = (newMode: 'light' | 'dark') => {
    mode.value = newMode
    applyTheme()
    saveToStorage()
  }

  /**
   * 设置主色调
   */
  const setPrimaryColor = (color: string) => {
    primaryColor.value = color
    applyTheme()
    saveToStorage()
  }

  /**
   * 切换侧边栏折叠状态
   */
  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
    saveToStorage()
  }

  /**
   * 设置侧边栏折叠状态
   */
  const setSidebarCollapsed = (collapsed: boolean) => {
    sidebarCollapsed.value = collapsed
    saveToStorage()
  }

  /**
   * 应用主题到DOM
   */
  const applyTheme = () => {
    const html = document.documentElement
    
    // 设置主题模式
    if (isDark.value) {
      html.classList.add('dark')
      html.classList.remove('light')
    } else {
      html.classList.add('light')
      html.classList.remove('dark')
    }
    
    // 设置主色调CSS变量
    html.style.setProperty('--el-color-primary', primaryColor.value)
    
    // 生成主色调的各种变体
    const primaryColorRgb = hexToRgb(primaryColor.value)
    if (primaryColorRgb) {
      const { r, g, b } = primaryColorRgb
      
      // 设置主色调的透明度变体
      html.style.setProperty('--el-color-primary-light-3', `rgba(${r}, ${g}, ${b}, 0.7)`)
      html.style.setProperty('--el-color-primary-light-5', `rgba(${r}, ${g}, ${b}, 0.5)`)
      html.style.setProperty('--el-color-primary-light-7', `rgba(${r}, ${g}, ${b}, 0.3)`)
      html.style.setProperty('--el-color-primary-light-8', `rgba(${r}, ${g}, ${b}, 0.2)`)
      html.style.setProperty('--el-color-primary-light-9', `rgba(${r}, ${g}, ${b}, 0.1)`)
    }
  }

  /**
   * 保存主题配置到localStorage
   */
  const saveToStorage = () => {
    const config = {
      mode: mode.value,
      primaryColor: primaryColor.value,
      sidebarCollapsed: sidebarCollapsed.value
    }
    localStorage.setItem('theme-config', JSON.stringify(config))
  }

  /**
   * 从localStorage加载主题配置
   */
  const loadFromStorage = () => {
    try {
      const stored = localStorage.getItem('theme-config')
      if (stored) {
        const config = JSON.parse(stored) as ThemeConfig
        mode.value = config.mode || 'light'
        primaryColor.value = config.primaryColor || '#409EFF'
        sidebarCollapsed.value = config.sidebarCollapsed || false
      }
    } catch {
      // 如果解析失败，使用默认值
      console.warn('Failed to load theme config from localStorage')
    }
  }

  /**
   * 重置主题配置
   */
  const resetTheme = () => {
    mode.value = 'light'
    primaryColor.value = '#409EFF'
    sidebarCollapsed.value = false
    applyTheme()
    saveToStorage()
  }

  /**
   * 初始化主题
   */
  const initializeTheme = () => {
    isLoading.value = true
    
    // 从localStorage加载配置
    loadFromStorage()
    
    // 检测系统主题偏好
    if (!localStorage.getItem('theme-config')) {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      mode.value = prefersDark ? 'dark' : 'light'
    }
    
    // 应用主题
    applyTheme()
    
    // 监听系统主题变化
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    const handleChange = (e: MediaQueryListEvent) => {
      if (!localStorage.getItem('theme-config')) {
        mode.value = e.matches ? 'dark' : 'light'
        applyTheme()
      }
    }
    mediaQuery.addEventListener('change', handleChange)
    
    isLoading.value = false
  }

  /**
   * 工具函数：将hex颜色转换为RGB
   */
  const hexToRgb = (hex: string) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null
  }

  return {
    // 状态
    mode,
    primaryColor,
    sidebarCollapsed,
    isLoading,
    
    // 计算属性
    isDark,
    isLight,
    themeConfig,
    
    // 方法
    toggleMode,
    setMode,
    setPrimaryColor,
    toggleSidebar,
    setSidebarCollapsed,
    applyTheme,
    resetTheme,
    initializeTheme
  }
})