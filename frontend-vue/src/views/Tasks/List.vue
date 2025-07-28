<template>
  <div class="task-list-view">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">任务管理</h1>
        <p class="page-subtitle">跟踪和管理您的所有任务</p>
      </div>
      <div class="header-right">
        <el-button type="primary" @click="createTask">
          <el-icon><Plus /></el-icon>
          新建任务
        </el-button>
      </div>
    </div>
    
    <!-- 筛选和搜索 -->
    <div class="filter-section">
      <div class="filter-left">
        <el-input
          v-model="searchQuery"
          placeholder="搜索任务标题、描述..."
          class="search-input"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      
      <div class="filter-right">
        <el-select v-model="statusFilter" placeholder="状态" clearable style="width: 120px">
          <el-option label="全部" value="" />
          <el-option label="待办" value="todo" />
          <el-option label="进行中" value="in-progress" />
          <el-option label="审核中" value="review" />
          <el-option label="已完成" value="done" />
        </el-select>
        
        <el-select v-model="priorityFilter" placeholder="优先级" clearable style="width: 120px">
          <el-option label="全部" value="" />
          <el-option label="紧急" value="urgent" />
          <el-option label="高" value="high" />
          <el-option label="中" value="medium" />
          <el-option label="低" value="low" />
        </el-select>
        
        <el-select v-model="projectFilter" placeholder="项目" clearable style="width: 150px">
          <el-option label="全部项目" value="" />
          <el-option
            v-for="project in projects"
            :key="project.id"
            :label="project.name"
            :value="project.id"
          />
        </el-select>
        
        <el-select v-model="sortBy" style="width: 140px">
          <el-option label="最新创建" value="created_desc" />
          <el-option label="最早创建" value="created_asc" />
          <el-option label="截止日期" value="due_date" />
          <el-option label="优先级" value="priority" />
          <el-option label="状态" value="status" />
        </el-select>
        
        <el-button-group>
          <el-button :type="viewMode === 'list' ? 'primary' : 'default'" @click="viewMode = 'list'">
            <el-icon><List /></el-icon>
          </el-button>
          <el-button :type="viewMode === 'board' ? 'primary' : 'default'" @click="viewMode = 'board'">
            <el-icon><Grid /></el-icon>
          </el-button>
        </el-button-group>
      </div>
    </div>
    
    <!-- 任务内容 -->
    <div class="tasks-container" v-loading="loading">
      <!-- 列表视图 -->
      <div v-if="viewMode === 'list'" class="tasks-table">
        <el-table :data="paginatedTasks" @row-click="viewTask">
          <el-table-column type="selection" width="55" />
          
          <el-table-column label="任务" min-width="250">
            <template #default="{ row }">
              <div class="task-info">
                <div class="task-title">
                  <el-tag
                    :type="getPriorityType(row.priority)"
                    size="small"
                    class="priority-tag"
                  >
                    {{ getPriorityText(row.priority) }}
                  </el-tag>
                  <span class="title-text">{{ row.title }}</span>
                </div>
                <div class="task-description">{{ row.description }}</div>
                <div class="task-tags">
                  <el-tag
                    v-for="tag in row.tags"
                    :key="tag"
                    size="small"
                    type="info"
                    class="tag-item"
                  >
                    {{ tag }}
                  </el-tag>
                </div>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="负责人" width="120">
            <template #default="{ row }">
              <div v-if="row.assignee" class="assignee-info">
                <el-avatar :size="24" :src="row.assignee.avatar">
                  {{ row.assignee.name.charAt(0) }}
                </el-avatar>
                <span class="assignee-name">{{ row.assignee.name }}</span>
              </div>
              <span v-else class="no-assignee">未分配</span>
            </template>
          </el-table-column>
          
          <el-table-column label="项目" width="150">
            <template #default="{ row }">
              <span class="project-name">{{ getProjectName(row.projectId) }}</span>
            </template>
          </el-table-column>
          
          <el-table-column label="截止日期" width="120">
            <template #default="{ row }">
              <span v-if="row.dueDate" :class="getDueDateClass(row.dueDate)">
                {{ formatDate(row.dueDate) }}
              </span>
              <span v-else class="no-due-date">无</span>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="80" fixed="right">
            <template #default="{ row }">
              <el-dropdown @command="handleTaskAction">
                <el-button type="text" size="small">
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :command="{ action: 'edit', task: row }">
                      编辑任务
                    </el-dropdown-item>
                    <el-dropdown-item :command="{ action: 'duplicate', task: row }">
                      复制任务
                    </el-dropdown-item>
                    <el-dropdown-item divided :command="{ action: 'delete', task: row }">
                      删除任务
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <!-- 看板视图 -->
      <div v-else class="tasks-board">
        <div class="board-columns">
          <div
            v-for="status in taskStatuses"
            :key="status.value"
            class="board-column"
          >
            <div class="column-header">
              <div class="column-title">
                <el-tag :type="status.type" size="small">{{ status.label }}</el-tag>
                <span class="task-count">({{ getTasksByStatus(status.value).length }})</span>
              </div>
            </div>
            
            <div class="column-content">
              <div
                v-for="task in getTasksByStatus(status.value)"
                :key="task.id"
                class="task-card"
                @click="viewTask(task.id)"
              >
                <div class="card-header">
                  <el-tag
                    :type="getPriorityType(task.priority)"
                    size="small"
                    class="priority-tag"
                  >
                    {{ getPriorityText(task.priority) }}
                  </el-tag>
                  <el-dropdown @command="handleTaskAction">
                    <el-button type="text" size="small" @click.stop>
                      <el-icon><MoreFilled /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item :command="{ action: 'edit', task }">
                          编辑任务
                        </el-dropdown-item>
                        <el-dropdown-item :command="{ action: 'duplicate', task }">
                          复制任务
                        </el-dropdown-item>
                        <el-dropdown-item divided :command="{ action: 'delete', task }">
                          删除任务
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
                
                <div class="card-content">
                  <h4 class="task-title">{{ task.title }}</h4>
                  <p class="task-description">{{ task.description }}</p>
                  
                  <div class="task-tags">
                    <el-tag
                      v-for="tag in task.tags.slice(0, 2)"
                      :key="tag"
                      size="small"
                      type="info"
                      class="tag-item"
                    >
                      {{ tag }}
                    </el-tag>
                    <span v-if="task.tags.length > 2" class="more-tags">
                      +{{ task.tags.length - 2 }}
                    </span>
                  </div>
                </div>
                
                <div class="card-footer">
                  <div class="task-meta">
                    <span class="project-name">{{ getProjectName(task.projectId) }}</span>
                    <span v-if="task.dueDate" :class="getDueDateClass(task.dueDate)">
                      {{ formatDate(task.dueDate) }}
                    </span>
                  </div>
                  
                  <div class="task-assignee">
                    <el-avatar v-if="task.assignee" :size="24" :src="task.assignee.avatar">
                      {{ task.assignee.name.charAt(0) }}
                    </el-avatar>
                    <div v-else class="no-assignee-avatar">
                      <el-icon><User /></el-icon>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-if="filteredTasks.length === 0 && !loading" class="empty-state">
        <div class="empty-icon">
          <el-icon><List /></el-icon>
        </div>
        <h3 class="empty-title">暂无任务</h3>
        <p class="empty-description">
          {{ searchQuery ? '没有找到匹配的任务' : '开始创建您的第一个任务吧' }}
        </p>
        <el-button v-if="!searchQuery" type="primary" @click="createTask">
          创建任务
        </el-button>
      </div>
    </div>
    
    <!-- 分页 (仅列表视图) -->
    <div v-if="viewMode === 'list' && filteredTasks.length > 0" class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[20, 50, 100]"
        :total="filteredTasks.length"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Search,
  List,
  Grid,
  User,
  MoreFilled
} from '@element-plus/icons-vue'
import { formatDate } from '@/utils'
import { taskApi, projectApi } from '@/api'
import type { Task, Project } from '@/api'

