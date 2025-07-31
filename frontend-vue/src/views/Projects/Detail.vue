<template>
  <div class="project-detail-page">
    <!-- 返回按钮 -->
    <div class="back-navigation">
      <el-button type="text" @click="goBack" class="back-button">
        <el-icon>
          <ArrowLeft />
        </el-icon>
        返回项目列表
      </el-button>
    </div>

    <div v-if="project" class="project-detail-content">
      <!-- 项目头部信息 -->
      <div class="project-header">
        <div class="project-title-section">
          <h1 class="project-title">{{ project.name }}</h1>
          <div class="project-tags">
            <span class="status-tag" :class="`status-${project.status}`">
              {{ getStatusText(project.status) }}
            </span>
          </div>
        </div>
      </div>

      <!-- 项目元信息 -->
      <div class="project-meta-section">
        <div class="meta-item">
          <div class="meta-label">创建日期</div>
          <div class="meta-value">{{ formatDateYMD(project.createdAt || '') }}</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">截止日期</div>
          <div class="meta-value">{{ formatDateYMD(project.endDate || '') }}</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">分类</div>
          <div class="meta-value">{{ project.category }}</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">优先级</div>
          <div class="meta-value">
            <span class="priority-tag" :class="`priority-${project.priority}`">
              {{ getPriorityText(project.priority) }}
            </span>
          </div>
        </div>
      </div>

      <!-- 项目进度卡片 -->
      <div class="progress-card">
        <div class="progress-header">
          <h3 class="progress-title">项目进度</h3>
          <div class="progress-info">
            <div class="progress-item">
              <span class="progress-percentage">{{ Math.round(animatedProgress) }}%</span>
              <span class="progress-label">完成度</span>
            </div>
            <div class="progress-item">
              <span class="progress-percentage progress-tasks">{{ Math.round(animatedCompletedTasks) }}/{{
                Math.round(animatedTotalTasks) }}</span>
              <span class="progress-label">任务完成</span>
            </div>
          </div>
        </div>
        <div class="progress-content">
          <div class="progress-bar-section">
            <el-progress :percentage="animatedProgress" :stroke-width="8" :show-text="false"
              :color="getProgressColor(animatedProgress)" />
          </div>
          <div class="progress-stats">
            <div class="stat-item stat-total">
              <div class="stat-header">
                <span class="stat-label">任务总数</span>
                <div class="stat-icon">
                  <el-icon>
                    <List />
                  </el-icon>
                </div>
              </div>
              <div class="stat-number">{{ Math.round(animatedTotalTasks) }}</div>
            </div>
            <div class="stat-item stat-completed">
              <div class="stat-header">
                <span class="stat-label">已完成</span>
                <div class="stat-icon">
                  <el-icon>
                    <SuccessFilled />
                  </el-icon>
                </div>
              </div>
              <div class="stat-number">{{ Math.round(animatedCompletedTasks) }}</div>
            </div>
            <div class="stat-item stat-pending">
              <div class="stat-header">
                <span class="stat-label">待办</span>
                <div class="stat-icon">
                  <el-icon>
                    <SwitchFilled />
                  </el-icon>
                </div>
              </div>
              <div class="stat-number">{{ Math.round(animatedPendingTasks) }}</div>
            </div>
            <div class="stat-item stat-overdue">
              <div class="stat-header">
                <span class="stat-label">逾期</span>
                <div class="stat-icon">
                  <el-icon>
                    <WarnTriangleFilled />
                  </el-icon>
                </div>
              </div>
              <div class="stat-number">{{ Math.round(animatedOverdueTasks) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 项目详情和时间线 -->
      <div class="content-section">
        <!-- 左侧：项目详情 -->
        <div class="project-description">
          <h3>项目详情</h3>
          <div class="markdown-content" v-html="renderMarkdown(project.description)">
          </div>
        </div>

        <!-- 右侧：项目时间线 -->
        <div class="timeline-section">
          <h3>项目时间线</h3>
          <div v-if="timeline.length === 0" class="empty-state">
            <el-empty description="暂无时间线" />
          </div>
          <el-timeline v-else class="project-timeline" style="max-width: 600px;">
            <el-timeline-item v-for="node in timeline" :key="node.id" :timestamp="formatDateTime(node.date)"
              :type="node.isMilestone ? 'primary' : 'info'" :size="node.isMilestone ? 'large' : 'normal'"
              placement="top">
              <div class="timeline-content">
                <div class="timeline-header">
                  <span class="timeline-title">{{ node.title }}</span>
                  <el-button :type="node.isMilestone ? 'warning' : 'primary'" size="small" link
                    @click="toggleMilestone(node)">
                    <el-icon>
                      <Star />
                    </el-icon>
                  </el-button>
                </div>
                <p v-if="node.description" class="timeline-description">
                  {{ node.description }}
                </p>
              </div>
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>

      <!-- 任务列表卡片 -->
      <div class="tasks-card">
        <div class="tasks-header">
          <h3>任务列表</h3>
          <el-button type="primary" @click="showAddTaskDialog = true">
            <el-icon>
              <Plus />
            </el-icon>
            添加任务
          </el-button>
        </div>

        <!-- 任务过滤和搜索 -->
        <div class="tasks-controls">
          <el-radio-group v-model="taskFilter" @change="handleTaskFilter">
            <el-radio-button label="all">全部</el-radio-button>
            <el-radio-button label="pending">待办</el-radio-button>
            <el-radio-button label="completed">已完成</el-radio-button>
            <el-radio-button label="overdue">已逾期</el-radio-button>
          </el-radio-group>
          <el-input v-model="taskSearch" placeholder="搜索任务名称或描述" clearable style="width: 300px;">
            <template #prefix>
              <el-icon>
                <Search />
              </el-icon>
            </template>
          </el-input>
        </div>

        <!-- 任务列表 -->
        <div v-if="filteredTasks.length === 0" class="empty-state">
          <el-empty description="暂无任务" />
        </div>

        <div v-else class="tasks-grid">
          <div v-for="task in filteredTasks" :key="task.id" class="task-card" :class="{
            'task-completed': task.status === 'completed',
            'task-overdue': isTaskOverdue(task)
          }">
            <div class="task-header">
              <el-checkbox :model-value="task.status === 'completed'" @change="handleTaskCheck(task)"
                class="task-checkbox" />
              <div class="task-title-section">
                <h4 class="task-title" :class="{ 'completed': task.status === 'completed' }">
                  {{ task.title }}
                </h4>
                <div class="task-date">
                  <el-icon>
                    <Calendar />
                  </el-icon>
                  {{ formatDate(task.dueDate || '') }}
                </div>
              </div>
              <div class="task-status-actions">
                <el-tag :type="getTaskStatusType(task.status) as any" size="small" class="task-status">
                  {{ getTaskStatusText(task.status) }}
                </el-tag>
                <el-dropdown trigger="click" @click.stop>
                  <el-button :icon="MoreFilled" text size="small" class="more-button" />
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="editTask(task)">
                        <el-icon>
                          <Edit />
                        </el-icon>
                        编辑
                      </el-dropdown-item>
                      <el-dropdown-item @click="deleteTask(task)">
                        <el-icon>
                          <Delete />
                        </el-icon>
                        删除
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>

            <p class="task-description" :class="{ 'completed': task.status === 'completed' }">
              {{ task.description || '暂无描述' }}
            </p>

            <div class="task-meta">
              <div class="time-info">
                <div class="time-item">
                  <el-icon>
                    <Clock />
                  </el-icon>
                  <span>{{ task.estimatedHours }}h</span>
                </div>
                <div class="time-item">
                  <el-icon>
                    <Timer />
                  </el-icon>
                  <span>{{ task.remainingHours }}h</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加任务对话框 -->
    <el-dialog v-model="showAddTaskDialog" title="添加任务" width="500px">
      <el-form ref="taskFormRef" :model="newTask" :rules="taskRules" label-width="80px">
        <el-form-item label="任务名称" prop="title">
          <el-input v-model="newTask.title" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input v-model="newTask.description" type="textarea" :rows="3" placeholder="请输入任务描述" />
        </el-form-item>
        <el-form-item label="预估工时" prop="estimatedHours">
          <el-input-number v-model="newTask.estimatedHours" :min="1" :max="1000" controls-position="right" />
        </el-form-item>
        <el-form-item label="截止日期" prop="dueDate">
          <el-date-picker v-model="newTask.dueDate" type="date" placeholder="选择截止日期" style="width: 100%" />
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="newTask.priority" placeholder="选择优先级">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
            <el-option label="紧急" value="urgent" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddTaskDialog = false">取消</el-button>
        <el-button type="primary" @click="addTask">确定</el-button>
      </template>
    </el-dialog>

    <!-- 编辑任务对话框 -->
    <el-dialog v-model="showEditTaskDialog" title="编辑任务" width="500px">
      <el-form ref="editTaskFormRef" :model="editingTask" :rules="taskRules" label-width="80px">
        <el-form-item label="任务名称" prop="title">
          <el-input v-model="editingTask.title" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input v-model="editingTask.description" type="textarea" :rows="3" placeholder="请输入任务描述" />
        </el-form-item>
        <el-form-item label="预估工时" prop="estimatedHours">
          <el-input-number v-model="editingTask.estimatedHours" :min="1" :max="1000" controls-position="right" />
        </el-form-item>
        <el-form-item label="截止日期" prop="dueDate">
          <el-date-picker v-model="editingTask.dueDate" type="date" placeholder="选择截止日期" style="width: 100%" />
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="editingTask.priority" placeholder="选择优先级">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
            <el-option label="紧急" value="urgent" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditTaskDialog = false">取消</el-button>
        <el-button type="primary" @click="updateTask">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  ElMessage,
  ElMessageBox,
  ElTag,
  ElEmpty,
  ElTimeline,
  ElTimelineItem,
  ElButton,
  ElProgress,
  ElCheckbox,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem,
  ElIcon
} from 'element-plus'
import {
  ArrowLeft,
  Search,
  Star,
  Plus,
  Calendar,
  Clock,
  Timer,
  MoreFilled,
  Edit,
  Delete,
  List
} from '@element-plus/icons-vue'
import type { Project, Task as BaseTask, TimelineNode } from '@/types'

