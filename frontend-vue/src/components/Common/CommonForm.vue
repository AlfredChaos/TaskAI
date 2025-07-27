<template>
  <el-form
    ref="formRef"
    :model="modelValue"
    :rules="rules"
    :inline="inline"
    :label-position="labelPosition"
    :label-width="labelWidth"
    :label-suffix="labelSuffix"
    :hide-required-asterisk="hideRequiredAsterisk"
    :show-message="showMessage"
    :inline-message="inlineMessage"
    :status-icon="statusIcon"
    :validate-on-rule-change="validateOnRuleChange"
    :size="size"
    :disabled="disabled"
    :scroll-to-error="scrollToError"
    :class="formClasses"
    :style="formStyles"
    @validate="handleValidate"
  >
    <slot />
    
    <!-- 操作按钮区域 -->
    <el-form-item v-if="showActions" :class="actionClasses">
      <slot name="actions">
        <div class="common-form__actions">
          <el-button
            v-if="showReset"
            :size="buttonSize"
            :disabled="loading"
            @click="handleReset"
          >
            {{ resetText }}
          </el-button>
          <el-button
            v-if="showSubmit"
            type="primary"
            :size="buttonSize"
            :loading="loading"
            @click="handleSubmit"
          >
            {{ submitText }}
          </el-button>
        </div>
      </slot>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts" name="CommonForm">
import { ref, computed } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'

interface Props {
  /** 表单数据对象 */
  modelValue: Record<string, unknown>
  /** 表单验证规则 */
  rules?: FormRules
  /** 行内表单模式 */
  inline?: boolean
  /** 表单域标签的位置 */
  labelPosition?: 'left' | 'right' | 'top'
  /** 表单域标签的宽度 */
  labelWidth?: string | number
  /** 表单域标签的后缀 */
  labelSuffix?: string
  /** 是否隐藏必填字段的标签旁边的红色星号 */
  hideRequiredAsterisk?: boolean
  /** 是否显示校验错误信息 */
  showMessage?: boolean
  /** 是否以行内形式展示校验信息 */
  inlineMessage?: boolean
  /** 是否在输入框中显示校验结果反馈图标 */
  statusIcon?: boolean
  /** 是否在 rules 属性改变后立即触发一次验证 */
  validateOnRuleChange?: boolean
  /** 用于控制该表单内组件的尺寸 */
  size?: 'large' | 'default' | 'small'
  /** 是否禁用该表单内的所有组件 */
  disabled?: boolean
  /** 当校验失败时，滚动到第一个错误表单项 */
  scrollToError?: boolean
  /** 是否显示操作按钮 */
  showActions?: boolean
  /** 是否显示重置按钮 */
  showReset?: boolean
  /** 是否显示提交按钮 */
  showSubmit?: boolean
  /** 重置按钮文本 */
  resetText?: string
  /** 提交按钮文本 */
  submitText?: string
  /** 按钮大小 */
  buttonSize?: 'large' | 'default' | 'small'
  /** 加载状态 */
  loading?: boolean
  /** 操作按钮对齐方式 */
  actionAlign?: 'left' | 'center' | 'right'
  /** 表单布局 */
  layout?: 'horizontal' | 'vertical' | 'inline'
  /** 栅格间隔 */
  gutter?: number
  /** 自定义样式 */
  customStyle?: Record<string, string>
  /** 自定义类名 */
  customClass?: string
}

interface Emits {
  'update:modelValue': [value: Record<string, unknown>]
  validate: [prop: string, isValid: boolean, message: string]
  submit: [formData: Record<string, unknown>]
  reset: []
}