// 组件名称定义
defineOptions({ name: 'TaskListView' })

const router = useRouter()

// 响应式数据
const loading = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const priorityFilter = ref('')
const projectFilter = ref('')
const sortBy = ref('created_desc')
const viewMode = ref<'list' | 'board'>('list')
const currentPage = ref(1)
const pageSize = ref(20)

// 任务状态配置
const taskStatuses = [
  { value: 'todo', label: '待办', type: 'info' },
  { value: 'in-progress', label: '进行中', type: 'primary' },
  { value: 'review', label: '审核中', type: 'warning' },
  { value: 'done', label: '已完成', type: 'success' }
]

// 响应式数据
const projects = ref<Project[]>([])

const tasks = ref<Task[]>([])

/**
 * 加载任务列表数据
 */
const loadTasks = async () => {
  try {
    loading.value = true
    const response = await taskApi.getTasks({
      page: currentPage.value,
      pageSize: pageSize.value,
      search: searchQuery.value,
      status: statusFilter.value,
      priority: priorityFilter.value,
      projectId: projectFilter.value
    })
    tasks.value = response.data.items
  } catch (error) {
    console.error('加载任务列表失败:', error)
    ElMessage.error('加载任务列表失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

/**
 * 加载项目列表数据
 */
const loadProjects = async () => {
  try {
    const response = await projectApi.getProjects()
    projects.value = response.data.items
  } catch (error) {
    console.error('加载项目列表失败:', error)
  }
}

// 计算属性
const filteredTasks = computed(() => {
  let result = tasks.value
  
  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(task => 
      task.title.toLowerCase().includes(query) ||
      (task.description && task.description.toLowerCase().includes(query))
    )
  }
  
  // 状态过滤
  if (statusFilter.value) {
    result = result.filter(task => task.status === statusFilter.value)
  }
  
  // 优先级过滤
  if (priorityFilter.value) {
    result = result.filter(task => task.priority === priorityFilter.value)
  }
  
  // 项目过滤
  if (projectFilter.value) {
    result = result.filter(task => task.projectId === projectFilter.value)
  }
  
  // 排序
  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'created_desc':
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      case 'created_asc':
        return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      case 'due_date':
        if (!a.dueDate && !b.dueDate) return 0
        if (!a.dueDate) return 1
        if (!b.dueDate) return -1
        return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime()
      case 'priority':
        const priorityOrder = { urgent: 4, high: 3, medium: 2, low: 1 }
        return priorityOrder[b.priority] - priorityOrder[a.priority]
      case 'status':
        const statusOrder = { todo: 1, 'in-progress': 2, review: 3, done: 4 }
        return statusOrder[a.status] - statusOrder[b.status]
      default:
        return 0
    }
  })
  
  return result
})

