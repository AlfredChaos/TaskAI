<template>
  <div class="tasks-index-page">
    <div class="page-header">
      <h1 class="page-title">任务管理</h1>
      <p class="page-description">管理和跟踪您的所有任务</p>
    </div>

    <!-- 表头 -->
    <div class="table-header">
      <div class="header-cell task-name">任务名称</div>
      <div class="header-cell project-name">所属项目</div>
      <div class="header-cell hours">预期工时</div>
      <div class="header-cell remaining-hours">剩余工时</div>
      <div class="header-cell due-date">截止日期</div>
    </div>

    <!-- 任务状态分组 -->
    <div class="task-groups">
      <!-- Pending 任务 -->
      <div class="task-group">
        <div class="group-header" @click="toggleGroup('pending')">
          <el-icon class="expand-icon" :class="{ expanded: expandedGroups.pending }">
            <ArrowRight />
          </el-icon>
          <span class="group-title">待办任务</span>
          <span class="task-count">({{ pendingTasks.length }})</span>
        </div>
        <el-collapse-transition>
          <div v-show="expandedGroups.pending" class="task-list">
            <div ref="pendingTasksRef" class="draggable-list">
              <div v-for="task in pendingTasks" :key="task.id" class="task-row" :class="getPriorityClass(task.priority)"
                :data-id="task.id">
                <div class="task-cell task-name">
                  <el-checkbox :model-value="task.status === 'completed'" @change="toggleTaskStatus(task)"
                    class="task-checkbox" />
                  <span class="task-title" @click="openTaskDetail(task)">{{ task.title }}</span>
                </div>
                <div class="task-cell project-name">
                  {{ getProjectName(task.projectId) }}
                </div>
                <div class="task-cell hours">
                  {{ task.estimatedHours || 0 }}h
                </div>
                <div class="task-cell remaining-hours">
                  {{ task.remainingHours || 0 }}h
                </div>
                <div class="task-cell due-date">
                  {{ formatDate(task.dueDate) }}
                </div>
              </div>
            </div>
            <div class="add-task-row" @click="openCreateTask('pending')">
              <el-icon>
                <Plus />
              </el-icon>
              <span>添加新任务</span>
            </div>
          </div>
        </el-collapse-transition>
      </div>

      <!-- Overdue 任务 -->
      <div class="task-group">
        <div class="group-header" @click="toggleGroup('overdue')">
          <el-icon class="expand-icon" :class="{ expanded: expandedGroups.overdue }">
            <ArrowRight />
          </el-icon>
          <span class="group-title">逾期任务</span>
          <span class="task-count">({{ overdueTasks.length }})</span>
        </div>
        <el-collapse-transition>
          <div v-show="expandedGroups.overdue" class="task-list">
            <div ref="overdueTasksRef" class="draggable-list">
              <div v-for="task in overdueTasks" :key="task.id" class="task-row overdue"
                :class="getPriorityClass(task.priority)" :data-id="task.id">
                <div class="task-cell task-name">
                  <el-checkbox :model-value="task.status === 'completed'" @change="toggleTaskStatus(task)"
                    class="task-checkbox" />
                  <span class="task-title" @click="openTaskDetail(task)">{{ task.title }}</span>
                </div>
                <div class="task-cell project-name">
                  {{ getProjectName(task.projectId) }}
                </div>
                <div class="task-cell hours">
                  {{ task.estimatedHours || 0 }}h
                </div>
                <div class="task-cell remaining-hours">
                  {{ task.remainingHours || 0 }}h
                </div>
                <div class="task-cell due-date">
                  {{ formatDate(task.dueDate) }}
                </div>
              </div>
            </div>
            <div class="add-task-row" @click="openCreateTask('overdue')">
              <el-icon>
                <Plus />
              </el-icon>
              <span>添加新任务</span>
            </div>
          </div>
        </el-collapse-transition>
      </div>

      <!-- Completed 任务 -->
      <div class="task-group">
        <div class="group-header" @click="toggleGroup('completed')">
          <el-icon class="expand-icon" :class="{ expanded: expandedGroups.completed }">
            <ArrowRight />
          </el-icon>
          <span class="group-title">已完成任务</span>
          <span class="task-count">({{ completedTasks.length }})</span>
        </div>
        <el-collapse-transition>
          <div v-show="expandedGroups.completed" class="task-list">
            <div ref="completedTasksRef" class="draggable-list">
              <div v-for="task in completedTasks" :key="task.id" class="task-row completed"
                :class="getPriorityClass(task.priority)" :data-id="task.id">
                <div class="task-cell task-name">
                  <el-checkbox :model-value="task.status === 'completed'" @change="toggleTaskStatus(task)"
                    class="task-checkbox" />
                  <span class="task-title" @click="openTaskDetail(task)">{{ task.title }}</span>
                </div>
                <div class="task-cell project-name">
                  {{ getProjectName(task.projectId) }}
                </div>
                <div class="task-cell hours">
                  {{ task.estimatedHours || 0 }}h
                </div>
                <div class="task-cell remaining-hours">
                  {{ task.remainingHours || 0 }}h
                </div>
                <div class="task-cell due-date">
                  {{ formatDate(task.dueDate) }}
                </div>
              </div>
            </div>
            <div class="add-task-row" @click="openCreateTask('completed')">
              <el-icon>
                <Plus />
              </el-icon>
              <span>添加新任务</span>
            </div>
          </div>
        </el-collapse-transition>
      </div>
    </div>

    <!-- 任务详情/编辑弹窗 -->
    <el-dialog v-model="showTaskDialog" :title="isEditing ? '编辑任务' : '任务详情'" width="600px" @close="closeTaskDialog">
      <el-form ref="taskFormRef" :model="currentTask" :rules="taskRules" label-width="100px" v-if="currentTask">
        <el-form-item label="任务名称" prop="title">
          <el-input v-model="currentTask.title" :disabled="!isEditing" />
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input v-model="currentTask.description" type="textarea" :rows="3" :disabled="!isEditing" />
        </el-form-item>
        <el-form-item label="所属项目" prop="projectId">
          <el-select v-model="currentTask.projectId" :disabled="!isEditing" style="width: 100%">
            <el-option v-for="project in projects" :key="project.id" :label="project.name" :value="project.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="currentTask.priority" :disabled="!isEditing" style="width: 100%">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
            <el-option label="紧急" value="urgent" />
          </el-select>
        </el-form-item>
        <el-form-item label="预期工时" prop="estimatedHours">
          <el-input-number v-model="currentTask.estimatedHours" :min="0" :disabled="!isEditing" style="width: 100%" />
        </el-form-item>
        <el-form-item label="剩余工时" prop="remainingHours">
          <el-input-number v-model="currentTask.remainingHours" :min="0" :disabled="!isEditing" style="width: 100%" />
        </el-form-item>
        <el-form-item label="截止日期" prop="dueDate">
          <el-date-picker v-model="currentTask.dueDate" type="date" :disabled="!isEditing" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="closeTaskDialog">取消</el-button>
          <el-button v-if="!isEditing" type="primary" @click="startEditing">编辑</el-button>
          <template v-else>
            <el-button type="danger" @click="deleteCurrentTask">删除</el-button>
            <el-button type="primary" @click="saveTask">保存</el-button>
          </template>
        </div>
      </template>
    </el-dialog>

    <!-- 新建任务弹窗 -->
    <el-dialog v-model="showCreateDialog" title="新建任务" width="600px" @close="closeCreateDialog">
      <el-form ref="createFormRef" :model="newTask" :rules="taskRules" label-width="100px">
        <el-form-item label="任务名称" prop="title">
          <el-input v-model="newTask.title" />
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input v-model="newTask.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="所属项目" prop="projectId">
          <el-select v-model="newTask.projectId" style="width: 100%">
            <el-option v-for="project in projects" :key="project.id" :label="project.name" :value="project.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="newTask.priority" style="width: 100%">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
            <el-option label="紧急" value="urgent" />
          </el-select>
        </el-form-item>
        <el-form-item label="预期工时" prop="estimatedHours">
          <el-input-number v-model="newTask.estimatedHours" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="剩余工时" prop="remainingHours">
          <el-input-number v-model="newTask.remainingHours" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="截止日期" prop="dueDate">
          <el-date-picker v-model="newTask.dueDate" type="date" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="closeCreateDialog">取消</el-button>
          <el-button type="primary" @click="createTask">创建</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { ArrowRight, Plus } from '@element-plus/icons-vue'
