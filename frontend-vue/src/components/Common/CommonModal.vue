<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    :width="width"
    :fullscreen="fullscreen"
    :top="top"
    :modal="modal"
    :modal-class="modalClass"
    :append-to-body="appendToBody"
    :lock-scroll="lockScroll"
    :custom-class="customClass"
    :open-delay="openDelay"
    :close-delay="closeDelay"
    :close-on-click-modal="closeOnClickModal"
    :close-on-press-escape="closeOnPressEscape"
    :show-close="showClose"
    :before-close="handleBeforeClose"
    :center="center"
    :align-center="alignCenter"
    :destroy-on-close="destroyOnClose"
    @open="handleOpen"
    @opened="handleOpened"
    @close="handleClose"
    @closed="handleClosed"
  >
    <!-- 自定义标题 -->
    <template v-if="$slots.title" #title>
      <slot name="title" />
    </template>
    
    <!-- 主要内容 -->
    <div :class="contentClasses" :style="contentStyles">
      <!-- 加载状态 -->
      <div v-if="loading" class="common-modal__loading">
        <el-icon class="is-loading">
          <Loading />
        </el-icon>
        <span>{{ loadingText }}</span>
      </div>
      
      <!-- 正常内容 -->
      <div v-else class="common-modal__content">
        <slot />
      </div>
    </div>
    
    <!-- 自定义底部 -->
    <template v-if="$slots.footer || showFooter" #footer>
      <slot name="footer">
        <div class="common-modal__footer">
          <el-button
            v-if="showCancel"
            :size="buttonSize"
            :disabled="confirmLoading"
            @click="handleCancel"
          >
            {{ cancelText }}
          </el-button>
          <el-button
            v-if="showConfirm"
            :type="confirmType"
            :size="buttonSize"
            :loading="confirmLoading"
            @click="handleConfirm"
          >
            {{ confirmText }}
          </el-button>
        </div>
      </slot>
    </template>
  </el-dialog>
</template>

<script setup lang="ts" name="CommonModal">
import { computed, watch } from 'vue'
import { Loading } from '@element-plus/icons-vue'

interface Props {
  /** 是否显示模态框 */
  modelValue: boolean
  /** 标题 */
  title?: string
  /** 宽度 */
  width?: string | number
  /** 是否全屏 */
  fullscreen?: boolean
  /** 距离顶部的距离 */
  top?: string
  /** 是否显示遮罩层 */
  modal?: boolean
  /** 遮罩层类名 */
  modalClass?: string
  /** 是否插入到body */
  appendToBody?: boolean
  /** 是否锁定滚动 */
  lockScroll?: boolean
  /** 自定义类名 */
  customClass?: string
  /** 打开延时 */
  openDelay?: number
  /** 关闭延时 */
  closeDelay?: number
  /** 点击遮罩层是否关闭 */
  closeOnClickModal?: boolean
  /** 按ESC是否关闭 */
  closeOnPressEscape?: boolean
  /** 是否显示关闭按钮 */
  showClose?: boolean
  /** 是否居中 */
  center?: boolean
  /** 是否垂直居中 */
  alignCenter?: boolean
  /** 关闭时是否销毁 */
  destroyOnClose?: boolean
  /** 是否显示底部 */
  showFooter?: boolean
  /** 是否显示取消按钮 */
  showCancel?: boolean
  /** 是否显示确认按钮 */
  showConfirm?: boolean
  /** 取消按钮文本 */
  cancelText?: string
  /** 确认按钮文本 */
  confirmText?: string
  /** 确认按钮类型 */
  confirmType?: 'primary' | 'success' | 'warning' | 'danger' | 'info'
  /** 按钮大小 */
  buttonSize?: 'large' | 'default' | 'small'
  /** 确认按钮加载状态 */
  confirmLoading?: boolean
  /** 整体加载状态 */
  loading?: boolean
  /** 加载文本 */
  loadingText?: string
  /** 内容最大高度 */
  maxHeight?: string
  /** 内容最小高度 */
  minHeight?: string
  /** 内容自定义样式 */
  contentStyle?: Record<string, string>
  /** 关闭前回调 */
  beforeClose?: (done: () => void) => void
}

interface Emits {
  'update:modelValue': [value: boolean]
  open: []
  opened: []
  close: []
  closed: []
  cancel: []
  confirm: []
}

const props = withDefaults(defineProps<Props>(), {
  width: '50%',
  fullscreen: false,
  top: '15vh',
  modal: true,
  appendToBody: false,
  lockScroll: true,
  openDelay: 0,
  closeDelay: 0,
  closeOnClickModal: true,
  closeOnPressEscape: true,
  showClose: true,
  center: false,
  alignCenter: false,
  destroyOnClose: false,
  showFooter: true,
  showCancel: true,
  showConfirm: true,
  cancelText: '取消',
  confirmText: '确定',
  confirmType: 'primary',
  buttonSize: 'default',
  confirmLoading: false,
  loading: false,
  loadingText: '加载中...'
})

