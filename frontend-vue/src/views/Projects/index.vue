<template>
  <div class="projects-index-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">项目管理</h1>
        <p class="page-description">管理和跟踪您的所有项目</p>
      </div>
    </div>

    <!-- 搜索和过滤区域 -->
    <div class="filter-section">
      <div class="filter-controls-row">
        <!-- 左侧：状态过滤和排序选择 -->
        <div class="left-controls">
          <div class="filter-group">
            <el-radio-group v-model="statusFilter" @change="handleFilter">
              <el-radio-button label="all">全部</el-radio-button>
              <el-radio-button label="active">进行中</el-radio-button>
              <el-radio-button label="completed">已完成</el-radio-button>
              <el-radio-button label="overdue">已延期</el-radio-button>
            </el-radio-group>
          </div>
          <div class="sort-group">
            <el-select v-model="sortBy" placeholder="排序方式" @change="handleSort" style="height: 38px;">
              <el-option label="最新创建" value="createdAt" />
              <el-option label="截止时间" value="endDate" />
              <el-option label="项目进度" value="progress" />
            </el-select>
          </div>
        </div>

        <!-- 右侧：搜索框和创建按钮 -->
        <div class="right-controls">
          <div class="search-bar">
            <el-input v-model="searchQuery" placeholder="搜索项目名称、描述或分类..." clearable @input="handleSearch">
              <template #prefix>
                <el-icon>
                  <Search />
                </el-icon>
              </template>
            </el-input>
          </div>
          <div class="create-action">
            <el-button type="primary" @click="handleCreateProject">
              <el-icon>
                <Plus />
              </el-icon>
              创建项目
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 项目列表 -->
    <div class="projects-grid" v-loading="loading">
      <div v-for="project in filteredProjects" :key="project.id" class="project-card"
        @click="handleProjectClick(project.id)">
        <!-- 项目头部 -->
        <div class="project-header">
          <h3 class="project-name">{{ project.name }}</h3>
          <el-dropdown trigger="click">
            <el-button :icon="MoreFilled" text size="small" class="more-button" @click.stop />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click.stop="handleDeleteProject(project.id)">
                  <el-icon>
                    <Delete />
                  </el-icon>
                  删除项目
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>

        <!-- 项目描述 -->
        <div class="project-info">
          <p class="project-description">{{ project.description }}</p>
        </div>



        <!-- 项目进度 -->
        <div class="project-progress">
          <div class="progress-header">
            <span class="progress-label">进度</span>
            <span class="progress-value">{{ Math.round(getAnimatedProgress(project.id)) }}%</span>
          </div>
          <el-progress :percentage="getAnimatedProgress(project.id)" :stroke-width="6"
            :color="getProgressColor(project.progress)" :show-text="false" />
        </div>

        <!-- 项目详情信息 -->
        <div class="project-details">
          <div class="detail-item">
            <el-icon>
              <Calendar />
            </el-icon>
            <span>{{ formatDeadline(project.endDate) }}</span>
          </div>
          <div class="detail-item">
            <el-icon>
              <Document />
            </el-icon>
            <span>{{ project.tasks.length }} 个任务</span>
          </div>
        </div>

        <!-- 项目底部：分类、状态和优先级 -->
        <div class="project-footer">
          <div class="footer-left">
            <el-tag size="small" type="info" class="category-tag">{{ project.category }}</el-tag>
            <span class="status-tag" :class="`status-${project.status}`">
              {{ getStatusText(project.status) }}
            </span>
          </div>
          <div class="footer-right">
            <span class="priority-tag" :class="`priority-${project.priority}`">
              {{ getPriorityText(project.priority) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="!loading && totalFilteredProjects > 0" class="pagination-wrapper">
      <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="totalFilteredProjects"
        layout="total, prev, pager, next, jumper" @current-change="handlePageChange" />
    </div>

    <!-- 空状态 -->
    <div v-if="!loading && totalFilteredProjects === 0" class="empty-state">
      <el-empty description="暂无项目数据">
        <el-button type="primary" @click="handleCreateProject">
          创建第一个项目
        </el-button>
      </el-empty>
    </div>


  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  ElMessage,
  ElMessageBox,
  ElButton,
  ElIcon,
  ElInput,
  ElRadioGroup,
  ElRadioButton,
  ElSelect,
  ElOption,
  ElTag,
  ElEmpty,
  ElPagination,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem
} from 'element-plus'
import {
  Plus,
  Search,
  Calendar,
  Document,
  MoreFilled,
  Delete
} from '@element-plus/icons-vue'
import { projectApi } from '../../api'
import type { Project } from '../../types'
import { formatDate } from '../../utils'

defineOptions({
  name: 'ProjectsIndex'
})

const router = useRouter()

// 响应式数据
const loading = ref(false)
const projects = ref<Project[]>([])
const animatedProgress = ref<Record<string, number>>({})
const searchQuery = ref('')
const statusFilter = ref('all')
const sortBy = ref('createdAt')
const currentPage = ref(1)
const pageSize = ref(8)

/**
 * 获取项目列表数据
 */
const loadProjects = async () => {
  try {
    loading.value = true
    const response = await projectApi.getProjects({
      page: 1,
      size: 100 // 获取所有项目用于前端过滤
    })
    projects.value = response.data

    // 初始化动画进度为0
    const initialProgress: Record<string, number> = {}
    response.data.forEach(project => {
      initialProgress[project.id] = 0
    })
    animatedProgress.value = initialProgress

    // 立即启动动画效果
    animateProgress()
  } catch (error) {
    console.error('获取项目列表失败:', error)
    ElMessage.error('获取项目列表失败')
  } finally {
    loading.value = false
  }
}

/**
 * 过滤和排序后的所有项目列表
 */
const allFilteredProjects = computed(() => {
  let result = [...projects.value]

  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(project =>
      project.name.toLowerCase().includes(query) ||
      project.description.toLowerCase().includes(query) ||
      project.category.toLowerCase().includes(query)
    )
  }

  // 状态过滤
  if (statusFilter.value !== 'all') {
    result = result.filter(project => project.status === statusFilter.value)
  }

  // 排序
  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'createdAt':
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      case 'endDate':
        if (!a.endDate && !b.endDate) return 0
        if (!a.endDate) return 1
        if (!b.endDate) return -1
        return new Date(a.endDate).getTime() - new Date(b.endDate).getTime()
      case 'progress':
        return b.progress - a.progress
      default:
        return 0
    }
  })

  return result
})

