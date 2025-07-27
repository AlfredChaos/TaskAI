import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { User } from '@/types'
import { authApi, userApi } from '@/api'

/**
 * 用户状态管理
 */
export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isManager = computed(() => user.value?.role === 'manager' || isAdmin.value)
  const userName = computed(() => user.value?.name || '')
  const userAvatar = computed(() => user.value?.avatar || '')

  /**
   * 登录
   */
  const login = async (email: string, password: string) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await authApi.login({ email, password })
      
      if (response.success) {
        token.value = response.data.token
        user.value = response.data.user
        
        // 保存token到localStorage
        localStorage.setItem('token', response.data.token)
        
        return { success: true }
      } else {
        error.value = response.message || '登录失败'
        return { success: false, message: error.value }
      }
    } catch {
      error.value = '网络错误，请稍后重试'
      return { success: false, message: error.value }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 登出
   */
  const logout = async () => {
    try {
      isLoading.value = true
      
      // 调用登出API
      await authApi.logout()
      
      // 清除本地状态
      user.value = null
      token.value = null
      error.value = null
      
      // 清除localStorage
      localStorage.removeItem('token')
      
      return { success: true }
    } catch (err) {
      console.error('登出失败:', err)
      // 即使API调用失败，也要清除本地状态
      user.value = null
      token.value = null
      localStorage.removeItem('token')
      
      return { success: true }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 获取当前用户信息
   */
  const fetchUserInfo = async () => {
    if (!token.value) {
      return { success: false, message: '未登录' }
    }

    try {
      isLoading.value = true
      error.value = null
      
      const response = await authApi.getCurrentUser()
      
      if (response.success) {
        user.value = response.data
        return { success: true }
      } else {
        error.value = response.message || '获取用户信息失败'
        return { success: false, message: error.value }
      }
    } catch {
      error.value = '网络错误，请稍后重试'
      return { success: false, message: error.value }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 更新用户信息
   */
  const updateUserInfo = async (userData: Partial<User>) => {
    if (!user.value) {
      return { success: false, message: '用户未登录' }
    }

    try {
      isLoading.value = true
      error.value = null
      
      const response = await userApi.updateUser(user.value.id, userData)
      
      if (response.success) {
        user.value = { ...user.value, ...response.data }
        return { success: true }
      } else {
        error.value = response.message || '更新用户信息失败'
        return { success: false, message: error.value }
      }
    } catch {
      error.value = '网络错误，请稍后重试'
      return { success: false, message: error.value }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 初始化用户状态
   */
  const initializeAuth = async () => {
    if (token.value) {
      await fetchUserInfo()
    }
  }

  /**
   * 清除错误信息
   */
  const clearError = () => {
    error.value = null
  }

  return {
    // 状态
    user,
    token,
    isLoading,
    error,
    
    // 计算属性
    isAuthenticated,
    isAdmin,
    isManager,
    userName,
    userAvatar,
    
    // 方法
    login,
    logout,
    fetchUserInfo,
    updateUserInfo,
    initializeAuth,
    clearError
  }
})