// 使用基础Task类型
type Task = BaseTask
import { projectApi } from '@/api/project'
import { taskApi } from '@/api/task'
import MarkdownIt from 'markdown-it'

// 初始化markdown-it实例
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
})

defineOptions({
  name: 'ProjectDetail'
})

const router = useRouter()
const route = useRoute()

// 响应式数据
const project = ref<Project | null>(null)
const timeline = ref<TimelineNode[]>([])
const taskFilter = ref('all')
const taskSearch = ref('')
const showAddTaskDialog = ref(false)
const showEditTaskDialog = ref(false)
const taskFormRef = ref()
const editTaskFormRef = ref()

// 动画相关数据
const animatedProgress = ref(0)
const animatedTotalTasks = ref(0)
const animatedCompletedTasks = ref(0)
const animatedPendingTasks = ref(0)
const animatedOverdueTasks = ref(0)
const isAnimating = ref(false)

// 新任务表单
const newTask = ref({
  title: '',
  description: '',
  estimatedHours: 8 as number,
  dueDate: '',
  priority: 'medium' as 'low' | 'medium' | 'high' | 'urgent'
})

// 编辑任务表单
const editingTask = ref({
  id: '',
  title: '',
  description: '',
  estimatedHours: 8 as number,
  dueDate: '',
  priority: 'medium' as 'low' | 'medium' | 'high' | 'urgent'
})

