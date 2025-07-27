// Mock数据配置
import { MockMethod } from 'vite-plugin-mock'
import { users, projects, tasks, messages, activities, notifications } from './data'

// 工具函数
function success<T>(data: T, message = 'success') {
  return {
    success: true,
    data,
    message
  }
}

function error(message = 'error', code = 500) {
  return {
    success: false,
    message,
    code
  }
}

function paginate<T>(data: T[], page = 1, pageSize = 10) {
  const start = (page - 1) * pageSize
  const end = start + pageSize
  const items = data.slice(start, end)
  
  return success({
    items,
    total: data.length,
    page,
    pageSize,
    totalPages: Math.ceil(data.length / pageSize)
  })
}

// 模拟延迟
function delay(ms = 300) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

const mockApis: MockMethod[] = [
  // 认证相关
  {
    url: '/api/auth/login',
    method: 'post',
    response: async ({ body }) => {
      await delay()
      const { email, password } = body
      
      if (email === 'admin@example.com' && password === '123456') {
        const user = users.find(u => u.email === email)
        return success({
          user,
          token: 'mock-jwt-token-' + Date.now()
        })
      }
      
      return error('邮箱或密码错误', 401)
    }
  },
  
  {
    url: '/api/auth/me',
    method: 'get',
    response: async () => {
      await delay()
      return success(users[0])
    }
  },
  
  {
    url: '/api/auth/logout',
    method: 'post',
    response: async () => {
      await delay()
      return success(null)
    }
  },
  
  // 用户相关
  {
    url: '/api/users',
    method: 'get',
    response: async ({ query }) => {
      await delay()
      const { page = 1, pageSize = 10, search = '' } = query
      
      let filteredUsers = users
      if (search) {
        filteredUsers = users.filter(user => 
          user.name.toLowerCase().includes(search.toLowerCase()) ||
          user.email.toLowerCase().includes(search.toLowerCase())
        )
      }
      
      return paginate(filteredUsers, Number(page), Number(pageSize))
    }
  },
  
  {
    url: '/api/users/:id',
    method: 'get',
    response: async ({ query }) => {
      await delay()
      const user = users.find(u => u.id === query.id)
      return user ? success(user) : error('用户不存在', 404)
    }
  },
  
  // 项目相关
  {
    url: '/api/projects',
    method: 'get',
    response: async ({ query }) => {
      await delay()
      const { page = 1, pageSize = 10, status = '', search = '' } = query
      
      let filteredProjects = projects
      if (status) {
        filteredProjects = filteredProjects.filter(p => p.status === status)
      }
      if (search) {
        filteredProjects = filteredProjects.filter(p => 
          p.name.toLowerCase().includes(search.toLowerCase()) ||
          p.description.toLowerCase().includes(search.toLowerCase())
        )
      }
      
      return paginate(filteredProjects, Number(page), Number(pageSize))
    }
  },
  
  {
    url: '/api/projects/:id',
    method: 'get',
    response: async ({ query }) => {
      await delay()
      const project = projects.find(p => p.id === query.id)
      return project ? success(project) : error('项目不存在', 404)
    }
  },
  
  {
    url: '/api/projects',
    method: 'post',
    response: async ({ body }) => {
      await delay()
      const newProject = {
        id: 'proj_' + Date.now(),
        ...body,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
      projects.push(newProject)
      return success(newProject)
    }
  },
  
  // 任务相关
  {
    url: '/api/tasks',
    method: 'get',
    response: async ({ query }) => {
      await delay()
      const { page = 1, pageSize = 10, projectId = '', status = '', search = '' } = query
      
      let filteredTasks = tasks
      if (projectId) {
        filteredTasks = filteredTasks.filter(t => t.projectId === projectId)
      }
      if (status) {
        filteredTasks = filteredTasks.filter(t => t.status === status)
      }
      if (search) {
        filteredTasks = filteredTasks.filter(t => 
          t.title.toLowerCase().includes(search.toLowerCase()) ||
          (t.description && t.description.toLowerCase().includes(search.toLowerCase()))
        )
      }
      
      return paginate(filteredTasks, Number(page), Number(pageSize))
    }
  },
  
  {
    url: '/api/tasks/:id',
    method: 'get',
    response: async ({ query }) => {
      await delay()
      const task = tasks.find(t => t.id === query.id)
      return task ? success(task) : error('任务不存在', 404)
    }
  },
  
  {
    url: '/api/tasks',
    method: 'post',
    response: async ({ body }) => {
      await delay()
      const newTask = {
        id: 'task_' + Date.now(),
        ...body,
        comments: [],
        attachments: [],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
      tasks.push(newTask)
      return success(newTask)
    }
  },
  
  {
    url: '/api/tasks/:id/status',
    method: 'patch',
    response: async ({ query, body }) => {
      await delay()
      const task = tasks.find(t => t.id === query.id)
      if (task) {
        task.status = body.status
        task.updatedAt = new Date().toISOString()
        return success(task)
      }
      return error('任务不存在', 404)
    }
  },
  
  // 消息相关
  {
    url: '/api/messages/channels',
    method: 'get',
    response: async () => {
      await delay()
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
  },
  
  {
    url: '/api/messages/channels/:channelId/messages',
    method: 'get',
    response: async ({ query }) => {
      await delay()
      const { page = 1, pageSize = 20 } = query
      return paginate(messages, Number(page), Number(pageSize))
    }
  },
  
  // 活动相关
  {
    url: '/api/activities',
    method: 'get',
    response: async ({ query }) => {
      await delay()
      const { page = 1, pageSize = 10 } = query
      return paginate(activities, Number(page), Number(pageSize))
    }
  },
  
  // 通知相关
  {
    url: '/api/notifications',
    method: 'get',
    response: async ({ query }) => {
      await delay()
      const { page = 1, pageSize = 10 } = query
      return paginate(notifications, Number(page), Number(pageSize))
    }
  },
  
  // 仪表板相关
  {
    url: '/api/dashboard/stats',
    method: 'get',
    response: async () => {
      await delay()
      return success({
        totalProjects: projects.length,
        activeProjects: projects.filter(p => p.status === 'active').length,
        completedTasks: tasks.filter(t => t.status === 'done').length,
        pendingTasks: tasks.filter(t => t.status !== 'done').length,
        teamMembers: users.length,
        recentActivities: activities.slice(0, 5)
      })
    }
  },
  
  {
    url: '/api/dashboard/project-progress',
    method: 'get',
    response: async () => {
      await delay()
      const data = projects.map(project => ({
        projectId: project.id,
        name: project.name,
        progress: project.progress
      }))
      return success(data)
    }
  },
  
  {
    url: '/api/dashboard/task-stats',
    method: 'get',
    response: async () => {
      await delay()
      const stats = [
        { status: 'todo', count: tasks.filter(t => t.status === 'todo').length },
        { status: 'in-progress', count: tasks.filter(t => t.status === 'in-progress').length },
        { status: 'review', count: tasks.filter(t => t.status === 'review').length },
        { status: 'done', count: tasks.filter(t => t.status === 'done').length }
      ]
      return success(stats)
    }
  },
  
  // 搜索相关
  {
    url: '/api/search',
    method: 'get',
    response: async ({ query }) => {
      await delay()
      const { query: searchQuery } = query
      
      if (!searchQuery) {
        return success([])
      }
      
      const results = []
      
      // 搜索项目
      const matchedProjects = projects.filter(p => 
        p.name.toLowerCase().includes(searchQuery.toLowerCase())
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
        t.title.toLowerCase().includes(searchQuery.toLowerCase())
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
  }
]

export default mockApis