import { useSortable } from '@vueuse/integrations/useSortable'
import { taskApi } from '@/api/task'
import { projectApi } from '@/api/project'
import type { Task, Project, TaskStatus } from '@/types'

defineOptions({
  name: 'TasksIndex'
})

// 响应式数据
const tasks = ref<Task[]>([])
const projects = ref<Project[]>([])
const loading = ref(false)

// 拖拽区域引用
const pendingTasksRef = ref<HTMLElement>()
const overdueTasksRef = ref<HTMLElement>()
const completedTasksRef = ref<HTMLElement>()

// 分组展开状态
const expandedGroups = reactive({
  pending: true,
  overdue: true,
  completed: false
})

// 弹窗状态
const showTaskDialog = ref(false)
const showCreateDialog = ref(false)
const isEditing = ref(false)
const currentTask = ref<Task | null>(null)
const originalTask = ref<Task | null>(null)

// 表单引用
const taskFormRef = ref<FormInstance>()
const createFormRef = ref<FormInstance>()

// 新建任务表单
const newTask = reactive<Partial<Task>>({
  title: '',
  description: '',
  projectId: '',
  priority: 'medium',
  estimatedHours: 0,
  remainingHours: 0,
  dueDate: '',
  status: 'pending'
})

// 表单验证规则
const taskRules: FormRules = {
  title: [
    { required: true, message: '请输入任务名称', trigger: 'blur' }
  ],
  projectId: [
    { required: true, message: '请选择所属项目', trigger: 'change' }
  ]
}

