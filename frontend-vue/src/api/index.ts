// API服务接口
import { http } from '@/utils/request'
import type {
  User,
  Project,
  Task,
  Message,
  Channel,
  Activity,
  Notification,
  DashboardStats,
  ApiResponse,
  PaginatedResponse,
  SearchResult,
  SearchFilters
} from '@/types'

// 认证相关API
export const authApi = {
  // 登录
  login(data: { email: string; password: string }): Promise<ApiResponse<{ user: User; token: string }>> {
    return http.post('/auth/login', data)
  },
  
  // 注册
  register(data: { name: string; email: string; password: string }): Promise<ApiResponse<{ user: User; token: string }>> {
    return http.post('/auth/register', data)
  },
  
  // 登出
  logout(): Promise<ApiResponse> {
    return http.post('/auth/logout')
  },
  
  // 获取当前用户信息
  getCurrentUser(): Promise<ApiResponse<User>> {
    return http.get('/auth/me')
  },
  
  // 刷新token
  refreshToken(): Promise<ApiResponse<{ token: string }>> {
    return http.post('/auth/refresh')
  }
}

// 用户相关API
export const userApi = {
  // 获取用户列表
  getUsers(params?: { page?: number; pageSize?: number; search?: string }): Promise<PaginatedResponse<User>> {
    return http.get('/users', { params })
  },
  
  // 获取用户详情
  getUser(id: string): Promise<ApiResponse<User>> {
    return http.get(`/users/${id}`)
  },
  
  // 更新用户信息
  updateUser(id: string, data: Partial<User>): Promise<ApiResponse<User>> {
    return http.put(`/users/${id}`, data)
  },
  
  // 更新用户头像
  updateAvatar(file: File): Promise<ApiResponse<{ avatar: string }>> {
    const formData = new FormData()
    formData.append('avatar', file)
    return http.post('/users/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  // 修改密码
  changePassword(data: { oldPassword: string; newPassword: string }): Promise<ApiResponse> {
    return http.post('/users/change-password', data)
  }
}

// 项目相关API
export const projectApi = {
  // 获取项目列表
  getProjects(params?: { page?: number; pageSize?: number; status?: string; search?: string }): Promise<PaginatedResponse<Project>> {
    return http.get('/projects', { params })
  },
  
  // 获取项目详情
  getProject(id: string): Promise<ApiResponse<Project>> {
    return http.get(`/projects/${id}`)
  },
  
  // 创建项目
  createProject(data: Omit<Project, 'id' | 'createdAt' | 'updatedAt'>): Promise<ApiResponse<Project>> {
    return http.post('/projects', data)
  },
  
  // 更新项目
  updateProject(id: string, data: Partial<Project>): Promise<ApiResponse<Project>> {
    return http.put(`/projects/${id}`, data)
  },
  
  // 删除项目
  deleteProject(id: string): Promise<ApiResponse> {
    return http.delete(`/projects/${id}`)
  },
  
  // 添加项目成员
  addMember(projectId: string, userId: string): Promise<ApiResponse> {
    return http.post(`/projects/${projectId}/members`, { userId })
  },
  
  // 移除项目成员
  removeMember(projectId: string, userId: string): Promise<ApiResponse> {
    return http.delete(`/projects/${projectId}/members/${userId}`)
  }
}

// 任务相关API
export const taskApi = {
  // 获取任务列表
  getTasks(params?: {
    page?: number
    pageSize?: number
    projectId?: string
    status?: string
    assignee?: string
    priority?: string
    search?: string
  }): Promise<PaginatedResponse<Task>> {
    return http.get('/tasks', { params })
  },
  
  // 获取任务详情
  getTask(id: string): Promise<ApiResponse<Task>> {
    return http.get(`/tasks/${id}`)
  },
  
  // 创建任务
  createTask(data: Omit<Task, 'id' | 'createdAt' | 'updatedAt' | 'comments' | 'attachments'>): Promise<ApiResponse<Task>> {
    return http.post('/tasks', data)
  },
  
  // 更新任务
  updateTask(id: string, data: Partial<Task>): Promise<ApiResponse<Task>> {
    return http.put(`/tasks/${id}`, data)
  },
  
  // 删除任务
  deleteTask(id: string): Promise<ApiResponse> {
    return http.delete(`/tasks/${id}`)
  },
  
  // 更新任务状态
  updateTaskStatus(id: string, status: Task['status']): Promise<ApiResponse<Task>> {
    return http.patch(`/tasks/${id}/status`, { status })
  },
  
  // 分配任务
  assignTask(id: string, assigneeId: string): Promise<ApiResponse<Task>> {
    return http.patch(`/tasks/${id}/assign`, { assigneeId })
  },
  
  // 添加任务评论
  addComment(taskId: string, content: string): Promise<ApiResponse> {
    return http.post(`/tasks/${taskId}/comments`, { content })
  },
  
  // 上传任务附件
  uploadAttachment(taskId: string, file: File): Promise<ApiResponse> {
    const formData = new FormData()
    formData.append('file', file)
    return http.post(`/tasks/${taskId}/attachments`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}

// 消息相关API
export const messageApi = {
  // 获取频道列表
  getChannels(): Promise<ApiResponse<Channel[]>> {
    return http.get('/messages/channels')
  },
  
  // 获取频道消息
  getMessages(channelId: string, params?: { page?: number; pageSize?: number }): Promise<PaginatedResponse<Message>> {
    return http.get(`/messages/channels/${channelId}/messages`, { params })
  },
  
  // 发送消息
  sendMessage(channelId: string, data: { content: string; type?: Message['type'] }): Promise<ApiResponse<Message>> {
    return http.post(`/messages/channels/${channelId}/messages`, data)
  },
  
  // 创建频道
  createChannel(data: { name: string; type: Channel['type']; members: string[] }): Promise<ApiResponse<Channel>> {
    return http.post('/messages/channels', data)
  },
  
  // 标记消息已读
  markAsRead(channelId: string): Promise<ApiResponse> {
    return http.post(`/messages/channels/${channelId}/read`)
  }
}

// 活动相关API
export const activityApi = {
  // 获取活动列表
  getActivities(params?: { page?: number; pageSize?: number; type?: string; projectId?: string }): Promise<PaginatedResponse<Activity>> {
    return http.get('/activities', { params })
  },
  
  // 获取用户活动
  getUserActivities(userId: string, params?: { page?: number; pageSize?: number }): Promise<PaginatedResponse<Activity>> {
    return http.get(`/activities/users/${userId}`, { params })
  }
}

// 通知相关API
export const notificationApi = {
  // 获取通知列表
  getNotifications(params?: { page?: number; pageSize?: number; isRead?: boolean }): Promise<PaginatedResponse<Notification>> {
    return http.get('/notifications', { params })
  },
  
  // 标记通知已读
  markAsRead(id: string): Promise<ApiResponse> {
    return http.patch(`/notifications/${id}/read`)
  },
  
  // 标记所有通知已读
  markAllAsRead(): Promise<ApiResponse> {
    return http.post('/notifications/read-all')
  },
  
  // 删除通知
  deleteNotification(id: string): Promise<ApiResponse> {
    return http.delete(`/notifications/${id}`)
  }
}

// 仪表板相关API
export const dashboardApi = {
  // 获取仪表板统计数据
  getStats(): Promise<ApiResponse<DashboardStats>> {
    return http.get('/dashboard/stats')
  },
  
  // 获取项目进度数据
  getProjectProgress(): Promise<ApiResponse<{ projectId: string; name: string; progress: number }[]>> {
    return http.get('/dashboard/project-progress')
  },
  
  // 获取任务统计数据
  getTaskStats(): Promise<ApiResponse<{ status: string; count: number }[]>> {
    return http.get('/dashboard/task-stats')
  },
  
  // 获取团队活动数据
  getTeamActivity(): Promise<ApiResponse<{ date: string; count: number }[]>> {
    return http.get('/dashboard/team-activity')
  }
}

// 搜索相关API
export const searchApi = {
  // 全局搜索
  search(query: string, filters?: SearchFilters): Promise<ApiResponse<SearchResult[]>> {
    return http.get('/search', { params: { query, ...filters } })
  },
  
  // 搜索用户
  searchUsers(query: string): Promise<ApiResponse<User[]>> {
    return http.get('/search/users', { params: { query } })
  },
  
  // 搜索项目
  searchProjects(query: string): Promise<ApiResponse<Project[]>> {
    return http.get('/search/projects', { params: { query } })
  },
  
  // 搜索任务
  searchTasks(query: string): Promise<ApiResponse<Task[]>> {
    return http.get('/search/tasks', { params: { query } })
  }
}

// 文件上传相关API
export const uploadApi = {
  // 上传文件
  uploadFile(file: File, onProgress?: (progress: number) => void): Promise<ApiResponse<{ url: string; filename: string }>> {
    const formData = new FormData()
    formData.append('file', file)
    
    return http.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      }
    })
  },
  
  // 删除文件
  deleteFile(url: string): Promise<ApiResponse> {
    return http.delete('/upload', { data: { url } })
  }
}