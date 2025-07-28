// 通知相关类型定义
import type { ApiResponse, PaginatedResponse } from '@/types'

/**
 * 获取通知列表请求参数
 */
export interface GetNotificationsParams {
  page?: number
  pageSize?: number
  isRead?: boolean
}

/**
 * 通知API响应类型
 */
export type NotificationApiResponse<T = unknown> = ApiResponse<T>
export type NotificationPaginatedResponse<T = unknown> = PaginatedResponse<T>