const paginatedTasks = computed(() => {
  if (viewMode.value === 'board') return filteredTasks.value
  
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredTasks.value.slice(start, end)
})

// 方法
const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    todo: 'info',
    'in-progress': 'primary',
    review: 'warning',
    done: 'success'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    todo: '待办',
    'in-progress': '进行中',
    review: '审核中',
    done: '已完成'
  }
  return statusMap[status] || '未知'
}

const getPriorityType = (priority: string) => {
  const priorityMap: Record<string, string> = {
    urgent: 'danger',
    high: 'warning',
    medium: 'primary',
    low: 'info'
  }
  return priorityMap[priority] || 'info'
}

const getPriorityText = (priority: string) => {
  const priorityMap: Record<string, string> = {
    urgent: '紧急',
    high: '高',
    medium: '中',
    low: '低'
  }
  return priorityMap[priority] || '未知'
}

const getProjectName = (projectId: string) => {
  const project = projects.value.find(p => p.id === projectId)
  return project?.name || '未知项目'
}

const getDueDateClass = (dueDate: string) => {
  const due = new Date(dueDate)
  const now = new Date()
  const diffDays = Math.ceil((due.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'overdue'
  if (diffDays <= 3) return 'due-soon'
  return 'due-normal'
}

const getTasksByStatus = (status: string) => {
  return filteredTasks.value.filter(task => task.status === status)
}

const handleSearch = () => {
  currentPage.value = 1
  loadTasks()
}

const createTask = () => {
  router.push('/tasks/create')
}

const viewTask = (taskId: string | Task) => {
  const id = typeof taskId === 'string' ? taskId : taskId.id
  router.push(`/tasks/${id}`)
}

const handleTaskAction = async (command: { action: string; task: Task }) => {
  const { action, task } = command
  
  switch (action) {
    case 'edit':
      router.push(`/tasks/${task.id}/edit`)
      break
    case 'duplicate':
      ElMessage.info('复制功能开发中')
      break
    case 'delete':
      try {
        await ElMessageBox.confirm(
          `确定要删除任务 "${task.title}" 吗？此操作不可恢复。`,
          '删除确认',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        // 执行删除操作
        await taskApi.deleteTask(task.id)
        ElMessage.success('任务删除成功')
        // 重新加载任务列表
        await loadTasks()
      } catch (error: unknown) {
        if (error !== 'cancel') {
          console.error('删除任务失败:', error)
          ElMessage.error('删除任务失败，请稍后重试')
        }
      }
      break
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadTasks()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  loadTasks()
}

// 生命周期
onMounted(() => {
  loadTasks()
  loadProjects()
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.task-list-view {
  .page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: $spacing-6;
    
    .header-left {
      .page-title {
        margin: 0 0 $spacing-2 0;
        font-size: $font-size-2xl;
        font-weight: $font-weight-bold;
        color: $text-primary;
      }
      
      .page-subtitle {
        margin: 0;
        font-size: $font-size-base;
        color: $text-secondary;
      }
    }
  }
  
  .filter-section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: $spacing-6;
    
    .filter-left {
      .search-input {
        width: 300px;
      }
    }
    
    .filter-right {
      display: flex;
      align-items: center;
      gap: $spacing-3;
    }
  }
  
  .tasks-container {
    min-height: 400px;
    
    .tasks-table {
      background: $background-color;
      border-radius: $border-radius-lg;
      overflow: hidden;
      
      .task-info {
        .task-title {
          display: flex;
          align-items: center;
          gap: $spacing-2;
          margin-bottom: $spacing-1;
          
          .priority-tag {
            flex-shrink: 0;
          }
          
          .title-text {
            font-weight: $font-weight-medium;
            color: $text-primary;
          }
        }
        
        .task-description {
          font-size: $font-size-sm;
          color: $text-secondary;
          margin-bottom: $spacing-2;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }
        
        .task-tags {
          display: flex;
          gap: $spacing-1;
          flex-wrap: wrap;
          
          .tag-item {
            font-size: $font-size-xs;
          }
        }
      }
      
      .assignee-info {
        display: flex;
        align-items: center;
        gap: $spacing-2;
        
        .assignee-name {
          font-size: $font-size-sm;
        }
      }
      
      .no-assignee {
        font-size: $font-size-sm;
        color: $text-disabled;
      }
      
      .project-name {
        font-size: $font-size-sm;
        color: $text-secondary;
      }
      
      .overdue {
        color: $danger-color;
        font-weight: $font-weight-medium;
      }
      
      .due-soon {
        color: $warning-color;
        font-weight: $font-weight-medium;
      }
      
      .due-normal {
        color: $text-secondary;
      }
      
      .no-due-date {
        color: $text-disabled;
        font-size: $font-size-sm;
      }
    }
    
    .tasks-board {
      .board-columns {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: $spacing-6;
        
        .board-column {
          background: $surface-color;
          border-radius: $border-radius-lg;
          padding: $spacing-4;
          
          .column-header {
            margin-bottom: $spacing-4;
            
            .column-title {
              display: flex;
              align-items: center;
              gap: $spacing-2;
              
              .task-count {
                font-size: $font-size-sm;
                color: $text-secondary;
              }
            }
          }
          
          .column-content {
            .task-card {
              background: $background-color;
              border-radius: $border-radius-base;
              padding: $spacing-4;
              margin-bottom: $spacing-3;
              box-shadow: $shadow-sm;
              cursor: pointer;
              transition: all $transition-base;
              
              &:hover {
                transform: translateY(-2px);
                box-shadow: $shadow-md;
              }
              
              .card-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: $spacing-3;
                
                .priority-tag {
                  font-size: $font-size-xs;
                }
              }
              
              .card-content {
                margin-bottom: $spacing-3;
                
                .task-title {
                  margin: 0 0 $spacing-2 0;
                  font-size: $font-size-base;
                  font-weight: $font-weight-medium;
                  color: $text-primary;
                  line-height: 1.4;
                }
                
                .task-description {
                  margin: 0 0 $spacing-3 0;
                  font-size: $font-size-sm;
                  color: $text-secondary;
                  line-height: 1.4;
                  display: -webkit-box;
                  -webkit-line-clamp: 2;
                  -webkit-box-orient: vertical;
                  overflow: hidden;
                }
                
                .task-tags {
                  display: flex;
                  gap: $spacing-1;
                  align-items: center;
                  
                  .tag-item {
                    font-size: $font-size-xs;
                  }
                  
                  .more-tags {
                    font-size: $font-size-xs;
                    color: $text-secondary;
                  }
                }
              }
              
              .card-footer {
                display: flex;
                align-items: center;
                justify-content: space-between;
                
                .task-meta {
                  display: flex;
                  flex-direction: column;
                  gap: $spacing-1;
                  
                  .project-name {
                    font-size: $font-size-xs;
                    color: $text-secondary;
                  }
                  
                  .overdue {
                    color: $danger-color;
                    font-weight: $font-weight-medium;
                    font-size: $font-size-xs;
                  }
                  
                  .due-soon {
                    color: $warning-color;
                    font-weight: $font-weight-medium;
                    font-size: $font-size-xs;
                  }
                  
                  .due-normal {
                    color: $text-secondary;
                    font-size: $font-size-xs;
                  }
                }
                
                .task-assignee {
                  .no-assignee-avatar {
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    background: $gray-200;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    
                    .el-icon {
                      font-size: 12px;
                      color: $text-disabled;
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    
    .empty-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: $spacing-12 $spacing-6;
      text-align: center;
      
      .empty-icon {
        margin-bottom: $spacing-4;
        
        .el-icon {
          font-size: 64px;
          color: $text-disabled;
        }
      }
      
      .empty-title {
        margin: 0 0 $spacing-2 0;
        font-size: $font-size-lg;
        color: $text-primary;
      }
      
      .empty-description {
        margin: 0 0 $spacing-6 0;
        font-size: $font-size-base;
        color: $text-secondary;
      }
    }
  }
  
  .pagination-container {
    display: flex;
    justify-content: center;
    margin-top: $spacing-8;
  }
}

// 响应式设计
@media (max-width: $breakpoint-xl) {
  .board-columns {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: $breakpoint-lg) {
  .board-columns {
    grid-template-columns: 1fr !important;
  }
}

@media (max-width: $breakpoint-md) {
  .filter-section {
    flex-direction: column;
    gap: $spacing-4;
    align-items: stretch;
    
    .filter-left {
      .search-input {
        width: 100%;
      }
    }
    
    .filter-right {
      justify-content: space-between;
      flex-wrap: wrap;
    }
  }
}

@media (max-width: $breakpoint-sm) {
  .page-header {
    flex-direction: column;
    gap: $spacing-4;
    align-items: stretch;
  }
}
</style>