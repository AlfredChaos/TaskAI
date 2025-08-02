<template>
  <div class="settings-page">
    <div class="page-header">
      <h1 class="page-title">设置</h1>
      <p class="page-description">管理您的工作时间和休息日设置</p>
    </div>

    <div class="settings-content">
      <!-- 工作日设置 -->
      <div class="settings-section">
        <div class="section-header">
          <h2 class="section-title">工作日设置</h2>
          <p class="section-description">配置您的工作时间安排</p>
        </div>

        <div class="setting-card">
          <div class="setting-item">
            <label class="setting-label">工作日</label>
            <el-select v-model="workSettings.workDays" placeholder="选择工作日" class="setting-select">
              <el-option label="周一到周日" value="1-7" />
              <el-option label="周一到周六" value="1-6" />
              <el-option label="周一到周五" value="1-5" />
            </el-select>
          </div>

          <div class="setting-item">
            <label class="setting-label">工作时间</label>
            <div class="time-range">
              <el-time-picker v-model="workSettings.startTime" placeholder="开始时间" format="HH:mm" value-format="HH:mm"
                class="time-picker" />
              <span class="time-separator">至</span>
              <el-time-picker v-model="workSettings.endTime" placeholder="结束时间" format="HH:mm" value-format="HH:mm"
                class="time-picker" />
            </div>
          </div>

          <div class="setting-actions">
            <el-button type="primary" class="save-btn" @click="saveWorkSettings">
              保存工作日设置
            </el-button>
          </div>
        </div>
      </div>

      <!-- 休息日设置 -->
      <div class="settings-section">
        <div class="section-header">
          <h2 class="section-title">休息日设置</h2>
          <p class="section-description">管理您的休息日和假期安排</p>
        </div>

        <div class="setting-card">
          <!-- 添加休息日 -->
          <div class="add-holiday">
            <h3 class="subsection-title">添加休息日</h3>
            <div class="holiday-form">
              <el-date-picker v-model="newHoliday.date" type="date" placeholder="选择日期" class="date-picker"
                format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
              <el-input v-model="newHoliday.reason" placeholder="休息日原因" class="reason-input" maxlength="50"
                show-word-limit />
              <el-button type="primary" class="add-btn" @click="addHoliday">
                添加
              </el-button>
            </div>
          </div>

          <!-- 快速设置 -->
          <div class="quick-settings">
            <h3 class="subsection-title">快速设置</h3>
            <div class="quick-actions">
              <el-button class="quick-btn" @click="setWeekendsAsHolidays">
                设置周末为休息日
              </el-button>
              <el-button class="quick-btn" @click="setNationalHolidays">
                设置法定节假日
              </el-button>
            </div>
          </div>

          <!-- 休息日列表 -->
          <div class="holidays-list">
            <h3 class="subsection-title">当前休息日</h3>
            <div v-if="holidays.length === 0" class="empty-state">
              <p>暂无休息日设置</p>
            </div>
            <div v-else class="holiday-items">
              <div v-for="holiday in holidays" :key="holiday.id" class="holiday-item">
                <div class="holiday-info">
                  <span class="holiday-date">{{ formatDate(holiday.date) }}</span>
                  <span class="holiday-reason">{{ holiday.reason }}</span>
                </div>
                <el-button type="text" class="delete-btn" @click="removeHoliday(holiday.id)">
                  删除
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { defineOptions } from 'vue'

// Name
defineOptions({ name: 'SettingsPage' })

// 接口定义
interface WorkSettings {
  workDays: string
  startTime: string
  endTime: string
}

interface Holiday {
  id: string
  date: string
  reason: string
}

interface NewHoliday {
  date: string
  reason: string
}

// 响应式数据
const workSettings = ref<WorkSettings>({
  workDays: '1-5',
  startTime: '09:00',
  endTime: '18:00'
})

const newHoliday = ref<NewHoliday>({
  date: '',
  reason: ''
})

const holidays = ref<Holiday[]>([])

/**
 * 保存工作日设置
 */
const saveWorkSettings = () => {
  // 验证时间设置
  if (!workSettings.value.startTime || !workSettings.value.endTime) {
    ElMessage.error('请设置完整的工作时间')
    return
  }

  if (workSettings.value.startTime >= workSettings.value.endTime) {
    ElMessage.error('开始时间必须早于结束时间')
    return
  }

  // 保存到本地存储
  localStorage.setItem('workSettings', JSON.stringify(workSettings.value))
  ElMessage.success('工作日设置保存成功')
}

/**
 * 添加休息日
 */
