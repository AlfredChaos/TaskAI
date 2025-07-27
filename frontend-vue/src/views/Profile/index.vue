<template>
  <div class="profile-index-page">
    <div class="page-header">
      <h1 class="page-title">个人资料</h1>
      <p class="page-description">管理您的个人信息和账户设置</p>
    </div>
    
    <div class="page-content">
      <el-card>
        <div class="content-placeholder">
          <el-icon class="placeholder-icon"><User /></el-icon>
          <h3>个人资料页面</h3>
          <p>这里将显示用户信息编辑和账户设置</p>
          <el-button type="primary" disabled>
            功能开发中
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { User } from '@element-plus/icons-vue'

defineOptions({
  name: 'ProfileIndex'
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.profile-index-page {
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