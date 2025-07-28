<template>
  <aside class="app-sidebar" :class="{ collapsed: collapsed }">
    <!-- 侧边栏头部 -->
    <div class="sidebar-header">
      <div class="logo">
        <img src="/favicon.ico" alt="TaskAI" class="logo-icon" />
        <span v-show="!collapsed" class="logo-text">TaskAI</span>
      </div>
      <el-button type="text" class="collapse-btn" @click="handleToggle">
        <el-icon>
          <Fold v-if="!collapsed" />
          <Expand v-else />
        </el-icon>
      </el-button>
    </div>

    <!-- 侧边栏导航 -->
    <nav class="sidebar-nav">
      <el-menu :default-active="$route.path" :collapse="collapsed" :unique-opened="true" router class="sidebar-menu">
        <!-- 仪表盘 -->
        <el-menu-item index="/dashboard">
          <el-icon>
            <Odometer />
          </el-icon>
          <span>仪表盘</span>
        </el-menu-item>

        <!-- 项目管理 -->
        <el-menu-item index="/projects">
          <el-icon>
            <Folder />
          </el-icon>
          <span>项目</span>
        </el-menu-item>

        <!-- 任务管理 -->
        <el-menu-item index="/tasks">
          <el-icon>
            <List />
          </el-icon>
          <span>任务</span>
        </el-menu-item>

        <!-- 智能报告 -->
        <el-menu-item index="/reports">
          <el-icon>
            <ChatLineSquare />
          </el-icon>
          <span>报告</span>
        </el-menu-item>

        <!-- 活动记录 -->
        <el-menu-item index="/events">
          <el-icon>
            <BellFilled />
          </el-icon>
          <span>事件</span>
        </el-menu-item>

        <!-- 设置 -->
        <el-menu-item index="/settings">
          <el-icon>
            <Setting />
          </el-icon>
          <span>设置</span>
        </el-menu-item>
      </el-menu>
    </nav>
  </aside>
</template>

<script setup lang="ts">

import {
  Odometer,
  Folder,
  List,
  Setting,
  Fold,
  Expand,
} from '@element-plus/icons-vue'
import { defineOptions } from 'vue'


// Name
defineOptions({
  name: 'AppSidebar'
})

// Props
interface Props {
  collapsed?: boolean
  currentUser?: {
    id: string
    name: string
    email: string
    avatar?: string
    role?: string
  } | null
}

withDefaults(defineProps<Props>(), {
  collapsed: false,
  currentUser: null,
})

// Emits
interface Emits {
  toggle: []
}

const emit = defineEmits<Emits>()

/**
 * 处理侧边栏折叠/展开
 */
const handleToggle = () => {
  emit('toggle')
}

</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.app-sidebar {
  width: $sidebar-width;
  background-color: white;
  border-right: 1px solid $border-color;
  transition: width $transition-base;
  display: flex;
  flex-direction: column;
  height: 100vh;

  &.collapsed {
    width: 64px;
  }

  .sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: $spacing-4;
    border-bottom: 1px solid $border-color;
    flex-shrink: 0;

    .logo {
      display: flex;
      align-items: center;
      gap: $spacing-2;

      .logo-icon {
        width: 24px;
        height: 24px;
        flex-shrink: 0;
      }

      .logo-text {
        font-size: $font-size-lg;
        font-weight: $font-weight-bold;
        color: $primary-color;
        white-space: nowrap;
      }
    }

    .collapse-btn {
      padding: $spacing-1;
      flex-shrink: 0;

      &:hover {
        background-color: $gray-50;
      }
    }
  }

  .sidebar-nav {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;

    .sidebar-menu {
      border: none;

      :deep(.el-menu-item),
      :deep(.el-sub-menu__title) {
        height: 48px;
        line-height: 48px;
        position: relative;

        &:hover {
          background-color: $gray-50;
        }

        &.is-active {
          background-color: rgba($primary-color, 0.1);
          color: $primary-color;

          .el-icon {
            color: $primary-color;
          }

          &::after {
            content: '';
            position: absolute;
            right: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background-color: $primary-color;
          }
        }
      }

      :deep(.el-sub-menu .el-menu-item) {
        height: 40px;
        line-height: 40px;
        padding-left: 48px !important;

        &.is-active {
          background-color: rgba($primary-color, 0.08);

          &::after {
            display: none;
          }
        }
      }

      .message-badge {
        position: absolute;
        top: 12px;
        right: 16px;

        :deep(.el-badge__content) {
          font-size: 10px;
          height: 16px;
          line-height: 16px;
          padding: 0 4px;
          min-width: 16px;
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: $breakpoint-md) {
  .app-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    z-index: $z-fixed;
    transform: translateX(-100%);
    transition: transform $transition-base;

    &.show {
      transform: translateX(0);
    }
  }
}

// 滚动条样式
.sidebar-nav {
  &::-webkit-scrollbar {
    width: 4px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba($text-secondary, 0.3);
    border-radius: 2px;

    &:hover {
      background: rgba($text-secondary, 0.5);
    }
  }
}
</style>