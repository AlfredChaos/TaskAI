/**
 * AI 相关 API 接口
 */

import { http } from '@/utils/request'
import type { ApiResponse, ModelProvider, ProviderModel } from '@/types'

/**
 * 供应商相关 API
 */
export const providerApi = {
  /**
   * 创建供应商
   * @param data 供应商数据
   */
  create(data: Partial<ModelProvider>): Promise<ApiResponse<ModelProvider>> {
    return http.post('/ai/providers/', data)
  },

  /**
   * 获取供应商列表
   * @param params 查询参数
   */
  list(params?: {
    page?: number
    size?: number
    is_active?: boolean
  }): Promise<ApiResponse<ModelProvider[]>> {
    return http.get('/ai/providers/', { params })
  },

  /**
   * 更新供应商
   * @param providerId 供应商ID
   * @param data 更新数据
   */
  update(providerId: string, data: Partial<ModelProvider>): Promise<ApiResponse<ModelProvider>> {
    return http.put(`/ai/providers/${providerId}`, data)
  },

  /**
   * 删除供应商
   * @param providerId 供应商ID
   */
  delete(providerId: string): Promise<ApiResponse<null>> {
    return http.delete(`/ai/providers/${providerId}`)
  },

  /**
   * 设置默认供应商
   * @param providerId 供应商ID
   */
  setDefault(providerId: string): Promise<ApiResponse<null>> {
    return http.post('/ai/providers/set-default', { provider_id: providerId })
  },

  /**
   * 获取供应商详情
   * @param providerId 供应商ID
   */
  get(providerId: string): Promise<ApiResponse<ModelProvider>> {
    return http.get(`/ai/providers/${providerId}`)
  }
}

/**
 * 模型相关 API
 */
export const modelApi = {
  /**
   * 获取供应商可用模型
   * @param params 查询参数
   */
  getAvailableModels(params?: {
    provider_id?: string
    page?: number
    size?: number
  }): Promise<ApiResponse<ProviderModel[]>> {
    return http.get('/ai/chat/models', { params })
  }
}

/**
 * 导出所有 AI 相关 API
 */
export default {
  provider: providerApi,
  model: modelApi
}