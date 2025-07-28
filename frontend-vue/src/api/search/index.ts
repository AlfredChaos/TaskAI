// 搜索相关API接口
import { http } from '@/utils/request'
import type {
  SearchParams,
  SearchResult,
  User,
  Project,
  Task,
  SearchApiResponse
} from './types'

/**
 * 搜索API模块
 */
export const searchApi = {
  /**
   * 全局搜索
   * @param query 搜索关键词
   * @param filters 搜索过滤器
   * @returns 搜索结果
   */
  search(query: string, filters?: SearchParams['filters']): Promise<SearchApiResponse<SearchResult[]>> {
    return http.get('/search', { params: { query, ...filters } })
  },
  
  /**
   * 搜索用户
   * @param query 搜索关键词
   * @returns 用户列表
   */
  searchUsers(query: string): Promise<SearchApiResponse<User[]>> {
    return http.get('/search/users', { params: { query } })
  },
  
  /**
   * 搜索项目
   * @param query 搜索关键词
   * @returns 项目列表
   */
  searchProjects(query: string): Promise<SearchApiResponse<Project[]>> {
    return http.get('/search/projects', { params: { query } })
  },
  
  /**
   * 搜索任务
   * @param query 搜索关键词
   * @returns 任务列表
   */
  searchTasks(query: string): Promise<SearchApiResponse<Task[]>> {
    return http.get('/search/tasks', { params: { query } })
  }
}

export * from './types'