// 表单验证规则
const taskRules = {
  title: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入任务描述', trigger: 'blur' }],
  estimatedHours: [{ required: true, message: '请输入预估工时', trigger: 'blur' }],
  dueDate: [{ required: true, message: '请选择截止日期', trigger: 'change' }],
  priority: [{ required: true, message: '请选择优先级', trigger: 'change' }]
}

// 计算属性
const totalTasks = computed(() => project.value?.tasks?.length || 0)
const completedTasks = computed(() =>
  project.value?.tasks?.filter(task => task.status === 'completed').length || 0
)
const pendingTasks = computed(() =>
  project.value?.tasks?.filter(task => task.status === 'pending').length || 0
)
const overdueTasks = computed(() =>
  project.value?.tasks?.filter(task => task.status === 'overdue').length || 0
)

const filteredTasks = computed(() => {
  if (!project.value?.tasks) return []

  let tasks = project.value.tasks

  // 按状态过滤
  if (taskFilter.value !== 'all') {
    tasks = tasks.filter(task => {
      if (taskFilter.value === 'overdue') {
        return task.dueDate && new Date(task.dueDate) < new Date() && task.status !== 'completed'
      }
      return task.status === taskFilter.value
    })
  }

  // 按搜索关键词过滤
  if (taskSearch.value) {
    const keyword = taskSearch.value.toLowerCase()
    tasks = tasks.filter(task =>
      task.title.toLowerCase().includes(keyword) ||
      (task.description || '').toLowerCase().includes(keyword)
    )
  }

  return tasks
})

