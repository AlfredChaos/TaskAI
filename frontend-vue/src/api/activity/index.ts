// 活动相关API接口
import { http } from '@/utils/request'
import type { Activity } from '@/types'
import type {
  GetActivitiesParams,
  GetUserActivitiesParams,
  ActivityPaginatedResponse
} from './types'

/**
 * 活动API模块
 */
export const activityApi = {
  /**
   * 获取活动列表
   * @param params 查询参数
   * @returns 活动列表
   */
  getActivities(params?: GetActivitiesParams): Promise<ActivityPaginatedResponse<Activity>> {
    return http.get('/activities', { params })
  },
  
  /**
   * 获取用户活动
   * @param userId 用户ID
   * @param params 查询参数
   * @returns 用户活动列表
   */
  getUserActivities(userId: string, params?: GetUserActivitiesParams): Promise<ActivityPaginatedResponse<Activity>> {
    return http.get(`/activities/users/${userId}`, { params })
  }
}

export * from './types'