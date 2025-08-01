<template>
  <div v-if="visible" :class="loadingClasses" :style="loadingStyles">
    <!-- 遮罩层 -->
    <div v-if="mask" class="common-loading__mask"></div>

    <!-- 加载内容 -->
    <div class="common-loading__content">
      <!-- 加载图标 -->
      <div class="common-loading__spinner">
        <!-- 默认旋转图标 -->
        <el-icon v-if="type === 'spinner'" class="is-loading" :size="iconSize">
          <Loading />
        </el-icon>

        <!-- 圆形进度条 -->
        <div v-else-if="type === 'circle'" class="common-loading__circle">
          <svg :width="iconSize" :height="iconSize" viewBox="0 0 50 50">
            <circle cx="25" cy="25" r="20" fill="none" stroke="#E5E7EB" stroke-width="4" />
            <circle cx="25" cy="25" r="20" fill="none" stroke="#6366F1" stroke-width="4" stroke-linecap="round"
              stroke-dasharray="126" stroke-dashoffset="94.5" class="common-loading__circle-path" />
          </svg>
        </div>

        <!-- 点状加载 -->
        <div v-else-if="type === 'dots'" class="common-loading__dots">
          <span class="common-loading__dot"></span>
          <span class="common-loading__dot"></span>
          <span class="common-loading__dot"></span>
        </div>

        <!-- 波浪加载 -->
        <div v-else-if="type === 'wave'" class="common-loading__wave">
          <div class="common-loading__wave-bar"></div>
          <div class="common-loading__wave-bar"></div>
          <div class="common-loading__wave-bar"></div>
          <div class="common-loading__wave-bar"></div>
          <div class="common-loading__wave-bar"></div>
        </div>

        <!-- 自定义图标 -->
        <el-icon v-else-if="customIcon" class="is-loading" :size="iconSize">
          <component :is="customIcon" />
        </el-icon>
      </div>

      <!-- 加载文本 -->
      <div v-if="text" class="common-loading__text">
        {{ text }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="CommonLoading">
import { computed } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import type { Component } from 'vue'

interface Props {
  /** 是否显示加载 */
  visible?: boolean
  /** 加载类型 */
  type?: 'spinner' | 'circle' | 'dots' | 'wave' | 'custom'
  /** 加载文本 */
  text?: string
  /** 是否显示遮罩 */
  mask?: boolean
  /** 大小 */
  size?: 'small' | 'default' | 'large' | number
  /** 自定义图标 */
  customIcon?: Component
  /** 背景色 */
  backgroundColor?: string
  /** 文本颜色 */
  textColor?: string
  /** 图标颜色 */
  iconColor?: string
  /** 是否全屏 */
  fullscreen?: boolean
  /** z-index */
  zIndex?: number
}

const props = withDefaults(defineProps<Props>(), {
  visible: true,
  type: 'spinner',
  mask: true,
  size: 'default',
  fullscreen: false,
  zIndex: 2000
})

// 计算属性
const iconSize = computed(() => {
  if (typeof props.size === 'number') {
    return props.size
  }
  const sizeMap = {
    small: 24,
    default: 32,
    large: 48
  }
  return sizeMap[props.size]
})

const loadingClasses = computed(() => [
  'common-loading',
  {
    'common-loading--fullscreen': props.fullscreen,
    'common-loading--with-mask': props.mask
  }
])

const loadingStyles = computed(() => {
  const styles: Record<string, string> = {
    zIndex: props.zIndex.toString()
  }

  if (props.backgroundColor) {
    styles.backgroundColor = props.backgroundColor
  }

  return styles
})
</script>

<style lang="scss" scoped>
.common-loading {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;

  // 全屏模式
  &--fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.9);
  }

  // 遮罩层
  &__mask {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(2px);
  }

  // 加载内容
  &__content {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1;
  }

  // 加载图标容器 (严格按照设计文档)
  &__spinner {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;

    .el-icon {
      color: #6366F1; // 使用设计文档的主色
    }
  }

  // 圆形进度条
  &__circle {
    &-path {
      animation: loading-circle 1.5s ease-in-out infinite;
    }
  }

  // 点状加载
  &__dots {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  &__dot {
    width: 8px;
    height: 8px;
    background-color: #6366F1; // 使用设计文档的主色
    border-radius: 50%;
    animation: loading-dots 1.4s ease-in-out infinite both;

    &:nth-child(1) {
      animation-delay: -0.32s;
    }

    &:nth-child(2) {
      animation-delay: -0.16s;
    }

    &:nth-child(3) {
      animation-delay: 0;
    }
  }

  // 波浪加载
  &__wave {
    display: flex;
    align-items: center;
    gap: 2px;
  }

  &__wave-bar {
    width: 4px;
    height: 20px;
    background-color: #6366F1; // 使用设计文档的主色
    border-radius: 2px;
    animation: loading-wave 1.2s ease-in-out infinite;

    &:nth-child(1) {
      animation-delay: -1.2s;
    }

    &:nth-child(2) {
      animation-delay: -1.1s;
    }

    &:nth-child(3) {
      animation-delay: -1.0s;
    }

    &:nth-child(4) {
      animation-delay: -0.9s;
    }

    &:nth-child(5) {
      animation-delay: -0.8s;
    }
  }

  // 加载文本 (严格按照设计文档)
  &__text {
    color: #6B7280; // 使用设计文档的次要文本颜色
    font-size: 14px;
    line-height: 1.4;
    text-align: center;
    font-weight: 500;
  }
}

// 动画定义
@keyframes loading-circle {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }

  50% {
    stroke-dasharray: 90, 200;
    stroke-dashoffset: -35;
  }

  100% {
    stroke-dasharray: 90, 200;
    stroke-dashoffset: -124;
  }
}

@keyframes loading-dots {

  0%,
  80%,
  100% {
    transform: scale(0);
    opacity: 0.5;
  }

  40% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes loading-wave {

  0%,
  40%,
  100% {
    transform: scaleY(0.4);
  }

  20% {
    transform: scaleY(1);
  }
}

// 响应式适配
@media (max-width: 768px) {
  .common-loading {
    &__text {
      font-size: 12px;
    }

    &__wave-bar {
      width: 3px;
      height: 16px;
    }

    &__dot {
      width: 6px;
      height: 6px;
    }
  }
}
</style>