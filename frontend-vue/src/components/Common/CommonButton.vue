<template>
  <el-button
    :type="type"
    :size="size"
    :plain="plain"
    :text="text"
    :bg="bg"
    :link="link"
    :round="round"
    :circle="circle"
    :loading="loading"
    :loading-icon="loadingIcon"
    :disabled="disabled"
    :icon="icon"
    :autofocus="autofocus"
    :native-type="nativeType"
    :auto-insert-space="autoInsertSpace"
    :color="color"
    :dark="dark"
    :tag="tag"
    :class="buttonClasses"
    :style="buttonStyles"
    @click="handleClick"
    @focus="handleFocus"
    @blur="handleBlur"
  >
    <!-- 前置图标 -->
    <template v-if="$slots.icon" #icon>
      <slot name="icon" />
    </template>
    
    <!-- 加载图标 -->
    <template v-if="$slots.loading" #loading>
      <slot name="loading" />
    </template>
    
    <!-- 按钮内容 -->
    <slot />
  </el-button>
</template>

<script setup lang="ts" name="CommonButton">
import { computed } from 'vue'
import type { Component } from 'vue'

interface Props {
  /** 按钮类型 */
  type?: 'primary' | 'success' | 'warning' | 'danger' | 'info' | 'text' | 'default'
  /** 按钮大小 */
  size?: 'large' | 'default' | 'small'
  /** 是否为朴素按钮 */
  plain?: boolean
  /** 是否为文字按钮 */
  text?: boolean
  /** 是否显示文字按钮背景颜色 */
  bg?: boolean
  /** 是否为链接按钮 */
  link?: boolean
  /** 是否为圆角按钮 */
  round?: boolean
  /** 是否为圆形按钮 */
  circle?: boolean
  /** 是否为加载中状态 */
  loading?: boolean
  /** 自定义加载图标 */
  loadingIcon?: Component
  /** 是否禁用 */
  disabled?: boolean
  /** 图标组件 */
  icon?: Component
  /** 是否默认聚焦 */
  autofocus?: boolean
  /** 原生type属性 */
  nativeType?: 'button' | 'submit' | 'reset'
  /** 是否在两个中文字符之间插入空格 */
  autoInsertSpace?: boolean
  /** 自定义颜色 */
  color?: string
  /** 是否为暗色模式 */
  dark?: boolean
  /** 自定义元素标签 */
  tag?: string | Component
  /** 按钮变体 */
  variant?: 'default' | 'gradient' | 'shadow' | 'outline' | 'ghost'
  /** 是否为块级按钮 */
  block?: boolean
  /** 自定义宽度 */
  width?: string
  /** 自定义高度 */
  height?: string
  /** 防抖延迟(ms) */
  debounce?: number
  /** 节流延迟(ms) */
  throttle?: number
  /** 自定义样式 */
  customStyle?: Record<string, string>
  /** 自定义类名 */
  customClass?: string
}

interface Emits {
  click: [event: MouseEvent]
  focus: [event: FocusEvent]
  blur: [event: FocusEvent]
}

const props = withDefaults(defineProps<Props>(), {
  type: 'default',
  size: 'default',
  plain: false,
  text: false,
  bg: false,
  link: false,
  round: false,
  circle: false,
  loading: false,
  disabled: false,
  autofocus: false,
  nativeType: 'button',
  autoInsertSpace: false,
  dark: false,
  variant: 'default',
  block: false,
  debounce: 0,
  throttle: 0
})

const emit = defineEmits<Emits>()

// 防抖和节流处理
let debounceTimer: number | null = null
let lastThrottleTime = 0

// 计算属性
const buttonClasses = computed(() => [
  'common-button',
  {
    [`common-button--${props.variant}`]: props.variant !== 'default',
    'common-button--block': props.block,
    'common-button--custom': props.customClass
  },
  props.customClass
])

const buttonStyles = computed(() => {
  const styles: Record<string, string> = {}
  
  if (props.width) {
    styles.width = props.width
  }
  
  if (props.height) {
    styles.height = props.height
  }
  
  if (props.block) {
    styles.width = '100%'
    styles.display = 'block'
  }
  
  return {
    ...styles,
    ...props.customStyle
  }
})

// 事件处理
const handleClick = (event: MouseEvent) => {
  if (props.disabled || props.loading) {
    return
  }
  
  // 防抖处理
  if (props.debounce > 0) {
    if (debounceTimer) {
      clearTimeout(debounceTimer)
    }
    debounceTimer = setTimeout(() => {
      emit('click', event)
    }, props.debounce)
    return
  }
  
  // 节流处理
  if (props.throttle > 0) {
    const now = Date.now()
    if (now - lastThrottleTime < props.throttle) {
      return
    }
    lastThrottleTime = now
  }
  
  emit('click', event)
}