// 计算属性 - 按状态分组的任务
const pendingTasks = computed({
  get: () => tasks.value.filter(task => task.status === 'pending'),
  set: (value) => {
    // 更新任务列表中的pending任务
    const otherTasks = tasks.value.filter(task => task.status !== 'pending')
    tasks.value = [...otherTasks, ...value]
  }
})

const overdueTasks = computed({
  get: () => tasks.value.filter(task => task.status === 'overdue'),
  set: (value) => {
    const otherTasks = tasks.value.filter(task => task.status !== 'overdue')
    tasks.value = [...otherTasks, ...value]
  }
})

const completedTasks = computed({
  get: () => tasks.value.filter(task => task.status === 'completed'),
  set: (value) => {
    const otherTasks = tasks.value.filter(task => task.status !== 'completed')
    tasks.value = [...otherTasks, ...value]
  }
})

/**
 * 加载任务列表
 */
const loadTasks = async () => {
  try {
    loading.value = true
    const response = await taskApi.getTasks()
    tasks.value = response.data.list || response.data || []
  } catch (error) {
    ElMessage.error('加载任务列表失败')
    console.error('Load tasks error:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 加载项目列表
 */
const loadProjects = async () => {
  try {
    const response = await projectApi.getProjects()
    projects.value = response.data || []
  } catch (error) {
    ElMessage.error('加载项目列表失败')
    console.error('Load projects error:', error)
  }
}

/**
 * 切换分组展开状态
 */
const toggleGroup = (group: keyof typeof expandedGroups) => {
  expandedGroups[group] = !expandedGroups[group]
}

/**
 * 获取项目名称
 */
const getProjectName = (projectId: string) => {
  const project = projects.value.find(p => p.id === projectId)
  return project?.name || '未知项目'
}

/**
 * 格式化日期
 */
const formatDate = (date?: string) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

/**
 * 获取优先级样式类
 */
const getPriorityClass = (priority: string) => {
  return `priority-${priority}`
}

/**
 * 切换任务状态
 */
const toggleTaskStatus = async (task: Task) => {
  try {
    const newStatus: TaskStatus = task.status === 'completed' ? 'pending' : 'completed'
    await taskApi.updateTaskStatus(task.id, newStatus)
    task.status = newStatus
    ElMessage.success('任务状态更新成功')
  } catch (error) {
    ElMessage.error('更新任务状态失败')
    console.error('Toggle task status error:', error)
  }
}

/**
 * 初始化拖拽功能
 */
const initializeSortable = () => {
  if (pendingTasksRef.value) {
    useSortable(pendingTasksRef.value, pendingTasks, {
      group: 'tasks',
      animation: 150
    })
  }
  if (overdueTasksRef.value) {
    useSortable(overdueTasksRef.value, overdueTasks, {
      group: 'tasks',
      animation: 150
    })
  }
  if (completedTasksRef.value) {
    useSortable(completedTasksRef.value, completedTasks, {
      group: 'tasks',
      animation: 150
    })
  }
}

/**
 * 打开任务详情
 */
const openTaskDetail = (task: Task) => {
  currentTask.value = { ...task }
  originalTask.value = { ...task }
  isEditing.value = false
  showTaskDialog.value = true
}

/**
 * 开始编辑
 */
const startEditing = () => {
  isEditing.value = true
}

/**
 * 保存任务
 */
const saveTask = async () => {
  if (!taskFormRef.value || !currentTask.value) return

  try {
    await taskFormRef.value.validate()
    await taskApi.updateTask(currentTask.value.id, currentTask.value)

    // 更新本地任务列表
    const index = tasks.value.findIndex(t => t.id === currentTask.value!.id)
    if (index !== -1) {
      tasks.value[index] = { ...currentTask.value }
    }

    ElMessage.success('任务更新成功')
    closeTaskDialog()
  } catch (error) {
    ElMessage.error('保存任务失败')
    console.error('Save task error:', error)
  }
}

/**
 * 删除当前任务
 */
const deleteCurrentTask = async () => {
  if (!currentTask.value) return

  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '确认删除', {
      type: 'warning'
    })

    await taskApi.deleteTask(currentTask.value.id)

    // 从本地任务列表中移除
    const index = tasks.value.findIndex(t => t.id === currentTask.value!.id)
    if (index !== -1) {
      tasks.value.splice(index, 1)
    }

    ElMessage.success('任务删除成功')
    closeTaskDialog()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除任务失败')
      console.error('Delete task error:', error)
    }
  }
}