const addHoliday = () => {
  if (!newHoliday.value.date) {
    ElMessage.error('请选择日期')
    return
  }

  if (!newHoliday.value.reason.trim()) {
    ElMessage.error('请填写休息日原因')
    return
  }

  // 检查是否已存在
  const exists = holidays.value.some(h => h.date === newHoliday.value.date)
  if (exists) {
    ElMessage.error('该日期已设置为休息日')
    return
  }

  // 添加新休息日
  const holiday: Holiday = {
    id: Date.now().toString(),
    date: newHoliday.value.date,
    reason: newHoliday.value.reason.trim()
  }

  holidays.value.push(holiday)
  holidays.value.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())

  // 保存到本地存储
  saveHolidays()

  // 重置表单
  newHoliday.value = { date: '', reason: '' }

  ElMessage.success('休息日添加成功')
}

/**
 * 删除休息日
 */
const removeHoliday = (id: string) => {
  holidays.value = holidays.value.filter(h => h.id !== id)
  saveHolidays()
  ElMessage.success('休息日删除成功')
}

/**
 * 设置周末为休息日
 */
const setWeekendsAsHolidays = () => {
  const currentYear = new Date().getFullYear()
  const weekends: Holiday[] = []

  // 生成当年所有周末
  for (let month = 0; month < 12; month++) {
    const daysInMonth = new Date(currentYear, month + 1, 0).getDate()
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(currentYear, month, day)
      const dayOfWeek = date.getDay()

      if (dayOfWeek === 0 || dayOfWeek === 6) { // 周日或周六
        const dateStr = date.toISOString().split('T')[0]
        const exists = holidays.value.some(h => h.date === dateStr)

        if (!exists) {
          weekends.push({
            id: `weekend-${dateStr}`,
            date: dateStr,
            reason: dayOfWeek === 0 ? '周日' : '周六'
          })
        }
      }
    }
  }

  holidays.value.push(...weekends)
  holidays.value.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
  saveHolidays()

  ElMessage.success(`已添加 ${weekends.length} 个周末休息日`)
}

/**
 * 设置法定节假日
 */
const setNationalHolidays = () => {
  const currentYear = new Date().getFullYear()
  const nationalHolidays: Holiday[] = [
    { id: `ny-${currentYear}`, date: `${currentYear}-01-01`, reason: '元旦' },
    { id: `cny1-${currentYear}`, date: `${currentYear}-02-10`, reason: '春节' },
    { id: `cny2-${currentYear}`, date: `${currentYear}-02-11`, reason: '春节' },
    { id: `cny3-${currentYear}`, date: `${currentYear}-02-12`, reason: '春节' },
    { id: `tomb-${currentYear}`, date: `${currentYear}-04-05`, reason: '清明节' },
    { id: `labor-${currentYear}`, date: `${currentYear}-05-01`, reason: '劳动节' },
    { id: `dragon-${currentYear}`, date: `${currentYear}-06-10`, reason: '端午节' },
    { id: `mid-${currentYear}`, date: `${currentYear}-09-17`, reason: '中秋节' },
    { id: `national1-${currentYear}`, date: `${currentYear}-10-01`, reason: '国庆节' },
    { id: `national2-${currentYear}`, date: `${currentYear}-10-02`, reason: '国庆节' },
    { id: `national3-${currentYear}`, date: `${currentYear}-10-03`, reason: '国庆节' }
  ]

  const newHolidays = nationalHolidays.filter(nh =>
    !holidays.value.some(h => h.date === nh.date)
  )

  holidays.value.push(...newHolidays)
  holidays.value.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
  saveHolidays()

  ElMessage.success(`已添加 ${newHolidays.length} 个法定节假日`)
}

/**
 * 保存休息日到本地存储
 */
const saveHolidays = () => {
  localStorage.setItem('holidays', JSON.stringify(holidays.value))
}

/**
 * 格式化日期显示
 */
const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr)
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const weekday = weekdays[date.getDay()]
  return `${dateStr} (${weekday})`
}

/**
 * 加载设置数据
 */
const loadSettings = () => {
  // 加载工作日设置
  const savedWorkSettings = localStorage.getItem('workSettings')
  if (savedWorkSettings) {
    workSettings.value = JSON.parse(savedWorkSettings)
  }

  // 加载休息日设置
  const savedHolidays = localStorage.getItem('holidays')
  if (savedHolidays) {
    holidays.value = JSON.parse(savedHolidays)
  }
}

// 组件挂载时加载设置
onMounted(() => {
  loadSettings()
})
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.settings-page {
  padding: $spacing-6;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: $spacing-8;

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

.settings-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-8;
}

.settings-section {
  .section-header {
    margin-bottom: $spacing-6;

    .section-title {
      font-size: $font-size-xl;
      font-weight: $font-weight-semibold;
      color: $text-primary;
      margin: 0 0 $spacing-1 0;
    }

    .section-description {
      font-size: $font-size-sm;
      color: $text-secondary;
      margin: 0;
    }
  }
}

.setting-card {
  background: white;
  border-radius: 10px;
  padding: $spacing-6;
  border: 1px solid $border-color;
}

