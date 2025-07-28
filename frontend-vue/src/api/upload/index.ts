// 文件上传相关API接口
import { http } from '@/utils/request'
import type {
  UploadFileResponse,
  UploadProgressCallback,
  UploadApiResponse
} from './types'

/**
 * 文件上传API模块
 */
export const uploadApi = {
  /**
   * 上传文件
   * @param file 要上传的文件
   * @param onProgress 上传进度回调函数
   * @returns 上传结果
   */
  uploadFile(file: File, onProgress?: UploadProgressCallback): Promise<UploadApiResponse<UploadFileResponse>> {
    const formData = new FormData()
    formData.append('file', file)
    
    return http.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      }
    })
  },
  
  /**
   * 删除文件
   * @param url 文件URL
   * @returns 删除结果
   */
  deleteFile(url: string): Promise<UploadApiResponse> {
    return http.delete('/upload', { data: { url } })
  }
}

export * from './types'