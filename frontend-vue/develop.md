# Tuscot 项目管理系统开发文档

## 📁 项目目录结构

```
frontend-vue/
├── public/                     # 静态资源
│   ├── favicon.ico
│   └── index.html
├── src/
│   ├── api/                    # API接口管理
│   │   ├── index.ts           # API统一入口
│   │   ├── modules/           # 按模块分类的API
│   │   │   ├── auth.ts        # 认证相关API
│   │   │   ├── dashboard.ts   # 仪表板API
│   │   │   ├── project.ts     # 项目管理API
│   │   │   ├── task.ts        # 任务管理API
│   │   │   ├── message.ts     # 消息聊天API
│   │   │   └── activity.ts    # 活动时间线API
│   │   └── request.ts         # HTTP请求封装
│   ├── assets/                # 静态资源
│   │   ├── images/
│   │   ├── icons/
│   │   └── styles/
│   │       ├── index.scss     # 全局样式入口
│   │       ├── variables.scss # 样式变量
│   │       └── mixins.scss    # 样式混入
│   ├── components/            # 公共组件
│   │   ├── common/           # 通用组件
│   │   │   ├── Avatar.vue    # 头像组件
│   │   │   ├── Card.vue      # 卡片组件
│   │   │   ├── Loading.vue   # 加载组件
│   │   │   └── Empty.vue     # 空状态组件
│   │   ├── charts/           # 图表组件
│   │   │   ├── PieChart.vue  # 饼图
│   │   │   ├── BarChart.vue  # 柱状图
│   │   │   └── LineChart.vue # 折线图
│   │   └── layout/           # 布局组件
│   │       ├── Header.vue    # 头部导航
│   │       ├── Sidebar.vue   # 侧边栏
│   │       └── Layout.vue    # 主布局
│   ├── composables/          # 组合式函数
│   │   ├── useAuth.ts        # 认证相关
│   │   ├── useTheme.ts       # 主题切换
│   │   └── usePermission.ts  # 权限管理
│   ├── mock/                 # Mock数据管理
│   │   ├── index.ts          # Mock入口
│   │   ├── data/             # Mock数据
│   │   │   ├── users.ts      # 用户数据
│   │   │   ├── projects.ts   # 项目数据
│   │   │   ├── tasks.ts      # 任务数据
│   │   │   ├── messages.ts   # 消息数据
│   │   │   └── activities.ts # 活动数据
│   │   └── handlers/         # Mock处理器
│   │       ├── auth.ts
│   │       ├── dashboard.ts
│   │       ├── project.ts
│   │       ├── task.ts
│   │       ├── message.ts
│   │       └── activity.ts
│   ├── router/               # 路由配置
│   │   ├── index.ts          # 路由入口
│   │   ├── routes.ts         # 路由定义
│   │   └── guards.ts         # 路由守卫
│   ├── stores/               # 状态管理
│   │   ├── index.ts          # Store入口
│   │   ├── auth.ts           # 认证状态
│   │   ├── user.ts           # 用户状态
│   │   ├── project.ts        # 项目状态
│   │   └── theme.ts          # 主题状态
│   ├── types/                # TypeScript类型定义
│   │   ├── api.ts            # API类型
│   │   ├── user.ts           # 用户类型
│   │   ├── project.ts        # 项目类型
│   │   ├── task.ts           # 任务类型
│   │   └── common.ts         # 通用类型
│   ├── utils/                # 工具函数库
│   │   ├── index.ts          # 工具函数入口
│   │   ├── date.ts           # 日期处理
│   │   ├── format.ts         # 格式化工具
│   │   ├── validate.ts       # 验证工具
│   │   ├── storage.ts        # 本地存储
│   │   ├── permission.ts     # 权限工具
│   │   └── constants.ts      # 常量定义
│   ├── views/                # 页面组件
│   │   ├── Dashboard/        # 仪表板页面
│   │   │   ├── index.vue
│   │   │   └── components/
│   │   ├── Project/          # 项目管理页面
│   │   │   ├── Board.vue     # 看板视图
│   │   │   ├── List.vue      # 列表视图
│   │   │   └── components/
│   │   ├── Task/             # 任务管理页面
│   │   │   ├── index.vue
│   │   │   └── components/
│   │   ├── Message/          # 消息聊天页面
│   │   │   ├── index.vue
│   │   │   └── components/
│   │   ├── Activity/         # 活动时间线页面
│   │   │   ├── index.vue
│   │   │   └── components/
│   │   └── Auth/             # 认证页面
│   │       ├── Login.vue
│   │       └── Register.vue
│   ├── App.vue               # 根组件
│   └── main.ts               # 应用入口
├── .env                      # 环境变量
├── .env.development          # 开发环境变量
├── .env.production           # 生产环境变量
├── .gitignore
├── index.html
├── package.json
├── tsconfig.json             # TypeScript配置
├── vite.config.ts            # Vite配置
└── README.md
```

