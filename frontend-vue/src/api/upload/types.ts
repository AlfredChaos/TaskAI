// 文件上传相关类型定义
import type { ApiResponse } from '@/types'

/**
 * 文件上传响应数据
 */
export interface UploadFileResponse {
  url: string
  filename: string
}

/**
 * 删除文件请求参数
 */
export interface DeleteFileRequest {
  url: string
}

/**
 * 文件上传进度回调函数
 */
export type UploadProgressCallback = (progress: number) => void

/**
 * 文件上传API响应类型
 */
export type UploadApiResponse<T = unknown> = ApiResponse<T>