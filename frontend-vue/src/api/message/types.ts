// 消息相关类型定义
import type { Message, Channel, ApiResponse, PaginatedResponse } from '@/types'

/**
 * 获取消息列表请求参数
 */
export interface GetMessagesParams {
  page?: number
  pageSize?: number
}

/**
 * 发送消息请求参数
 */
export interface SendMessageRequest {
  content: string
  type?: Message['type']
}

/**
 * 创建频道请求参数
 */
export interface CreateChannelRequest {
  name: string
  type: Channel['type']
  members: string[]
}

/**
 * 消息API响应类型
 */
export type MessageApiResponse<T = unknown> = ApiResponse<T>
export type MessagePaginatedResponse<T = unknown> = PaginatedResponse<T>