/**
 * 过滤后的项目总数
 */
const totalFilteredProjects = computed(() => allFilteredProjects.value.length)

/**
 * 当前页的项目列表
 */
const filteredProjects = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return allFilteredProjects.value.slice(start, end)
})

/**
 * 获取状态文本
 */
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    active: '进行中',
    completed: '已完成',
    overdue: '已延期',
    cancelled: '已取消'
  }
  return statusMap[status] || status
}

/**
 * 获取进度条颜色
 */
const getProgressColor = (progress: number) => {
  if (progress >= 80) return '#67c23a'
  if (progress >= 50) return '#e6a23c'
  return '#f56c6c'
}

/**
 * 格式化截止时间
 */
const formatDeadline = (endDate?: string) => {
  if (!endDate) return '无截止时间'
  const date = new Date(endDate)
  const now = new Date()
  const diffTime = date.getTime() - now.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays < 0) {
    return `已逾期 ${Math.abs(diffDays)} 天`
  } else if (diffDays === 0) {
    return '今日截止'
  } else if (diffDays <= 7) {
    return `${diffDays} 天后截止`
  } else {
    return formatDate(endDate)
  }
}

/**
 * 获取优先级文本
 */
const getPriorityText = (priority: string) => {
  const priorityMap: Record<string, string> = {
    urgent: '紧急',
    high: '高',
    medium: '中',
    low: '低'
  }
  return priorityMap[priority] || priority
}

/**
 * 处理删除项目
 */
const handleDeleteProject = async (projectId: string) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个项目吗？删除后无法恢复。',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await projectApi.deleteProject(projectId)
    ElMessage.success('项目删除成功')
    loadProjects() // 重新加载项目列表
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除项目失败:', error)
      ElMessage.error('删除项目失败')
    }
  }
}

/**
 * 处理搜索
 */
const handleSearch = () => {
  // 搜索逻辑已在计算属性中处理
  currentPage.value = 1 // 重置到第一页
}

/**
 * 处理过滤
 */
const handleFilter = () => {
  // 过滤逻辑已在计算属性中处理
  currentPage.value = 1 // 重置到第一页
}

/**
 * 处理排序
 */
const handleSort = () => {
  // 排序逻辑已在计算属性中处理
  currentPage.value = 1 // 重置到第一页
}

/**
 * 处理项目点击
 */
const handleProjectClick = (projectId: string) => {
  router.push(`/projects/${projectId}`)
}