/**
 * 返回项目列表
 */
const goBack = () => {
  router.push('/projects')
}

/**
 * 加载项目详情数据
 */
const loadProjectDetail = async () => {
  const projectId = route.params.id as string
  if (!projectId) return

  try {
    // 重置动画数据
    resetAnimationData()

    const response = await projectApi.getProject(projectId)
    project.value = response.data

    // 数据加载完成后启动动画
    setTimeout(() => {
      animateNumbers()
    }, 100)
  } catch {
    ElMessage.error('加载项目详情失败')
  }
}

/**
 * 加载项目时间线数据
 */
const loadTimeline = async () => {
  const projectId = route.params.id as string
  if (!projectId) return

  try {
    const response = await projectApi.getProjectTimeline(projectId)
    timeline.value = Array.isArray(response.data) ? response.data as TimelineNode[] : []
  } catch {
    timeline.value = []
    ElMessage.error('加载项目时间线失败')
  }
}

/**
 * 处理任务过滤
 */
const handleTaskFilter = () => {
  // 过滤逻辑已在计算属性中处理
}

/**
 * 处理任务勾选
 */
const handleTaskCheck = async (task: Task) => {
  try {
    const newStatus = task.status === 'completed' ? 'pending' : 'completed'
    await taskApi.updateTask(task.id, { status: newStatus })
    task.status = newStatus
    ElMessage.success(newStatus === 'completed' ? '任务已完成' : '任务已重新激活')
    await loadProjectDetail()
    await loadTimeline()
  } catch {
    ElMessage.error('操作失败')
  }
}

/**
 * 添加任务
 */
const addTask = async () => {
  if (!taskFormRef.value) return

  try {
    await taskFormRef.value.validate()

    const taskData = {
      ...newTask.value,
      projectId: route.params.id as string,
      status: 'pending' as const,
      remainingHours: newTask.value.estimatedHours || 0,
      estimatedHours: newTask.value.estimatedHours || 0,
      reporter: {
        id: 'user_1',
        name: '当前用户',
        email: 'user@example.com',
        role: 'member' as const,
        status: 'online' as const,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      tags: [],
      attachments: [],
      comments: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      priority: newTask.value.priority as 'low' | 'medium' | 'high' | 'urgent'
    }

    await taskApi.createTask(taskData)

    ElMessage.success('任务添加成功')
    showAddTaskDialog.value = false

    // 重置表单
    newTask.value = {
      title: '',
      description: '',
      estimatedHours: 8,
      dueDate: '',
      priority: 'medium' as 'low' | 'medium' | 'high' | 'urgent'
    }

    // 重新加载项目详情
    await loadProjectDetail()
  } catch {
    ElMessage.error('任务添加失败')
  }
}

/**
 * 编辑任务
 */
const editTask = (task: Task) => {
  editingTask.value = {
    id: task.id,
    title: task.title,
    description: task.description || '',
    estimatedHours: task.estimatedHours || 0,
    dueDate: task.dueDate || '',
    priority: task.priority
  }
  showEditTaskDialog.value = true
}

/**
 * 更新任务
 */
const updateTask = async () => {
  if (!editTaskFormRef.value) return

  try {
    await editTaskFormRef.value.validate()

    await taskApi.updateTask(editingTask.value.id, {
      title: editingTask.value.title,
      description: editingTask.value.description,
      estimatedHours: editingTask.value.estimatedHours || 0,
      dueDate: editingTask.value.dueDate,
      priority: editingTask.value.priority
    })

    ElMessage.success('任务更新成功')
    showEditTaskDialog.value = false
    await loadProjectDetail()
  } catch {
    ElMessage.error('任务更新失败')
  }
}

/**
 * 删除任务
 */
const deleteTask = async (task: Task) => {
  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '确认删除', {
      type: 'warning'
    })

    await taskApi.deleteTask(task.id)
    ElMessage.success('任务删除成功')
    await loadProjectDetail()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

/**
 * 切换里程碑状态
 */
const toggleMilestone = async (node: TimelineNode) => {
  try {
    await projectApi.setTimelineMilestone(
      route.params.id as string,
      node.id,
      !node.isMilestone
    )

    ElMessage.success(
      node.isMilestone ? '已取消里程碑标记' : '已设为里程碑'
    )

    await loadTimeline()
  } catch {
    ElMessage.error('操作失败')
  }
}

// 工具方法
const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN')
}

