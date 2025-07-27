<template>
  <div class="task-detail-page">
    <div class="page-header">
      <div class="header-left">
        <el-button 
          type="text" 
          @click="goBack"
          class="back-button"
        >
          <el-icon><ArrowLeft /></el-icon>
          返回任务列表
        </el-button>
        <h1 class="page-title">{{ task?.title || '任务详情' }}</h1>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="editTask">
          <el-icon><Edit /></el-icon>
          编辑任务
        </el-button>
      </div>
    </div>
    
    <div class="page-content" v-if="task">
      <el-row :gutter="24">
        <el-col :span="16">
          <el-card class="task-info-card">
            <template #header>
              <span>任务信息</span>
            </template>
            <div class="task-info">
              <div class="info-item">
                <label>任务描述：</label>
                <p>{{ task.description || '暂无描述' }}</p>
              </div>
              <div class="info-item">
                <label>任务状态：</label>
                <el-tag :type="getStatusType(task.status)">{{ getStatusText(task.status) }}</el-tag>
              </div>
              <div class="info-item">
                <label>优先级：</label>
                <el-tag :type="getPriorityType(task.priority)">{{ getPriorityText(task.priority) }}</el-tag>
              </div>
              <div class="info-item">
                <label>截止时间：</label>
                <span>{{ task.dueDate || '无' }}</span>
              </div>
              <div class="info-item">
                <label>创建时间：</label>
                <span>{{ task.createdAt }}</span>
              </div>
              <div class="info-item">
                <label>更新时间：</label>
                <span>{{ task.updatedAt }}</span>
              </div>
            </div>
          </el-card>
          
          <el-card class="task-comments-card">
            <template #header>
              <div class="card-header">
                <span>任务评论</span>
                <el-button type="primary" size="small" @click="addComment">
                  <el-icon><Plus /></el-icon>
                  添加评论
                </el-button>
              </div>
            </template>
            <div class="comments-placeholder">
              <el-empty description="暂无评论" />
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card class="task-assignee-card">
            <template #header>
              <span>任务分配</span>
            </template>
            <div class="assignee-info" v-if="task.assignee">
              <el-avatar :src="task.assignee.avatar" :size="48">
                {{ task.assignee.name.charAt(0) }}
              </el-avatar>
              <div class="assignee-details">
                <div class="assignee-name">{{ task.assignee.name }}</div>
                <div class="assignee-email">{{ task.assignee.email }}</div>
              </div>
            </div>
            <div v-else class="no-assignee">
              <el-empty description="未分配" :image-size="60" />
            </div>
          </el-card>
          
          <el-card class="task-project-card">
            <template #header>
              <span>所属项目</span>
            </template>
            <div class="project-info" v-if="project">
              <div class="project-name">{{ project.name }}</div>
              <div class="project-status">
                <el-tag :type="getStatusType(project.status)">{{ getStatusText(project.status) }}</el-tag>
              </div>
            </div>
          </el-card>
          
          <el-card class="task-attachments-card">
            <template #header>
              <div class="card-header">
                <span>附件</span>
                <el-button type="primary" size="small" @click="uploadAttachment">
                  <el-icon><Plus /></el-icon>
                  上传附件
                </el-button>
              </div>
            </template>
            <div class="attachments-placeholder">
              <el-empty description="暂无附件" :image-size="60" />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div v-else class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Edit, Plus } from '@element-plus/icons-vue'
import type { Task, Project, User } from '@/types'

defineOptions({
  name: 'TaskDetail'
})

const route = useRoute()
const router = useRouter()
const task = ref<Task & { assignee?: User }>()
const project = ref<Project>()

/**
 * 获取状态类型
 */
const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    'todo': 'info',
    'in-progress': 'warning',
    'completed': 'success',
    'cancelled': 'danger',
    'active': 'success'
  }
  return statusMap[status] || 'info'
}

/**
 * 获取状态文本
 */
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'todo': '待办',
    'in-progress': '进行中',
    'completed': '已完成',
    'cancelled': '已取消',
    'active': '进行中'
  }
  return statusMap[status] || status
}

