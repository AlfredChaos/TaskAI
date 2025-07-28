// HTTP请求工具
import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import type { ApiResponse } from '@/types'
import { config } from '@/config'
import { MockService } from '@/services/mockService'

// 创建axios实例
const request: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 添加认证token
    const token = localStorage.getItem('token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    const { data } = response
    console.log(response)
    // 检查业务状态码
    if (data.success) {
      return response
    } else {
      // 业务错误处理
      ElMessage.error(data.message || '请求失败')
      return Promise.reject(new Error(data.message || '请求失败'))
    }
  },
  (error) => {
    // HTTP错误处理
    let message = '网络错误'
    
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          message = data?.message || '请求参数错误'
          break
        case 401:
          message = '未授权，请重新登录'
          // 清除token并跳转到登录页
          localStorage.removeItem('token')
          window.location.href = '/login'
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = '请求的资源不存在'
          break
        case 500:
          message = '服务器内部错误'
          break
        default:
          message = data?.message || `请求失败 (${status})`
      }
    } else if (error.request) {
      message = '网络连接失败'
    }
    
    ElMessage.error(message)
    console.error('Response error:', error)
    return Promise.reject(error)
  }
)

/**
 * 检查是否应该使用mock数据
 * @param url 请求URL
 */
function shouldUseMock(): boolean {
  return config.useMockData
}

/**
 * 处理mock请求
 * @param method HTTP方法
 * @param url 请求URL
 * @param data 请求数据
 * @param requestConfig 请求配置
 */
async function handleMockRequest<T = unknown>(
  method: string,
  url: string,
  data?: unknown,
  requestConfig?: AxiosRequestConfig
): Promise<ApiResponse<T>> {
  console.log(`[Mock] ${method.toUpperCase()} ${url}`, data)
  
  // 提取查询参数
  const params = requestConfig?.params || {}
  
  // 调用mock服务
  const response = await MockService.handleRequest(
    method.toUpperCase(),
    url,
    data as Record<string, unknown>,
    params as Record<string, unknown>
  )
  
  return response as ApiResponse<T>
}

// 请求方法封装
export const http = {
  async get<T = unknown>(url: string, requestConfig?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    if (shouldUseMock()) {
      return handleMockRequest<T>('GET', url, undefined, requestConfig)
    }
    return request.get(url, requestConfig).then(res => res.data)
  },
  
  async post<T = unknown>(url: string, data?: unknown, requestConfig?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    if (shouldUseMock()) {
      return handleMockRequest<T>('POST', url, data, requestConfig)
    }
    return request.post(url, data, requestConfig).then(res => res.data)
  },
  
  async put<T = unknown>(url: string, data?: unknown, requestConfig?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    if (shouldUseMock()) {
      return handleMockRequest<T>('PUT', url, data, requestConfig)
    }
    return request.put(url, data, requestConfig).then(res => res.data)
  },
  
  async delete<T = unknown>(url: string, requestConfig?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    if (shouldUseMock()) {
      return handleMockRequest<T>('DELETE', url, undefined, requestConfig)
    }
    return request.delete(url, requestConfig).then(res => res.data)
  },
  
  async patch<T = unknown>(url: string, data?: unknown, requestConfig?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    if (shouldUseMock()) {
      return handleMockRequest<T>('PATCH', url, data, requestConfig)
    }
    return request.patch(url, data, requestConfig).then(res => res.data)
  }
}

export default request