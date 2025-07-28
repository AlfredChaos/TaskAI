// 通用组件统一导出
import CommonAvatar from './Avatar.vue'
import CommonCard from './CommonCard.vue'
import CommonLoading from './CommonLoading.vue'
import CommonEmpty from './CommonEmpty.vue'
import CommonModal from './CommonModal.vue'
import CommonButton from './CommonButton.vue'
import CommonForm from './CommonForm.vue'
import DevTools from './DevTools.vue'

// 导出所有组件
export {
  CommonAvatar,
  CommonCard,
  CommonLoading,
  CommonEmpty,
  CommonModal,
  CommonButton,
  CommonForm,
  DevTools
}

// 默认导出
export default {
  CommonAvatar,
  CommonCard,
  CommonLoading,
  CommonEmpty,
  CommonModal,
  CommonButton,
  CommonForm,
  DevTools
}

// 组件类型定义
export type {
  // 可以在这里添加组件的类型定义
}

// 组件安装函数（用于全局注册）
export const installCommonComponents = (app: import('vue').App) => {
  app.component('CommonAvatar', CommonAvatar)
  app.component('CommonCard', CommonCard)
  app.component('CommonLoading', CommonLoading)
  app.component('CommonEmpty', CommonEmpty)
  app.component('CommonModal', CommonModal)
  app.component('CommonButton', CommonButton)
  app.component('CommonForm', CommonForm)
  app.component('DevTools', DevTools)
}