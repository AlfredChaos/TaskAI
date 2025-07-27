// 全局类型定义

// 用户相关类型
export interface User {
  id: string
  name: string
  email: string
  avatar?: string
  role: 'admin' | 'manager' | 'member'
  status: 'online' | 'offline' | 'away'
  createdAt: string
  updatedAt: string
}

// 项目相关类型
export interface Project {
  id: string
  name: string
  description: string
  status: 'active' | 'completed' | 'paused' | 'cancelled'
  progress: number
  startDate: string
  endDate?: string
  members: User[]
  tasks: Task[]
  createdAt: string
  updatedAt: string
}

// 任务相关类型
export interface Task {
  id: string
  title: string
  description?: string
  status: 'todo' | 'in-progress' | 'review' | 'done'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  assignee?: User
  reporter: User
  projectId: string
  dueDate?: string
  tags: string[]
  attachments: Attachment[]
  comments: Comment[]
  createdAt: string
  updatedAt: string
}

// 评论类型
export interface Comment {
  id: string
  content: string
  author: User
  taskId: string
  createdAt: string
  updatedAt: string
}

// 附件类型
export interface Attachment {
  id: string
  name: string
  url: string
  size: number
  type: string
  uploadedBy: User
  createdAt: string
}

// 消息相关类型
export interface Message {
  id: string
  content: string
  type: 'text' | 'image' | 'file' | 'system'
  sender: User
  receiver?: User
  channelId?: string
  isRead: boolean
  createdAt: string
}

export interface Channel {
  id: string
  name: string
  type: 'direct' | 'group' | 'project'
  members: User[]
  lastMessage?: Message
  unreadCount: number
  createdAt: string
}

// 活动相关类型
export interface Activity {
  id: string
  type: 'task_created' | 'task_updated' | 'task_completed' | 'comment_added' | 'file_uploaded' | 'user_joined'
  description: string
  actor: User
  target?: {
    type: 'task' | 'project' | 'user'
    id: string
    name: string
  }
  metadata?: Record<string, unknown>
  createdAt: string
}

// 通知类型
export interface Notification {
  id: string
  title: string
  message: string
  type: 'info' | 'success' | 'warning' | 'error'
  isRead: boolean
  actionUrl?: string
  createdAt: string
}

// API响应类型
export interface ApiResponse<T = unknown> {
  success: boolean
  data: T
  message?: string
  code?: number
}

export interface PaginatedResponse<T = unknown> {
  success: boolean
  data: {
    items: T[]
    total: number
    page: number
    pageSize: number
    totalPages: number
  }
  message?: string
}

// 表单相关类型
export interface FormRule {
  required?: boolean
  message?: string
  trigger?: 'blur' | 'change'
  min?: number
  max?: number
  pattern?: RegExp
  validator?: (rule: FormRule, value: unknown, callback: (error?: Error) => void) => void
}

// 路由相关类型
export interface RouteMenuItem {
  path: string
  name: string
  icon?: string
  children?: RouteMenuItem[]
  meta?: {
    title: string
    requiresAuth?: boolean
    roles?: string[]
  }
}

// 主题相关类型
export interface ThemeConfig {
  mode: 'light' | 'dark'
  primaryColor: string
  sidebarCollapsed: boolean
}

// 统计数据类型
export interface DashboardStats {
  totalProjects: number
  activeProjects: number
  completedTasks: number
  pendingTasks: number
  teamMembers: number
  recentActivities: Activity[]
}

// 图表数据类型
export interface ChartData {
  labels: string[]
  datasets: {
    label: string
    data: number[]
    backgroundColor?: string | string[]
    borderColor?: string
    borderWidth?: number
  }[]
}

// 文件上传类型
export interface UploadFile {
  name: string
  size: number
  type: string
  url?: string
  status: 'uploading' | 'success' | 'error'
  progress?: number
}

// 搜索相关类型
export interface SearchResult {
  type: 'project' | 'task' | 'user' | 'message'
  id: string
  title: string
  description?: string
  url: string
  highlight?: string
}

export interface SearchFilters {
  type?: string[]
  dateRange?: [string, string]
  status?: string[]
  assignee?: string[]
  priority?: string[]
}