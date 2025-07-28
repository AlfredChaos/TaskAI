// 消息相关API接口
import { http } from '@/utils/request'
import type { Message, Channel } from '@/types'
import type {
  GetMessagesParams,
  SendMessageRequest,
  CreateChannelRequest,
  MessageApiResponse,
  MessagePaginatedResponse
} from './types'

/**
 * 消息API模块
 */
export const messageApi = {
  /**
   * 获取频道列表
   * @returns 频道列表
   */
  getChannels(): Promise<MessageApiResponse<Channel[]>> {
    return http.get('/messages/channels')
  },
  
  /**
   * 获取频道消息
   * @param channelId 频道ID
   * @param params 查询参数
   * @returns 消息列表
   */
  getMessages(channelId: string, params?: GetMessagesParams): Promise<MessagePaginatedResponse<Message>> {
    return http.get(`/messages/channels/${channelId}/messages`, { params })
  },
  
  /**
   * 发送消息
   * @param channelId 频道ID
   * @param data 消息数据
   * @returns 发送的消息
   */
  sendMessage(channelId: string, data: SendMessageRequest): Promise<MessageApiResponse<Message>> {
    return http.post(`/messages/channels/${channelId}/messages`, data)
  },
  
  /**
   * 创建频道
   * @param data 频道数据
   * @returns 创建的频道
   */
  createChannel(data: CreateChannelRequest): Promise<MessageApiResponse<Channel>> {
    return http.post('/messages/channels', data)
  },
  
  /**
   * 标记消息已读
   * @param channelId 频道ID
   * @returns 标记结果
   */
  markAsRead(channelId: string): Promise<MessageApiResponse> {
    return http.post(`/messages/channels/${channelId}/read`)
  }
}

export * from './types'