<template>
  <div class="dashboard-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">仪表板</h1>
      <p class="page-subtitle">欢迎回来，{{ currentUser?.name || 'Admin' }}！</p>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card" v-for="stat in stats" :key="stat.key">
        <div class="stat-icon" :class="stat.iconClass">
          <component :is="stat.icon" />
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
          <div class="stat-change" :class="stat.changeClass">
            <el-icon><ArrowUp v-if="stat.trend === 'up'" /><ArrowDown v-else /></el-icon>
            {{ stat.change }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-section">
      <el-row :gutter="24">
        <el-col :span="16">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>项目进度趋势</span>
                <el-select v-model="chartPeriod" size="small" style="width: 120px">
                  <el-option label="最近7天" value="7d" />
                  <el-option label="最近30天" value="30d" />
                  <el-option label="最近90天" value="90d" />
                </el-select>
              </div>
            </template>
            <div ref="progressChartRef" class="chart-container"></div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card class="chart-card">
            <template #header>
              <span>任务状态分布</span>
            </template>
            <div ref="statusChartRef" class="chart-container"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 最近活动和快速操作 -->
    <div class="bottom-section">
      <el-row :gutter="24">
        <el-col :span="12">
          <el-card class="activity-card">
            <template #header>
              <div class="card-header">
                <span>最近活动</span>
                <el-link type="primary" :underline="false" @click="viewAllActivities">
                  查看全部
                </el-link>
              </div>
            </template>
            <div class="activity-list">
              <div class="activity-item" v-for="activity in recentActivities" :key="activity.id">
                <el-avatar :size="32" :src="activity.user.avatar">
                  {{ activity.user.name.charAt(0) }}
                </el-avatar>
                <div class="activity-content">
                  <div class="activity-text">
                    <strong>{{ activity.user.name }}</strong>
                    {{ activity.action }}
                    <strong>{{ activity.target }}</strong>
                  </div>
                  <div class="activity-time">{{ formatTime(activity.createdAt) }}</div>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card class="quick-actions-card">
            <template #header>
              <span>快速操作</span>
            </template>
            <div class="quick-actions">
              <div class="action-item" @click="createProject">
                <div class="action-icon project">
                  <el-icon><Folder /></el-icon>
                </div>
                <div class="action-text">
                  <div class="action-title">创建项目</div>
                  <div class="action-desc">开始一个新项目</div>
                </div>
              </div>
              
              <div class="action-item" @click="createTask">
                <div class="action-icon task">
                  <el-icon><List /></el-icon>
                </div>
                <div class="action-text">
                  <div class="action-title">创建任务</div>
                  <div class="action-desc">添加新的任务</div>
                </div>
              </div>
              
              <div class="action-item" @click="inviteUser">
                <div class="action-icon user">
                  <el-icon><Plus /></el-icon>
                </div>
                <div class="action-text">
                  <div class="action-title">邀请成员</div>
                  <div class="action-desc">邀请团队成员</div>
                </div>
              </div>
              
              <div class="action-item" @click="viewReports">
                <div class="action-icon report">
                  <el-icon><TrendCharts /></el-icon>
                </div>
                <div class="action-text">
                  <div class="action-title">查看报告</div>
                  <div class="action-desc">项目统计报告</div>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts" name="DashboardView">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Odometer,
  Folder,
  List,
  User,
  ArrowUp,
  ArrowDown,
  Plus,
  TrendCharts
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { getRelativeTime } from '@/utils'

const router = useRouter()

// 响应式数据
const progressChartRef = ref<HTMLElement>()
const statusChartRef = ref<HTMLElement>()
const chartPeriod = ref('30d')

// 计算属性
const currentUser = computed(() => ({ name: 'Admin' }))

// 统计数据
const stats = ref([
  {
    key: 'projects',
    label: '活跃项目',
    value: '12',
    change: '+2.5%',
    trend: 'up',
    changeClass: 'positive',
    icon: Folder,
    iconClass: 'project'
  },
  {
    key: 'tasks',
    label: '待办任务',
    value: '48',
    change: '-5.2%',
    trend: 'down',
    changeClass: 'negative',
    icon: List,
    iconClass: 'task'
  },
  {
    key: 'members',
    label: '团队成员',
    value: '24',
    change: '+12.3%',
    trend: 'up',
    changeClass: 'positive',
    icon: User,
    iconClass: 'user'
  },
  {
    key: 'completion',
    label: '完成率',
    value: '85%',
    change: '+3.1%',
    trend: 'up',
    changeClass: 'positive',
    icon: Odometer,
    iconClass: 'completion'
  }
])

// 最近活动数据
const recentActivities = ref([
  {
    id: 1,
    user: { name: '张三', avatar: '' },
    action: '完成了任务',
    target: '用户界面设计',
    createdAt: new Date(Date.now() - 1000 * 60 * 30) // 30分钟前
  },
  {
    id: 2,
    user: { name: '李四', avatar: '' },
    action: '创建了项目',
    target: '移动端应用开发',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 2) // 2小时前
  },
  {
    id: 3,
    user: { name: '王五', avatar: '' },
    action: '更新了任务',
    target: '数据库优化',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 4) // 4小时前
  },
  {
    id: 4,
    user: { name: '赵六', avatar: '' },
    action: '评论了任务',
    target: 'API接口开发',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 8) // 8小时前
  }
])

