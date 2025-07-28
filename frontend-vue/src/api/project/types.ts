// 项目相关类型定义
import type { Project, ApiResponse, PaginatedResponse } from '@/types'

/**
 * 获取项目列表请求参数
 */
export interface GetProjectsParams {
  page?: number
  pageSize?: number
  status?: string
  search?: string
}

/**
 * 创建项目请求参数
 */
export type CreateProjectRequest = Omit<Project, 'id' | 'createdAt' | 'updatedAt'>

/**
 * 更新项目请求参数
 */
export type UpdateProjectRequest = Partial<Project>

/**
 * 添加项目成员请求参数
 */
export interface AddMemberRequest {
  userId: string
}

/**
 * 项目API响应类型
 */
export type ProjectApiResponse<T = unknown> = ApiResponse<T>
export type ProjectPaginatedResponse<T = unknown> = PaginatedResponse<T>