const props = withDefaults(defineProps<Props>(), {
  inline: false,
  labelPosition: 'right',
  labelWidth: 'auto',
  labelSuffix: '',
  hideRequiredAsterisk: false,
  showMessage: true,
  inlineMessage: false,
  statusIcon: false,
  validateOnRuleChange: true,
  size: 'default',
  disabled: false,
  scrollToError: false,
  showActions: true,
  showReset: true,
  showSubmit: true,
  resetText: '重置',
  submitText: '提交',
  buttonSize: 'default',
  loading: false,
  actionAlign: 'right',
  layout: 'horizontal',
  gutter: 20
})

const emit = defineEmits<Emits>()

// 表单引用
const formRef = ref<FormInstance>()

// 计算属性
const formClasses = computed(() => [
  'common-form',
  {
    [`common-form--${props.layout}`]: props.layout !== 'horizontal',
    'common-form--inline': props.inline,
    'common-form--custom': props.customClass
  },
  props.customClass
])

const formStyles = computed(() => {
  const styles: Record<string, string> = {}
  
  if (props.gutter && props.layout !== 'inline') {
    styles['--form-gutter'] = `${props.gutter}px`
  }
  
  return {
    ...styles,
    ...props.customStyle
  }
})

const actionClasses = computed(() => [
  'common-form__action-item',
  `common-form__action-item--${props.actionAlign}`
])

// 事件处理
const handleValidate = (prop: string, isValid: boolean, message: string) => {
  emit('validate', prop, isValid, message)
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    emit('submit', props.modelValue)
  } catch {
    console.warn('表单验证失败')
  }
}

const handleReset = () => {
  if (!formRef.value) return
  
  formRef.value.resetFields()
  emit('reset')
}

// 暴露方法
const validate = async (callback?: (isValid: boolean) => void) => {
  if (!formRef.value) return false
  
  try {
    const isValid = await formRef.value.validate()
    callback?.(isValid)
    return isValid
  } catch {
    callback?.(false)
    return false
  }
}

const validateField = async (props: string | string[], callback?: (isValid: boolean) => void) => {
  if (!formRef.value) return false
  
  try {
    await formRef.value.validateField(props)
    callback?.(true)
    return true
  } catch {
    callback?.(false)
    return false
  }
}

const resetFields = (props?: string | string[]) => {
  if (!formRef.value) return
  
  formRef.value.resetFields(props)
}

const clearValidate = (props?: string | string[]) => {
  if (!formRef.value) return
  
  formRef.value.clearValidate(props)
}

const scrollToField = (prop: string) => {
  if (!formRef.value) return
  
  formRef.value.scrollToField(prop)
}

// 获取表单实例
const getFormInstance = () => formRef.value

// 暴露给父组件
defineExpose({
  validate,
  validateField,
  resetFields,
  clearValidate,
  scrollToField,
  getFormInstance
})
</script>

<style lang="scss" scoped>
.common-form {
  // 基础样式
  --form-gutter: 20px;
  
  // 垂直布局
  &--vertical {
    :deep(.el-form-item) {
      margin-bottom: var(--form-gutter);
      
      .el-form-item__label {
        display: block;
        text-align: left;
        padding: 0 0 8px 0;
        line-height: 1.5;
      }
      
      .el-form-item__content {
        margin-left: 0 !important;
      }
    }
  }
  
  // 行内布局
  &--inline {
    :deep(.el-form-item) {
      margin-right: var(--form-gutter);
      margin-bottom: 16px;
      
      &:last-child {
        margin-right: 0;
      }
    }
  }
  
  // 操作按钮项 (严格按照设计文档)
  &__action-item {
    margin-top: 24px;
    margin-bottom: 0;
    padding-top: 16px;
    border-top: 1px solid #F3F4F6; // 添加分隔线
    
    &--left {
      :deep(.el-form-item__content) {
        justify-content: flex-start;
      }
    }
    
    &--center {
      :deep(.el-form-item__content) {
        justify-content: center;
      }
    }
    
    &--right {
      :deep(.el-form-item__content) {
        justify-content: flex-end;
      }
    }
  }
  
  // 操作按钮容器 (严格按照设计文档)
  &__actions {
    display: flex;
    gap: 12px;
    align-items: center;
    
    .el-button {
      border-radius: 8px; // 使用设计文档的圆角
      font-weight: 500;
      
      // 主按钮样式
      &--primary {
        background: #6366F1; // 使用设计文档的主色
        border-color: #6366F1;
        
        &:hover {
          background: #4F46E5;
          border-color: #4F46E5;
        }
      }
      
      // 次要按钮样式
      &--default {
        background: #FFFFFF;
        border-color: #D1D5DB;
        color: #374151;
        
        &:hover {
          background: #F9FAFB;
          border-color: #9CA3AF;
        }
      }
    }
  }
}

