// 任务相关类型定义
import type { Task, ApiResponse, PaginatedResponse } from '@/types'

/**
 * 获取任务列表请求参数
 */
export interface GetTasksParams {
  page?: number
  pageSize?: number
  projectId?: string
  status?: string
  assignee?: string
  priority?: string
  search?: string
}

/**
 * 创建任务请求参数
 */
export type CreateTaskRequest = Omit<Task, 'id' | 'createdAt' | 'updatedAt' | 'comments' | 'attachments'>

/**
 * 更新任务请求参数
 */
export type UpdateTaskRequest = Partial<Task>

/**
 * 更新任务状态请求参数
 */
export interface UpdateTaskStatusRequest {
  status: Task['status']
}

/**
 * 分配任务请求参数
 */
export interface AssignTaskRequest {
  assigneeId: string
}

/**
 * 添加评论请求参数
 */
export interface AddCommentRequest {
  content: string
}

/**
 * 任务API响应类型
 */
export type TaskApiResponse<T = unknown> = ApiResponse<T>
export type TaskPaginatedResponse<T = unknown> = PaginatedResponse<T>