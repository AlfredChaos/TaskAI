<template>
  <div class="dashboard-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">仪表盘</h1>
        <p class="page-subtitle">欢迎回来，{{ currentUser?.name || 'Admin' }}！</p>
      </div>
      <div class="header-right">
        <div class="current-datetime">
          <div class="date">{{ currentDate }}</div>
          <div class="time">{{ currentTime }}</div>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <!-- 今日任务卡片 -->
      <div class="stat-card today-tasks">
        <div class="stat-icon" :style="{ backgroundColor: stats[0].iconBg }">
          <el-icon color="white">
            <component :is="stats[0].icon" />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">
            <CountUp :end-value="stats[0].completedTasks || 0" />
            <span class="total">/
              <CountUp :end-value="stats[0].totalTasks || 0" />
            </span>
          </div>
          <div class="stat-label">{{ stats[0].label }}</div>
          <div class="stat-details">
            <div class="detail-item">
              <span class="detail-label">已完成任务：</span>
              <span class="detail-value">{{ stats[0].completedTasks || 0 }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">今日待办任务：</span>
              <span class="detail-value">{{ (stats[0].totalTasks || 0) - (stats[0].completedTasks || 0) }}</span>
            </div>
          </div>
          <ProgressBar :completed="stats[0].completedTasks || 0" :total="stats[0].totalTasks || 0" color="#64CBF4" />
        </div>
      </div>

      <!-- 总任务卡片 -->
      <div class="stat-card all-tasks">
        <div class="stat-icon" :style="{ backgroundColor: stats[1].iconBg }">
          <el-icon color="white">
            <component :is="stats[1].icon" />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">
            <CountUp :end-value="stats[1].completedTasks || 0" />
            <span class="total">/
              <CountUp :end-value="stats[1].totalTasks || 0" />
            </span>
          </div>
          <div class="stat-label">{{ stats[1].label }}</div>
          <div class="stat-details">
            <div class="detail-item">
              <span class="detail-label">已完成任务：</span>
              <span class="detail-value">{{ stats[1].completedTasks || 0 }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">待办任务：</span>
              <span class="detail-value">{{ (stats[1].totalTasks || 0) - (stats[1].completedTasks || 0) }}</span>
            </div>
          </div>
          <ProgressBar :completed="stats[1].completedTasks || 0" :total="stats[1].totalTasks || 0" color="#FF9F38" />
        </div>
      </div>

      <!-- 总项目卡片 -->
      <div class="stat-card all-projects">
        <div class="stat-icon" :style="{ backgroundColor: stats[2].iconBg }">
          <el-icon color="white">
            <component :is="stats[2].icon" />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">
            <CountUp :end-value="stats[2].completedProjects || 0" />
            <span class="total">/
              <CountUp :end-value="stats[2].totalProjects || 0" />
            </span>
          </div>
          <div class="stat-label">{{ stats[2].label }}</div>
          <div class="stat-details">
            <div class="detail-item">
              <span class="detail-label">已完成项目：</span>
              <span class="detail-value">{{ stats[2].completedProjects || 0 }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">进行中项目：</span>
              <span class="detail-value">{{ (stats[2].totalProjects || 0) - (stats[2].completedProjects || 0) }}</span>
            </div>
          </div>
          <ProgressBar :completed="stats[2].completedProjects || 0" :total="stats[2].totalProjects || 0"
            color="#E391EA" />
        </div>
      </div>

      <!-- 项目延期比率卡片 -->
      <div class="stat-card overdue-rate">
        <div class="stat-icon" :style="{ backgroundColor: stats[3].iconBg }">
          <el-icon color="white">
            <component :is="stats[3].icon" />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">
            <CountUp :end-value="Math.round(stats[3].percentage || 0)" />
            <span class="unit">%</span>
          </div>
          <div class="stat-label">{{ stats[3].label }}</div>
          <div class="stat-details">
            <div class="detail-item">
              <span class="detail-label">延期项目：</span>
              <span class="detail-value">{{ stats[3].overdueProjects || 0 }}个</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">总项目数：</span>
              <span class="detail-value">{{ projectsTotal || 0 }}个</span>
            </div>
          </div>
          <div class="progress-section">
            <ProgressBar :completed="stats[3].overdueProjects || 0" :total="projectsTotal || 0"
              :color="stats[3].iconBg" />
          </div>
        </div>
      </div>
    </div>

    <!-- 任务看板 -->
    <div class="kanban-board">
      <h2 class="board-title">今日任务看板</h2>
      <div class="kanban-columns">
        <!-- 待办任务列 -->
        <div class="kanban-column" @dragover="onDragOver" @drop="onDrop('pending')">
          <div class="column-header">
            <div class="column-title">
              <span class="title-text">待办</span>
              <span class="task-count">({{ pendingTasks.length }})</span>
            </div>
            <el-button type="primary" :icon="Plus" circle size="small" class="add-task-btn"
              @click="openCreateTaskDialog('pending')" />
          </div>
          <div class="task-list">
            <div v-for="task in pendingTasks" :key="task.id" class="task-card" draggable="true"
              @dragstart="onDragStart(task)" @dragend="onDragEnd">
              <div class="task-header">
                <h4 class="task-title">{{ task.title }}</h4>
                <el-dropdown trigger="click">
                  <el-button :icon="MoreFilled" text size="small" />
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="deleteTask(task)">
                        <el-icon>
                          <Delete />
                        </el-icon>
                        删除任务
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
              <p class="task-description">{{ task.description || '暂无描述' }}</p>
              <div class="task-meta">
                <div class="meta-item">
                  <span class="meta-label">预估工时：</span>
                  <span class="meta-value">{{ task.estimatedHours || 0 }}h</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">剩余工时：</span>
                  <span class="meta-value">{{ task.remainingHours || 0 }}h</span>
                </div>
                <div class="meta-item" v-if="task.dueDate">
                  <span class="meta-label">截止日期：</span>
                  <span class="meta-value">{{ formatDate(task.dueDate) }}</span>
                </div>
              </div>
              <div class="task-priority">
                <el-tag :type="getPriorityType(task.priority)" size="small">
                  {{ task.priority === 'low' ? '低' : task.priority === 'medium' ? '中' : task.priority === 'high' ? '高' :
                    '紧急' }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>

        <!-- 已完成任务列 -->
        <div class="kanban-column" @dragover="onDragOver" @drop="onDrop('completed')">
          <div class="column-header">
            <div class="column-title">
              <span class="title-text">已完成</span>
              <span class="task-count">({{ completedTasks.length }})</span>
            </div>
            <el-button type="success" :icon="Plus" circle size="small" class="add-task-btn"
              @click="openCreateTaskDialog('completed')" />
          </div>
          <div class="task-list">
            <div v-for="task in completedTasks" :key="task.id" class="task-card completed" draggable="true"
              @dragstart="onDragStart(task)" @dragend="onDragEnd">
              <div class="task-header">
                <h4 class="task-title">{{ task.title }}</h4>
                <el-dropdown trigger="click">
                  <el-button :icon="MoreFilled" text size="small" />
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="deleteTask(task)">
                        <el-icon>
                          <Delete />
                        </el-icon>
                        删除任务
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
              <p class="task-description">{{ task.description || '暂无描述' }}</p>
              <div class="task-meta">
                <div class="meta-item">
                  <span class="meta-label">预估工时：</span>
                  <span class="meta-value">{{ task.estimatedHours || 0 }}h</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">剩余工时：</span>
                  <span class="meta-value">{{ task.remainingHours || 0 }}h</span>
                </div>
                <div class="meta-item" v-if="task.dueDate">
                  <span class="meta-label">截止日期：</span>
                  <span class="meta-value">{{ formatDate(task.dueDate) }}</span>
                </div>
              </div>
              <div class="task-priority">
                <el-tag :type="getPriorityType(task.priority)" size="small">
                  {{ task.priority === 'low' ? '低' : task.priority === 'medium' ? '中' : task.priority === 'high' ? '高' :
                    '紧急' }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>

        <!-- 逾期任务列 -->
        <div class="kanban-column" @dragover="onDragOver" @drop="onDrop('overdue')">
          <div class="column-header">
            <div class="column-title">
              <span class="title-text">逾期</span>
              <span class="task-count">({{ overdueTasks.length }})</span>
            </div>
            <el-button type="danger" :icon="Plus" circle size="small" class="add-task-btn"
              @click="openCreateTaskDialog('overdue')" />
          </div>
          <div class="task-list">
            <div v-for="task in overdueTasks" :key="task.id" class="task-card overdue" draggable="true"
              @dragstart="onDragStart(task)" @dragend="onDragEnd">
              <div class="task-header">
                <h4 class="task-title">{{ task.title }}</h4>
                <el-dropdown trigger="click">
                  <el-button :icon="MoreFilled" text size="small" />
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="deleteTask(task)">
                        <el-icon>
                          <Delete />
                        </el-icon>
                        删除任务
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
              <p class="task-description">{{ task.description || '暂无描述' }}</p>
              <div class="task-meta">
                <div class="meta-item">
                  <span class="meta-label">预估工时：</span>
                  <span class="meta-value">{{ task.estimatedHours || 0 }}h</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">剩余工时：</span>
                  <span class="meta-value">{{ task.remainingHours || 0 }}h</span>
                </div>
                <div class="meta-item" v-if="task.dueDate">
                  <span class="meta-label">截止日期：</span>
                  <span class="meta-value">{{ formatDate(task.dueDate) }}</span>
                </div>
              </div>
              <div class="task-priority">
                <el-tag :type="getPriorityType(task.priority)" size="small">
                  {{ task.priority === 'low' ? '低' : task.priority === 'medium' ? '中' : task.priority === 'high' ? '高' :
                    '紧急' }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建任务对话框 -->
    <el-dialog v-model="showCreateTaskDialog" title="创建新任务" width="500px"
      :before-close="() => showCreateTaskDialog = false">
      <el-form :model="createTaskForm" label-width="100px">
        <el-form-item label="任务标题" required>
          <el-input v-model="createTaskForm.title" placeholder="请输入任务标题" />
        </el-form-item>
        <el-form-item label="任务描述">
          <el-input v-model="createTaskForm.description" type="textarea" :rows="3" placeholder="请输入任务描述" />
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="createTaskForm.priority" placeholder="请选择优先级">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
            <el-option label="紧急" value="urgent" />
          </el-select>
        </el-form-item>
        <el-form-item label="截止日期">
          <el-date-picker v-model="createTaskForm.dueDate" type="date" placeholder="请选择截止日期" style="width: 100%" />
        </el-form-item>
        <el-form-item label="预估工时">
          <el-input-number v-model="createTaskForm.estimatedHours" :min="0" :step="0.5" placeholder="预估工时（小时）"
            style="width: 100%" />
        </el-form-item>
        <el-form-item label="剩余工时">
          <el-input-number v-model="createTaskForm.remainingHours" :min="0" :step="0.5" placeholder="剩余工时（小时）"
            style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateTaskDialog = false">取消</el-button>
          <el-button type="primary" @click="createTask">创建</el-button>
        </span>
      </template>
    </el-dialog>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Folder,
  Document,
  WarningFilled,
  Plus,
  MoreFilled,
  Delete
} from '@element-plus/icons-vue'
import { dashboardApi, authApi, taskApi } from '@/api'
import type { DashboardStats, User as UserType, Task, CreateTaskRequest } from '@/api'
import CountUp from '@/components/Common/CountUp.vue'
import ProgressBar from '@/components/Common/ProgressBar.vue'
import { ElMessageBox, ElDialog, ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElDatePicker, ElInputNumber, ElButton } from 'element-plus'

// 组件名称定义
defineOptions({ name: 'DashboardView' })



// 响应式数据
const loading = ref(false)
const currentUser = ref<UserType | null>(null)
const dashboardStats = ref<DashboardStats | null>(null)
const todayTasks = ref<Task[]>([])
const allTasks = ref<Task[]>([])
const showCreateTaskDialog = ref(false)
const createTaskForm = ref<CreateTaskRequest>({
  title: '',
  description: '',
  status: 'pending',
  priority: 'medium',
  projectId: '',
  dueDate: '',
  estimatedHours: 0,
  remainingHours: 0,
  tags: [],
  reporter: currentUser.value!
})
const draggedTask = ref<Task | null>(null)

// 统计数据
const todayCompleted = ref(0)
const todayTotal = ref(0)
const allCompleted = ref(0)
const allTotal = ref(0)
const projectsCompleted = ref(0)
const projectsTotal = ref(0)
const overdueRate = ref(0)

// 任务看板数据
const pendingTasks = computed(() => allTasks.value.filter(task => task.status === 'pending'))
const completedTasks = computed(() => allTasks.value.filter(task => task.status === 'completed'))
const overdueTasks = computed(() => allTasks.value.filter(task => task.status === 'overdue'))

// 当前日期时间
const currentDate = ref('')
const currentTime = ref('')

// 更新当前时间
const updateDateTime = () => {
  const now = new Date()
  currentDate.value = now.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
  currentTime.value = now.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 统计数据
const stats = computed(() => [
  {
    label: '今日任务',
    icon: Document,
    iconBg: '#64CBF4',
    completedTasks: todayCompleted.value || 0,
    totalTasks: todayTotal.value || 0
  },
  {
    label: '总任务',
    icon: Document,
    iconBg: '#FF9F38',
    completedTasks: allCompleted.value || 0,
    totalTasks: allTotal.value || 0
  },
  {
    label: '总项目',
    icon: Folder,
    iconBg: '#E391EA',
    completedProjects: projectsCompleted.value || 0,
    totalProjects: projectsTotal.value || 0
  },
  {
    label: '项目延期比率',
    icon: WarningFilled,
    iconBg: '#6C5DD3',
    percentage: overdueRate.value || 0,
    overdueProjects: Math.round(((overdueRate.value || 0) / 100) * (projectsTotal.value || 0))
  }
])

// API调用方法
const loadDashboardData = async () => {
  try {
    loading.value = true

    // 并行加载所有数据
    const [statsRes, userRes, todayTasksRes, allTasksRes] = await Promise.all([
      dashboardApi.getStats(),
      authApi.getCurrentUser(),
      taskApi.getTodayTasks(),
      taskApi.getTasks()
    ])

    dashboardStats.value = statsRes.data
    currentUser.value = userRes.data
    // 加载今日待办任务
    todayTasks.value = todayTasksRes.data || []
    // 加载所有任务
    allTasks.value = allTasksRes.data?.list || []

    // 更新统计卡片数据
    if (statsRes.data) {
      const data = statsRes.data

      // 更新今日任务数据
      todayCompleted.value = data.completedTasks || 15
      todayTotal.value = (data.completedTasks || 15) + (data.pendingTasks || 5)

      // 更新总任务数据
      allCompleted.value = data.completedTasks || 45
      allTotal.value = (data.completedTasks || 45) + (data.pendingTasks || 23)

      // 更新总项目数据
      projectsCompleted.value = data.completedProjects || 8
      projectsTotal.value = data.totalProjects || 12

      // 更新项目延期比率数据
      const overdueProjects = 2 // 从mock数据推算
      overdueRate.value = (data.totalProjects || 0) > 0
        ? (overdueProjects / (data.totalProjects || 0)) * 100
        : 0
    }


  } catch (error) {
    console.error('加载仪表板数据失败:', error)
    ElMessage.error('加载数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}



// 任务看板方法

/**
 * 打开创建任务对话框
 * @param status 任务状态
 */
const openCreateTaskDialog = (status: Task['status']) => {
  createTaskForm.value = {
    title: '',
    description: '',
    status,
    priority: 'medium',
    projectId: '',
    dueDate: '',
    estimatedHours: 0,
    remainingHours: 0,
    tags: [],
    reporter: currentUser.value!
  }
  showCreateTaskDialog.value = true
}

/**
 * 创建任务
 */
const createTask = async () => {
  try {
    await taskApi.createTask(createTaskForm.value)
    ElMessage.success('任务创建成功')
    showCreateTaskDialog.value = false
    // 重新加载任务数据
    await loadTasksData()
  } catch (error) {
    console.error('创建任务失败:', error)
    ElMessage.error('创建任务失败，请稍后重试')
  }
}

/**
 * 删除任务
 * @param task 要删除的任务
 */
const deleteTask = async (task: Task) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除任务「${task.title}」吗？此操作不可撤销。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await taskApi.deleteTask(task.id)
    ElMessage.success('任务删除成功')
    // 重新加载任务数据
    await loadTasksData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除任务失败:', error)
      ElMessage.error('删除任务失败，请稍后重试')
    }
  }
}

/**
 * 拖拽开始
 * @param task 被拖拽的任务
 */
const onDragStart = (task: Task) => {
  draggedTask.value = task
}

/**
 * 拖拽结束
 */
const onDragEnd = () => {
  draggedTask.value = null
}

/**
 * 拖拽放置
 * @param status 目标状态
 */
const onDrop = async (status: Task['status']) => {
  if (!draggedTask.value || draggedTask.value.status === status) {
    return
  }

  try {
    await taskApi.updateTaskStatus(draggedTask.value.id, status)
    ElMessage.success('任务状态更新成功')
    // 重新加载任务数据
    await loadTasksData()
  } catch (error) {
    console.error('更新任务状态失败:', error)
    ElMessage.error('更新任务状态失败，请稍后重试')
  }
}

/**
 * 允许拖拽放置
 * @param event 拖拽事件
 */
const onDragOver = (event: DragEvent) => {
  event.preventDefault()
}

/**
 * 重新加载任务数据
 */
const loadTasksData = async () => {
  try {
    const allTasksRes = await taskApi.getTasks()
    allTasks.value = allTasksRes.data?.list || []
  } catch (error) {
    console.error('加载任务数据失败:', error)
  }
}

/**
 * 获取优先级对应的标签类型
 * @param priority 优先级
 * @returns Element Plus标签类型
 */
const getPriorityType = (priority: string) => {
  const typeMap: Record<string, string> = {
    high: 'danger',
    medium: 'warning',
    low: 'info',
    urgent: 'danger'
  }
  return typeMap[priority] || 'info'
}

/**
 * 格式化日期
 * @param date 日期字符串
 * @returns 格式化后的日期
 */
const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN')
}









// 生命周期
onMounted(() => {
  loadDashboardData()

  // 初始化时间显示
  updateDateTime()

  // 每秒更新时间
  setInterval(updateDateTime, 1000)
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.dashboard-view {
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

    .header-right {
      .current-datetime {
        text-align: right;

        .date {
          font-size: $font-size-lg;
          font-weight: $font-weight-semibold;
          color: $text-primary;
          margin-bottom: $spacing-1;
        }

        .time {
          font-size: $font-size-base;
          color: $text-secondary;
          font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }
      }
    }
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: $spacing-6;
    margin-bottom: $spacing-8;

    .stat-card {
      display: flex;
      align-items: flex-start;
      padding: $spacing-6;
      background: white;
      border-radius: $border-radius-lg;
      box-shadow: $shadow-sm;
      transition: transform $transition-base, box-shadow $transition-base;

      &:hover {
        transform: translateY(-2px);
        box-shadow: $shadow-md;
      }

      .stat-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: $border-radius-base;
        margin-right: $spacing-4;
        flex-shrink: 0;

        .el-icon {
          font-size: 24px;
          color: white;
        }
      }

      .stat-content {
        flex: 1;
        min-width: 0;

        .stat-value {
          font-size: $font-size-2xl;
          font-weight: $font-weight-bold;
          color: $text-primary;
          margin-bottom: $spacing-1;
          display: flex;
          align-items: baseline;
          gap: 4px;

          .total {
            font-size: $font-size-base;
            color: $text-secondary;
            font-weight: normal;
          }
        }

        .stat-label {
          font-size: $font-size-sm;
          color: $text-secondary;
          margin-bottom: $spacing-2;
        }

        .stat-details {
          margin-bottom: $spacing-3;

          .detail-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: $spacing-1;

            &:last-child {
              margin-bottom: 0;
            }

            .detail-label {
              font-size: $font-size-xs;
              color: $text-secondary;
            }

            .detail-value {
              font-size: $font-size-xs;
              color: $text-primary;
              font-weight: $font-weight-medium;
            }
          }
        }

        .stat-date {
          font-size: $font-size-xs;
          color: $text-secondary;
          margin-bottom: $spacing-3;
        }
      }

      &.overdue-rate {
        .stat-value {
          .unit {
            font-size: $font-size-lg;
            color: $text-secondary;
            font-weight: normal;
            margin-left: 2px;
          }
        }

        .progress-section {
          margin-top: $spacing-3;
        }
      }
    }
  }

  // 任务看板样式
  .kanban-board {
    margin-top: $spacing-8;

    .board-title {
      margin: 0 0 $spacing-6 0;
      font-size: $font-size-xl;
      font-weight: $font-weight-bold;
      color: $text-primary;
    }

    .kanban-columns {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: $spacing-6;
      min-height: 600px;
    }

    .kanban-column {

      border-radius: $border-radius-lg;
      padding: $spacing-4;
      min-height: 100%;

      .column-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: $spacing-4;
        padding-bottom: $spacing-3;
        border-bottom: 2px solid #e9ecef;

        .column-title {
          display: flex;
          align-items: center;
          gap: $spacing-2;

          .title-text {
            font-size: $font-size-lg;
            font-weight: $font-weight-semibold;
            color: $text-primary;
          }

          .task-count {
            font-size: $font-size-sm;
            color: $text-secondary;
            font-weight: normal;
          }
        }

        .add-task-btn {
          opacity: 0.7;
          transition: opacity $transition-base;

          &:hover {
            opacity: 1;
          }
        }
      }

      .task-list {
        display: flex;
        flex-direction: column;
        gap: $spacing-3;
        min-height: 500px;
      }

      .task-card {
        background: white;
        border-radius: $border-radius-base;
        padding: $spacing-4;
        box-shadow: $shadow-sm;
        cursor: grab;
        transition: transform $transition-base, box-shadow $transition-base;

        &:hover {
          transform: translateY(-2px);
          box-shadow: $shadow-md;
        }

        &:active {
          cursor: grabbing;
        }

        &.completed {
          border-left-color: #67C23A;
          opacity: 0.8;

          .task-title {
            text-decoration: line-through;
            color: $text-secondary;
          }
        }

        &.overdue {
          border-left-color: #F56C6C;
          background: #fef0f0;
        }

        .task-header {
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
          margin-bottom: $spacing-2;

          .task-title {
            margin: 0;
            font-size: $font-size-base;
            font-weight: $font-weight-semibold;
            color: $text-primary;
            line-height: 1.4;
            flex: 1;
            margin-right: $spacing-2;
          }
        }

        .task-description {
          margin: 0 0 $spacing-3 0;
          font-size: $font-size-sm;
          color: $text-secondary;
          line-height: 1.5;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }

        .task-meta {
          margin-bottom: $spacing-3;

          .meta-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: $spacing-1;
            font-size: $font-size-xs;

            &:last-child {
              margin-bottom: 0;
            }

            .meta-label {
              color: $text-secondary;
            }

            .meta-value {
              color: $text-primary;
              font-weight: $font-weight-medium;
            }
          }
        }

        .task-priority {
          display: flex;
          justify-content: flex-end;
        }
      }

      // 拖拽时的样式
      &.drag-over {
        background: #e3f2fd;
        border: 2px dashed #2196f3;
      }
    }
  }

}

@media (max-width: $breakpoint-md) {
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }

  .kanban-board {
    .kanban-columns {
      grid-template-columns: 1fr;
      gap: $spacing-4;
    }

    .kanban-column {
      .task-list {
        min-height: auto;
      }
    }
  }
}
</style>