/**
 * 关闭任务弹窗
 */
const closeTaskDialog = () => {
  showTaskDialog.value = false
  isEditing.value = false
  currentTask.value = null
  originalTask.value = null
}

/**
 * 打开新建任务弹窗
 */
const openCreateTask = (status: TaskStatus) => {
  Object.assign(newTask, {
    title: '',
    description: '',
    projectId: '',
    priority: 'medium',
    estimatedHours: 0,
    remainingHours: 0,
    dueDate: '',
    status
  })
  showCreateDialog.value = true
}

/**
 * 创建任务
 */
const createTask = async () => {
  if (!createFormRef.value) return

  try {
    await createFormRef.value.validate()
    const taskData = {
      title: newTask.title || '',
      description: newTask.description || '',
      projectId: newTask.projectId || '',
      priority: newTask.priority || 'medium',
      estimatedHours: newTask.estimatedHours || 0,
      remainingHours: newTask.remainingHours || 0,
      dueDate: newTask.dueDate || '',
      status: newTask.status || 'pending',
      reporter: {
        id: 'current-user',
        name: '当前用户',
        email: 'user@example.com',
        role: 'member' as const,
        status: 'online' as const,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      },
      tags: []
    }
    const response = await taskApi.createTask(taskData)

    // 添加到本地任务列表
    tasks.value.push(response.data)

    ElMessage.success('任务创建成功')
    closeCreateDialog()
  } catch (error) {
    ElMessage.error('创建任务失败')
    console.error('Create task error:', error)
  }
}

