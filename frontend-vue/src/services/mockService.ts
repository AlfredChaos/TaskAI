/**
 * Mock数据服务
 * 用于在开发环境中拦截API调用并返回mock数据
 */

import { config } from '@/config'
import type { ApiResponse, PaginatedResponse, Project, Task, TaskStatus } from '@/types'
import { users, projects, tasks, messages, activities, notifications } from '../../mock/data'

/**
 * 模拟网络延迟
 * @param ms 延迟毫秒数
 */
function delay(ms = 300): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * 创建成功响应
 * @param data 响应数据
 * @param message 响应消息
 */
function success<T>(data: T, message = '操作成功'): ApiResponse<T> {
  return {
    success: true,
    message,
    code: 200,
    timestamp: new Date().toISOString(),
    data
  }
}

/**
 * 创建错误响应
 * @param message 错误消息
 * @param code 错误代码
 */
function error(message = '操作失败', code = 500): ApiResponse<null> {
  return {
    success: false,
    message,
    code,
    timestamp: new Date().toISOString(),
    data: null
  }
}

/**
 * 分页处理
 * @param data 数据数组
 * @param page 页码
 * @param pageSize 每页大小
 */
function paginate<T>(data: T[], page = 1, pageSize = 10): ApiResponse<PaginatedResponse<T>> {
  const start = (page - 1) * pageSize
  const end = start + pageSize
  const list = data.slice(start, end)
  
  const paginatedData: PaginatedResponse<T> = {
    list,
    total: data.length,
    page,
    pageSize,
    totalPages: Math.ceil(data.length / pageSize)
  }
  
  return success(paginatedData)
}

/**
 * Mock服务类
 */
export class MockService {
  /**
   * 检查是否应该使用mock数据
   */
  static shouldUseMock(): boolean {
    return config.useMockData
  }

  /**
   * 认证相关mock
   */
  static async auth(method: string, url: string, data?: Record<string, unknown>): Promise<ApiResponse> {
    await delay()
    
    if (url.includes('/auth/login')) {
      const { email, password } = data || {}
      if (email === 'admin@example.com' && password === '123456') {
        const user = users.find(u => u.email === email)
        return success({
          user,
          token: 'mock-jwt-token-' + Date.now()
        })
      }
      return error('邮箱或密码错误', 401)
    }
    
    if (url.includes('/auth/me')) {
      return success(users[0])
    }
    
    if (url.includes('/auth/logout')) {
      return success(null)
    }
    
    return error('未找到对应的mock接口', 404)
  }

  /**
   * 用户相关mock
   */
  static async user(method: string, url: string, params?: Record<string, unknown>): Promise<ApiResponse> {
    await delay()
    
    if (method === 'GET' && url === '/users') {
      const { page = 1, pageSize = 10, search = '' } = params || {}
      
      let filteredUsers = users
      if (search) {
        const searchStr = String(search).toLowerCase()
        filteredUsers = users.filter(user => 
          user.name.toLowerCase().includes(searchStr) ||
          user.email.toLowerCase().includes(searchStr)
        )
      }
      
      return paginate(filteredUsers, Number(page), Number(pageSize))
    }
    
    if (method === 'GET' && url.includes('/users/')) {
      const userId = url.split('/').pop()
      const user = users.find(u => u.id === userId)
      return user ? success(user) : error('用户不存在', 404)
    }
    
    return error('未找到对应的mock接口', 404)
  }