const handleFocus = (event: FocusEvent) => {
  emit('focus', event)
}

const handleBlur = (event: FocusEvent) => {
  emit('blur', event)
}
</script>

<style lang="scss" scoped>
.common-button {
  // 基础样式
  transition: all 0.3s ease;
  
  // 变体样式
  &--gradient {
    background: linear-gradient(135deg, var(--el-color-primary), var(--el-color-primary-light-3));
    border: none;
    color: white;
    
    &:hover {
      background: linear-gradient(135deg, var(--el-color-primary-dark-2), var(--el-color-primary));
      transform: translateY(-1px);
    }
    
    &:active {
      transform: translateY(0);
    }
  }
  
  &--shadow {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    
    &:hover {
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
      transform: translateY(-2px);
    }
    
    &:active {
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      transform: translateY(0);
    }
  }
  
  &--outline {
    background: transparent;
    border: 2px solid var(--el-color-primary);
    color: var(--el-color-primary);
    
    &:hover {
      background: var(--el-color-primary);
      color: white;
    }
  }
  
  &--ghost {
    background: rgba(var(--el-color-primary-rgb), 0.1);
    border: 1px solid rgba(var(--el-color-primary-rgb), 0.3);
    color: var(--el-color-primary);
    
    &:hover {
      background: rgba(var(--el-color-primary-rgb), 0.2);
      border-color: var(--el-color-primary);
    }
  }
  
  // 块级按钮
  &--block {
    width: 100%;
    display: block;
  }
  
  // 禁用状态
  &:disabled {
    cursor: not-allowed;
    opacity: 0.6;
    transform: none !important;
    box-shadow: none !important;
  }
  
  // 加载状态
  &.is-loading {
    pointer-events: none;
  }
}

// 全局样式覆盖
:deep(.el-button) {
  // 增强动画效果 - 按照设计文档规范
  transition: all 0.15s ease; /* --transition-fast */
  
  // 聚焦样式 - 按照设计文档规范
  &:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2); /* focus-ring */
  }
  
  // 图标间距
  .el-icon {
    margin-right: 6px;
    
    &:last-child {
      margin-right: 0;
      margin-left: 6px;
    }
    
    &:only-child {
      margin: 0;
    }
  }
  
  // 大小变体增强 - 按照设计文档规范
  &.el-button--large {
    padding: 16px 24px; /* --space-4 --space-6 */
    font-size: 18px; /* --text-lg */
    height: 48px;
    border-radius: 8px; /* --radius-md */
  }
  
  &.el-button--default {
    padding: 12px 16px; /* --space-3 --space-4 */
    font-size: 16px; /* --text-base */
    height: 40px;
    border-radius: 8px; /* --radius-md */
  }
  
  &.el-button--small {
    padding: 8px 12px; /* --space-2 --space-3 */
    font-size: 14px; /* --text-sm */
    height: 32px;
    border-radius: 4px; /* --radius-sm */
  }
  
  // 圆形按钮
  &.is-circle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  
  // 文字按钮增强
  &.el-button--text {
    padding: 8px 12px;
    
    &:hover {
      background-color: rgba(var(--el-color-primary-rgb), 0.1);
    }
  }
  
  // 链接按钮
  &.el-button--text.is-link {
    padding: 4px 8px;
    text-decoration: underline;
    
    &:hover {
      text-decoration: none;
    }
  }
}

// 响应式适配
@media (max-width: 768px) {
  .common-button {
    // 移动端减少动画效果
    &--shadow:hover {
      transform: none;
    }
    
    &--gradient:hover {
      transform: none;
    }
  }
  
  :deep(.el-button) {
    // 移动端按钮大小调整 - 按照设计文档规范
    &.el-button--large {
      padding: 12px 20px;
      font-size: 16px;
      height: 44px; /* 触摸目标最小尺寸 */
    }
    
    &.el-button--default {
      padding: 10px 16px;
      font-size: 15px;
      height: 40px;
    }
    
    &.el-button--small {
      padding: 8px 12px;
      font-size: 13px;
      height: 36px;
    }
  }
}

@media (max-width: 480px) {
  :deep(.el-button) {
    // 小屏幕进一步调整
    &.el-button--large {
      padding: 8px 16px;
      font-size: 14px;
    }
    
    &.el-button--default {
      padding: 6px 12px;
      font-size: 13px;
    }
    
    &.el-button--small {
      padding: 4px 8px;
      font-size: 11px;
    }
  }
}
</style>