## 🔧 技术栈配置

### 核心依赖
```json
{
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.0",
    "pinia": "^2.1.0",
    "element-plus": "^2.4.0",
    "@element-plus/icons-vue": "^2.3.0",
    "echarts": "^5.4.0",
    "vue-echarts": "^6.6.0",
    "vuedraggable": "^4.1.0",
    "@vueuse/core": "^10.5.0",
    "axios": "^1.6.0",
    "dayjs": "^1.11.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "typescript": "^5.2.0",
    "vite": "^5.0.0",
    "sass": "^1.69.0",
    "mockjs": "^1.1.0",
    "vite-plugin-mock": "^3.0.0"
  }
}
```

## 📝 编码规范

### 1. 命名规范
- **文件命名**：PascalCase（组件）、kebab-case（页面）
- **变量命名**：camelCase
- **常量命名**：UPPER_SNAKE_CASE
- **类型命名**：PascalCase，接口以I开头

### 2. Vue组件规范
```vue
<!-- 组件模板示例 -->
<template>
  <div class="component-name">
    <!-- 内容 -->
  </div>
</template>

<script setup lang="ts">
// 1. 导入依赖
import { ref, computed, onMounted } from 'vue'
import type { ComponentProps } from '@/types'

// 2. 定义Props
interface Props {
  title: string
  data?: any[]
}
const props = withDefaults(defineProps<Props>(), {
  data: () => []
})

// 3. 定义Emits
const emit = defineEmits<{
  change: [value: string]
  update: [data: any]
}>()

// 4. 响应式数据
const loading = ref(false)
const list = ref<any[]>([])

// 5. 计算属性
const filteredList = computed(() => {
  return list.value.filter(item => item.active)
})

// 6. 方法定义
/**
 * 处理数据更新
 * @param data 更新的数据
 */
const handleUpdate = (data: any) => {
  emit('update', data)
}

// 7. 生命周期
onMounted(() => {
  // 初始化逻辑
})
</script>

<style lang="scss" scoped>
.component-name {
  // 样式定义
}
</style>
```

### 3. TypeScript规范
```typescript
// 类型定义示例
export interface User {
  id: number
  name: string
  email: string
  avatar?: string
  role: UserRole
  createdAt: string
  updatedAt: string
}

export enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  GUEST = 'guest'
}

export type ApiResponse<T = any> = {
  code: number
  message: string
  data: T
}
```

## 🌐 统一API管理

### API入口配置
```typescript
// src/api/index.ts
import request from './request'
import * as auth from './modules/auth'
import * as dashboard from './modules/dashboard'
import * as project from './modules/project'
import * as task from './modules/task'
import * as message from './modules/message'
import * as activity from './modules/activity'

export const api = {
  auth,
  dashboard,
  project,
  task,
  message,
  activity
}

export { request }
export default api
```

### HTTP请求封装
```typescript
// src/api/request.ts
import axios from 'axios'
import type { AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    const { code, message, data } = response.data
    if (code === 200) {
      return data
    } else {
      ElMessage.error(message || '请求失败')
      return Promise.reject(new Error(message))
    }
  },
  (error) => {
    ElMessage.error(error.message || '网络错误')
    return Promise.reject(error)
  }
)

export default request
```

## 🛠️ 公共工具库