const formatDateTime = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    active: '进行中',
    paused: '已暂停',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

const getTaskStatusType = (status: string) => {
  const types: Record<string, string> = {
    pending: 'warning',
    completed: 'success',
    overdue: 'danger'
  }
  return types[status] || 'info'
}

const getTaskStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '待办',
    completed: '已完成',
    overdue: '已逾期'
  }
  return texts[status] || status
}

const isTaskOverdue = (task: Task) => {
  if (task.status === 'completed') return false
  if (!task.dueDate) return false

  const today = new Date()
  const dueDate = new Date(task.dueDate)
  today.setHours(0, 0, 0, 0)
  dueDate.setHours(0, 0, 0, 0)

  return dueDate < today
}

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
 * 获取进度条颜色
 */
const getProgressColor = (progress: number) => {
  if (progress >= 80) return '#67c23a'
  if (progress >= 50) return '#e6a23c'
  return '#f56c6c'
}

const formatDateYMD = (date: string) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).replace(/\//g, '-')
}

// 渲染markdown内容
const renderMarkdown = (content: string) => {
  if (!content) return ''
  return md.render(content)
}

/**
 * 数字滚动动画
 */
const animateNumbers = () => {
  if (!project.value || isAnimating.value) return

  isAnimating.value = true
  const duration = 1500 // 动画持续时间
  const startTime = Date.now()

  const targetProgress = project.value.progress
  const targetTotal = totalTasks.value
  const targetCompleted = completedTasks.value
  const targetPending = pendingTasks.value
  const targetOverdue = overdueTasks.value

  const animate = () => {
    const elapsed = Date.now() - startTime
    const progress = Math.min(elapsed / duration, 1)

    // 使用缓动函数
    const easeOutQuart = 1 - Math.pow(1 - progress, 4)

    animatedProgress.value = targetProgress * easeOutQuart
    animatedTotalTasks.value = targetTotal * easeOutQuart
    animatedCompletedTasks.value = targetCompleted * easeOutQuart
    animatedPendingTasks.value = targetPending * easeOutQuart
    animatedOverdueTasks.value = targetOverdue * easeOutQuart

    if (progress < 1) {
      requestAnimationFrame(animate)
    } else {
      // 确保最终值准确
      animatedProgress.value = targetProgress
      animatedTotalTasks.value = targetTotal
      animatedCompletedTasks.value = targetCompleted
      animatedPendingTasks.value = targetPending
      animatedOverdueTasks.value = targetOverdue
      isAnimating.value = false
    }
  }

  requestAnimationFrame(animate)
}

/**
 * 重置动画数据
 */
const resetAnimationData = () => {
  animatedProgress.value = 0
  animatedTotalTasks.value = 0
  animatedCompletedTasks.value = 0
  animatedPendingTasks.value = 0
  animatedOverdueTasks.value = 0
  isAnimating.value = false
}

