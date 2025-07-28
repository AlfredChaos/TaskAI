// 用户相关API接口
import { http } from '@/utils/request'
import type { User } from '@/types'
import type {
  GetUsersParams,
  UpdateUserRequest,
  UpdateAvatarResponse,
  ChangePasswordRequest,
  UserApiResponse,
  UserPaginatedResponse
} from './types'

/**
 * 用户API模块
 */
export const userApi = {
  /**
   * 获取用户列表
   * @param params 查询参数
   * @returns 用户列表
   */
  getUsers(params?: GetUsersParams): Promise<UserPaginatedResponse<User>> {
    return http.get('/users', { params })
  },
  
  /**
   * 获取用户详情
   * @param id 用户ID
   * @returns 用户详情
   */
  getUser(id: string): Promise<UserApiResponse<User>> {
    return http.get(`/users/${id}`)
  },
  
  /**
   * 更新用户信息
   * @param id 用户ID
   * @param data 更新数据
   * @returns 更新后的用户信息
   */
  updateUser(id: string, data: UpdateUserRequest): Promise<UserApiResponse<User>> {
    return http.put(`/users/${id}`, data)
  },
  
  /**
   * 更新用户头像
   * @param file 头像文件
   * @returns 头像URL
   */
  updateAvatar(file: File): Promise<UserApiResponse<UpdateAvatarResponse>> {
    const formData = new FormData()
    formData.append('avatar', file)
    return http.post('/users/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  /**
   * 修改密码
   * @param data 密码修改参数
   * @returns 修改结果
   */
  changePassword(data: ChangePasswordRequest): Promise<UserApiResponse> {
    return http.post('/users/change-password', data)
  }
}

export * from './types'