// 全局样式覆盖
:deep(.el-form) {
  // 表单项样式增强
  .el-form-item {
    margin-bottom: 16px; // 使用设计文档的间距
    
    &:last-child {
      margin-bottom: 0;
    }
    
    // 标签样式 (严格按照设计文档)
    .el-form-item__label {
      font-weight: 500;
      color: #374151; // 使用设计文档的文本颜色
      line-height: 1.4;
      font-size: 14px; // 使用设计文档的字体大小
      
      &::before {
        margin-right: 4px;
      }
    }
    
    // 内容区域
    .el-form-item__content {
      display: flex;
      align-items: flex-start;
      flex-wrap: wrap;
      
      // 输入框等组件 (严格按照设计文档)
      .el-input,
      .el-select,
      .el-cascader,
      .el-date-editor {
        width: 100%;
        
        .el-input__inner,
        .el-select__wrapper {
          border-radius: 8px; // 使用设计文档的圆角
          border: 1px solid #D1D5DB; // 使用设计文档的边框颜色
          font-size: 14px; // 使用设计文档的字体大小
          
          &:focus {
            border-color: #6366F1; // 使用设计文档的主色
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
          }
        }
      }
      
      // 多选框和单选框
      .el-checkbox-group,
      .el-radio-group {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
      }
    }
    
    // 错误信息样式 (严格按照设计文档)
    .el-form-item__error {
      font-size: 12px;
      line-height: 1.4;
      padding-top: 4px;
      color: #EF4444; // 使用设计文档的错误色
    }
  }
  
  // 行内表单特殊处理
  &.el-form--inline {
    .el-form-item {
      margin-right: 16px;
      margin-bottom: 16px;
      
      .el-form-item__content {
        .el-input,
        .el-select {
          width: auto;
          min-width: 120px;
        }
      }
    }
  }
}

// 响应式适配
@media (max-width: 768px) {
  .common-form {
    // 移动端强制垂直布局
    &:not(.common-form--inline) {
      :deep(.el-form-item) {
        .el-form-item__label {
          display: block;
          text-align: left;
          padding: 0 0 6px 0;
          line-height: 1.4;
        }
        
        .el-form-item__content {
          margin-left: 0 !important;
        }
      }
    }
    
    // 操作按钮适配
    &__actions {
      flex-direction: column;
      gap: 8px;
      width: 100%;
      
      .el-button {
        width: 100%;
      }
    }
    
    &__action-item {
      &--left,
      &--center,
      &--right {
        :deep(.el-form-item__content) {
          justify-content: stretch;
        }
      }
    }
  }
  
  :deep(.el-form) {
    .el-form-item {
      margin-bottom: 16px;
      
      .el-form-item__label {
        font-size: 14px;
      }
      
      .el-form-item__error {
        font-size: 11px;
      }
    }
  }
}

@media (max-width: 480px) {
  .common-form {
    --form-gutter: 12px;
    
    &__action-item {
      margin-top: 16px;
    }
  }
  
  :deep(.el-form) {
    .el-form-item {
      margin-bottom: 12px;
      
      .el-form-item__label {
        font-size: 13px;
        padding-bottom: 4px;
      }
    }
  }
}
</style>