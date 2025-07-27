<template>
  <div class="tasks-index-page">
    <div class="page-header">
      <h1 class="page-title">任务管理</h1>
      <p class="page-description">管理和跟踪您的所有任务</p>
    </div>
    
    <div class="page-content">
      <el-card>
        <div class="content-placeholder">
          <el-icon class="placeholder-icon"><List /></el-icon>
          <h3>任务管理页面</h3>
          <p>这里将显示任务列表和管理功能</p>
          <el-button type="primary" @click="goToTaskList">
            查看任务列表
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { List } from '@element-plus/icons-vue'

defineOptions({
  name: 'TasksIndex'
})

const router = useRouter()

/**
 * 跳转到任务列表页面
 */
const goToTaskList = () => {
  router.push('/tasks/list')
}
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.tasks-index-page {
  .page-header {
    margin-bottom: $spacing-6;
    
    .page-title {
      font-size: $font-size-2xl;
      font-weight: $font-weight-bold;
      color: $text-primary;
      margin: 0 0 $spacing-2 0;
    }
    
    .page-description {
      font-size: $font-size-base;
      color: $text-secondary;
      margin: 0;
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
      }
    }
  }
}
</style>