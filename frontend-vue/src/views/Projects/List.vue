<template>
  <div class="project-list-view">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">项目管理</h1>
        <p class="page-subtitle">管理和跟踪您的所有项目</p>
      </div>
      <div class="header-right">
        <el-button type="primary" @click="createProject">
          <el-icon><Plus /></el-icon>
          新建项目
        </el-button>
      </div>
    </div>
    
    <!-- 筛选和搜索 -->
    <div class="filter-section">
      <div class="filter-left">
        <el-input
          v-model="searchQuery"
          placeholder="搜索项目名称、描述..."
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
          <el-option label="进行中" value="active" />
          <el-option label="已完成" value="completed" />
          <el-option label="已暂停" value="paused" />
        </el-select>
        
        <el-select v-model="sortBy" style="width: 140px">
          <el-option label="最新创建" value="created_desc" />
          <el-option label="最早创建" value="created_asc" />
          <el-option label="名称A-Z" value="name_asc" />
          <el-option label="名称Z-A" value="name_desc" />
          <el-option label="进度升序" value="progress_asc" />
          <el-option label="进度降序" value="progress_desc" />
        </el-select>
        
        <el-button-group>
          <el-button :type="viewMode === 'grid' ? 'primary' : 'default'" @click="viewMode = 'grid'">
            <el-icon><Grid /></el-icon>
          </el-button>
          <el-button :type="viewMode === 'list' ? 'primary' : 'default'" @click="viewMode = 'list'">
            <el-icon><List /></el-icon>
          </el-button>
        </el-button-group>
      </div>
    </div>
    
    <!-- 项目列表 -->
    <div class="projects-container" v-loading="loading">
      <!-- 网格视图 -->
      <div v-if="viewMode === 'grid'" class="projects-grid">
        <div
          v-for="project in filteredProjects"
          :key="project.id"
          class="project-card"
          @click="viewProject(project.id)"
        >
          <div class="card-header">
            <div class="project-avatar">
              <img v-if="project.avatar" :src="project.avatar" :alt="project.name" />
              <div v-else class="avatar-placeholder">
                {{ project.name.charAt(0).toUpperCase() }}
              </div>
            </div>
            <div class="project-status">
              <el-tag :type="getStatusType(project.status)" size="small">
                {{ getStatusText(project.status) }}
              </el-tag>
            </div>
          </div>
          
          <div class="card-content">
            <h3 class="project-name">{{ project.name }}</h3>
            <p class="project-description">{{ project.description }}</p>
            
            <div class="project-progress">
              <div class="progress-header">
                <span class="progress-label">进度</span>
                <span class="progress-value">{{ project.progress }}%</span>
              </div>
              <el-progress
                :percentage="project.progress"
                :stroke-width="6"
                :show-text="false"
                :color="getProgressColor(project.progress)"
              />
            </div>
            
            <div class="project-meta">
              <div class="meta-item">
                <el-icon><User /></el-icon>
                <span>{{ project.memberCount }} 成员</span>
              </div>
              <div class="meta-item">
                <el-icon><List /></el-icon>
                <span>{{ project.taskCount }} 任务</span>
              </div>
              <div class="meta-item">
                <el-icon><Calendar /></el-icon>
                <span>{{ formatDate(project.deadline) }}</span>
              </div>
            </div>
          </div>
          
          <div class="card-footer">
            <div class="project-members">
              <el-avatar-group :max="3" size="small">
                <el-avatar
                  v-for="member in project.members.slice(0, 3)"
                  :key="member.id"
                  :src="member.avatar"
                  :title="member.name"
                >
                  {{ member.name.charAt(0) }}
                </el-avatar>
              </el-avatar-group>
            </div>
            <div class="project-actions">
              <el-dropdown @command="handleProjectAction">
                <el-button type="text" size="small">
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :command="{ action: 'edit', project }">
                      编辑项目
                    </el-dropdown-item>
                    <el-dropdown-item :command="{ action: 'duplicate', project }">
                      复制项目
                    </el-dropdown-item>
                    <el-dropdown-item divided :command="{ action: 'delete', project }">
                      删除项目
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 列表视图 -->
      <div v-else class="projects-table">
        <el-table :data="filteredProjects" @row-click="viewProject">
          <el-table-column label="项目" min-width="200">
            <template #default="{ row }">
              <div class="table-project-info">
                <div class="project-avatar small">
                  <img v-if="row.avatar" :src="row.avatar" :alt="row.name" />
                  <div v-else class="avatar-placeholder">
                    {{ row.name.charAt(0).toUpperCase() }}
                  </div>
                </div>
                <div class="project-details">
                  <div class="project-name">{{ row.name }}</div>
                  <div class="project-description">{{ row.description }}</div>
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
          
          <el-table-column label="进度" width="150">
            <template #default="{ row }">
              <div class="table-progress">
                <el-progress
                  :percentage="row.progress"
                  :stroke-width="4"
                  :color="getProgressColor(row.progress)"
                />
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="成员" width="120">
            <template #default="{ row }">
              <el-avatar-group :max="3" size="small">
                <el-avatar
                  v-for="member in row.members.slice(0, 3)"
                  :key="member.id"
                  :src="member.avatar"
                  :title="member.name"
                >
                  {{ member.name.charAt(0) }}
                </el-avatar>
              </el-avatar-group>
            </template>
          </el-table-column>
          
          <el-table-column label="截止日期" width="120">
            <template #default="{ row }">
              {{ formatDate(row.deadline) }}
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="80" fixed="right">
            <template #default="{ row }">
              <el-dropdown @command="handleProjectAction">
                <el-button type="text" size="small">
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :command="{ action: 'edit', project: row }">
                      编辑项目
                    </el-dropdown-item>
                    <el-dropdown-item :command="{ action: 'duplicate', project: row }">
                      复制项目
                    </el-dropdown-item>
                    <el-dropdown-item divided :command="{ action: 'delete', project: row }">
                      删除项目
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <!-- 空状态 -->
      <div v-if="filteredProjects.length === 0 && !loading" class="empty-state">
        <div class="empty-icon">
          <el-icon><Folder /></el-icon>
        </div>
        <h3 class="empty-title">暂无项目</h3>
        <p class="empty-description">
          {{ searchQuery ? '没有找到匹配的项目' : '开始创建您的第一个项目吧' }}
        </p>
        <el-button v-if="!searchQuery" type="primary" @click="createProject">
          创建项目
        </el-button>
      </div>
    </div>
    
    <!-- 分页 -->
    <div v-if="filteredProjects.length > 0" class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[12, 24, 48, 96]"
        :total="totalProjects"
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
  Grid,
  List,
  User,
  Calendar,
  MoreFilled,
  Folder
} from '@element-plus/icons-vue'
import { formatDate } from '@/utils'
import type { Project } from '@/types'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const sortBy = ref('created_desc')
const viewMode = ref<'grid' | 'list'>('grid')
const currentPage = ref(1)
const pageSize = ref(12)