/**
 * 获取优先级类型
 */
const getPriorityType = (priority: string) => {
  const priorityMap: Record<string, string> = {
    'low': 'info',
    'medium': 'warning',
    'high': 'danger'
  }
  return priorityMap[priority] || 'info'
}

/**
 * 获取优先级文本
 */
const getPriorityText = (priority: string) => {
  const priorityMap: Record<string, string> = {
    'low': '低',
    'medium': '中',
    'high': '高'
  }
  return priorityMap[priority] || priority
}

/**
 * 返回上一页
 */
const goBack = () => {
  router.back()
}

/**
 * 编辑任务
 */
const editTask = () => {
  ElMessage.info('编辑任务功能开发中')
}

/**
 * 添加评论
 */
const addComment = () => {
  ElMessage.info('添加评论功能开发中')
}

/**
 * 上传附件
 */
const uploadAttachment = () => {
  ElMessage.info('上传附件功能开发中')
}

/**
 * 加载任务详情
 */
const loadTaskDetail = async () => {
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 模拟任务数据
    task.value = {
      id: route.params.id as string,
      title: '示例任务',
      description: '这是一个示例任务，用于演示任务详情页面的功能。',
      status: 'in-progress',
      priority: 'high',
      dueDate: '2024-02-01',
      projectId: '1',
      reporter: {
        id: '1',
        name: '李四',
        email: 'lisi@example.com',
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        role: 'member',
        status: 'online',
        createdAt: '2024-01-01',
        updatedAt: '2024-01-01'
      },
      tags: [],
      attachments: [],
      comments: [],
      createdAt: '2024-01-15',
      updatedAt: '2024-01-20',
      assignee: {
        id: '1',
        name: '张三',
        email: 'zhangsan@example.com',
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        role: 'member',
        status: 'online',
        createdAt: '2024-01-01',
        updatedAt: '2024-01-01'
      }
    }
    
    // 模拟项目数据
    project.value = {
      id: '1',
      name: '示例项目',
      description: '示例项目描述',
      status: 'active',
      progress: 75,
      startDate: '2024-01-01',
      createdAt: '2024-01-01',
      updatedAt: '2024-01-20',
      tasks: [],
      members: []
    }
  } catch (error) {
    console.error('加载任务详情失败:', error)
    ElMessage.error('加载任务详情失败')
  }
}

onMounted(() => {
  loadTaskDetail()
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.task-detail-page {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $spacing-6;
    
    .header-left {
      display: flex;
      align-items: center;
      gap: $spacing-4;
      
      .back-button {
        padding: 0;
        
        .el-icon {
          margin-right: $spacing-1;
        }
      }
      
      .page-title {
        font-size: $font-size-2xl;
        font-weight: $font-weight-bold;
        color: $text-primary;
        margin: 0;
      }
    }
  }
  
  .page-content {
    .el-card {
      margin-bottom: $spacing-6;
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
    }
    
    .task-info {
      .info-item {
        margin-bottom: $spacing-4;
        
        &:last-child {
          margin-bottom: 0;
        }
        
        label {
          font-weight: $font-weight-medium;
          color: $text-primary;
          margin-right: $spacing-2;
        }
        
        p {
          margin: $spacing-1 0 0 0;
          color: $text-secondary;
          line-height: 1.6;
        }
      }
    }
    
    .assignee-info {
      display: flex;
      align-items: center;
      gap: $spacing-3;
      
      .assignee-details {
        flex: 1;
        
        .assignee-name {
          font-weight: $font-weight-medium;
          color: $text-primary;
          margin-bottom: $spacing-1;
        }
        
        .assignee-email {
          font-size: $font-size-sm;
          color: $text-secondary;
        }
      }
    }
    
    .project-info {
      .project-name {
        font-weight: $font-weight-medium;
        color: $text-primary;
        margin-bottom: $spacing-2;
      }
    }
  }
  
  .loading-container {
    padding: $spacing-6;
  }
}
</style>