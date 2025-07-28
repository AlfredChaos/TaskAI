// 认证相关API接口
import { http } from '@/utils/request'
import type { User } from '@/types'
import type {
  LoginRequest,
  RegisterRequest,
  LoginResponse,
  RegisterResponse,
  RefreshTokenResponse,
  AuthApiResponse
} from './types'

/**
 * 认证API模块
 */
export const authApi = {
  /**
   * 用户登录
   * @param data 登录参数
   * @returns 登录响应
   */
  login(data: LoginRequest): Promise<AuthApiResponse<LoginResponse>> {
    return http.post('/auth/login', data)
  },
  
  /**
   * 用户注册
   * @param data 注册参数
   * @returns 注册响应
   */
  register(data: RegisterRequest): Promise<AuthApiResponse<RegisterResponse>> {
    return http.post('/auth/register', data)
  },
  
  /**
   * 用户登出
   * @returns 登出响应
   */
  logout(): Promise<AuthApiResponse> {
    return http.post('/auth/logout')
  },
  
  /**
   * 获取当前用户信息
   * @returns 用户信息
   */
  getCurrentUser(): Promise<AuthApiResponse<User>> {
    return http.get('/auth/me')
  },
  
  /**
   * 刷新访问令牌
   * @returns 新的访问令牌
   */
  refreshToken(): Promise<AuthApiResponse<RefreshTokenResponse>> {
    return http.post('/auth/refresh')
  }
}

export * from './types'