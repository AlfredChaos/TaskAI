<template>
  <div :class="emptyClasses" :style="emptyStyles">
    <!-- 图标或图片 -->
    <div class="common-empty__image">
      <!-- 自定义图片 -->
      <img v-if="image" :src="image" :alt="imageAlt" />
      
      <!-- 自定义图标 -->
      <el-icon v-else-if="icon" :size="iconSize">
        <component :is="icon" />
      </el-icon>
      
      <!-- 默认空状态图标 -->
      <div v-else class="common-empty__default-icon">
        <svg viewBox="0 0 64 41" :width="iconSize" :height="iconSize * 0.64">
          <g transform="translate(0 1)" fill="none" fill-rule="evenodd">
            <ellipse fill="#f5f5f5" cx="32" cy="33" rx="32" ry="7"></ellipse>
            <g fill-rule="nonzero" stroke="#d9d9d9">
              <path d="M55 12.76L44.854 1.258C44.367.474 43.656 0 42.907 0H21.093c-.749 0-1.46.474-1.947 1.257L9 12.761V22h46v-9.24z"></path>
              <path d="M41.613 15.931c0-1.605.994-2.93 2.227-2.931H55v18.137C55 33.26 53.68 35 52.05 35h-40.1C10.32 35 9 33.259 9 31.137V13h11.16c1.233 0 2.227 1.323 2.227 2.928v.022c0 1.605 1.005 2.901 2.237 2.901h14.752c1.232 0 2.237-1.308 2.237-2.913v-.007z" fill="#fafafa"></path>
            </g>
          </g>
        </svg>
      </div>
    </div>
    
    <!-- 描述文本 -->
    <div class="common-empty__description">
      <slot name="description">
        <span>{{ description || defaultDescription }}</span>
      </slot>
    </div>
    
    <!-- 操作按钮 -->
    <div v-if="$slots.default || showAction" class="common-empty__action">
      <slot>
        <el-button v-if="showAction" :type="actionType" @click="handleAction">
          {{ actionText }}
        </el-button>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts" name="CommonEmpty">
import { computed } from 'vue'
import type { Component } from 'vue'

interface Props {
  /** 空状态描述 */
  description?: string
  /** 自定义图片 */
  image?: string
  /** 图片alt属性 */
  imageAlt?: string
  /** 自定义图标 */
  icon?: Component
  /** 图标大小 */
  iconSize?: number
  /** 是否显示操作按钮 */
  showAction?: boolean
  /** 操作按钮文本 */
  actionText?: string
  /** 操作按钮类型 */
  actionType?: 'primary' | 'success' | 'warning' | 'danger' | 'info' | 'text'
  /** 空状态类型 */
  type?: 'default' | 'search' | 'network' | 'permission' | 'error'
  /** 大小 */
  size?: 'small' | 'default' | 'large'
  /** 自定义样式 */
  customStyle?: Record<string, string>
}

interface Emits {
  action: []
}

const props = withDefaults(defineProps<Props>(), {
  iconSize: 64,
  showAction: false,
  actionText: '重试',
  actionType: 'primary',
  type: 'default',
  size: 'default',
  imageAlt: 'empty'
})

const emit = defineEmits<Emits>()

// 计算属性
const defaultDescription = computed(() => {
  const typeDescriptions = {
    default: '暂无数据',
    search: '搜索无结果',
    network: '网络连接失败',
    permission: '暂无权限访问',
    error: '出现了一些错误'
  }
  return typeDescriptions[props.type]
})

const emptyClasses = computed(() => [
  'common-empty',
  `common-empty--${props.size}`,
  `common-empty--${props.type}`
])

const emptyStyles = computed(() => {
  return props.customStyle || {}
})

// 事件处理
const handleAction = () => {
  emit('action')
}
</script>

<style lang="scss" scoped>
.common-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
  
  // 大小变体
  &--small {
    padding: 20px 16px;
    
    .common-empty__image {
      margin-bottom: 12px;
    }
    
    .common-empty__description {
      font-size: 12px;
      margin-bottom: 12px;
    }
  }
  
  &--default {
    padding: 40px 20px;
    
    .common-empty__image {
      margin-bottom: 16px;
    }
    
    .common-empty__description {
      font-size: 14px;
      margin-bottom: 16px;
    }
  }
  
  &--large {
    padding: 60px 24px;
    
    .common-empty__image {
      margin-bottom: 24px;
    }
    
    .common-empty__description {
      font-size: 16px;
      margin-bottom: 24px;
    }
  }
  
  // 类型变体 (严格按照设计文档)
  &--search {
    .common-empty__description {
      color: #6B7280; // 使用设计文档的次要文本颜色
    }
  }
  
  &--network {
    .common-empty__description {
      color: #F59E0B; // 使用设计文档的警告色
    }
  }
  
  &--permission {
    .common-empty__description {
      color: #EF4444; // 使用设计文档的错误色
    }
  }
  
  &--error {
    .common-empty__description {
      color: #EF4444; // 使用设计文档的错误色
    }
  }
  
  // 图片/图标容器
  &__image {
    display: flex;
    align-items: center;
    justify-content: center;
    
    img {
      max-width: 100%;
      height: auto;
    }
    
    .el-icon {
      color: #9CA3AF; // 使用设计文档的占位符颜色
    }
  }
  
  // 默认图标
  &__default-icon {
    opacity: 0.6;
    
    svg {
      display: block;
    }
  }
  
  // 描述文本 (严格按照设计文档)
  &__description {
    color: #6B7280; // 使用设计文档的次要文本颜色
    line-height: 1.4;
    max-width: 400px;
    font-weight: 500;
    
    span {
      display: block;
    }
  }
  
  // 操作区域
  &__action {
    margin-top: 8px;
  }
  
  // 响应式适配
  @media (max-width: 768px) {
    padding: 30px 16px;
    
    &__description {
      font-size: 13px;
      max-width: 300px;
    }
    
    &--large {
      padding: 40px 20px;
      
      .common-empty__image {
        margin-bottom: 20px;
      }
      
      .common-empty__description {
        font-size: 14px;
        margin-bottom: 20px;
      }
    }
  }
  
  @media (max-width: 480px) {
    padding: 20px 12px;
    
    &__description {
      font-size: 12px;
      max-width: 250px;
    }
  }
}
</style>