  /**
   * 项目相关mock
   */
  static async project(method: string, url: string, data?: Record<string, unknown>, params?: Record<string, unknown>): Promise<ApiResponse> {
    await delay()
    
    if (method === 'GET' && url === '/projects') {
      const { page = 1, pageSize = 10, status = '', search = '' } = params || {}
      
      let filteredProjects = projects
      if (status) {
        filteredProjects = filteredProjects.filter(p => p.status === status)
      }
      if (search) {
        const searchStr = String(search).toLowerCase()
        filteredProjects = filteredProjects.filter(p => 
          p.name.toLowerCase().includes(searchStr) ||
          p.description.toLowerCase().includes(searchStr)
        )
      }
      
      return paginate(filteredProjects, Number(page), Number(pageSize))
    }
    
    if (method === 'GET' && url.includes('/projects/')) {
      const projectId = url.split('/').pop()
      const project = projects.find(p => p.id === projectId)
      return project ? success(project) : error('项目不存在', 404)
    }
    
    if (method === 'POST' && url === '/projects') {
      const projectData = data as Partial<Project>
      const newProject: Project = {
        id: 'proj_' + Date.now(),
        name: projectData?.name || '新项目',
        description: projectData?.description || '',
        category: projectData?.category || '其他',
        status: projectData?.status || 'active',
        progress: projectData?.progress || 0,
        startDate: projectData?.startDate || new Date().toISOString(),
        endDate: projectData?.endDate,
        members: [],
        tasks: [],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
      projects.push(newProject)
      return success(newProject)
    }
    
    if (method === 'PUT' && url.includes('/projects/')) {
      const projectId = url.split('/').pop()
      const projectIndex = projects.findIndex(p => p.id === projectId)
      
      if (projectIndex === -1) {
        return error('项目不存在', 404)
      }
      
      const projectData = data as Partial<Project>
      const updatedProject = {
        ...projects[projectIndex],
        ...projectData,
        updatedAt: new Date().toISOString()
      }
      
      projects[projectIndex] = updatedProject
      return success(updatedProject)
    }
    
    return error('未找到对应的mock接口', 404)
  }

  /**
   * 任务相关mock
   */
  static async task(method: string, url: string, data?: Record<string, unknown>, params?: Record<string, unknown>): Promise<ApiResponse> {
    await delay()
    
    if (method === 'GET' && url === '/tasks/today') {
      // 获取今日待办任务（状态为 todo 或 in-progress 的任务）
      // const todayTasks = tasks.filter(t => 
      //   t.status === 'todo' || t.status === 'in-progress'
      // )
      return success(tasks)
    }
    
    if (method === 'GET' && url === '/tasks') {
      const { page = 1, pageSize = 10, projectId = '', status = '', search = '' } = params || {}
      
      let filteredTasks = tasks
      if (projectId) {
        filteredTasks = filteredTasks.filter(t => t.projectId === projectId)
      }
      if (status) {
        filteredTasks = filteredTasks.filter(t => t.status === status)
      }
      if (search) {
        const searchStr = String(search).toLowerCase()
        filteredTasks = filteredTasks.filter(t => 
          t.title.toLowerCase().includes(searchStr) ||
          (t.description && t.description.toLowerCase().includes(searchStr))
        )
      }
      
      return paginate(filteredTasks, Number(page), Number(pageSize))
    }
    
    if (method === 'GET' && url.includes('/tasks/')) {
      const taskId = url.split('/').pop()
      const task = tasks.find(t => t.id === taskId)
      return task ? success(task) : error('任务不存在', 404)
    }
    
    if (method === 'POST' && url === '/tasks') {
      const taskData = data as Partial<Task>
      const defaultUser = users[0] // 使用第一个用户作为默认reporter
      const newTask: Task = {
        id: 'task_' + Date.now(),
        title: taskData?.title || '新任务',
        description: taskData?.description,
        status: taskData?.status || 'todo',
        priority: taskData?.priority || 'medium',
        reporter: defaultUser,
        assignee: taskData?.assignee,
        projectId: taskData?.projectId || '',
        dueDate: taskData?.dueDate,
        tags: [],
        comments: [],
        attachments: [],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
      tasks.push(newTask)
      return success(newTask)
    }
    
    if (method === 'PUT' && url.includes('/tasks/')) {
      const taskId = url.split('/').pop()
      const taskIndex = tasks.findIndex(t => t.id === taskId)
      
      if (taskIndex === -1) {
        return error('任务不存在', 404)
      }
      
      const taskData = data as Partial<Task>
      const updatedTask = {
        ...tasks[taskIndex],
        ...taskData,
        updatedAt: new Date().toISOString()
      }
      
      tasks[taskIndex] = updatedTask
      return success(updatedTask)
    }
    
    if (method === 'PATCH' && url.includes('/tasks/') && url.includes('/status')) {
      const taskId = url.split('/')[2] // 从 /tasks/{id}/status 中提取 id
      const taskIndex = tasks.findIndex(t => t.id === taskId)
      
      if (taskIndex === -1) {
        return error('任务不存在', 404)
      }
      
      const { status } = data as { status: TaskStatus }
      tasks[taskIndex] = {
        ...tasks[taskIndex],
        status,
        updatedAt: new Date().toISOString()
      }
      
      return success(tasks[taskIndex])
    }
    
    return error('未找到对应的mock接口', 404)
  }

  /**
   * 消息相关mock
   */
  static async message(method: string, url: string, params?: Record<string, unknown>): Promise<ApiResponse> {
    await delay()
    
    if (url.includes('/messages/channels') && !url.includes('/messages')) {
      const channels = [
        {
          id: 'channel_1',
          name: '项目讨论',
          type: 'group',
          members: users.slice(0, 3),
          unreadCount: 2,
          createdAt: '2024-01-01T00:00:00Z'
        },
        {
          id: 'channel_2',
          name: '技术交流',
          type: 'group',
          members: users.slice(1, 4),
          unreadCount: 0,
          createdAt: '2024-01-02T00:00:00Z'
        }
      ]
      return success(channels)
    }
    
    if (url.includes('/messages/channels/') && url.includes('/messages')) {
      const { page = 1, pageSize = 20 } = params || {}
      return paginate(messages, Number(page), Number(pageSize))
    }
    
    return error('未找到对应的mock接口', 404)
  }

  /**
   * 活动相关mock
   */
  static async activity(method: string, url: string, params?: Record<string, unknown>): Promise<ApiResponse> {
    await delay()
    
    if (method === 'GET' && url === '/activities') {
      const { page = 1, pageSize = 10 } = params || {}
      return paginate(activities, Number(page), Number(pageSize))
    }
    
    return error('未找到对应的mock接口', 404)
  }

  /**
   * 通知相关mock
   */
  static async notification(method: string, url: string, params?: Record<string, unknown>): Promise<ApiResponse> {
    await delay()
    
    if (method === 'GET' && url === '/notifications') {
      const { page = 1, pageSize = 10 } = params || {}
      return paginate(notifications, Number(page), Number(pageSize))
    }
    
    return error('未找到对应的mock接口', 404)
  }

  /**
   * 仪表板相关mock
   */
  static async dashboard(method: string, url: string): Promise<ApiResponse> {
    await delay()
    
    if (url.includes('/dashboard/stats')) {
      const today = new Date()
      const todayStr = today.toISOString().split('T')[0]
      
      // 计算今日任务（模拟：假设有一些任务的创建日期是今天）
      const todayTasks = tasks.filter(t => t.createdAt.startsWith(todayStr))
      const todayCompletedTasks = todayTasks.filter(t => t.status === 'done').length
      const todayTotalTasks = Math.max(todayTasks.length, 5) // 至少显示5个任务
      
      // 计算总任务
      const allCompletedTasks = tasks.filter(t => t.status === 'done').length
      const allTotalTasks = tasks.length
      
      // 计算项目数据
      const completedProjects = projects.filter(p => p.status === 'completed').length
      const totalProjects = projects.length
      
      // 计算延期项目（模拟：假设有endDate且已过期的项目）
      const overdueProjects = projects.filter(p => {
        if (!p.endDate) return false
        const endDate = new Date(p.endDate)
        return endDate < today && p.status !== 'completed'
      }).length
      
      return success({
        // 今日任务数据
        todayCompletedTasks,
        todayTotalTasks,
        
        // 总任务数据
        allCompletedTasks,
        allTotalTasks,
        
        // 项目数据
        completedProjects,
        totalProjects,
        
        // 延期项目数据
        overdueProjects,
        
        // 保留原有字段以兼容其他地方的使用
        activeProjects: projects.filter(p => p.status === 'active').length,
        completedTasks: allCompletedTasks,
        pendingTasks: allTotalTasks - allCompletedTasks,
        teamMembers: users.length,
        recentActivities: activities.slice(0, 5)
      })
    }
    
    if (url.includes('/dashboard/project-progress')) {
      const data = projects.map(project => ({
        projectId: project.id,
        name: project.name,
        progress: project.progress
      }))
      return success(data)
    }
    
    if (url.includes('/dashboard/task-stats')) {
      const stats = [
        { status: 'todo', count: tasks.filter(t => t.status === 'todo').length },
        { status: 'in-progress', count: tasks.filter(t => t.status === 'in-progress').length },
        { status: 'review', count: tasks.filter(t => t.status === 'review').length },
        { status: 'done', count: tasks.filter(t => t.status === 'done').length }
      ]
      return success(stats)
    }
    
    if (url.includes('/dashboard/project-category-distribution')) {
      // 统计项目类别分布
      const categoryMap = new Map<string, number>()
      
      projects.forEach(project => {
        const category = project.category || '其他'
        categoryMap.set(category, (categoryMap.get(category) || 0) + 1)
      })
      
      const categoryData = Array.from(categoryMap.entries()).map(([category, count]) => ({
        category,
        count
      }))
      
      return success(categoryData)
    }
    
    if (url.includes('/dashboard/today-tasks')) {
      // 获取今日待办任务
      const today = new Date().toISOString().split('T')[0]
      const todayTasks = tasks.filter(task => {
        // 包含今日截止的任务和逾期任务
        return task.dueDate === today || task.status === 'overdue' || 
               (task.status === 'pending' && task.dueDate && task.dueDate <= today)
      })
      
      return success(todayTasks)
    }
    
    return error('未找到对应的mock接口', 404)
  }

  /**
   * 搜索相关mock
   */
  static async search(method: string, url: string, params?: Record<string, unknown>): Promise<ApiResponse> {
    await delay()
    
    if (method === 'GET' && url === '/search') {
      const { query: searchQuery } = params || {}
      
      if (!searchQuery) {
        return success([])
      }
      
      const results = []
      
      // 搜索项目
      const searchStr = String(searchQuery).toLowerCase()
      const matchedProjects = projects.filter(p => 
        p.name.toLowerCase().includes(searchStr)
      )
      results.push(...matchedProjects.map(p => ({
        type: 'project',
        id: p.id,
        title: p.name,
        description: p.description,
        url: `/projects/${p.id}`
      })))
      
      // 搜索任务
      const matchedTasks = tasks.filter(t => 
        t.title.toLowerCase().includes(searchStr)
      )
      results.push(...matchedTasks.map(t => ({
        type: 'task',
        id: t.id,
        title: t.title,
        description: t.description,
        url: `/tasks/${t.id}`
      })))
      
      return success(results)
    }
    
    return error('未找到对应的mock接口', 404)
  }

  /**
   * 上传相关mock
   */
  static async upload(method: string, url: string): Promise<ApiResponse> {
    await delay(1000) // 模拟上传时间
    
    if (method === 'POST' && url === '/upload') {
      return success({
        url: 'https://example.com/uploads/mock-file-' + Date.now() + '.jpg',
        filename: 'mock-file.jpg',
        size: 1024 * 1024 // 1MB
      })
    }
    
    return error('未找到对应的mock接口', 404)
  }

  /**
   * 路由mock请求到对应的处理函数
   * @param method HTTP方法
   * @param url 请求URL
   * @param data 请求数据
   * @param params 查询参数
   */
  static async handleRequest(method: string, url: string, data?: Record<string, unknown>, params?: Record<string, unknown>): Promise<ApiResponse> {
    // 移除URL前缀
    const cleanUrl = url.replace(/^\/api/, '')
    
    // 根据URL路径路由到对应的mock处理函数
    if (cleanUrl.startsWith('/auth')) {
      return this.auth(method, cleanUrl, data)
    }
    
    if (cleanUrl.startsWith('/users')) {
      return this.user(method, cleanUrl, params)
    }
    
    if (cleanUrl.startsWith('/projects')) {
      return this.project(method, cleanUrl, data, params)
    }
    
    if (cleanUrl.startsWith('/tasks')) {
      return this.task(method, cleanUrl, data, params)
    }
    
    if (cleanUrl.startsWith('/messages')) {
      return this.message(method, cleanUrl, params)
    }
    
    if (cleanUrl.startsWith('/activities')) {
      return this.activity(method, cleanUrl, params)
    }
    
    if (cleanUrl.startsWith('/notifications')) {
      return this.notification(method, cleanUrl, params)
    }
    
    if (cleanUrl.startsWith('/dashboard')) {
      return this.dashboard(method, cleanUrl)
    }
    
    if (cleanUrl.startsWith('/search')) {
      return this.search(method, cleanUrl, params)
    }
    
    if (cleanUrl.startsWith('/upload')) {
      return this.upload(method, cleanUrl)
    }
    
    return error('未找到对应的mock接口', 404)
  }
}

export default MockService