### 工具函数示例
```typescript
// src/utils/date.ts
import dayjs from 'dayjs'

/**
 * 格式化日期
 * @param date 日期
 * @param format 格式
 */
export const formatDate = (date: string | Date, format = 'YYYY-MM-DD HH:mm:ss') => {
  return dayjs(date).format(format)
}

/**
 * 获取相对时间
 * @param date 日期
 */
export const getRelativeTime = (date: string | Date) => {
  return dayjs(date).fromNow()
}

// src/utils/format.ts
/**
 * 格式化文件大小
 * @param size 文件大小（字节）
 */
export const formatFileSize = (size: number): string => {
  const units = ['B', 'KB', 'MB', 'GB']
  let index = 0
  while (size >= 1024 && index < units.length - 1) {
    size /= 1024
    index++
  }
  return `${size.toFixed(2)} ${units[index]}`
}

/**
 * 格式化数字
 * @param num 数字
 */
export const formatNumber = (num: number): string => {
  return num.toLocaleString()
}
```

## 🎭 Mock数据管理

### Mock配置
```typescript
// src/mock/index.ts
import { createProdMockServer } from 'vite-plugin-mock/es/createProdMockServer'
import authMock from './handlers/auth'
import dashboardMock from './handlers/dashboard'
import projectMock from './handlers/project'
import taskMock from './handlers/task'
import messageMock from './handlers/message'
import activityMock from './handlers/activity'

const mockModules = [
  ...authMock,
  ...dashboardMock,
  ...projectMock,
  ...taskMock,
  ...messageMock,
  ...activityMock
]

export function setupProdMockServer() {
  createProdMockServer(mockModules)
}
```

### Mock数据示例
```typescript
// src/mock/data/users.ts
export const mockUsers = [
  {
    id: 1,
    name: 'Rudolph G',
    email: 'rudolph@example.com',
    avatar: '/avatars/rudolph.jpg',
    role: 'Product Designer',
    tasks: 194,
    points: 1230
  },
  {
    id: 2,
    name: 'Anna F',
    email: 'anna@example.com',
    avatar: '/avatars/anna.jpg',
    role: 'Frontend Engineer',
    tasks: 194,
    points: 1230
  }
]

// src/mock/handlers/dashboard.ts
import { MockMethod } from 'vite-plugin-mock'
import { mockUsers } from '../data/users'

export default [
  {
    url: '/api/dashboard/stats',
    method: 'get',
    response: () => {
      return {
        code: 200,
        message: 'success',
        data: {
          totalEmployees: 2.3016,
          totalTasks: 2.3016,
          completedTasks: 2.3016,
          incompleteTasks: 2.3016,
          taskTarget: 10468,
          completionRate: 82
        }
      }
    }
  },
  {
    url: '/api/dashboard/top-employees',
    method: 'get',
    response: () => {
      return {
        code: 200,
        message: 'success',
        data: mockUsers
      }
    }
  }
] as MockMethod[]
```

## ✅ 详细开发计划 TODO

### 🏗️ 阶段一：项目基础搭建（第1-2天）
- [x] 初始化Vue3 + Vite + TypeScript项目
- [x] 配置ESLint、Prettier代码规范
- [x] 安装并配置Element Plus
- [x] 配置Sass/SCSS预处理器
- [x] 设置环境变量配置
- [x] 配置Vite构建优化
- [x] 创建基础目录结构
- [x] 配置路径别名(@符号)

### 🎨 阶段二：基础组件开发（第3-4天）
- [x] 创建Layout布局组件
  - [x] Header头部导航组件
  - [x] Sidebar侧边栏组件
  - [x] 主布局容器组件
- [x] 开发通用组件
  - [x] Avatar头像组件
  - [x] Card卡片组件
  - [x] Loading加载组件
  - [x] Empty空状态组件
  - [x] Modal模态框组件
  - [x] Button按钮组件
  - [x] Form表单组件
- [x] 配置全局样式变量

### 🔧 阶段三：核心功能搭建（第5-6天）
- [x] 配置Vue Router路由
  - [x] 路由定义和配置
  - [x] 路由守卫实现
  - [ ] 动态路由权限
- [x] 配置Pinia状态管理
  - [x] 用户状态管理
  - [x] 认证状态管理
  - [x] 主题状态管理
  - [x] 项目状态管理
  - [x] 任务状态管理
