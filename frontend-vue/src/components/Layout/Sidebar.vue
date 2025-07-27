<template>
  <aside class="app-sidebar" :class="{ collapsed: collapsed }">
    <!-- 侧边栏头部 -->
    <div class="sidebar-header">
      <div class="logo">
        <img src="/favicon.ico" alt="Tuscot" class="logo-icon" />
        <span v-show="!collapsed" class="logo-text">Tuscot</span>
      </div>
      <el-button
        type="text"
        class="collapse-btn"
        @click="handleToggle"
      >
        <el-icon><Fold v-if="!collapsed" /><Expand v-else /></el-icon>
      </el-button>
    </div>
    
    <!-- 侧边栏导航 -->
    <nav class="sidebar-nav">
      <el-menu
        :default-active="$route.path"
        :collapse="collapsed"
        :unique-opened="true"
        router
        class="sidebar-menu"
      >
        <!-- 仪表板 -->
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <span>仪表板</span>
        </el-menu-item>
        
        <!-- 项目管理 -->
        <el-sub-menu index="/projects">
          <template #title>
            <el-icon><Folder /></el-icon>
            <span>项目</span>
          </template>
          <el-menu-item index="/projects">项目列表</el-menu-item>
          <el-menu-item index="/projects/board">项目看板</el-menu-item>
        </el-sub-menu>
        
        <!-- 任务管理 -->
        <el-sub-menu index="/tasks">
          <template #title>
            <el-icon><List /></el-icon>
            <span>任务</span>
          </template>
          <el-menu-item index="/tasks">任务列表</el-menu-item>
          <el-menu-item index="/tasks/board">任务看板</el-menu-item>
        </el-sub-menu>
        
        <!-- 消息中心 -->
        <el-menu-item index="/messages">
          <el-icon><ChatDotRound /></el-icon>
          <span>消息</span>
          <el-badge
            v-if="unreadMessageCount > 0"
            :value="unreadMessageCount"
            :max="99"
            class="message-badge"
          />
        </el-menu-item>
        
        <!-- 活动记录 -->
        <el-menu-item index="/activities">
          <el-icon><Clock /></el-icon>
          <span>活动</span>
        </el-menu-item>
        
        <!-- 团队管理 -->
        <el-sub-menu index="/team">
          <template #title>
            <el-icon><UserFilled /></el-icon>
            <span>团队</span>
          </template>
          <el-menu-item index="/team/members">成员管理</el-menu-item>
          <el-menu-item index="/team/roles">角色权限</el-menu-item>
        </el-sub-menu>
        
        <!-- 设置 -->
        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <span>设置</span>
        </el-menu-item>
      </el-menu>
    </nav>
    
    <!-- 侧边栏底部 -->
    <div class="sidebar-footer">
      <div class="user-info" @click="handleUserClick">
        <el-avatar :size="32" :src="currentUser?.avatar">
          {{ getNameInitials(currentUser?.name || 'User') }}
        </el-avatar>
        <div v-show="!collapsed" class="user-details">
          <div class="user-name">{{ currentUser?.name || '用户' }}</div>
          <div class="user-role">{{ currentUser?.role || '成员' }}</div>
        </div>
        <el-icon v-show="!collapsed" class="user-arrow"><ArrowRight /></el-icon>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">

import {
  Odometer,
  Folder,
  List,
  ChatDotRound,
  Clock,
  UserFilled,
  Setting,
  Fold,
  Expand,
  ArrowRight
} from '@element-plus/icons-vue'
import { getNameInitials } from '@/utils'

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
  unreadMessageCount?: number
}

withDefaults(defineProps<Props>(), {
  collapsed: false,
  currentUser: null,
  unreadMessageCount: 0
})

// Emits
interface Emits {
  toggle: []
  userClick: []
}

const emit = defineEmits<Emits>()

/**
 * 处理侧边栏折叠/展开
 */
const handleToggle = () => {
  emit('toggle')
}

/**
 * 处理用户信息点击
 */
const handleUserClick = () => {
  emit('userClick')
}
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.app-sidebar {
  width: $sidebar-width;
  background-color: $background-color;
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
  
  .sidebar-footer {
    border-top: 1px solid $border-color;
    padding: $spacing-3;
    flex-shrink: 0;
    
    .user-info {
      display: flex;
      align-items: center;
      gap: $spacing-2;
      cursor: pointer;
      padding: $spacing-2;
      border-radius: $border-radius-base;
      transition: background-color $transition-base;
      
      &:hover {
        background-color: $gray-50;
      }
      
      .user-details {
        flex: 1;
        min-width: 0;
        
        .user-name {
          font-size: $font-size-sm;
          font-weight: $font-weight-medium;
          color: $text-primary;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        
        .user-role {
          font-size: $font-size-xs;
          color: $text-secondary;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
      }
      
      .user-arrow {
        font-size: 12px;
        color: $text-secondary;
        flex-shrink: 0;
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