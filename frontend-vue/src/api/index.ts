/**
 * API服务统一入口
 * 提供模块化的API接口，便于维护和扩展
 */

// 导入各个模块的API
export { authApi } from './auth'
export { userApi } from './user'
export { projectApi } from './project'
export { taskApi } from './task'
export { messageApi } from './message'
export { activityApi } from './activity'
export { notificationApi } from './notification'
export { dashboardApi } from './dashboard'
export { searchApi } from './search'
export { uploadApi } from './upload'

// 导出各个模块的类型定义
export * from './auth/types'
export * from './user/types'
export * from './project/types'
export * from './task/types'
export * from './message/types'
export * from './activity/types'
export * from './notification/types'
export * from './dashboard/types'
export * from './search/types'
export * from './upload/types'

// 重新导出通用类型
export type {
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