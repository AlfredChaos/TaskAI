// 认证相关类型定义
import type { User, ApiResponse } from '@/types'

/**
 * 登录请求参数
 */
export interface LoginRequest {
  email: string
  password: string
}

/**
 * 注册请求参数
 */
export interface RegisterRequest {
  name: string
  email: string
  password: string
}

/**
 * 登录响应数据
 */
export interface LoginResponse {
  user: User
  token: string
}

/**
 * 注册响应数据
 */
export interface RegisterResponse {
  user: User
  token: string
}

/**
 * 刷新Token响应数据
 */
export interface RefreshTokenResponse {
  token: string
}

/**
 * 认证API响应类型
 */
export type AuthApiResponse<T = unknown> = ApiResponse<T>