// 方法
const formatTime = (date: Date) => {
  return getRelativeTime(date)
}

const initCharts = () => {
  // 初始化进度趋势图
  if (progressChartRef.value) {
    const progressChart = echarts.init(progressChartRef.value)
    const progressOption = {
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
      },
      yAxis: {
        type: 'value',
        max: 100
      },
      series: [
        {
          name: '完成率',
          type: 'line',
          smooth: true,
          data: [65, 72, 68, 75, 82, 78, 85],
          itemStyle: {
            color: '#409EFF'
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
                { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
              ]
            }
          }
        }
      ]
    }
    progressChart.setOption(progressOption)
  }
  
  // 初始化状态分布图
  if (statusChartRef.value) {
    const statusChart = echarts.init(statusChartRef.value)
    const statusOption = {
      tooltip: {
        trigger: 'item'
      },
      series: [
        {
          type: 'pie',
          radius: ['40%', '70%'],
          data: [
            { value: 35, name: '进行中', itemStyle: { color: '#409EFF' } },
            { value: 25, name: '已完成', itemStyle: { color: '#67C23A' } },
            { value: 15, name: '待开始', itemStyle: { color: '#E6A23C' } },
            { value: 10, name: '已暂停', itemStyle: { color: '#F56C6C' } }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    }
    statusChart.setOption(statusOption)
  }
}

const createProject = () => {
  router.push('/projects/create')
}

const createTask = () => {
  router.push('/tasks/create')
}

const inviteUser = () => {
  ElMessage.info('邀请功能开发中')
}

const viewReports = () => {
  ElMessage.info('报告功能开发中')
}

const viewAllActivities = () => {
  router.push('/activities')
}

// 生命周期
onMounted(() => {
  initCharts()
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.dashboard-view {
  .page-header {
    margin-bottom: $spacing-6;
    
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
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: $spacing-6;
    margin-bottom: $spacing-8;
    
    .stat-card {
      display: flex;
      align-items: center;
      padding: $spacing-6;
      background: $background-color;
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
        
        .el-icon {
          font-size: 24px;
          color: white;
        }
        
        &.project {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        &.task {
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        
        &.user {
          background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        
        &.completion {
          background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }
      }
      
      .stat-content {
        flex: 1;
        
        .stat-value {
          font-size: $font-size-2xl;
          font-weight: $font-weight-bold;
          color: $text-primary;
          margin-bottom: $spacing-1;
        }
        
        .stat-label {
          font-size: $font-size-sm;
          color: $text-secondary;
          margin-bottom: $spacing-2;
        }
        
        .stat-change {
          display: flex;
          align-items: center;
          gap: $spacing-1;
          font-size: $font-size-sm;
          font-weight: $font-weight-medium;
          
          &.positive {
            color: $success-color;
          }
          
          &.negative {
            color: $danger-color;
          }
          
          .el-icon {
            font-size: 12px;
          }
        }
      }
    }
  }
  
  .charts-section {
    margin-bottom: $spacing-8;
    
    .chart-card {
      .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }
      
      .chart-container {
        height: 300px;
      }
    }
  }
  
  .bottom-section {
    .activity-card {
      .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }
      
      .activity-list {
        .activity-item {
          display: flex;
          align-items: flex-start;
          gap: $spacing-3;
          padding: $spacing-3 0;
          border-bottom: 1px solid $border-color;
          
          &:last-child {
            border-bottom: none;
          }
          
          .activity-content {
            flex: 1;
            
            .activity-text {
              font-size: $font-size-sm;
              color: $text-primary;
              margin-bottom: $spacing-1;
              
              strong {
                color: $primary-color;
              }
            }
            
            .activity-time {
              font-size: $font-size-xs;
              color: $text-secondary;
            }
          }
        }
      }
    }
    
    .quick-actions-card {
      .quick-actions {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: $spacing-4;
        
        .action-item {
          display: flex;
          align-items: center;
          gap: $spacing-3;
          padding: $spacing-4;
          border-radius: $border-radius-base;
          cursor: pointer;
          transition: background-color $transition-base;
          
          &:hover {
            background-color: $gray-50;
          }
          
          .action-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border-radius: $border-radius-base;
            
            .el-icon {
              font-size: 20px;
              color: white;
            }
            
            &.project {
              background: $primary-color;
            }
            
            &.task {
              background: $success-color;
            }
            
            &.user {
              background: $warning-color;
            }
            
            &.report {
              background: $info;
            }
          }
          
          .action-text {
            .action-title {
              font-size: $font-size-sm;
              font-weight: $font-weight-medium;
              color: $text-primary;
              margin-bottom: $spacing-1;
            }
            
            .action-desc {
              font-size: $font-size-xs;
              color: $text-secondary;
            }
          }
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: $breakpoint-lg) {
  .charts-section {
    .el-col {
      margin-bottom: $spacing-6;
    }
  }
  
  .bottom-section {
    .el-col {
      margin-bottom: $spacing-6;
    }
  }
}

@media (max-width: $breakpoint-md) {
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
  
  .quick-actions {
    grid-template-columns: 1fr !important;
  }
}
</style>