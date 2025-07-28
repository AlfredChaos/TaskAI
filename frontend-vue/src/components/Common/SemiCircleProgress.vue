<template>
  <div class="semi-circle-progress" :style="{ width: size + 'px', height: (size / 2 + 20) + 'px' }">
    <svg :width="size" :height="size / 2 + 20" class="progress-svg">
      <!-- 背景弧线 -->
      <path
        :d="backgroundPath"
        :stroke="backgroundColor"
        :stroke-width="strokeWidth"
        fill="none"
        stroke-linecap="round"
      />
      <!-- 进度弧线 -->
      <path
        :d="progressPath"
        :stroke="progressColor"
        :stroke-width="strokeWidth"
        fill="none"
        stroke-linecap="round"
        class="progress-path"
        :style="{ strokeDasharray: `${progressLength} ${totalLength}` }"
      />
    </svg>
    
    <!-- 中心内容 -->
    <div class="center-content">
      <div class="main-value">
        <CountUp :end-value="percentage" :formatter="formatPercentage" />
      </div>
      <div class="sub-text" v-if="subText">{{ subText }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import CountUp from './CountUp.vue'

/**
 * 半圆环形进度图组件
 * 用于显示百分比进度，支持动画效果
 */
interface Props {
  /** 百分比值 (0-100) */
  percentage: number
  /** 组件尺寸 */
  size?: number
  /** 线条宽度 */
  strokeWidth?: number
  /** 进度条颜色 */
  progressColor?: string
  /** 背景颜色 */
  backgroundColor?: string
  /** 副文本 */
  subText?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 120,
  strokeWidth: 8,
  progressColor: '#6C5DD3',
  backgroundColor: '#f0f0f0',
  subText: ''
})

/**
 * 计算半圆弧线路径
 */
const radius = computed(() => (props.size - props.strokeWidth) / 2)
const centerX = computed(() => props.size / 2)
const centerY = computed(() => props.size / 2)

/**
 * 背景弧线路径
 */
const backgroundPath = computed(() => {
  const r = radius.value
  const cx = centerX.value
  const cy = centerY.value
  
  return `M ${cx - r} ${cy} A ${r} ${r} 0 0 1 ${cx + r} ${cy}`
})

/**
 * 进度弧线路径
 */
const progressPath = computed(() => {
  return backgroundPath.value
})

/**
 * 总弧线长度
 */
const totalLength = computed(() => {
  return Math.PI * radius.value
})

/**
 * 进度弧线长度
 */
const progressLength = computed(() => {
  const progress = Math.max(0, Math.min(100, props.percentage))
  return (progress / 100) * totalLength.value
})

/**
 * 格式化百分比显示
 */
const formatPercentage = (value: number): string => {
  return Math.round(value) + '%'
}
</script>

<style scoped lang="scss">
.semi-circle-progress {
  position: relative;
  display: inline-block;
  
  .progress-svg {
    transform: rotate(0deg);
  }
  
  .progress-path {
    transition: stroke-dasharray 0.6s ease-in-out;
  }
  
  .center-content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -20%);
    text-align: center;
    
    .main-value {
      font-size: 24px;
      font-weight: bold;
      color: #333;
      line-height: 1;
    }
    
    .sub-text {
      font-size: 12px;
      color: #666;
      margin-top: 4px;
      line-height: 1;
    }
  }
}
</style>