.setting-item {
  display: flex;
  align-items: center;
  margin-bottom: $spacing-6;

  &:last-child {
    margin-bottom: 0;
  }

  .setting-label {
    min-width: 120px;
    font-size: $font-size-base;
    font-weight: $font-weight-medium;
    color: $text-primary;
    margin-right: $spacing-4;
  }
}

.setting-select {
  width: 200px;

  :deep(.el-select__wrapper) {
    border-radius: 10px;
    border: 1px solid $border-color;
    box-shadow: none;

    &:hover {
      border-color: $primary-color;
    }

    &.is-focused {
      border-color: $primary-color;
      box-shadow: none;
    }
  }
}

.time-range {
  display: flex;
  align-items: center;
  gap: $spacing-3;

  .time-picker {
    width: 120px;

    :deep(.el-input__wrapper) {
      border-radius: 10px;
      border: 1px solid $border-color;
      box-shadow: none;

      &:hover {
        border-color: $primary-color;
      }

      &.is-focus {
        border-color: $primary-color;
        box-shadow: none;
      }
    }
  }

  .time-separator {
    color: $text-secondary;
    font-size: $font-size-sm;
  }
}

.setting-actions {
  margin-top: $spacing-6;
  padding-top: $spacing-6;
  border-top: 1px solid $border-color;
}

.save-btn {
  border-radius: 10px;
  border: none;
  box-shadow: none;
  padding: $spacing-3 $spacing-6;
  font-weight: $font-weight-medium;

  &:hover {
    transform: translateY(-1px);
  }
}

.add-holiday {
  margin-bottom: $spacing-8;

  .holiday-form {
    display: flex;
    gap: $spacing-4;
    align-items: flex-start;
    flex-wrap: wrap;

    .date-picker {
      width: 200px;

      :deep(.el-input__wrapper) {
        border-radius: 10px;
        border: 1px solid $border-color;
        box-shadow: none;

        &:hover {
          border-color: $primary-color;
        }

        &.is-focus {
          border-color: $primary-color;
          box-shadow: none;
        }
      }
    }

    .reason-input {
      flex: 1;
      min-width: 200px;

      :deep(.el-input__wrapper) {
        border-radius: 10px;
        border: 1px solid $border-color;
        box-shadow: none;

        &:hover {
          border-color: $primary-color;
        }

        &.is-focus {
          border-color: $primary-color;
          box-shadow: none;
        }
      }
    }

    .add-btn {
      border-radius: 10px;
      border: none;
      box-shadow: none;
      padding: $spacing-3 $spacing-4;
      font-weight: $font-weight-medium;

      &:hover {
        transform: translateY(-1px);
      }
    }
  }
}

.quick-settings {
  margin-bottom: $spacing-8;

  .quick-actions {
    display: flex;
    gap: $spacing-4;
    flex-wrap: wrap;

    .quick-btn {
      border-radius: 10px;
      border: 1px solid $border-color;
      box-shadow: none;
      padding: $spacing-3 $spacing-4;
      font-weight: $font-weight-medium;
      background: white;
      color: $text-primary;

      &:hover {
        border-color: $primary-color;
        color: $primary-color;
        transform: translateY(-1px);
      }
    }
  }
}

.subsection-title {
  font-size: $font-size-lg;
  font-weight: $font-weight-semibold;
  color: $text-primary;
  margin: 0 0 $spacing-4 0;
}

.holidays-list {
  .empty-state {
    text-align: center;
    padding: $spacing-8;
    color: $text-secondary;

    p {
      margin: 0;
      font-size: $font-size-base;
    }
  }

  .holiday-items {
    display: flex;
    flex-direction: column;
    gap: $spacing-3;

    .holiday-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: $spacing-4;
      background: $gray-50;
      border-radius: 10px;
      border: 1px solid $border-color;

      .holiday-info {
        display: flex;
        flex-direction: column;
        gap: $spacing-1;

        .holiday-date {
          font-size: $font-size-base;
          font-weight: $font-weight-medium;
          color: $text-primary;
        }

        .holiday-reason {
          font-size: $font-size-sm;
          color: $text-secondary;
        }
      }

      .delete-btn {
        color: $danger-color;
        border: none;
        box-shadow: none;
        padding: $spacing-1 $spacing-2;

        &:hover {
          background: rgba($danger-color, 0.1);
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: $breakpoint-md) {
  .settings-page {
    padding: $spacing-4;
  }

  .setting-item {
    flex-direction: column;
    align-items: flex-start;
    gap: $spacing-2;

    .setting-label {
      min-width: auto;
      margin-right: 0;
    }
  }

  .time-range {
    width: 100%;

    .time-picker {
      flex: 1;
    }
  }

  .holiday-form {
    flex-direction: column;

    .date-picker,
    .reason-input {
      width: 100%;
    }
  }

  .quick-actions {
    flex-direction: column;

    .quick-btn {
      width: 100%;
    }
  }
}
</style>