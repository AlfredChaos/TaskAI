// 仪表板相关API接口
import { http } from '@/utils/request'
import type {
  DashboardStats,
  ProjectProgressData,
  TaskStatsData,
  TeamActivityData,
  DashboardApiResponse
} from './types'

/**
 * 仪表板API模块
 */
export const dashboardApi = {
  /**
   * 获取仪表板统计数据
   * @returns 统计数据
   */
  getStats(): Promise<DashboardApiResponse<DashboardStats>> {
    const res = http.get('/dashboard/stats')
    console.log(res)
    return http.get('/dashboard/stats')
  },
  
  /**
   * 获取项目进度数据
   * @returns 项目进度列表
   */
  getProjectProgress(): Promise<DashboardApiResponse<ProjectProgressData[]>> {
    return http.get('/dashboard/project-progress')
  },
  
  /**
   * 获取任务统计数据
   * @returns 任务统计列表
   */
  getTaskStats(): Promise<DashboardApiResponse<TaskStatsData[]>> {
    return http.get('/dashboard/task-stats')
  },
  
  /**
   * 获取团队活动数据
   * @returns 团队活动列表
   */
  getTeamActivity(): Promise<DashboardApiResponse<TeamActivityData[]>> {
    return http.get('/dashboard/team-activity')
  },
  
  /**
   * 获取项目类别分布
   * @returns 项目类别分布列表
   */
  getProjectCategoryDistribution(): Promise<DashboardApiResponse<{ category: string; count: number }[]>> {
    return http.get('/dashboard/project-category-distribution')
  }
}

export * from './types'