/**
 * 处理分页变化
 */
const handlePageChange = (page: number) => {
  currentPage.value = page
}

/**
 * 动画更新进度条
 */
const animateProgress = () => {
  projects.value.forEach((project) => {
    const targetProgress = project.progress
    const projectId = project.id

    const animateToTarget = () => {
      const currentProgress = animatedProgress.value[projectId] || 0

      if (currentProgress < targetProgress) {
        // 使用更平滑的增量计算
        const remaining = targetProgress - currentProgress
        const increment = Math.max(0.5, remaining * 0.08) // 每次增加剩余量的8%

        const timer = setInterval(() => {
          const current = animatedProgress.value[projectId] || 0
          if (current >= targetProgress - 0.1) {
            animatedProgress.value[projectId] = targetProgress
            clearInterval(timer)
          } else {
            const newValue = current + increment
            animatedProgress.value[projectId] = Math.min(newValue, targetProgress)
          }
        }, 10) // 增加间隔时间，让动画更平滑
      } else {
        animatedProgress.value[projectId] = targetProgress
      }
    }

    animateToTarget()
  })
}

/**
 * 获取动画进度值
 */
const getAnimatedProgress = (projectId: string) => {
  return animatedProgress.value[projectId] || 0
}

/**
 * 处理创建项目
 */
const handleCreateProject = () => {
  router.push('/projects/create')
}

