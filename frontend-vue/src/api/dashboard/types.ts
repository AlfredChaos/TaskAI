// 仪表板相关类型定义
import type { DashboardStats, ApiResponse } from '@/types'

/**
 * 项目进度数据
 */
export interface ProjectProgressData {
  projectId: string
  name: string
  progress: number
}

/**
 * 任务统计数据
 */
export interface TaskStatsData {
  status: string
  count: number
}

/**
 * 团队活动数据
 */
export interface TeamActivityData {
  date: string
  count: number
}

/**
 * 仪表板API响应类型
 */
export type DashboardApiResponse<T = unknown> = ApiResponse<T>

// 重新导出DashboardStats类型
export type { DashboardStats }