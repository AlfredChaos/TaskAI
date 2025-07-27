// 通用工具函数
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

// 配置dayjs
dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

/**
 * 格式化日期
 * @param date 日期
 * @param format 格式
 * @returns 格式化后的日期字符串
 */
export function formatDate(date: string | Date, format = 'YYYY-MM-DD HH:mm:ss'): string {
  return dayjs(date).format(format)
}

/**
 * 获取相对时间
 * @param date 日期
 * @returns 相对时间字符串
 */
export function getRelativeTime(date: string | Date): string {
  return dayjs(date).fromNow()
}

/**
 * 格式化文件大小
 * @param bytes 字节数
 * @returns 格式化后的文件大小
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 生成随机ID
 * @param length 长度
 * @returns 随机ID
 */
export function generateId(length = 8): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

/**
 * 防抖函数
 * @param func 要防抖的函数
 * @param wait 等待时间
 * @returns 防抖后的函数
 */
export function debounce<T extends (...args: unknown[]) => unknown>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: number | null = null
  
  return function (...args: Parameters<T>) {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

/**
 * 节流函数
 * @param func 要节流的函数
 * @param limit 时间限制
 * @returns 节流后的函数
 */
export function throttle<T extends (...args: unknown[]) => unknown>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle = false
  
  return function (...args: Parameters<T>) {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

/**
 * 深拷贝
 * @param obj 要拷贝的对象
 * @returns 拷贝后的对象
 */
export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj.getTime()) as T
  if (obj instanceof Array) return obj.map(item => deepClone(item)) as T
  if (typeof obj === 'object') {
    const clonedObj = {} as T
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key])
      }
    }
    return clonedObj
  }
  return obj
}

/**
 * 获取文件扩展名
 * @param filename 文件名
 * @returns 扩展名
 */
export function getFileExtension(filename: string): string {
  return filename.slice(((filename.lastIndexOf('.') - 1) >>> 0) + 2)
}

/**
 * 检查是否为图片文件
 * @param filename 文件名
 * @returns 是否为图片
 */
export function isImageFile(filename: string): boolean {
  const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']
  const extension = getFileExtension(filename).toLowerCase()
  return imageExtensions.includes(extension)
}

/**
 * 获取用户头像颜色
 * @param name 用户名
 * @returns 颜色值
 */
export function getAvatarColor(name: string): string {
  const colors = [
    '#f56565', '#ed8936', '#ecc94b', '#48bb78',
    '#38b2ac', '#4299e1', '#667eea', '#9f7aea',
    '#ed64a6', '#f687b3'
  ]
  
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  
  return colors[Math.abs(hash) % colors.length]
}

/**
 * 获取用户名首字母
 * @param name 用户名
 * @returns 首字母
 */
export function getNameInitials(name: string): string {
  return name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

/**
 * 验证邮箱格式
 * @param email 邮箱
 * @returns 是否有效
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * 验证手机号格式
 * @param phone 手机号
 * @returns 是否有效
 */
export function isValidPhone(phone: string): boolean {
  const phoneRegex = /^1[3-9]\d{9}$/
  return phoneRegex.test(phone)
}

/**
 * 获取任务状态颜色
 * @param status 任务状态
 * @returns 颜色类名
 */
export function getTaskStatusColor(status: string): string {
  const colorMap: Record<string, string> = {
    'todo': 'text-gray-500',
    'in-progress': 'text-blue-500',
    'review': 'text-orange-500',
    'done': 'text-green-500'
  }
  return colorMap[status] || 'text-gray-500'
}

/**
 * 获取优先级颜色
 * @param priority 优先级
 * @returns 颜色类名
 */
export function getPriorityColor(priority: string): string {
  const colorMap: Record<string, string> = {
    'low': 'text-green-500',
    'medium': 'text-yellow-500',
    'high': 'text-orange-500',
    'urgent': 'text-red-500'
  }
  return colorMap[priority] || 'text-gray-500'
}

/**
 * 计算进度百分比
 * @param completed 已完成数量
 * @param total 总数量
 * @returns 百分比
 */
export function calculateProgress(completed: number, total: number): number {
  if (total === 0) return 0
  return Math.round((completed / total) * 100)
}

/**
 * 格式化数字
 * @param num 数字
 * @returns 格式化后的数字字符串
 */
export function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

/**
 * 获取浏览器信息
 * @returns 浏览器信息
 */
export function getBrowserInfo(): { name: string; version: string } {
  const ua = navigator.userAgent
  let name = 'Unknown'
  let version = 'Unknown'
  
  if (ua.includes('Chrome')) {
    name = 'Chrome'
    const match = ua.match(/Chrome\/(\d+)/)
    version = match ? match[1] : 'Unknown'
  } else if (ua.includes('Firefox')) {
    name = 'Firefox'
    const match = ua.match(/Firefox\/(\d+)/)
    version = match ? match[1] : 'Unknown'
  } else if (ua.includes('Safari')) {
    name = 'Safari'
    const match = ua.match(/Version\/(\d+)/)
    version = match ? match[1] : 'Unknown'
  }
  
  return { name, version }
}

/**
 * 复制文本到剪贴板
 * @param text 要复制的文本
 * @returns Promise
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    // 降级方案
    const textArea = document.createElement('textarea')
    textArea.value = text
    document.body.appendChild(textArea)
    textArea.select()
    const success = document.execCommand('copy')
    document.body.removeChild(textArea)
    return success
  }
}

/**
 * 下载文件
 * @param url 文件URL
 * @param filename 文件名
 */
export function downloadFile(url: string, filename: string): void {
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}