// 扩展Project类型以包含额外属性
interface ExtendedProject extends Project {
  avatar?: string
  memberCount: number
  taskCount: number
  deadline: Date
}

// 模拟项目数据
const projects = ref<ExtendedProject[]>([
  {
    id: '1',
    name: '移动端应用开发',
    description: '开发一款跨平台的移动应用，支持iOS和Android系统',
    status: 'active',
    progress: 75,
    startDate: '2024-01-10',
    endDate: '2024-03-15',
    memberCount: 8,
    taskCount: 24,
    deadline: new Date('2024-03-15'),
    createdAt: '2024-01-10',
    updatedAt: '2024-02-20',
    avatar: '',
    members: [
      { 
        id: '1', 
        name: '张三', 
        avatar: '', 
        email: 'zhangsan@example.com',
        role: 'member' as const,
        status: 'online' as const,
        createdAt: '2024-01-01',
        updatedAt: '2024-02-01'
      },
      { 
        id: '2', 
        name: '李四', 
        avatar: '', 
        email: 'lisi@example.com',
        role: 'member' as const,
        status: 'online' as const,
        createdAt: '2024-01-01',
        updatedAt: '2024-02-01'
      },
      { 
        id: '3', 
        name: '王五', 
        avatar: '', 
        email: 'wangwu@example.com',
        role: 'member' as const,
        status: 'online' as const,
        createdAt: '2024-01-01',
        updatedAt: '2024-02-01'
      }
    ],
    tasks: []
  },
  {
    id: '2',
    name: '企业官网重构',
    description: '重新设计和开发公司官方网站，提升用户体验',
    status: 'completed',
    progress: 100,
    startDate: '2023-12-01',
    endDate: '2024-02-28',
    memberCount: 5,
    taskCount: 18,
    deadline: new Date('2024-02-28'),
    createdAt: '2023-12-01',
    updatedAt: '2024-02-28',
    avatar: '',
    members: [
      { 
        id: '4', 
        name: '赵六', 
        avatar: '', 
        email: 'zhaoliu@example.com',
        role: 'member' as const,
        status: 'online' as const,
        createdAt: '2024-01-01',
        updatedAt: '2024-02-01'
      },
      { 
        id: '5', 
        name: '钱七', 
        avatar: '', 
        email: 'qianqi@example.com',
        role: 'member' as const,
        status: 'online' as const,
        createdAt: '2024-01-01',
        updatedAt: '2024-02-01'
      }
    ],
    tasks: []
  },
  {
    id: '3',
    name: 'AI智能客服系统',
    description: '基于机器学习的智能客服系统，提供24/7客户支持',
    status: 'paused',
    progress: 45,
    startDate: '2024-01-15',
    endDate: '2024-05-20',
    memberCount: 12,
    taskCount: 36,
    deadline: new Date('2024-05-20'),
    createdAt: '2024-01-15',
    updatedAt: '2024-02-10',
    avatar: '',
    members: [
      { 
        id: '6', 
        name: '孙八', 
        avatar: '', 
        email: 'sunba@example.com',
        role: 'member' as const,
        status: 'online' as const,
        createdAt: '2024-01-01',
        updatedAt: '2024-02-01'
      },
      { 
        id: '7', 
        name: '周九', 
        avatar: '', 
        email: 'zhoujiu@example.com',
        role: 'member' as const,
        status: 'online' as const,
        createdAt: '2024-01-01',
        updatedAt: '2024-02-01'
      },
      { 
        id: '8', 
        name: '吴十', 
        avatar: '', 
        email: 'wushi@example.com',
        role: 'member' as const,
        status: 'online' as const,
        createdAt: '2024-01-01',
        updatedAt: '2024-02-01'
      }
    ],
    tasks: []
  }
])

