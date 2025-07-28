// 任务相关API接口
import { http } from '@/utils/request'
import type { Task } from '@/types'
import type {
  GetTasksParams,
  CreateTaskRequest,
  UpdateTaskRequest,
  TaskApiResponse,
  TaskPaginatedResponse
} from './types'

/**
 * 任务API模块
 */
export const taskApi = {
  /**
   * 获取今日待办任务
   * @returns 今日待办任务列表
   */
  getTodayTasks(): Promise<TaskApiResponse<Task[]>> {
    return http.get('/tasks/today')
  },

  /**
   * 获取任务列表
   * @param params 查询参数
   * @returns 任务列表
   */
  getTasks(params?: GetTasksParams): Promise<TaskApiResponse<TaskPaginatedResponse<Task>>> {
    return http.get('/tasks', { params })
  },
  
  /**
   * 获取任务详情
   * @param id 任务ID
   * @returns 任务详情
   */
  getTask(id: string): Promise<TaskApiResponse<Task>> {
    return http.get(`/tasks/${id}`)
  },
  
  /**
   * 创建任务
   * @param data 任务数据
   * @returns 创建的任务
   */
  createTask(data: CreateTaskRequest): Promise<TaskApiResponse<Task>> {
    return http.post('/tasks', data)
  },
  
  /**
   * 更新任务
   * @param id 任务ID
   * @param data 更新数据
   * @returns 更新后的任务
   */
  updateTask(id: string, data: UpdateTaskRequest): Promise<TaskApiResponse<Task>> {
    return http.put(`/tasks/${id}`, data)
  },
  
  /**
   * 删除任务
   * @param id 任务ID
   * @returns 删除结果
   */
  deleteTask(id: string): Promise<TaskApiResponse> {
    return http.delete(`/tasks/${id}`)
  },
  
  /**
   * 更新任务状态
   * @param id 任务ID
   * @param status 新状态
   * @returns 更新后的任务
   */
  updateTaskStatus(id: string, status: Task['status']): Promise<TaskApiResponse<Task>> {
    return http.patch(`/tasks/${id}/status`, { status })
  },
  
  /**
   * 分配任务
   * @param id 任务ID
   * @param assigneeId 被分配人ID
   * @returns 更新后的任务
   */
  assignTask(id: string, assigneeId: string): Promise<TaskApiResponse<Task>> {
    return http.patch(`/tasks/${id}/assign`, { assigneeId })
  },
  
  /**
   * 添加任务评论
   * @param taskId 任务ID
   * @param content 评论内容
   * @returns 添加结果
   */
  addComment(taskId: string, content: string): Promise<TaskApiResponse> {
    return http.post(`/tasks/${taskId}/comments`, { content })
  },
  
  /**
   * 上传任务附件
   * @param taskId 任务ID
   * @param file 附件文件
   * @returns 上传结果
   */
  uploadAttachment(taskId: string, file: File): Promise<TaskApiResponse> {
    const formData = new FormData()
    formData.append('file', file)
    return http.post(`/tasks/${taskId}/attachments`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}

export * from './types'