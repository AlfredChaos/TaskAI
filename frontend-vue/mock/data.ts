// Mock数据
import type { User, Project, Task, Notification, TimelineNode } from '../src/types'

// 用户数据
export const users: User[] = [
  {
    id: 'user_1',
    name: '张三',
    email: 'admin@example.com',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Zhang',
    role: 'admin',
    status: 'online',
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-01T00:00:00Z'
  },
  {
    id: 'user_2',
    name: '李四',
    email: 'lisi@example.com',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Li',
    role: 'manager',
    status: 'online',
    createdAt: '2024-01-02T00:00:00Z',
    updatedAt: '2024-01-02T00:00:00Z'
  },
  {
    id: 'user_3',
    name: '王五',
    email: 'wangwu@example.com',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Wang',
    role: 'member',
    status: 'away',
    createdAt: '2024-01-03T00:00:00Z',
    updatedAt: '2024-01-03T00:00:00Z'
  },
  {
    id: 'user_4',
    name: '赵六',
    email: 'zhaoliu@example.com',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Zhao',
    role: 'member',
    status: 'offline',
    createdAt: '2024-01-04T00:00:00Z',
    updatedAt: '2024-01-04T00:00:00Z'
  },
  {
    id: 'user_5',
    name: '孙七',
    email: 'sunqi@example.com',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sun',
    role: 'member',
    status: 'online',
    createdAt: '2024-01-05T00:00:00Z',
    updatedAt: '2024-01-05T00:00:00Z'
  }
]

// 项目时间线数据
export const timelineNodes: TimelineNode[] = [
  {
    id: 'timeline_1',
    type: 'project_created',
    title: '项目创建',
    description: 'TaskAI项目管理系统正式启动',
    date: '2024-01-01T00:00:00Z',
    isMilestone: true,
    projectId: 'proj_1',
    createdAt: '2024-01-01T00:00:00Z'
  },
  {
    id: 'timeline_2',
    type: 'task_completed',
    title: '设计系统架构任务完成',
    description: '系统架构设计已完成',
    date: '2024-01-15T00:00:00Z',
    isMilestone: false,
    taskId: 'task_1',
    projectId: 'proj_1',
    createdAt: '2024-01-15T00:00:00Z'
  },
  {
    id: 'timeline_3',
    type: 'project_created',
    title: '项目创建',
    description: '移动端应用开发项目启动',
    date: '2024-02-01T00:00:00Z',
    isMilestone: true,
    projectId: 'proj_2',
    createdAt: '2024-02-01T00:00:00Z'
  },
  {
    id: 'timeline_4',
    type: 'project_created',
    title: '项目创建',
    description: '数据分析平台项目启动',
    date: '2024-01-15T00:00:00Z',
    isMilestone: true,
    projectId: 'proj_3',
    createdAt: '2024-01-15T00:00:00Z'
  },
  {
    id: 'timeline_5',
    type: 'project_completed',
    title: '项目完成',
    description: '客户关系管理系统项目已完成',
    date: '2023-12-31T00:00:00Z',
    isMilestone: true,
    projectId: 'proj_4',
    createdAt: '2023-12-31T00:00:00Z'
  }
]