- [x] 封装HTTP请求
  - [x] Axios请求拦截器
  - [x] 响应拦截器
  - [x] 错误处理机制
- [x] 配置Mock数据系统
  - [x] Mock服务器配置
  - [x] Mock数据结构设计

### 📊 阶段四：仪表板页面（第7-8天）
- [x] 创建仪表板页面结构
- [x] 开发统计卡片组件
- [x] 集成ECharts图表库
  - [x] 圆形进度条组件
  - [x] 柱状图组件
  - [x] 饼图组件
- [x] 开发员工排行榜组件
- [x] 实现团队统计组件
- [x] 添加仪表板Mock数据
- [x] 响应式布局适配

### 📋 阶段五：项目看板页面（第9-10天）
- [x] 创建看板页面布局
- [ ] 集成Vue Draggable拖拽功能
- [x] 开发项目卡片组件
  - [x] 卡片基础信息展示
  - [ ] 标签系统
  - [x] 进度指示器
  - [x] 团队成员头像
- [ ] 实现拖拽排序功能
- [x] 添加项目状态管理
- [x] 创建项目Mock数据
- [x] 实现卡片筛选功能

### 📝 阶段六：任务列表页面（第11-12天）
- [x] 创建任务列表页面
- [x] 开发可展开表格组件
- [x] 实现任务状态管理
  - [x] 复选框状态切换
  - [x] 任务优先级显示
  - [x] 任务分组功能
- [x] 添加表格操作功能
  - [x] 排序功能
  - [x] 筛选功能
  - [x] 搜索功能
- [x] 创建任务详情页面
- [x] 添加任务Mock数据
- [ ] 实现批量操作功能

### 💬 阶段七：消息聊天页面（第13-14天）
- [x] 创建聊天页面布局
- [ ] 开发联系人列表组件
- [ ] 开发聊天消息组件
  - [ ] 消息气泡样式
  - [ ] 时间戳显示
  - [ ] 消息状态指示
- [ ] 实现文件上传预览
- [ ] 添加表情选择器
- [ ] 创建消息输入框组件
- [x] 添加聊天Mock数据
- [ ] 实现消息搜索功能

### 📈 阶段八：活动时间线页面（第15-16天）
- [x] 创建活动时间线页面
- [ ] 开发时间线组件
- [ ] 开发活动卡片组件
  - [ ] 活动类型图标
  - [ ] 活动描述信息
  - [ ] 时间显示
- [ ] 实现项目进度条
- [ ] 添加活动筛选功能
- [x] 创建活动Mock数据
- [ ] 实现无限滚动加载

### 🔐 阶段九：认证系统（第17天）
- [x] 创建登录页面
- [ ] 创建注册页面
- [x] 实现表单验证
- [x] 集成认证API
- [x] 实现Token管理
- [x] 添加权限控制
- [x] 创建认证Mock数据

### 🎯 阶段十：优化与完善（第18-21天）
- [ ] 性能优化
  - [ ] 组件懒加载
  - [ ] 图片懒加载
  - [ ] 代码分割
- [ ] 用户体验优化
  - [ ] 加载状态优化
  - [ ] 错误边界处理
  - [ ] 骨架屏实现
- [ ] 响应式适配
  - [ ] 移动端适配
  - [ ] 平板端适配
- [ ] 国际化支持（可选）
- [ ] 单元测试编写
- [ ] 文档完善
- [ ] 部署配置

### 📱 额外功能（可选扩展）
- [ ] PWA支持
- [ ] 暗黑模式
- [ ] 数据导出功能
- [ ] 通知系统
- [ ] 快捷键支持
- [ ] 全文搜索
- [ ] 数据可视化报表

## 🚀 开发启动命令

```bash
# 安装依赖
npm install

# 开发环境启动
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview

# 代码检查
npm run lint

# 代码格式化
npm run format
```

## 📋 开发注意事项

1. **严格遵循TypeScript类型定义**
2. **所有API调用必须使用Mock数据**
3. **组件开发遵循单一职责原则**
4. **保持代码注释的完整性**
5. **定期进行代码Review**
6. **及时更新开发进度**

这份开发文档为Tuscot项目提供了完整的技术架构和开发指南，确保项目能够高质量、高效率地完成开发。