const emit = defineEmits<Emits>()

// 计算属性
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value: boolean) => {
    emit('update:modelValue', value)
  }
})

const contentClasses = computed(() => [
  'common-modal__wrapper',
  {
    'common-modal__wrapper--loading': props.loading
  }
])

const contentStyles = computed(() => {
  const styles: Record<string, string> = {}
  
  if (props.maxHeight) {
    styles.maxHeight = props.maxHeight
  }
  
  if (props.minHeight) {
    styles.minHeight = props.minHeight
  }
  
  return {
    ...styles,
    ...props.contentStyle
  }
})

// 事件处理
const handleBeforeClose = (done: () => void) => {
  if (props.beforeClose) {
    props.beforeClose(done)
  } else {
    done()
  }
}

const handleOpen = () => {
  emit('open')
}

const handleOpened = () => {
  emit('opened')
}

const handleClose = () => {
  emit('close')
}

const handleClosed = () => {
  emit('closed')
}

const handleCancel = () => {
  emit('cancel')
  dialogVisible.value = false
}

const handleConfirm = () => {
  emit('confirm')
}

// 监听确认加载状态，自动关闭
watch(
  () => props.confirmLoading,
  () => {
    // 当确认加载从true变为false时，可能需要关闭模态框
    // 这里不自动关闭，让父组件控制
  }
)
</script>

<style lang="scss" scoped>
.common-modal {
  &__wrapper {
    position: relative;
    
    &--loading {
      min-height: 100px;
    }
  }
  
  &__loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    color: #6B7280; // 使用设计文档的次要文本颜色
    
    .el-icon {
      font-size: 24px;
      margin-bottom: 12px;
      color: #6366F1; // 使用设计文档的主色
    }
    
    span {
      font-size: 14px;
      font-weight: 500;
    }
  }
  
  &__content {
    max-height: 60vh;
    overflow-y: auto;
    
    // 自定义滚动条 (严格按照设计文档)
    &::-webkit-scrollbar {
      width: 6px;
    }
    
    &::-webkit-scrollbar-track {
      background: #F3F4F6;
      border-radius: 3px;
    }
    
    &::-webkit-scrollbar-thumb {
      background: #D1D5DB;
      border-radius: 3px;
      
      &:hover {
        background: #9CA3AF;
      }
    }
  }
  
  &__footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    
    .el-button {
      min-width: 80px;
    }
  }
}

// 全局样式覆盖 (严格按照设计文档)
:deep(.el-dialog) {
  border-radius: 12px; // 使用设计文档的圆角
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); // 使用设计文档的阴影
  
  .el-dialog__header {
    padding: 24px 24px 16px;
    border-bottom: 1px solid #F3F4F6; // 使用设计文档的边框颜色
    
    .el-dialog__title {
      font-size: 18px; // 使用设计文档的字体大小
      font-weight: 600;
      color: #111827; // 使用设计文档的主要文本颜色
    }
  }
  
  .el-dialog__body {
    padding: 24px;
    color: #374151; // 使用设计文档的常规文本颜色
    line-height: 1.4;
  }
  
  .el-dialog__footer {
    padding: 16px 24px 24px;
    border-top: 1px solid #F3F4F6; // 使用设计文档的边框颜色
  }
  
  .el-dialog__close {
    font-size: 16px;
    color: #9CA3AF; // 使用设计文档的占位符颜色
    
    &:hover {
      color: #6366F1; // 使用设计文档的主色
    }
  }
}

// 响应式适配
@media (max-width: 768px) {
  :deep(.el-dialog) {
    width: 90% !important;
    margin: 5vh auto;
    
    .el-dialog__header {
      padding: 16px 16px 8px;
      
      .el-dialog__title {
        font-size: 15px;
      }
    }
    
    .el-dialog__body {
      padding: 16px;
      font-size: 14px;
    }
    
    .el-dialog__footer {
      padding: 8px 16px 16px;
    }
  }
  
  .common-modal {
    &__content {
      max-height: 50vh;
    }
    
    &__footer {
      gap: 8px;
      
      .el-button {
        min-width: 70px;
        font-size: 13px;
      }
    }
  }
}

@media (max-width: 480px) {
  :deep(.el-dialog) {
    width: 95% !important;
    margin: 3vh auto;
  }
  
  .common-modal {
    &__loading {
      padding: 30px 15px;
      
      .el-icon {
        font-size: 20px;
        margin-bottom: 8px;
      }
      
      span {
        font-size: 13px;
      }
    }
    
    &__footer {
      flex-direction: column;
      gap: 8px;
      
      .el-button {
        width: 100%;
      }
    }
  }
}
</style>