// 组件挂载时加载数据
onMounted(() => {
  loadProjectDetail()
  loadTimeline()
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.project-detail-page {
  max-width: 1200px;
  margin: 0 auto;

  .back-navigation {
    margin-bottom: $spacing-6;

    .back-button {
      color: $text-secondary;
      font-size: $font-size-sm;
      padding: 0;

      &:hover {
        color: $primary-color;
      }

      .el-icon {
        margin-right: $spacing-1;
      }
    }
  }

  .project-header {
    margin-bottom: $spacing-6;

    .project-title-section {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: $spacing-4;

      .project-title {
        font-size: 32px;
        font-weight: bold;
        color: $text-primary;
        margin: 0;
        line-height: 1.2;
      }

      .project-tags {
        display: flex;
        align-items: center;
        gap: $spacing-3;

        .status-tag {
          padding: 8px 16px;
          border-radius: 10px;
          font-size: $font-size-sm;
          font-weight: 600;
          border: 2px solid;
          background: transparent;

          &.status-active {
            color: #1c7ed6;
            border-color: #1c7ed6;
          }

          &.status-completed {
            color: #12b886;
            border-color: #12b886;
          }

          &.status-overdue {
            color: #fd7e14;
            border-color: #fd7e14;
          }

          &.status-cancelled {
            color: #e03131;
            border-color: #e03131;
          }
        }

        .category-tag {
          background: #f8f9fa;
          color: #6c757d;
          border: none;
          font-size: $font-size-sm;
        }
      }
    }
  }

  .project-meta-section {
    display: flex;
    gap: $spacing-8;
    margin-bottom: $spacing-6;
    padding: $spacing-6;
    background: white;
    border-radius: 10px;
    border: 1px solid #e9ecef;

    .meta-item {
      flex: 1;
      text-align: center;

      .meta-label {
        font-size: $font-size-sm;
        color: $text-secondary;
        font-weight: 600;
        margin-bottom: $spacing-2;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }

      .meta-value {
        font-size: $font-size-lg;
        color: $text-primary;
        font-weight: 600;

        .priority-tag {
          display: inline-flex;
          align-items: center;
          padding: 6px 12px;
          border-radius: 6px;
          font-size: $font-size-sm;
          font-weight: 600;

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

  .progress-card {
    background: white;
    border-radius: 10px;
    padding: $spacing-6;
    margin-bottom: $spacing-6;
    border: 1px solid #e9ecef;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);

    .progress-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: $spacing-4;

      .progress-title {
        font-size: $font-size-xl;
        font-weight: 600;
        color: $text-primary;
        margin: 0;
      }

      .progress-info {
        display: flex;
        align-items: flex-start;
        gap: $spacing-4;

        .progress-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;

          .progress-percentage {
            font-size: 28px;
            font-weight: bold;
            color: $primary-color;
            line-height: 1;
            margin-bottom: $spacing-1;
          }

          .progress-tasks {
            color: black;
          }

          .progress-label {
            font-size: $font-size-sm;
            color: $text-secondary;
            font-weight: bold;
          }
        }
      }
    }

    .progress-content {
      .progress-bar-section {
        margin-bottom: $spacing-4;
      }

      .progress-stats {
        display: flex;
        justify-content: space-around;
        gap: $spacing-4;

        .stat-item {
          display: flex;
          flex-direction: column;
          padding: $spacing-4;
          border-radius: 12px;
          flex: 1;
          transition: all 0.3s ease;
          background: transparent;

          &:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
          }

          .stat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: $spacing-2;

            .stat-label {
              font-size: $font-size-sm;
              color: $text-secondary;
              font-weight: 500;
            }

            .stat-icon {
              display: flex;
              align-items: center;
              justify-content: center;
              width: 24px;
              height: 24px;
              border-radius: 6px;
              font-size: 16px;
            }
          }

          .stat-number {
            font-size: 32px;
            font-weight: bold;
            line-height: 1;
          }

          // 任务总数样式
          &.stat-total {
            background: #EEEFF7;

            .stat-icon {
              color: #64748b;
            }

            .stat-number {
              color: #475569;
            }
          }

          // 已完成任务样式
          &.stat-completed {
            background: #FFECD7;

            .stat-icon {
              color: #16a34a;
            }

            .stat-number {
              color: #15803d;
            }
          }

          // 待办任务样式
          &.stat-pending {
            background: #FAE6D2;

            .stat-icon {
              color: #d97706;
            }

            .stat-number {
              color: #b45309;
            }
          }

          // 逾期任务样式
          &.stat-overdue {
            background: #BFF1DF;

            .stat-icon {
              color: #dc2626;
            }

            .stat-number {
              color: #b91c1c;
            }
          }
        }
      }
    }
  }

  .content-section {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: $spacing-6;
    margin-bottom: $spacing-6;

    @media (max-width: 1024px) {
      grid-template-columns: 1fr;
    }

    .project-description {
      background: white;
      border-radius: 10px;
      padding: $spacing-6;
      border: 1px solid #e9ecef;
      height: 600px; // 设置固定高度
      display: flex;
      flex-direction: column;

      h3 {
        font-size: $font-size-xl;
        font-weight: 600;
        color: $text-primary;
        margin: 0 0 $spacing-4 0;
        flex-shrink: 0; // 防止标题被压缩
      }

      .markdown-content {
        line-height: 1.6;
        color: $text-primary;
        flex: 1; // 占据剩余空间
        overflow-y: auto; // 添加垂直滚动条
        padding-right: $spacing-2; // 为滚动条留出空间

        :deep(h1),
        :deep(h2),
        :deep(h3),
        :deep(h4),
        :deep(h5),
        :deep(h6) {
          margin-top: $spacing-4;
          margin-bottom: $spacing-2;
          color: $text-primary;
        }

        :deep(p) {
          margin-bottom: $spacing-3;
        }

        :deep(ul),
        :deep(ol) {
          margin-bottom: $spacing-3;
          padding-left: $spacing-5;
        }

        :deep(code) {
          background: #f8f9fa;
          padding: 2px 4px;
          border-radius: 4px;
          font-size: 0.9em;
        }

        :deep(pre) {
          background: #f8f9fa;
          padding: $spacing-3;
          border-radius: 6px;
          overflow-x: auto;
          margin-bottom: $spacing-3;
        }
      }
    }

    .timeline-section {
      background: white;
      border-radius: 10px;
      padding: $spacing-6;
      border: 1px solid #e9ecef;
      height: 600px; // 设置固定高度，与项目详情区域保持一致
      display: flex;
      flex-direction: column;

      h3 {
        font-size: $font-size-xl;
        font-weight: 600;
        color: $text-primary;
        margin: 0 0 $spacing-4 0;
        flex-shrink: 0; // 防止标题被压缩
      }

      .empty-state {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .project-timeline {
        flex: 1; // 占据剩余空间
        overflow-y: auto; // 添加垂直滚动条
        padding-right: $spacing-2; // 为滚动条留出空间

        :deep(.el-timeline-item) {
          .el-timeline-item__node {
            left: 2px
          }
        }

        .timeline-content {
          .timeline-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: $spacing-2;

            .timeline-title {
              font-weight: 600;
              color: $text-primary;
            }
          }

          .timeline-description {
            color: $text-secondary;
            margin: 0;
            line-height: 1.5;
          }
        }
      }
    }
  }

  .tasks-card {
    background: white;
    border-radius: 10px;
    padding: $spacing-6;
    border: 1px solid #e9ecef;

    .tasks-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: $spacing-4;

      h3 {
        font-size: $font-size-xl;
        font-weight: 600;
        color: $text-primary;
        margin: 0;
      }
    }

    .tasks-controls {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: $spacing-4;
      gap: $spacing-4;

      @media (max-width: 768px) {
        flex-direction: column;
        align-items: stretch;
      }

      :deep(.el-radio-group) {
        .el-radio-button {
          .el-radio-button__inner {
            padding: 8px 16px;
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

    .tasks-grid {
      display: grid;
      gap: $spacing-4;

      .task-card {
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: $spacing-4;
        transition: all 0.2s ease;

        &:hover {
          border-color: #d0d7de;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }

        &.task-completed {
          background: #f8f9fa;
        }

        &.task-overdue {
          background: #fef2f2;
        }

        .task-header {
          display: flex;
          align-items: flex-start;
          gap: $spacing-3;
          margin-bottom: $spacing-3;

          .task-checkbox {
            margin-top: 2px;
          }

          .task-title-section {
            flex: 1;
            min-width: 0;

            .task-title {
              font-size: $font-size-base;
              font-weight: 600;
              color: $text-primary;
              margin: 0 0 $spacing-1 0;
              line-height: 1.4;

              &.completed {
                text-decoration: line-through;
                color: $text-secondary;
              }
            }

            .task-date {
              display: flex;
              align-items: center;
              gap: $spacing-1;
              font-size: $font-size-sm;
              color: gray;

              .el-icon {
                font-size: 14px;
              }
            }
          }

          .task-status-actions {
            display: flex;
            align-items: center;
            gap: $spacing-2;

            .task-status {
              font-size: 12px;
            }

            .more-button {
              padding: 4px;
              min-height: auto;

              &:hover {
                background: #f5f5f5;
              }
            }
          }
        }

        .task-description {
          font-size: $font-size-sm;
          margin: 0 0 $spacing-3 0;
          line-height: 1.5;
          padding-left: 28px; // 对齐checkbox

          &.completed {
            text-decoration: line-through;
          }
        }

        .task-meta {
          padding-left: 28px; // 对齐checkbox

          .time-info {
            display: flex;
            gap: $spacing-4;

            .time-item {
              display: flex;
              align-items: center;
              gap: $spacing-1;
              font-size: $font-size-sm;
              color: gray;
              font-weight: blod;

              .el-icon {
                font-size: 14px;
              }
            }
          }
        }
      }
    }

    .empty-state {
      text-align: center;
      padding: $spacing-8 0;
    }
  }
}
</style>