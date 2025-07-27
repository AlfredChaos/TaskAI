import './assets/main.css'
import './styles/index.scss'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'
import { initializeStores } from './stores'

const app = createApp(App)

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

// 初始化应用
const initApp = async () => {
  // 初始化stores
  await initializeStores()
  
  // 挂载应用
  app.mount('#app')
}

// 启动应用
initApp().catch(console.error)
