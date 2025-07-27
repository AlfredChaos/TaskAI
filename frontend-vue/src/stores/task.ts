import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { Task } from '@/types'
import { taskApi } from '@/api'

/**
 * 任务状态管理
 */
export const useTaskStore = defineStore('task', () => {
  // 状态
  const tasks = ref<Task[]>([])
  const currentTask = ref<Task | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const pagination = ref({
    current: 1,
    pageSize: 10,
    total: 0
  })
  const filters = ref({
    projectId: '',
    status: '',
    assignee: '',
    priority: '',
    search: ''
  })

  // 计算属性
  const taskCount = computed(() => tasks.value.length)
  const todoTasks = computed(() => 
    tasks.value.filter(t => t.status === 'todo')
  )
  const inProgressTasks = computed(() => 
    tasks.value.filter(t => t.status === 'in-progress')
  )
  const reviewTasks = computed(() => 
    tasks.value.filter(t => t.status === 'review')
  )
  const doneTasks = computed(() => 
    tasks.value.filter(t => t.status === 'done')
  )
  const highPriorityTasks = computed(() => 
    tasks.value.filter(t => t.priority === 'high' || t.priority === 'urgent')
  )
  const myTasks = computed(() => {
    // 这里需要从用户store获取当前用户ID
    // 暂时返回所有任务
    return tasks.value
  })
  const overdueTasks = computed(() => {
    const now = new Date()
    return tasks.value.filter(t => 
      t.dueDate && new Date(t.dueDate) < now && t.status !== 'done'
    )
  })

  /**
   * 获取任务列表
   */
  const fetchTasks = async (params?: {
    page?: number
    pageSize?: number
    projectId?: string
    status?: string
    assignee?: string
    priority?: string
    search?: string
  }) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await taskApi.getTasks({
        page: params?.page || pagination.value.current,
        pageSize: params?.pageSize || pagination.value.pageSize,
        projectId: params?.projectId || filters.value.projectId,
        status: params?.status || filters.value.status,
        assignee: params?.assignee || filters.value.assignee,
        priority: params?.priority || filters.value.priority,
        search: params?.search || filters.value.search
      })
      
      if (response.success) {
        tasks.value = response.data.items
        pagination.value = {
          current: response.data.page,
          pageSize: response.data.pageSize,
          total: response.data.total
        }
      } else {
        throw new Error(response.message || '获取任务列表失败')
      }
    } catch {
      error.value = '获取任务列表失败'
      tasks.value = []
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 获取任务详情
   */
  const fetchTask = async (id: string) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await taskApi.getTask(id)
      
      if (response.success) {
        currentTask.value = response.data as Task
        
        // 更新任务列表中的对应任务
        const index = tasks.value.findIndex(t => t.id === id)
        if (index !== -1) {
          tasks.value[index] = response.data as Task
        }
      } else {
        throw new Error(response.message || '获取任务详情失败')
      }
    } catch {
      error.value = '获取任务详情失败'
      currentTask.value = null
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 创建任务
   */
  const createTask = async (taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt' | 'comments' | 'attachments'>) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await taskApi.createTask(taskData)
      
      if (response.success) {
        const newTask = response.data as Task
        tasks.value.unshift(newTask)
        pagination.value.total += 1
        return newTask
      } else {
        throw new Error(response.message || '创建任务失败')
      }
    } catch {
      error.value = '创建任务失败'
      throw error
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 更新任务
   */
  const updateTask = async (id: string, taskData: Partial<Task>) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await taskApi.updateTask(id, taskData)
      
      if (response.success) {
        const updatedTask = response.data as Task
        
        // 更新任务列表
        const index = tasks.value.findIndex(t => t.id === id)
        if (index !== -1) {
          tasks.value[index] = updatedTask
        }
        
        // 更新当前任务
        if (currentTask.value?.id === id) {
          currentTask.value = updatedTask
        }
        
        return updatedTask
      } else {
        throw new Error(response.message || '更新任务失败')
      }
    } catch {
      error.value = '更新任务失败'
      throw error
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 更新任务状态
   */
  const updateTaskStatus = async (id: string, status: Task['status']) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await taskApi.updateTaskStatus(id, status)
      
      if (response.success) {
        const updatedTask = response.data as Task
        
        // 更新任务列表
        const index = tasks.value.findIndex(t => t.id === id)
        if (index !== -1) {
          tasks.value[index] = updatedTask
        }
        
        // 更新当前任务
        if (currentTask.value?.id === id) {
          currentTask.value = updatedTask
        }
        
        return updatedTask
      } else {
        throw new Error(response.message || '更新任务状态失败')
      }
    } catch {
      error.value = '更新任务状态失败'
      throw error
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 分配任务
   */
  const assignTask = async (id: string, assigneeId: string) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await taskApi.assignTask(id, assigneeId)
      
      if (response.success) {
        const updatedTask = response.data as Task
        
        // 更新任务列表
        const index = tasks.value.findIndex(t => t.id === id)
        if (index !== -1) {
          tasks.value[index] = updatedTask
        }
        
        // 更新当前任务
        if (currentTask.value?.id === id) {
          currentTask.value = updatedTask
        }
        
        return updatedTask
      } else {
        throw new Error(response.message || '分配任务失败')
      }
    } catch {
      error.value = '分配任务失败'
      throw error
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 删除任务
   */
  const deleteTask = async (id: string) => {
    try {
      isLoading.value = true
      error.value = null
      
      const response = await taskApi.deleteTask(id)
      
      if (response.success) {
        // 从任务列表中移除
        const index = tasks.value.findIndex(t => t.id === id)
        if (index !== -1) {
          tasks.value.splice(index, 1)
          pagination.value.total -= 1
        }
        
        // 清空当前任务（如果是被删除的任务）
        if (currentTask.value?.id === id) {
          currentTask.value = null
        }
      } else {
        throw new Error(response.message || '删除任务失败')
      }
    } catch {
      error.value = '删除任务失败'
      throw error
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 添加任务评论
   */
  const addComment = async (taskId: string, content: string) => {
    try {
      const response = await taskApi.addComment(taskId, content)
      
      if (response.success) {
        // 重新获取任务详情以更新评论
        if (currentTask.value?.id === taskId) {
          await fetchTask(taskId)
        }
      } else {
        throw new Error(response.message || '添加评论失败')
      }
    } catch {
      error.value = '添加评论失败'
      throw error
    }
  }

  /**
   * 上传任务附件
   */
  const uploadAttachment = async (taskId: string, file: File) => {
    try {
      const response = await taskApi.uploadAttachment(taskId, file)
      
      if (response.success) {
        // 重新获取任务详情以更新附件
        if (currentTask.value?.id === taskId) {
          await fetchTask(taskId)
        }
      } else {
        throw new Error(response.message || '上传附件失败')
      }
    } catch {
      error.value = '上传附件失败'
      throw error
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
      projectId: '',
      status: '',
      assignee: '',
      priority: '',
      search: ''
    }
  }

  /**
   * 设置当前任务
   */
  const setCurrentTask = (task: Task | null) => {
    currentTask.value = task
  }

  /**
   * 清空错误
   */
  const clearError = () => {
    error.value = null
  }

  /**
   * 刷新任务列表
   */
  const refreshTasks = () => {
    return fetchTasks()
  }

  /**
   * 根据项目ID获取任务
   */
  const getTasksByProject = (projectId: string) => {
    return tasks.value.filter(t => t.projectId === projectId)
  }

  /**
   * 根据状态获取任务统计
   */
  const getTaskStats = () => {
    return {
      total: taskCount.value,
      todo: todoTasks.value.length,
      inProgress: inProgressTasks.value.length,
      review: reviewTasks.value.length,
      done: doneTasks.value.length,
      overdue: overdueTasks.value.length,
      highPriority: highPriorityTasks.value.length
    }
  }

  return {
    // 状态
    tasks,
    currentTask,
    isLoading,
    error,
    pagination,
    filters,
    
    // 计算属性
    taskCount,
    todoTasks,
    inProgressTasks,
    reviewTasks,
    doneTasks,
    highPriorityTasks,
    myTasks,
    overdueTasks,
    
    // 方法
    fetchTasks,
    fetchTask,
    createTask,
    updateTask,
    updateTaskStatus,
    assignTask,
    deleteTask,
    addComment,
    uploadAttachment,
    setFilters,
    resetFilters,
    setCurrentTask,
    clearError,
    refreshTasks,
    getTasksByProject,
    getTaskStats
  }
})