// 计算属性
const filteredProjects = computed(() => {
  let result = projects.value
  
  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(project => 
      project.name.toLowerCase().includes(query) ||
      project.description.toLowerCase().includes(query)
    )
  }
  
  // 状态过滤
  if (statusFilter.value) {
    result = result.filter(project => project.status === statusFilter.value)
  }
  
  // 排序
  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'created_desc':
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      case 'created_asc':
        return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      case 'name_asc':
        return a.name.localeCompare(b.name)
      case 'name_desc':
        return b.name.localeCompare(a.name)
      case 'progress_asc':
        return a.progress - b.progress
      case 'progress_desc':
        return b.progress - a.progress
      default:
        return 0
    }
  })
  
  return result
})

const totalProjects = computed(() => filteredProjects.value.length)

// 方法
const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    active: 'primary',
    completed: 'success',
    paused: 'warning'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    active: '进行中',
    completed: '已完成',
    paused: '已暂停'
  }
  return statusMap[status] || '未知'
}

const getProgressColor = (progress: number) => {
  if (progress >= 80) return '#67C23A'
  if (progress >= 60) return '#E6A23C'
  if (progress >= 40) return '#409EFF'
  return '#F56C6C'
}

const handleSearch = () => {
  currentPage.value = 1
}

const createProject = () => {
  router.push('/projects/create')
}

