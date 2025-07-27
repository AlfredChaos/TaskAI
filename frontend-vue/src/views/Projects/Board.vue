<template>
  <div class="project-board-page">
    <div class="page-header">
      <div class="header-left">
        <el-button 
          type="text" 
          @click="goBack"
          class="back-button"
        >
          <el-icon><ArrowLeft /></el-icon>
          返回项目详情
        </el-button>
        <h1 class="page-title">{{ project?.name || '项目看板' }}</h1>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="createTask">
          <el-icon><Plus /></el-icon>
          新建任务
        </el-button>
      </div>
    </div>
    
    <div class="page-content">
      <el-card>
        <div class="content-placeholder">
          <el-icon class="placeholder-icon"><Grid /></el-icon>
          <h3>项目看板页面</h3>
          <p>这里将显示项目的看板视图，包括待办、进行中、已完成等状态的任务列表</p>
          <el-button type="primary" disabled>
            功能开发中
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Plus, Grid } from '@element-plus/icons-vue'
import type { Project } from '@/types'

defineOptions({
  name: 'ProjectBoard'
})

const route = useRoute()
const router = useRouter()
const project = ref<Project>()

/**
 * 返回上一页
 */
const goBack = () => {
  router.push(`/projects/${route.params.id}`)
}

/**
 * 创建任务
 */
const createTask = () => {
  ElMessage.info('创建任务功能开发中')
}

/**
 * 加载项目信息
 */
const loadProject = async () => {
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 模拟项目数据
    project.value = {
      id: route.params.id as string,
      name: '示例项目',
      description: '这是一个示例项目',
      status: 'active',
      progress: 75,
      startDate: '2024-01-15',
      createdAt: '2024-01-15',
      updatedAt: '2024-01-20',
      tasks: [],
      members: []
    }
  } catch (error) {
    console.error('加载项目信息失败:', error)
    ElMessage.error('加载项目信息失败')
  }
}

onMounted(() => {
  loadProject()
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.project-board-page {
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
    .content-placeholder {
      text-align: center;
      padding: $spacing-12 $spacing-6;
      
      .placeholder-icon {
        font-size: 64px;
        color: $primary-color;
        margin-bottom: $spacing-4;
      }
      
      h3 {
        font-size: $font-size-xl;
        font-weight: $font-weight-semibold;
        color: $text-primary;
        margin: 0 0 $spacing-2 0;
      }
      
      p {
        font-size: $font-size-base;
        color: $text-secondary;
        margin: 0 0 $spacing-6 0;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
      }
    }
  }
}
</style>