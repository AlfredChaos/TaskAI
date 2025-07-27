<template>
  <div 
    :class="cardClasses"
    :style="cardStyles"
    @click="handleClick"
  >
    <!-- 卡片头部 -->
    <div v-if="$slots.header || title" class="common-card__header">
      <slot name="header">
        <div class="common-card__title">
          <el-icon v-if="icon" class="common-card__icon">
            <component :is="icon" />
          </el-icon>
          <span>{{ title }}</span>
        </div>
        <div v-if="$slots.extra" class="common-card__extra">
          <slot name="extra"></slot>
        </div>
      </slot>
    </div>
    
    <!-- 卡片内容 -->
    <div class="common-card__body">
      <slot></slot>
    </div>
    
    <!-- 卡片底部 -->
    <div v-if="$slots.footer" class="common-card__footer">
      <slot name="footer"></slot>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="common-card__loading">
      <el-icon class="is-loading">
        <Loading />
      </el-icon>
      <span>{{ loadingText }}</span>
    </div>
  </div>
</template>

<script setup lang="ts" name="CommonCard">
import { computed } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import type { Component } from 'vue'

interface Props {
  /** 卡片标题 */
  title?: string
  /** 标题图标 */
  icon?: Component
  /** 是否显示阴影 */
  shadow?: 'always' | 'hover' | 'never'
  /** 卡片大小 */
  size?: 'small' | 'default' | 'large'
  /** 是否可点击 */
  clickable?: boolean
  /** 是否显示边框 */
  bordered?: boolean
  /** 是否加载中 */
  loading?: boolean
  /** 加载文本 */
  loadingText?: string
  /** 自定义背景色 */
  backgroundColor?: string
  /** 圆角大小 */
  borderRadius?: string
  /** 内边距 */
  padding?: string
  /** 最小高度 */
  minHeight?: string
}

interface Emits {
  click: [event: MouseEvent]
}

const props = withDefaults(defineProps<Props>(), {
  shadow: 'always',
  size: 'default',
  clickable: false,
  bordered: true,
  loading: false,
  loadingText: '加载中...'
})

const emit = defineEmits<Emits>()

// 计算属性
const cardClasses = computed(() => [
  'common-card',
  `common-card--${props.size}`,
  `common-card--shadow-${props.shadow}`,
  {
    'common-card--clickable': props.clickable,
    'common-card--bordered': props.bordered,
    'common-card--loading': props.loading
  }
])

const cardStyles = computed(() => {
  const styles: Record<string, string> = {}
  
  if (props.backgroundColor) {
    styles.backgroundColor = props.backgroundColor
  }
  
  if (props.borderRadius) {
    styles.borderRadius = props.borderRadius
  }
  
  if (props.padding) {
    styles.padding = props.padding
  }
  
  if (props.minHeight) {
    styles.minHeight = props.minHeight
  }
  
  return styles
})

// 事件处理
const handleClick = (event: MouseEvent) => {
  if (props.clickable && !props.loading) {
    emit('click', event)
  }
}
</script>

<style lang="scss" scoped>
.common-card {
  position: relative;
  background: white;
  border: 1px solid #E5E7EB; /* --gray-200 */
  border-radius: 12px; /* --radius-lg */
  overflow: hidden;
  transition: all 0.3s;
  
  // 阴影效果 - 按照设计文档规范
  &--shadow-always {
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* --shadow-sm */
  }
  
  &--shadow-hover {
    &:hover {
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); /* --shadow-md */
    }
  }
  
  &--shadow-never {
    box-shadow: none;
  }
  
  // 大小 - 按照设计文档规范
  &--small {
    .common-card__header {
      padding: 16px 16px 12px; /* --space-4 --space-4 --space-3 */
    }
    
    .common-card__body {
      padding: 16px; /* --space-4 */
    }
    
    .common-card__footer {
      padding: 12px 16px; /* --space-3 --space-4 */
    }
  }
  
  &--default {
    .common-card__header {
      padding: 24px 24px 16px; /* --space-6 --space-6 --space-4 */
    }
    
    .common-card__body {
      padding: 24px; /* --space-6 */
    }
    
    .common-card__footer {
      padding: 16px 24px; /* --space-4 --space-6 */
    }
  }
  
  &--large {
    .common-card__header {
      padding: 32px 32px 24px; /* --space-8 --space-8 --space-6 */
    }
    
    .common-card__body {
      padding: 32px; /* --space-8 */
    }
    
    .common-card__footer {
      padding: 24px 32px; /* --space-6 --space-8 */
    }
  }
  
  // 可点击
  &--clickable {
    cursor: pointer;
    
    &:hover {
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); /* --shadow-md */
      transform: translateY(-2px);
    }
    
    &:active {
      transform: translateY(0);
    }
  }
  
  // 无边框
  &:not(&--bordered) {
    border: none;
  }
  
  // 加载状态
  &--loading {
    pointer-events: none;
    
    .common-card__header,
    .common-card__body,
    .common-card__footer {
      opacity: 0.6;
    }
  }
  
  // 头部
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--el-border-color-lighter);
    background-color: var(--el-fill-color-blank);
  }
  
  &__title {
    display: flex;
    align-items: center;
    font-size: 16px;
    font-weight: 500;
    color: var(--el-text-color-primary);
  }
  
  &__icon {
    margin-right: 8px;
    color: var(--el-color-primary);
  }
  
  &__extra {
    color: var(--el-text-color-regular);
    font-size: 14px;
  }
  
  // 内容
  &__body {
    color: var(--el-text-color-primary);
    line-height: 1.6;
  }
  
  // 底部
  &__footer {
    border-top: 1px solid var(--el-border-color-lighter);
    background-color: var(--el-fill-color-blank);
    color: var(--el-text-color-regular);
  }
  
  // 加载遮罩
  &__loading {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: rgba(255, 255, 255, 0.9);
    color: var(--el-text-color-regular);
    font-size: 14px;
    
    .el-icon {
      font-size: 24px;
      margin-bottom: 8px;
      color: var(--el-color-primary);
    }
  }
  
  // 响应式适配
  @media (max-width: 768px) {
    &--default {
      .common-card__header,
      .common-card__body,
      .common-card__footer {
        padding: 12px 16px;
      }
    }
    
    &--large {
      .common-card__header,
      .common-card__body,
      .common-card__footer {
        padding: 16px 20px;
      }
    }
  }
}
</style>