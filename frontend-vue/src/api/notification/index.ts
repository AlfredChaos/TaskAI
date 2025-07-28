// 通知相关API接口
import { http } from '@/utils/request'
import type { Notification } from '@/types'
import type {
  GetNotificationsParams,
  NotificationApiResponse,
  NotificationPaginatedResponse
} from './types'

/**
 * 通知API模块
 */
export const notificationApi = {
  /**
   * 获取通知列表
   * @param params 查询参数
   * @returns 通知列表
   */
  getNotifications(params?: GetNotificationsParams): Promise<NotificationPaginatedResponse<Notification>> {
    return http.get('/notifications', { params })
  },
  
  /**
   * 标记通知已读
   * @param id 通知ID
   * @returns 标记结果
   */
  markAsRead(id: string): Promise<NotificationApiResponse> {
    return http.patch(`/notifications/${id}/read`)
  },
  
  /**
   * 标记所有通知已读
   * @returns 标记结果
   */
  markAllAsRead(): Promise<NotificationApiResponse> {
    return http.post('/notifications/read-all')
  },
  
  /**
   * 删除通知
   * @param id 通知ID
   * @returns 删除结果
   */
  deleteNotification(id: string): Promise<NotificationApiResponse> {
    return http.delete(`/notifications/${id}`)
  }
}

export * from './types'