// 项目数据
export const projects: Project[] = [
  {
    id: 'proj_1',
    name: 'TaskAI项目管理系统',
    description: '一个现代化的项目管理系统，支持任务管理、团队协作、进度跟踪等功能',
    category: '软件开发',
    status: 'active',
    priority: 'high',
    progress: 75,
    startDate: '2024-01-01',
    endDate: '2024-06-30',
    members: users.slice(0, 4),
    tasks: [],
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-15T00:00:00Z'
  },
  {
    id: 'proj_2',
    name: '移动端应用开发',
    description: '开发一款跨平台的移动端应用，提供便捷的移动办公体验',
    category: '移动开发',
    status: 'active',
    priority: 'medium',
    progress: 45,
    startDate: '2024-02-01',
    endDate: '2024-08-31',
    members: users.slice(1, 4),
    tasks: [],
    createdAt: '2024-02-01T00:00:00Z',
    updatedAt: '2024-02-15T00:00:00Z'
  },
  {
    id: 'proj_3',
    name: '数据分析平台',
    description: "构建一个用于数据可视化的 Web 应用程序",
    category: '数据分析',
    status: 'overdue',
    priority: 'urgent',
    progress: 30,
    startDate: '2024-01-15',
    endDate: '2024-07-15',
    members: users.slice(2, 5),
    tasks: [],
    createdAt: '2024-01-15T00:00:00Z',
    updatedAt: '2024-02-01T00:00:00Z'
  },
  {
    id: 'proj_4',
    name: '客户关系管理系统',
    description: '完善的CRM系统，帮助企业更好地管理客户关系和销售流程',
    category: '企业管理',
    status: 'completed',
    priority: 'medium',
    progress: 100,
    startDate: '2023-09-01',
    endDate: '2023-12-31',
    members: users.slice(0, 3),
    tasks: [],
    createdAt: '2023-09-01T00:00:00Z',
    updatedAt: '2023-12-31T00:00:00Z'
  },
  {
    id: 'proj_5',
    name: '电商平台重构',
    description: '重构现有电商平台，提升性能和用户体验',
    category: '软件开发',
    status: 'active',
    priority: 'high',
    progress: 60,
    startDate: '2024-01-20',
    endDate: '2024-05-20',
    members: users.slice(0, 3),
    tasks: [],
    createdAt: '2024-01-20T00:00:00Z',
    updatedAt: '2024-02-10T00:00:00Z'
  },
  {
    id: 'proj_6',
    name: '智能推荐系统',
    description: '基于机器学习的智能推荐系统开发',
    category: '人工智能',
    status: 'active',
    priority: 'low',
    progress: 25,
    startDate: '2024-02-15',
    endDate: '2024-08-15',
    members: users.slice(2, 5),
    tasks: [],
    createdAt: '2024-02-15T00:00:00Z',
    updatedAt: '2024-02-20T00:00:00Z'
  },
  {
    id: 'proj_7',
    name: '营销活动管理',
    description: '营销活动策划和执行管理系统',
    category: '市场营销',
    status: 'completed',
    priority: 'low',
    progress: 100,
    startDate: '2023-10-01',
    endDate: '2024-01-31',
    members: users.slice(1, 4),
    tasks: [],
    createdAt: '2023-10-01T00:00:00Z',
    updatedAt: '2024-01-31T00:00:00Z'
  },
  {
    id: 'proj_8',
    name: '财务报表系统',
    description: '企业财务报表自动化生成系统',
    category: '企业管理',
    status: 'active',
    priority: 'medium',
    progress: 80,
    startDate: '2023-11-01',
    endDate: '2024-03-31',
    members: users.slice(0, 2),
    tasks: [],
    createdAt: '2023-11-01T00:00:00Z',
    updatedAt: '2024-02-15T00:00:00Z'
  }
]

