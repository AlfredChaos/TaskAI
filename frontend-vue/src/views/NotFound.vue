<template>
  <div class="not-found-page">
    <div class="not-found-container">
      <div class="not-found-content">
        <div class="error-code">404</div>
        <h1 class="error-title">页面未找到</h1>
        <p class="error-description">
          抱歉，您访问的页面不存在或已被移除。
        </p>
        <div class="error-actions">
          <el-button type="primary" @click="goHome">
            <el-icon><House /></el-icon>
            返回首页
          </el-button>
          <el-button @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            返回上页
          </el-button>
        </div>
      </div>
      <div class="not-found-illustration">
        <el-icon class="illustration-icon"><Warning /></el-icon>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { House, ArrowLeft, Warning } from '@element-plus/icons-vue'

defineOptions({
  name: 'NotFoundPage'
})

const router = useRouter()

/**
 * 返回首页
 */
const goHome = () => {
  router.push('/')
}

/**
 * 返回上一页
 */
const goBack = () => {
  router.back()
}
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: $spacing-4;
}

.not-found-container {
  display: flex;
  align-items: center;
  gap: $spacing-12;
  max-width: 800px;
  
  @media (max-width: 768px) {
    flex-direction: column;
    text-align: center;
    gap: $spacing-8;
  }
}

.not-found-content {
  flex: 1;
  
  .error-code {
    font-size: 120px;
    font-weight: $font-weight-bold;
    color: $primary-color;
    line-height: 1;
    margin-bottom: $spacing-4;
    
    @media (max-width: 768px) {
      font-size: 80px;
    }
  }
  
  .error-title {
    font-size: $font-size-3xl;
    font-weight: $font-weight-bold;
    color: $text-primary;
    margin: 0 0 $spacing-4 0;
    
    @media (max-width: 768px) {
      font-size: $font-size-2xl;
    }
  }
  
  .error-description {
    font-size: $font-size-lg;
    color: $text-secondary;
    margin: 0 0 $spacing-8 0;
    line-height: 1.6;
  }
  
  .error-actions {
    display: flex;
    gap: $spacing-4;
    
    @media (max-width: 768px) {
      justify-content: center;
    }
  }
}

.not-found-illustration {
  flex: 0 0 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  
  .illustration-icon {
    font-size: 200px;
    color: rgba($primary-color, 0.3);
    
    @media (max-width: 768px) {
      font-size: 120px;
    }
  }
}
</style>