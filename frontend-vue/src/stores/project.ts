import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { Project } from '@/types'
import { projectApi } from '@/api'

/**
 * 项目状态管理
 */
export const useProjectStore = defineStore('project', () => {
  // 状态
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const pagination = ref({
    current: 1,
    pageSize: 10,
    total: 0
  })
  const filters = ref({
    status: '',
    search: ''
  })

  // 计算属性
  const projectCount = computed(() => projects.value.length)
  const activeProjects = computed(() => 
    projects.value.filter(p => p.status === 'active')
  )
  const completedProjects = computed(() => 
    projects.value.filter(p => p.status === 'completed')
  )
  const pausedProjects = computed(() => 
    projects.value.filter(p => p.status === 'paused')
  )
  const cancelledProjects = computed(() => 
    projects.value.filter(p => p.status === 'cancelled')
  )
  const myProjects = computed(() => {
    // 这里需要从用户store获取当前用户ID
    // 暂时返回所有项目
    return projects.value
  })

  /**
   * 获取项目列表
   */
  const fetchProjects = async (params?: {
    page?: number
    pageSize?: number
    status?: string
    search?: string
  }) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await projectApi.getProjects({
        page: params?.page || pagination.value.current,
        pageSize: params?.pageSize || pagination.value.pageSize,
        status: params?.status || filters.value.status,
        search: params?.search || filters.value.search
      })
      
      if (response.success) {
        projects.value = response.data.items
        pagination.value = {
          current: response.data.page,
          pageSize: response.data.pageSize,
          total: response.data.total
        }
      } else {
        throw new Error(response.message || '获取项目列表失败')
      }
    } catch {
      error.value = '获取项目列表失败'
      projects.value = []
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 获取项目详情
   */
  const fetchProject = async (id: string) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await projectApi.getProject(id)
      
      if (response.success) {
        currentProject.value = response.data as Project
        
        // 更新项目列表中的对应项目
        const index = projects.value.findIndex(p => p.id === id)
        if (index !== -1) {
          projects.value[index] = response.data as Project
        }
      } else {
        throw new Error(response.message || '获取项目详情失败')
      }
    } catch {
      error.value = '获取项目详情失败'
      currentProject.value = null
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 创建项目
   */
  const createProject = async (projectData: Omit<Project, 'id' | 'createdAt' | 'updatedAt'>) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await projectApi.createProject(projectData)
      
      if (response.success) {
        const newProject = response.data as Project
        projects.value.unshift(newProject)
        pagination.value.total += 1
        return newProject
      } else {
        throw new Error(response.message || '创建项目失败')
      }
    } catch {
      error.value = '创建项目失败'
      throw error
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 更新项目
   */
  const updateProject = async (id: string, projectData: Partial<Project>) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await projectApi.updateProject(id, projectData)
      
      if (response.success) {
        const updatedProject = response.data as Project
        
        // 更新项目列表
        const index = projects.value.findIndex(p => p.id === id)
        if (index !== -1) {
          projects.value[index] = updatedProject
        }
        
        // 更新当前项目
        if (currentProject.value?.id === id) {
          currentProject.value = updatedProject
        }
        
        return updatedProject
      } else {
        throw new Error(response.message || '更新项目失败')
      }
    } catch {
      error.value = '更新项目失败'
      throw error
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 删除项目
   */
  const deleteProject = async (id: string) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await projectApi.deleteProject(id)
      
      if (response.success) {
        // 从项目列表中移除
        const index = projects.value.findIndex(p => p.id === id)
        if (index !== -1) {
          projects.value.splice(index, 1)
          pagination.value.total -= 1
        }
        
        // 清空当前项目（如果是被删除的项目）
        if (currentProject.value?.id === id) {
          currentProject.value = null
        }
      } else {
        throw new Error(response.message || '删除项目失败')
      }
    } catch {
      error.value = '删除项目失败'
      throw error
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 设置过滤条件
   */
  const setFilters = (newFilters: Partial<typeof filters.value>) => {
    filters.value = { ...filters.value, ...newFilters }
  }

  /**
   * 重置过滤条件
   */
  const resetFilters = () => {
    filters.value = {
      status: '',
      search: ''
    }
  }

  /**
   * 设置当前项目
   */
  const setCurrentProject = (project: Project | null) => {
    currentProject.value = project
  }

  /**
   * 清空错误
   */
  const clearError = () => {
    error.value = null
  }

  /**
   * 刷新项目列表
   */
  const refreshProjects = () => {
    return fetchProjects()
  }

  return {
    // 状态
    projects,
    currentProject,
    isLoading,
    error,
    pagination,
    filters,
    
    // 计算属性
    projectCount,
    activeProjects,
    completedProjects,
    pausedProjects,
    cancelledProjects,
    myProjects,
    
    // 方法
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
    setFilters,
    resetFilters,
    setCurrentProject,
    clearError,
    refreshProjects
  }
})