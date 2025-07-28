<template>
  <div class="app-layout">
    <!-- 侧边栏 -->
    <Sidebar :collapsed="sidebarCollapsed" :current-user="currentUser" @toggle="toggleSidebar" />

    <!-- 主内容区 -->
    <div class="layout-main">
      <!-- 顶部导航栏 -->
      <Header :current-user="currentUser" :unread-count="unreadCount" @search="handleSearch"
        @notification-click="showNotifications" @create="handleCreate" @user-action="handleUserAction" />

      <!-- 页面内容 -->
      <main class="layout-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import Sidebar from './Sidebar.vue'
import Header from './Header.vue'
// import { useUserStore } from '@/stores/user'
// import { useNotificationStore } from '@/stores/notification'

// 定义组件名称
defineOptions({ name: 'AppLayout' })

const router = useRouter()
// const userStore = useUserStore()
// const notificationStore = useNotificationStore()

// 响应式数据
const sidebarCollapsed = ref(false)

// 计算属性
const currentUser = computed(() => ({
  id: '1',
  name: 'Admin',
  email: 'admin@example.com',
  avatar: '',
  role: '管理员'
}))
const unreadCount = computed(() => 0)

// 方法
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

/**
 * 处理搜索
 */
const handleSearch = (query: string) => {
  console.log('搜索:', query)
}

const showNotifications = () => {
  // 显示通知面板
  console.log('显示通知')
}

/**
 * 处理新建操作
 */
const handleCreate = (type: string) => {
  console.log('新建:', type)
}

const handleUserAction = (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      // userStore.logout()
      ElMessage.success('已退出登录')
      router.push('/login')
      break
  }
}

// 生命周期
onMounted(() => {
  // 获取当前用户信息
  // userStore.getCurrentUser()
  // 获取通知数量
  // notificationStore.getUnreadCount()
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.app-layout {
  display: flex;
  height: 100vh;
  background-color: $surface-color;
}



.layout-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}



.layout-content {
  flex: 1;
  padding: $spacing-6;
  overflow-y: auto;
  background-color: $surface-color;
}

// 响应式设计
@media (max-width: $breakpoint-md) {
  .layout-main {
    margin-left: 0;
  }
}
</style>