const viewProject = (projectId: string | ExtendedProject) => {
  const id = typeof projectId === 'string' ? projectId : projectId.id
  router.push(`/projects/${id}`)
}

const handleProjectAction = async (command: { action: string; project: ExtendedProject }) => {
  const { action, project } = command
  
  switch (action) {
    case 'edit':
      router.push(`/projects/${project.id}/edit`)
      break
    case 'duplicate':
      ElMessage.info('复制功能开发中')
      break
    case 'delete':
      try {
        await ElMessageBox.confirm(
          `确定要删除项目 "${project.name}" 吗？此操作不可恢复。`,
          '删除确认',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        // 执行删除操作
        const index = projects.value.findIndex(p => p.id === project.id)
        if (index > -1) {
          projects.value.splice(index, 1)
          ElMessage.success('项目删除成功')
        }
      } catch {
        // 用户取消删除
      }
      break
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
}

// 生命周期
onMounted(() => {
  // 这里可以调用API获取项目数据
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.project-list-view {
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
  
  .projects-container {
    min-height: 400px;
    
    .projects-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: $spacing-6;
      
      .project-card {
        background: $background-color;
        border-radius: $border-radius-lg;
        box-shadow: $shadow-sm;
        transition: all $transition-base;
        cursor: pointer;
        overflow: hidden;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: $shadow-md;
        }
        
        .card-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: $spacing-4;
          border-bottom: 1px solid $border-color;
          
          .project-avatar {
            width: 40px;
            height: 40px;
            border-radius: $border-radius-base;
            overflow: hidden;
            
            img {
              width: 100%;
              height: 100%;
              object-fit: cover;
            }
            
            .avatar-placeholder {
              width: 100%;
              height: 100%;
              display: flex;
              align-items: center;
              justify-content: center;
              background: $primary-color;
              color: white;
              font-weight: $font-weight-bold;
              font-size: $font-size-lg;
            }
          }
        }
        
        .card-content {
          padding: $spacing-4;
          
          .project-name {
            margin: 0 0 $spacing-2 0;
            font-size: $font-size-lg;
            font-weight: $font-weight-semibold;
            color: $text-primary;
          }
          
          .project-description {
            margin: 0 0 $spacing-4 0;
            font-size: $font-size-sm;
            color: $text-secondary;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
          }
          
          .project-progress {
            margin-bottom: $spacing-4;
            
            .progress-header {
              display: flex;
              align-items: center;
              justify-content: space-between;
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
          
          .project-meta {
            display: flex;
            align-items: center;
            gap: $spacing-4;
            
            .meta-item {
              display: flex;
              align-items: center;
              gap: $spacing-1;
              font-size: $font-size-xs;
              color: $text-secondary;
              
              .el-icon {
                font-size: 14px;
              }
            }
          }
        }
        
        .card-footer {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: $spacing-4;
          border-top: 1px solid $border-color;
          background: $surface-color;
        }
      }
    }
    
    .projects-table {
      background: $background-color;
      border-radius: $border-radius-lg;
      overflow: hidden;
      
      .table-project-info {
        display: flex;
        align-items: center;
        gap: $spacing-3;
        
        .project-avatar.small {
          width: 32px;
          height: 32px;
          border-radius: $border-radius-sm;
          overflow: hidden;
          
          img {
            width: 100%;
            height: 100%;
            object-fit: cover;
          }
          
          .avatar-placeholder {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: $primary-color;
            color: white;
            font-weight: $font-weight-bold;
            font-size: $font-size-sm;
          }
        }
        
        .project-details {
          .project-name {
            font-weight: $font-weight-medium;
            color: $text-primary;
            margin-bottom: $spacing-1;
          }
          
          .project-description {
            font-size: $font-size-sm;
            color: $text-secondary;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
            overflow: hidden;
          }
        }
      }
      
      .table-progress {
        padding-right: $spacing-2;
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
@media (max-width: $breakpoint-lg) {
  .projects-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)) !important;
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
    }
  }
  
  .projects-grid {
    grid-template-columns: 1fr !important;
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