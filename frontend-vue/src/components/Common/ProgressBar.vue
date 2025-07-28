<template>
  <div class="progress-bar-container">
    <div class="progress-info" v-if="showInfo">
      <span class="progress-text">{{ completed }}/{{ total }}</span>
      <span class="progress-percentage">{{ Math.round(percentage) }}%</span>
    </div>
    <div class="progress-bar" :style="{ height: height + 'px' }">
      <div 
        class="progress-fill" 
        :style="{ 
          width: percentage + '%', 
          backgroundColor: color,
          transition: 'width 0.6s ease-in-out'
        }"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

/**
 * 进度条组件
 * 用于显示任务或项目的完成进度
 */
interface Props {
  /** 已完成数量 */
  completed: number
  /** 总数量 */
  total: number
  /** 进度条高度 */
  height?: number
  /** 进度条颜色 */
  color?: string
  /** 是否显示进度信息 */
  showInfo?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  height: 6,
  color: '#409EFF',
  showInfo: true
})

/**
 * 计算百分比
 */
const percentage = computed(() => {
  if (props.total === 0) return 0
  return Math.max(0, Math.min(100, (props.completed / props.total) * 100))
})
</script>

<style scoped lang="scss">
.progress-bar-container {
  .progress-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 12px;
    
    .progress-text {
      color: #666;
    }
    
    .progress-percentage {
      color: #333;
      font-weight: 500;
    }
  }
  
  .progress-bar {
    background-color: #f0f0f0;
    border-radius: 3px;
    overflow: hidden;
    
    .progress-fill {
      height: 100%;
      border-radius: 3px;
      position: relative;
      
      &::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
          90deg,
          transparent 0%,
          rgba(255, 255, 255, 0.3) 50%,
          transparent 100%
        );
        animation: shimmer 2s infinite;
      }
    }
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style>