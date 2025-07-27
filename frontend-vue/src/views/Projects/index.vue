<template>
  <div class="projects-index-page">
    <div class="page-header">
      <h1 class="page-title">项目管理</h1>
      <p class="page-description">管理和跟踪您的所有项目</p>
    </div>
    
    <div class="page-content">
      <el-card>
        <div class="content-placeholder">
          <el-icon class="placeholder-icon"><Folder /></el-icon>
          <h3>项目管理页面</h3>
          <p>这里将显示项目列表和管理功能</p>
          <el-button type="primary" @click="goToProjectList">
            查看项目列表
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Folder } from '@element-plus/icons-vue'

defineOptions({
  name: 'ProjectsIndex'
})

const router = useRouter()

/**
 * 跳转到项目列表页面
 */
const goToProjectList = () => {
  router.push('/projects/list')
}
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.projects-index-page {
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