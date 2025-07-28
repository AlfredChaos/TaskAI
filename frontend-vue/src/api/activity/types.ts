// 活动相关类型定义
import type { ApiResponse, PaginatedResponse } from '@/types'

/**
 * 获取活动列表请求参数
 */
export interface GetActivitiesParams {
  page?: number
  pageSize?: number
  type?: string
  projectId?: string
}

/**
 * 获取用户活动请求参数
 */
export interface GetUserActivitiesParams {
  page?: number
  pageSize?: number
}

/**
 * 活动API响应类型
 */
export type ActivityApiResponse<T = unknown> = ApiResponse<T>
export type ActivityPaginatedResponse<T = unknown> = PaginatedResponse<T>