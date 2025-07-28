<template>
  <header class="layout-header">
    <div class="header-left">
      <!-- 面包屑导航 -->
      <el-breadcrumb separator="/" class="breadcrumb">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-if="$route.meta.title">{{ $route.meta.title }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="header-center">
      <!-- 搜索框 -->
      <el-input v-model="searchQuery" placeholder="搜索项目、任务、用户..." class="search-input" clearable
        @keyup.enter="handleSearch">
        <template #prefix>
          <el-icon>
            <Search />
          </el-icon>
        </template>
      </el-input>
    </div>

    <div class="header-right">
      <!-- 新建按钮 -->
      <el-dropdown @command="handleCreate">
        <el-button type="primary" class="create-btn">
          <el-icon>
            <Plus />
          </el-icon>
          <span>新建</span>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="project">新建项目</el-dropdown-item>
            <el-dropdown-item command="task">新建任务</el-dropdown-item>
            <el-dropdown-item command="report">新建报告</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>

      <!-- 用户菜单 -->
      <el-dropdown @command="handleUserAction">
        <div class="user-info">
          <el-avatar :size="40" :src="currentUser?.avatar">
            {{ getNameInitials(currentUser?.name || 'User') }}
          </el-avatar>
          <div class="user-details">
            <div class="user-name">{{ currentUser?.name }}</div>
            <div class="user-role">{{ currentUser?.role || '普通用户' }}</div>
          </div>
          <el-icon class="user-arrow">
            <ArrowDown />
          </el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">
              <el-icon>
                <User />
              </el-icon>
              个人资料
            </el-dropdown-item>
            <el-dropdown-item command="settings">
              <el-icon>
                <Setting />
              </el-icon>
              设置
            </el-dropdown-item>
            <el-dropdown-item divided command="logout">
              <el-icon>
                <SwitchButton />
              </el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  Search,
  Plus,
  ArrowDown,
  User,
  Setting,
  SwitchButton
} from '@element-plus/icons-vue'
import { getNameInitials } from '@/utils'
import { defineProps } from 'vue'

// Name
defineOptions({ name: 'AppHeader' })

// Props
interface Props {
  currentUser?: {
    id: string
    name: string
    email: string
    avatar?: string
    role?: string
  } | null
  unreadCount?: number
}

withDefaults(defineProps<Props>(), {
  currentUser: null,
  unreadCount: 0
})

// Emits
interface Emits {
  search: [query: string]
  notificationClick: []
  create: [type: string]
  userAction: [action: string]
}

const emit = defineEmits<Emits>()

const router = useRouter()
const searchQuery = ref('')

/**
 * 处理搜索
 */
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    emit('search', searchQuery.value)
    router.push({
      path: '/search',
      query: { q: searchQuery.value }
    })
  }
}

/**
 * 处理新建操作
 */
const handleCreate = (command: string) => {
  emit('create', command)
  switch (command) {
    case 'project':
      router.push('/projects/create')
      break
    case 'task':
      router.push('/tasks/create')
      break
    case 'team':
      router.push('/team/invite')
      break
  }
}

/**
 * 处理用户操作
 */
const handleUserAction = (command: string) => {
  emit('userAction', command)
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      // 这里应该调用登出逻辑
      router.push('/login')
      break
  }
}
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.layout-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: $topbar-height;
  padding: 0 $spacing-6;
  background-color: white;
  border-bottom: 1px solid $border-color;

  .header-left {
    flex: 1;

    .breadcrumb {
      font-size: $font-size-sm;

      :deep(.el-breadcrumb__item) {
        .el-breadcrumb__inner {
          color: $text-secondary;

          &:hover {
            color: $primary-color;
          }
        }

        &:last-child .el-breadcrumb__inner {
          color: $text-primary;
          font-weight: $font-weight-medium;
        }
      }
    }
  }

  .header-center {
    flex: 2;
    display: flex;
    justify-content: center;

    .search-input {
      width: 300px;
      height: 48px;
      border-radius: 10px;

      :deep(.el-input__wrapper) {
        border-radius: 10px;
        background-color: $gray-50;
        box-shadow: none;
        border: 1px solid transparent;
        transition: all $transition-base;

        &:hover {
          background-color: $background-color;
          border-color: $border-color;
        }

        &.is-focus {
          background-color: $background-color;
          border-color: $primary-color;
          box-shadow: 0 0 0 2px rgba($primary-color, 0.1);
        }
      }

      :deep(.el-input__prefix) {
        color: $text-secondary;
      }
    }
  }

  .header-right {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: $spacing-4;

    .create-btn {
      width: 146px;
      height: 44px;
      display: flex;
      align-items: center;
      gap: $spacing-1;
      border-radius: 14px;
      padding: $spacing-2 $spacing-4;
      font-weight: $font-weight-medium;
      margin-right: 40px;

      &:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba($primary-color, 0.3);
      }
    }

    .user-info {
      min-width: 200px;
      max-width: 240px;
      display: flex;
      align-items: center;
      gap: $spacing-3;
      cursor: pointer;
      padding: $spacing-2;
      border-radius: $border-radius-lg;
      transition: background-color $transition-base;

      &:hover {
        background-color: $gray-50;
      }

      .user-details {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 2px;
        min-width: 0; // 允许flex子项收缩

        .user-name {
          font-size: $font-size-base;
          font-weight: $font-weight-medium;
          color: $text-primary;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          line-height: 1.2;
        }

        .user-role {
          font-size: $font-size-xs;
          color: $text-secondary;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          line-height: 1;
        }
      }

      .user-arrow {
        font-size: 12px;
        color: $text-secondary;
        transition: transform $transition-base;
        flex-shrink: 0;
      }

      &:hover .user-arrow {
        transform: rotate(180deg);
      }
    }
  }
}

// 响应式设计
@media (max-width: $breakpoint-md) {
  .layout-header {
    padding: 0 $spacing-4;

    .header-center {
      display: none;
    }

    .header-right {
      gap: $spacing-2;

      .user-info {
        min-width: auto;
        max-width: 160px;

        .user-details {
          .user-name {
            font-size: $font-size-sm;
          }

          .user-role {
            display: none;
          }
        }
      }
    }
  }
}

@media (max-width: $breakpoint-sm) {
  .layout-header {
    .header-left {
      .breadcrumb {
        :deep(.el-breadcrumb__item) {
          &:not(:last-child) {
            display: none;
          }
        }
      }
    }

    .create-btn {
      span {
        display: none;
      }
    }
  }
}
</style>