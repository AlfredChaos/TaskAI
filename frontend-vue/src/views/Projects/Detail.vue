<template>
  <div class="project-detail-page">
    <div class="page-header">
      <div class="header-left">
        <el-button 
          type="text" 
          @click="goBack"
          class="back-button"
        >
          <el-icon><ArrowLeft /></el-icon>
          返回项目列表
        </el-button>
        <h1 class="page-title">{{ project?.name || '项目详情' }}</h1>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="editProject">
          <el-icon><Edit /></el-icon>
          编辑项目
        </el-button>
      </div>
    </div>
    
    <div class="page-content" v-if="project">
      <el-row :gutter="24">
        <el-col :span="16">
          <el-card class="project-info-card">
            <template #header>
              <span>项目信息</span>
            </template>
            <div class="project-info">
              <div class="info-item">
                <label>项目描述：</label>
                <p>{{ project.description || '暂无描述' }}</p>
              </div>
              <div class="info-item">
                <label>项目状态：</label>
                <el-tag :type="getStatusType(project.status)">{{ getStatusText(project.status) }}</el-tag>
              </div>
              <div class="info-item">
                <label>创建时间：</label>
                <span>{{ project.createdAt }}</span>
              </div>
              <div class="info-item">
                <label>更新时间：</label>
                <span>{{ project.updatedAt }}</span>
              </div>
            </div>
          </el-card>
          
          <el-card class="project-tasks-card">
            <template #header>
              <div class="card-header">
                <span>项目任务</span>
                <el-button type="primary" size="small" @click="createTask">
                  <el-icon><Plus /></el-icon>
                  新建任务
                </el-button>
              </div>
            </template>
            <div class="tasks-placeholder">
              <el-empty description="暂无任务数据" />
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card class="project-members-card">
            <template #header>
              <div class="card-header">
                <span>项目成员</span>
                <el-button type="primary" size="small" @click="inviteMember">
                  <el-icon><Plus /></el-icon>
                  邀请成员
                </el-button>
              </div>
            </template>
            <div class="members-list">
              <div 
                v-for="member in project.members" 
                :key="member.id"
                class="member-item"
              >
                <el-avatar :src="member.avatar" :size="32">
                  {{ member.name.charAt(0) }}
                </el-avatar>
                <div class="member-info">
                  <div class="member-name">{{ member.name }}</div>
                  <div class="member-role">{{ member.role }}</div>
                </div>
              </div>
            </div>
          </el-card>
          
          <el-card class="project-stats-card">
            <template #header>
              <span>项目统计</span>
            </template>
            <div class="stats-list">
              <div class="stat-item">
                <div class="stat-value">{{ project.taskCount || 0 }}</div>
                <div class="stat-label">总任务数</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ project.memberCount || 0 }}</div>
                <div class="stat-label">团队成员</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">75%</div>
                <div class="stat-label">完成进度</div>
              </div>
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
import type { Project, User } from '@/types'

defineOptions({
  name: 'ProjectDetail'
})

const route = useRoute()
const router = useRouter()
const project = ref<Project & { 
  members: (User & { role: string })[], 
  taskCount: number, 
  memberCount: number 
}>()

/**
 * 获取状态类型
 */
const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    'active': 'success',
    'completed': 'info',
    'paused': 'warning',
    'cancelled': 'danger'
  }
  return statusMap[status] || 'info'
}

/**
 * 获取状态文本
 */
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'active': '进行中',
    'completed': '已完成',
    'paused': '已暂停',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
}

/**
 * 返回上一页
 */
const goBack = () => {
  router.back()
}

/**
 * 编辑项目
 */
const editProject = () => {
  ElMessage.info('编辑项目功能开发中')
}

/**
 * 创建任务
 */
const createTask = () => {
  ElMessage.info('创建任务功能开发中')
}

/**
 * 邀请成员
 */
const inviteMember = () => {
  ElMessage.info('邀请成员功能开发中')
}

/**
 * 加载项目详情
 */
const loadProjectDetail = async () => {
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 模拟项目数据
    project.value = {
      id: route.params.id as string,
      name: '示例项目',
      description: '这是一个示例项目，用于演示项目详情页面的功能。',
      status: 'active',
      progress: 75,
      startDate: '2024-01-15',
      createdAt: '2024-01-15',
      updatedAt: '2024-01-20',
      tasks: [],
      members: [
        {
          id: '1',
          name: '张三',
          email: 'zhangsan@example.com',
          avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
          role: 'manager',
          status: 'online',
          createdAt: '2024-01-01',
          updatedAt: '2024-01-01'
        },
        {
          id: '2',
          name: '李四',
          email: 'lisi@example.com',
          avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
          role: 'member',
          status: 'online',
          createdAt: '2024-01-01',
          updatedAt: '2024-01-01'
        }
      ],
      taskCount: 12,
      memberCount: 2
    }
  } catch (error) {
    console.error('加载项目详情失败:', error)
    ElMessage.error('加载项目详情失败')
  }
}

onMounted(() => {
  loadProjectDetail()
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.project-detail-page {
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
    
    .project-info {
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
    
    .members-list {
      .member-item {
        display: flex;
        align-items: center;
        gap: $spacing-3;
        padding: $spacing-3 0;
        border-bottom: 1px solid $border-color;
        
        &:last-child {
          border-bottom: none;
        }
        
        .member-info {
          flex: 1;
          
          .member-name {
            font-weight: $font-weight-medium;
            color: $text-primary;
            margin-bottom: $spacing-1;
          }
          
          .member-role {
            font-size: $font-size-sm;
            color: $text-secondary;
          }
        }
      }
    }
    
    .stats-list {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: $spacing-4;
      
      .stat-item {
        text-align: center;
        
        .stat-value {
          font-size: $font-size-2xl;
          font-weight: $font-weight-bold;
          color: $primary-color;
          margin-bottom: $spacing-1;
        }
        
        .stat-label {
          font-size: $font-size-sm;
          color: $text-secondary;
        }
      }
    }
  }
  
  .loading-container {
    padding: $spacing-6;
  }
}
</style>