/**
 * 应用配置文件
 * 管理应用的全局配置项
 */

// 开发环境配置
interface DevConfig {
  // 是否启用mock数据
  useMockData: boolean
  // API基础URL
  apiBaseUrl: string
  // 请求超时时间
  timeout: number
}

// 生产环境配置
interface ProdConfig {
  // API基础URL
  apiBaseUrl: string
  // 请求超时时间
  timeout: number
}

// 开发环境配置
const devConfig: DevConfig = {
  useMockData: true, // 开发阶段默认启用mock数据
  apiBaseUrl: '/api',
  timeout: 10000
}

// 生产环境配置
const prodConfig: ProdConfig = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'https://api.example.com',
  timeout: 10000
}

// 根据环境选择配置
const isDev = import.meta.env.DEV

/**
 * 应用配置
 */
export const config = {
  // 是否为开发环境
  isDev,
  // 是否启用mock数据（仅开发环境有效）
  useMockData: isDev ? devConfig.useMockData : false,
  // API基础URL
  apiBaseUrl: isDev ? devConfig.apiBaseUrl : prodConfig.apiBaseUrl,
  // 请求超时时间
  timeout: isDev ? devConfig.timeout : prodConfig.timeout
}

/**
 * 切换mock数据开关
 * @param enabled 是否启用mock数据
 */
export function toggleMockData(enabled: boolean) {
  if (isDev) {
    devConfig.useMockData = enabled
    // 重新加载页面以应用新配置
    window.location.reload()
  } else {
    console.warn('Mock数据只能在开发环境中使用')
  }
}

/**
 * 获取当前mock数据状态
 * @returns 是否启用mock数据
 */
export function getMockDataStatus(): boolean {
  return config.useMockData
}

export default config