// 项目相关API接口
import { http } from '@/utils/request'
import type { Project } from '@/types'
import type {
  GetProjectsParams,
  CreateProjectRequest,
  UpdateProjectRequest,
  ProjectApiResponse,
  ProjectPaginatedResponse
} from './types'

/**
 * 项目API模块
 */
export const projectApi = {
  /**
   * 获取项目列表
   * @param params 查询参数
   * @returns 项目列表
   */
  getProjects(params?: GetProjectsParams): Promise<ProjectPaginatedResponse<Project>> {
    return http.get('/projects', { params })
  },
  
  /**
   * 获取项目详情
   * @param id 项目ID
   * @returns 项目详情
   */
  getProject(id: string): Promise<ProjectApiResponse<Project>> {
    return http.get(`/projects/${id}`)
  },
  
  /**
   * 创建项目
   * @param data 项目数据
   * @returns 创建的项目
   */
  createProject(data: CreateProjectRequest): Promise<ProjectApiResponse<Project>> {
    return http.post('/projects', data)
  },
  
  /**
   * 更新项目
   * @param id 项目ID
   * @param data 更新数据
   * @returns 更新后的项目
   */
  updateProject(id: string, data: UpdateProjectRequest): Promise<ProjectApiResponse<Project>> {
    return http.put(`/projects/${id}`, data)
  },
  
  /**
   * 删除项目
   * @param id 项目ID
   * @returns 删除结果
   */
  deleteProject(id: string): Promise<ProjectApiResponse> {
    return http.delete(`/projects/${id}`)
  },
  
  /**
   * 添加项目成员
   * @param projectId 项目ID
   * @param userId 用户ID
   * @returns 添加结果
   */
  addMember(projectId: string, userId: string): Promise<ProjectApiResponse> {
    return http.post(`/projects/${projectId}/members`, { userId })
  },
  
  /**
   * 移除项目成员
   * @param projectId 项目ID
   * @param userId 用户ID
   * @returns 移除结果
   */
  removeMember(projectId: string, userId: string): Promise<ProjectApiResponse> {
    return http.delete(`/projects/${projectId}/members/${userId}`)
  }
}

export * from './types'