// 任务数据
export const tasks: Task[] = [
  {
    id: 'task_1',
    title: '设计系统架构',
    description: '设计整个系统的技术架构，包括前端、后端和数据库设计',
    status: 'completed',
    priority: 'high',
    assignee: users[0],
    reporter: users[1],
    projectId: 'proj_1',
    dueDate: '2024-01-15',
    estimatedHours: 40,
    remainingHours: 0,
    tags: ['架构', '设计'],
    attachments: [],
    comments: [],
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-15T00:00:00Z'
  },
  {
    id: 'task_2',
    title: '实现用户认证功能',
    description: '开发用户登录、注册、密码重置等认证相关功能',
    status: 'pending',
    priority: 'high',
    assignee: users[1],
    reporter: users[0],
    projectId: 'proj_1',
    dueDate: new Date().toISOString().split('T')[0], // 今日截止
    estimatedHours: 24,
    remainingHours: 16,
    tags: ['认证', '安全'],
    attachments: [],
    comments: [],
    createdAt: '2024-01-10T00:00:00Z',
    updatedAt: '2024-01-20T00:00:00Z'
  },
  {
    id: 'task_3',
    title: '设计UI界面',
    description: '设计系统的用户界面，包括页面布局、组件设计等',
    status: 'overdue',
    priority: 'medium',
    assignee: users[2],
    reporter: users[0],
    projectId: 'proj_1',
    dueDate: '2024-01-25', // 已过期
    estimatedHours: 32,
    remainingHours: 8,
    tags: ['UI', '设计'],
    attachments: [],
    comments: [],
    createdAt: '2024-01-05T00:00:00Z',
    updatedAt: '2024-01-22T00:00:00Z'
  },
  {
    id: 'task_4',
    title: '数据库设计',
    description: '设计数据库表结构，建立数据模型',
    status: 'pending',
    priority: 'medium',
    assignee: users[3],
    reporter: users[0],
    projectId: 'proj_1',
    dueDate: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().split('T')[0], // 明日截止
    estimatedHours: 16,
    remainingHours: 16,
    tags: ['数据库', '设计'],
    attachments: [],
    comments: [],
    createdAt: '2024-01-12T00:00:00Z',
    updatedAt: '2024-01-12T00:00:00Z'
  },
  {
    id: 'task_5',
    title: '移动端界面适配',
    description: '适配移动端界面，确保在不同设备上的显示效果',
    status: 'pending',
    priority: 'low',
    assignee: users[2],
    reporter: users[1],
    projectId: 'proj_2',
    dueDate: new Date().toISOString().split('T')[0], // 今日截止
    estimatedHours: 20,
    remainingHours: 12,
    tags: ['移动端', '适配'],
    attachments: [],
    comments: [],
    createdAt: '2024-02-01T00:00:00Z',
    updatedAt: '2024-02-10T00:00:00Z'
  },
  {
    id: 'task_6',
    title: 'API接口开发',
    description: '开发后端API接口，提供数据服务',
    status: 'overdue',
    priority: 'urgent',
    assignee: users[4],
    reporter: users[1],
    projectId: 'proj_2',
    dueDate: '2024-02-20', // 已过期
    estimatedHours: 30,
    remainingHours: 18,
    tags: ['API', '后端'],
    attachments: [],
    comments: [],
    createdAt: '2024-02-05T00:00:00Z',
    updatedAt: '2024-02-05T00:00:00Z'
  },
  {
    id: 'task_7',
    title: '编写单元测试',
    description: '为核心功能编写单元测试，确保代码质量',
    status: 'pending',
    priority: 'medium',
    assignee: users[0],
    reporter: users[1],
    projectId: 'proj_1',
    dueDate: new Date().toISOString().split('T')[0], // 今日截止
    estimatedHours: 12,
    remainingHours: 12,
    tags: ['测试', '质量'],
    attachments: [],
    comments: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    id: 'task_8',
    title: '性能优化',
    description: '优化系统性能，提升响应速度',
    status: 'pending',
    priority: 'high',
    assignee: users[1],
    reporter: users[0],
    projectId: 'proj_1',
    dueDate: new Date().toISOString().split('T')[0], // 今日截止
    estimatedHours: 8,
    remainingHours: 6,
    tags: ['性能', '优化'],
    attachments: [],
    comments: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
]





// 通知数据
export const notifications: Notification[] = [
  {
    id: 'notif_1',
    title: '新任务分配',
    message: '您被分配了新任务：实现用户认证功能',
    type: 'info',
    isRead: false,
    actionUrl: '/tasks/task_2',
    createdAt: '2024-01-01T09:30:00Z'
  },
  {
    id: 'notif_2',
    title: '任务即将到期',
    message: '任务"设计UI界面"将在3天后到期',
    type: 'warning',
    isRead: false,
    actionUrl: '/tasks/task_3',
    createdAt: '2024-01-01T10:00:00Z'
  },
  {
    id: 'notif_3',
    title: '项目进度更新',
    message: 'TaskAI项目管理系统进度已更新至75%',
    type: 'success',
    isRead: true,
    actionUrl: '/projects/proj_1',
    createdAt: '2024-01-01T11:00:00Z'
  },
  {
    id: 'notif_4',
    title: '新消息',
    message: '您在项目讨论组有新消息',
    type: 'info',
    isRead: true,
    actionUrl: '/messages/channel_1',
    createdAt: '2024-01-01T12:00:00Z'
  },
  {
    id: 'notif_5',
    title: '系统维护通知',
    message: '系统将在今晚22:00-24:00进行维护',
    type: 'warning',
    isRead: false,
    actionUrl: '',
    createdAt: '2024-01-01T15:00:00Z'
  }
]