// 组件挂载时加载数据
onMounted(() => {
  loadProjects()
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.projects-index-page {
  .page-header {
    margin-bottom: $spacing-6;

    .header-content {
      .page-title {
        font-size: $font-size-2xl;
        font-weight: $font-weight-bold;
        color: $text-primary;
        margin: 0 0 $spacing-2 0;
      }

      .page-description {
        font-size: $font-size-base;
        color: $text-secondary;
        margin: 0;
      }
    }
  }

  .filter-section {
    margin-bottom: $spacing-6;

    .filter-controls-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: $spacing-6;
    }

    .left-controls {
      display: flex;
      gap: $spacing-4;
      align-items: center;
      flex-shrink: 0;
    }

    .right-controls {
      display: flex;
      gap: $spacing-4;
      align-items: center;
      flex-shrink: 0;
    }

    .search-bar {
      width: 300px;

      :deep(.el-input) {
        height: 40px;

        .el-input__wrapper {
          border-radius: 6px;
        }
      }
    }

    .create-action {
      .el-button {
        height: 40px;
        padding: 0 $spacing-4;
        border-radius: 6px;
        font-weight: 500;
      }
    }

    .filter-group {
      :deep(.el-radio-group) {
        .el-radio-button {
          margin-right: 0;

          .el-radio-button__inner {
            height: 40px;
            line-height: 38px;
            padding: 0 $spacing-4;
            border-radius: 0;
            font-weight: 500;
          }

          &:first-child .el-radio-button__inner {
            border-top-left-radius: 6px;
            border-bottom-left-radius: 6px;
          }

          &:last-child .el-radio-button__inner {
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
          }
        }
      }
    }

    .sort-group {
      :deep(.el-select) {
        width: 150px;

        .el-select__wrapper {
          min-height: 38px;
          border-radius: 6px;
        }
      }
    }
  }

  .projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: $spacing-6;
    margin-bottom: $spacing-6;

    .project-card {
      background: white;
      border: 1px solid #e4e7ed;
      border-radius: 10px;
      padding: $spacing-6;
      transition: all 0.3s ease;
      cursor: pointer;
      position: relative;

      &:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
      }

      .project-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: $spacing-4;

        .project-name {
          font-size: $font-size-lg;
          font-weight: $font-weight-semibold;
          color: $text-primary;
          margin: 0;
          line-height: 1.4;
          flex: 1;
        }

        .more-button {
          :deep(.el-button) {
            padding: 4px;
            min-height: auto;

            &:hover {
              background: #f5f5f5;
            }
          }
        }
      }

      .project-info {
        margin-bottom: $spacing-4;

        .project-description {
          font-size: $font-size-sm;
          color: $text-secondary;
          margin: 0;
          line-height: 1.5;
          height: calc(1.5em * 2); // 固定两行高度
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
          text-overflow: ellipsis;
        }
      }



      .project-progress {
        margin-bottom: $spacing-4;

        .progress-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: $spacing-2;

          .progress-label {
            font-size: $font-size-sm;
            color: $text-secondary;
          }

          .progress-value {
            font-size: $font-size-sm;
            font-weight: $font-weight-medium;
            color: $text-primary;
          }
        }
      }

      .project-details {
        margin-bottom: $spacing-4;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: $spacing-4;

        .detail-item {
          display: flex;
          align-items: center;
          gap: $spacing-2;
          font-size: $font-size-sm;
          color: $text-secondary;
          flex: 1;

          .el-icon {
            font-size: 14px;
          }
        }
      }

      .project-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: $spacing-2;

        .footer-left {
          display: flex;
          align-items: center;
          gap: $spacing-2;

          .category-tag {
            font-size: 12px;
            height: 24px;
            line-height: 22px;
          }

          .status-tag {
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
            border: 1px solid;
            height: 24px;
            line-height: 20px;
            display: inline-flex;
            align-items: center;

            &.status-active {
              color: #1c7ed6;
              border-color: #1c7ed6;
              background: transparent;
            }

            &.status-completed {
              color: #12b886;
              border-color: #12b886;
              background: transparent;
            }

            &.status-overdue {
              color: #fd7e14;
              border-color: #fd7e14;
              background: transparent;
            }

            &.status-cancelled {
              color: #e03131;
              border-color: #e03131;
              background: transparent;
            }
          }
        }

        .footer-right {
          .priority-tag {
            display: inline-flex;
            align-items: center;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
            height: 24px;
            line-height: 16px;

            &.priority-urgent {
              background: #fef2f2;
              color: #dc2626;
            }

            &.priority-high {
              background: #fef3c7;
              color: #d97706;
            }

            &.priority-medium {
              background: #dbeafe;
              color: #2563eb;
            }

            &.priority-low {
              background: #f0fdf4;
              color: #16a34a;
            }
          }
        }
      }
    }
  }

  .pagination-wrapper {
    display: flex;
    justify-content: flex-end;
    margin-top: $spacing-6;
    padding: $spacing-4 0;

    :deep(.el-pagination) {
      height: 38px;

      .el-pagination__total {
        margin-right: auto;
      }

      .el-pagination__jump {
        height: 38px;

        .el-input {
          height: 38px;

          .el-input__wrapper {
            height: 38px;
            border-radius: 6px;
          }
        }
      }

      // 左按钮边框样式（上、左、下）
      .btn-prev {
        border: 1px solid var(--el-border-color);
        border-right: none;
        border-radius: 6px 0 0 6px;
        width: 38px;
        height: 38px;
      }

      // 右按钮边框样式（上、右、下）
      .btn-next {
        border: 1px solid var(--el-border-color);
        border-left: none;
        border-radius: 0 6px 6px 0;
        width: 38px;
        height: 38px;
      }

      // 中间页码按钮边框样式（上、下）
      .number {
        border-top: 1px solid var(--el-border-color);
        border-bottom: 1px solid var(--el-border-color);
        border-left: none;
        border-right: none;
        border-radius: 0;
        height: 38px;
      }
    }
  }

  .empty-state {
    text-align: center;
    padding: $spacing-8 0;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .projects-index-page {
    padding: $spacing-4;

    .filter-section {
      padding: $spacing-3;
      margin-bottom: $spacing-4;

      .filter-controls-row {
        flex-direction: column;
        align-items: stretch;
        gap: $spacing-3;
      }

      .left-controls,
      .right-controls {
        flex-direction: column;
        align-items: stretch;
        gap: $spacing-3;
      }

      .search-bar {
        width: 100%;

        :deep(.el-input) {
          .el-input__wrapper {
            border-radius: 6px;
          }
        }
      }

      .filter-group,
      .sort-group {
        width: 100%;

        :deep(.el-select) {
          width: 100%;

          .el-input {
            .el-input__wrapper {
              border-radius: 6px;
            }
          }
        }
      }

      .create-action {
        .el-button {
          width: 100%;
          justify-content: center;
        }
      }
    }

    .projects-grid {
      grid-template-columns: 1fr;
      gap: $spacing-4;
    }

    .pagination-wrapper {
      justify-content: center;
      margin-top: $spacing-4;
      padding: $spacing-3 0;

      :deep(.el-pagination) {
        .el-pagination__total {
          margin-right: 0;
          margin-bottom: $spacing-2;
        }

        .el-pager {
          li {
            min-width: 38px;
            height: 38px;
            line-height: 38px;
          }
        }

        .btn-prev,
        .btn-next {
          min-width: 38px;
          height: 38px;
          line-height: 38px;
        }
      }
    }
  }
}
</style>