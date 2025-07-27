<template>
  <div 
    :class="avatarClasses"
    :style="avatarStyles"
    @click="handleClick"
  >
    <!-- 头像图片 -->
    <img 
      v-if="src && !imageError" 
      :src="src" 
      :alt="alt"
      @error="handleImageError"
      @load="handleImageLoad"
    />
    
    <!-- 文字头像 -->
    <span 
      v-else-if="name" 
      :class="textClasses"
      :style="textStyles"
    >
      {{ displayText }}
    </span>
    
    <!-- 默认图标 -->
    <el-icon v-else :size="iconSize">
      <User />
    </el-icon>
    
    <!-- 在线状态指示器 -->
    <div 
      v-if="showStatus && status" 
      :class="statusClasses"
    ></div>
    
    <!-- 徽章 -->
    <div 
      v-if="badge && badge > 0" 
      :class="badgeClasses"
    >
      {{ badgeText }}
    </div>
  </div>
</template>

<script setup lang="ts" name="CommonAvatar">
import { computed, ref } from 'vue'
import { User } from '@element-plus/icons-vue'

interface Props {
  /** 头像图片地址 */
  src?: string
  /** 头像大小 */
  size?: 'small' | 'default' | 'large' | number
  /** 头像形状 */
  shape?: 'circle' | 'square'
  /** 用户名称（用于生成文字头像） */
  name?: string
  /** 图片alt属性 */
  alt?: string
  /** 在线状态 */
  status?: 'online' | 'offline' | 'away' | 'busy'
  /** 是否显示状态指示器 */
  showStatus?: boolean
  /** 徽章数字 */
  badge?: number
  /** 是否可点击 */
  clickable?: boolean
  /** 自定义背景色 */
  backgroundColor?: string
  /** 自定义文字颜色 */
  textColor?: string
}

interface Emits {
  click: [event: MouseEvent]
  imageLoad: [event: Event]
  imageError: [event: Event]
}

const props = withDefaults(defineProps<Props>(), {
  size: 'default',
  shape: 'circle',
  alt: 'avatar',
  showStatus: false,
  clickable: false,
  backgroundColor: '#409EFF',
  textColor: '#ffffff'
})

const emit = defineEmits<Emits>()

// 响应式状态
const imageError = ref(false)

// 计算属性
const sizeValue = computed(() => {
  if (typeof props.size === 'number') {
    return props.size
  }
  // 按照设计文档规范：sm=24px, md=32px, lg=40px, xl=48px
  const sizeMap = {
    small: 24,
    default: 32,
    large: 40
  }
  return sizeMap[props.size]
})

const iconSize = computed(() => {
  return Math.floor(sizeValue.value * 0.6)
})

const displayText = computed(() => {
  if (!props.name) return ''
  
  // 提取中文姓名的最后一个字符，或英文姓名的首字母
  const name = props.name.trim()
  if (/[\u4e00-\u9fa5]/.test(name)) {
    // 中文名取最后一个字
    return name.slice(-1)
  } else {
    // 英文名取首字母
    return name.split(' ').map(word => word.charAt(0)).join('').slice(0, 2).toUpperCase()
  }
})

const badgeText = computed(() => {
  if (!props.badge || props.badge <= 0) return ''
  return props.badge > 99 ? '99+' : props.badge.toString()
})

// 样式类
const avatarClasses = computed(() => [
  'common-avatar',
  `common-avatar--${props.shape}`,
  `common-avatar--${typeof props.size === 'string' ? props.size : 'custom'}`,
  {
    'common-avatar--clickable': props.clickable,
    'common-avatar--with-status': props.showStatus && props.status,
    'common-avatar--with-badge': props.badge && props.badge > 0
  }
])

const textClasses = computed(() => [
  'common-avatar__text'
])

const statusClasses = computed(() => [
  'common-avatar__status',
  `common-avatar__status--${props.status}`
])

const badgeClasses = computed(() => [
  'common-avatar__badge'
])

// 样式对象
const avatarStyles = computed(() => ({
  width: `${sizeValue.value}px`,
  height: `${sizeValue.value}px`,
  fontSize: `${Math.floor(sizeValue.value * 0.4)}px`
}))

const textStyles = computed(() => ({
  backgroundColor: props.backgroundColor,
  color: props.textColor
}))

// 事件处理
const handleClick = (event: MouseEvent) => {
  if (props.clickable) {
    emit('click', event)
  }
}

const handleImageError = (event: Event) => {
  imageError.value = true
  emit('imageError', event)
}

const handleImageLoad = (event: Event) => {
  imageError.value = false
  emit('imageLoad', event)
}
</script>

<style lang="scss" scoped>
.common-avatar {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: #E5E7EB; /* --gray-200 */
  color: #6B7280; /* --gray-500 */
  white-space: nowrap;
  text-align: center;
  vertical-align: middle;
  transition: all 0.3s;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  // 形状 - 按照设计文档规范
  &--circle {
    border-radius: 50%; /* --radius-full */
  }
  
  &--square {
    border-radius: 8px; /* --radius-md */
  }
  
  // 大小 - 按照设计文档规范
  &--small {
    width: 24px;
    height: 24px;
    font-size: 10px;
  }
  
  &--default {
    width: 32px;
    height: 32px;
    font-size: 12px;
  }
  
  &--large {
    width: 40px;
    height: 40px;
    font-size: 14px;
  }
  
  // 可点击
  &--clickable {
    cursor: pointer;
    
    &:hover {
      opacity: 0.8;
      transform: scale(1.05);
    }
  }
  
  // 文字头像
  &__text {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 500;
  }
  
  // 状态指示器
  &__status {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 25%;
    height: 25%;
    border: 2px solid var(--el-bg-color);
    border-radius: 50%;
    
    &--online {
      background-color: var(--el-color-success);
    }
    
    &--offline {
      background-color: var(--el-color-info);
    }
    
    &--away {
      background-color: var(--el-color-warning);
    }
    
    &--busy {
      background-color: var(--el-color-danger);
    }
  }
  
  // 徽章
  &__badge {
    position: absolute;
    top: -2px;
    right: -2px;
    min-width: 16px;
    height: 16px;
    padding: 0 4px;
    background-color: var(--el-color-danger);
    color: white;
    font-size: 10px;
    font-weight: 500;
    line-height: 16px;
    text-align: center;
    border-radius: 8px;
    border: 1px solid var(--el-bg-color);
    box-sizing: border-box;
  }
  
  // 响应式适配
  @media (max-width: 768px) {
    &--large {
      width: 48px !important;
      height: 48px !important;
      font-size: 20px !important;
    }
  }
}
</style>