// 搜索相关类型定义
import type { User, Project, Task, SearchResult, SearchFilters, ApiResponse } from '@/types'

/**
 * 搜索请求参数
 */
export interface SearchParams {
  query: string
  filters?: SearchFilters
}

/**
 * 搜索用户请求参数
 */
export interface SearchUsersParams {
  query: string
}

/**
 * 搜索项目请求参数
 */
export interface SearchProjectsParams {
  query: string
}

/**
 * 搜索任务请求参数
 */
export interface SearchTasksParams {
  query: string
}

/**
 * 搜索API响应类型
 */
export type SearchApiResponse<T = unknown> = ApiResponse<T>

// 重新导出搜索相关类型
export type { SearchResult, SearchFilters, User, Project, Task }