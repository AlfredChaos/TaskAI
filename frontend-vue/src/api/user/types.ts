// 用户相关类型定义
import type { User, ApiResponse, PaginatedResponse } from '@/types'

/**
 * 获取用户列表请求参数
 */
export interface GetUsersParams {
  page?: number
  pageSize?: number
  search?: string
}

/**
 * 更新用户信息请求参数
 */
export type UpdateUserRequest = Partial<User>

/**
 * 更新头像响应数据
 */
export interface UpdateAvatarResponse {
  avatar: string
}

/**
 * 修改密码请求参数
 */
export interface ChangePasswordRequest {
  oldPassword: string
  newPassword: string
}

/**
 * 用户API响应类型
 */
export type UserApiResponse<T = unknown> = ApiResponse<T>
export type UserPaginatedResponse<T = unknown> = PaginatedResponse<T>