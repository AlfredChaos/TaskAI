/**
 * API服务
 * 统一管理所有API调用
 */

import type { ApiResponse, Task, TaskStatus, Activity } from '@/types'
import { MockService } from './mockService'

/**
 * 基础请求函数
 */
async function request<T>(
  method: string,
  url: string,
  data?: Record<string, unknown>,
  params?: Record<string, unknown>
): Promise<ApiResponse<T>> {
  // 如果启用了mock数据，使用mock服务
  if (MockService.shouldUseMock()) {
    return MockService.handleRequest(method, url, data, params) as Promise<ApiResponse<T>>
  }
  
  // 这里可以添加真实的API调用逻辑
  throw new Error('真实API调用尚未实现')
}

/**
 * 任务相关API
 */
export const taskApi = {
  /**
   * 获取今日待办任务
   */
  getTodayTasks(): Promise<ApiResponse<Task[]>> {
    return request<Task[]>('GET', '/tasks/today')
  },

  /**
   * 更新任务状态
   */
  updateTaskStatus(taskId: string, status: TaskStatus): Promise<ApiResponse<Task>> {
    return request<Task>('PATCH', `/tasks/${taskId}/status`, { status })
  },

  /**
   * 获取任务列表
   */
  getTasks(params?: {
    page?: number
    pageSize?: number
    projectId?: string
    status?: string
    search?: string
  }): Promise<ApiResponse<{ list: Task[], total: number, page: number, pageSize: number, totalPages: number }>> {
    return request('GET', '/tasks', undefined, params)
  },

  /**
   * 创建任务
   */
  createTask(taskData: Partial<Task>): Promise<ApiResponse<Task>> {
    return request<Task>('POST', '/tasks', taskData)
  },

  /**
   * 更新任务
   */
  updateTask(taskId: string, taskData: Partial<Task>): Promise<ApiResponse<Task>> {
    return request<Task>('PUT', `/tasks/${taskId}`, taskData)
  }
}

/**
 * 仪表板相关API
 */
export const dashboardApi = {
  /**
   * 获取仪表板统计数据
   */
  getStats(): Promise<ApiResponse<{
    todayCompletedTasks: number
    todayTotalTasks: number
    allCompletedTasks: number
    allTotalTasks: number
    completedProjects: number
    totalProjects: number
    overdueProjects: number
    activeProjects: number
    completedTasks: number
    pendingTasks: number
    teamMembers: number
    recentActivities: Activity[]
  }>> {
    return request('GET', '/dashboard/stats')
  },

  /**
   * 获取项目类别分布
   */
  getProjectCategoryDistribution(): Promise<ApiResponse<{ category: string, count: number }[]>> {
    return request('GET', '/dashboard/project-category-distribution')
  },

  /**
   * 获取今日待办任务
   */
  getTodayTasks(): Promise<ApiResponse<Task[]>> {
    return request<Task[]>('GET', '/dashboard/today-tasks')
  }
}

export default {
  task: taskApi,
  dashboard: dashboardApi
}