/**
 * 关闭新建任务弹窗
 */
const closeCreateDialog = () => {
  showCreateDialog.value = false
  createFormRef.value?.resetFields()
}

// 组件挂载时加载数据
onMounted(() => {
  loadTasks()
  loadProjects()
  initializeSortable()
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.tasks-index-page {
  .page-header {
    margin-bottom: $spacing-6;

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

  .table-header {
    display: flex;
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 10px;
    padding: 12px 16px;
    font-weight: 600;
    color: #495057;
    margin-bottom: 0;

    .header-cell {
      &.task-name {
        flex: 2;
        min-width: 200px;
      }

      &.project-name {
        flex: 1;
        min-width: 120px;
      }

      &.hours {
        flex: 0.8;
        min-width: 80px;
        text-align: center;
      }

      &.remaining-hours {
        flex: 0.8;
        min-width: 80px;
        text-align: center;
      }

      &.due-date {
        flex: 1;
        min-width: 100px;
        text-align: center;
      }
    }
  }

  .task-groups {
    border-top: none;
    border-radius: 0 0 8px 8px;

    .task-group {
      margin-top: 24px;
      border-bottom: 1px solid #e9ecef;
      border: 1px solid #e9ecef;
      background: white;
      border-radius: 10px;

      &:last-child {
        border-bottom: none;
      }

      .group-header {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        background: #f8f9fa;
        cursor: pointer;
        transition: background-color 0.2s;
        border-radius: 10px 10px 0 0;

        &:hover {
          background: #e9ecef;
        }

        .expand-icon {
          margin-right: 8px;
          transition: transform 0.2s;
          color: #6c757d;

          &.expanded {
            transform: rotate(90deg);
          }
        }

        .group-title {
          font-weight: 600;
          color: #495057;
        }

        .task-count {
          margin-left: 8px;
          color: #6c757d;
          font-size: 14px;
        }
      }

      .task-list {
        .draggable-list {
          min-height: 20px;
        }

        .task-row {
          display: flex;
          align-items: center;
          padding: 12px 16px;
          border-bottom: 1px solid #f1f3f4;
          transition: background-color 0.2s;
          border-left: 4px solid transparent;

          &:hover {
            background: #f8f9fa;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
          }

          &.overdue {
            background: #fff5f5;
          }

          &.completed {
            background: #f0f9ff;
            opacity: 0.8;

            .task-title {
              text-decoration: line-through;
              color: #6c757d;
            }
          }

          // 优先级颜色
          &.priority-low {
            border-left-color: #28a745;
          }

          &.priority-medium {
            border-left-color: #ffc107;
          }

          &.priority-high {
            border-left-color: #fd7e14;
          }

          &.priority-urgent {
            border-left-color: #dc3545;
          }

          .task-cell {
            &.task-name {
              flex: 2;
              min-width: 200px;
              display: flex;
              align-items: center;

              .task-checkbox {
                margin-right: 12px;
              }

              .task-title {
                cursor: pointer;
                color: #007bff;
                text-decoration: none;
                transition: color 0.2s;

                &:hover {
                  color: #0056b3;
                  text-decoration: underline;
                }
              }
            }

            &.project-name {
              flex: 1;
              min-width: 120px;
              color: #6c757d;
            }

            &.hours,
            &.remaining-hours {
              flex: 0.8;
              min-width: 80px;
              text-align: center;
              color: #495057;
            }

            &.due-date {
              flex: 1;
              min-width: 100px;
              text-align: center;
              color: #495057;
            }
          }
        }

        .add-task-row {
          display: flex;
          align-items: center;
          padding: 12px 16px;
          color: #6c757d;
          cursor: pointer;
          transition: all 0.2s;
          border-top: 1px dashed #dee2e6;

          &:hover {
            background: #f8f9fa;
            color: #007bff;
          }

          .el-icon {
            margin-right: 8px;
          }
        }
      }
    }
  }

  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
  }
}
</style>