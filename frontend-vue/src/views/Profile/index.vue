<template>
  <div class="profile-page">
    <div class="page-header">
      <h1 class="page-title">我的账户</h1>
    </div>

    <div class="profile-card">
      <!-- 头像和基本信息区域 -->
      <div class="user-header">
        <div class="avatar-section">
          <div class="avatar-container" @mouseenter="showEditIcon = true" @mouseleave="showEditIcon = false"
            @click="openAvatarUpload">
            <el-avatar :size="80" :src="userProfile.avatar" class="user-avatar">
              {{ getNameInitials(userProfile.name) }}
            </el-avatar>
            <div class="avatar-overlay" :class="{ visible: showEditIcon }">
              <el-icon class="edit-icon">
                <Camera />
              </el-icon>
            </div>
          </div>
        </div>
        <div class="user-info">
          <h2 class="user-name">{{ userProfile.name }}</h2>
          <p class="user-email">{{ userProfile.email }}</p>
        </div>
      </div>

      <!-- 用户名输入框 -->
      <div class="form-section">
        <label class="form-label">用户名</label>
        <div class="input-container">
          <el-input v-model="userProfile.name" placeholder="请输入用户名" class="profile-input" maxlength="20" />
        </div>
      </div>

      <!-- 邮箱输入框 -->
      <div class="form-section">
        <label class="form-label">邮箱</label>
        <div class="input-container">
          <el-input v-model="userProfile.email" placeholder="请输入邮箱地址" class="profile-input" type="email" />
        </div>
      </div>

      <!-- 密码重置区域 -->
      <div class="form-section">
        <label class="form-label">密码</label>
        <div class="password-section">
          <p class="password-hint">如果您不想使用验证码登录，可以设置永久密码</p>
          <el-button class="reset-password-btn" @click="openPasswordDialog">
            重置密码
          </el-button>
        </div>
      </div>

      <!-- 账号关联数据 -->
      <div class="form-section">
        <label class="form-label">账号关联数据</label>
        <div class="data-section">
          <p class="data-description">您的账号相关的用户数据。</p>
          <div class="project-list-container">
            <div class="project-header" @click="toggleProjectList">
              <span>显示 {{ projectList.length }} 个项目</span>
              <el-icon class="arrow-icon" :class="{ 'rotated': showProjectDropdown }">
                <ArrowDown />
              </el-icon>
            </div>
            <div v-if="showProjectDropdown" class="project-dropdown">
              <div v-if="projectLoading" class="loading-text">加载中...</div>
              <div v-else-if="projectList.length === 0" class="empty-text">暂无项目</div>
              <div v-else class="project-list">
                <div v-for="project in projectList" :key="project.id" class="project-item">
                  <span class="project-name">{{ project.name }}</span>
                  <span class="project-status" :class="`status-${project.status}`">
                    {{ getStatusText(project.status) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 头像上传弹窗 -->
    <el-dialog v-model="avatarDialogVisible" title="" width="500px" :show-close="true" class="avatar-dialog">
      <div class="upload-content">
        <div class="upload-icon">
          <el-icon>
            <Picture />
          </el-icon>
        </div>
        <p class="upload-text">将图片拖放到此处，或 <span class="browse-link" @click="triggerFileInput">浏览</span></p>
        <p class="upload-hint">支持 PNG、JPG、JPEG、WEBP 和 GIF 格式</p>
        <input ref="fileInput" type="file" accept="image/*" style="display: none" @change="handleFileSelect">
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="avatarDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmAvatarUpload" :disabled="!selectedFile">确认</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 密码重置弹窗 -->
    <el-dialog v-model="passwordDialogVisible" title="重置密码" width="400px" :show-close="true" class="password-dialog">
      <div class="password-form">
        <div class="password-item">
          <label class="password-label">原密码</label>
          <el-input v-model="passwordForm.oldPassword" type="password" placeholder="请输入" class="password-input"
            show-password />
        </div>
        <div class="password-item">
          <label class="password-label">新密码</label>
          <el-input v-model="passwordForm.newPassword" type="password" placeholder="请输入" class="password-input"
            show-password />
        </div>
        <div class="password-item">
          <label class="password-label">确认密码</label>
          <el-input v-model="passwordForm.confirmPassword" type="password" placeholder="请输入" class="password-input"
            show-password />
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="passwordDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="resetPassword">重置</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Camera, Picture, ArrowDown } from '@element-plus/icons-vue'
import { getNameInitials } from '@/utils'
import { projectApi } from '@/api/project'
import type { Project } from '@/types'

// 组件名称
defineOptions({
  name: 'ProfilePage'
})

// 用户资料数据结构
interface UserProfile {
  id: string
  name: string
  email: string
  avatar?: string
}

// 密码表单数据结构
interface PasswordForm {
  oldPassword: string
  newPassword: string
  confirmPassword: string
}

// 响应式数据
const userProfile = reactive<UserProfile>({
  id: 'USER_' + Date.now().toString(36).toUpperCase(),
  name: 'Alfred',
  email: 'alfred@test.com',
  avatar: ''
})

const passwordForm = reactive<PasswordForm>({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 控制状态
const showEditIcon = ref(false)
const avatarDialogVisible = ref(false)
const passwordDialogVisible = ref(false)
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement>()
const showProjectDropdown = ref(false)
const projectLoading = ref(false)
const projectList = ref<Project[]>([])

/**
 * 组件挂载时初始化数据
 */
onMounted(() => {
  loadUserProfile()
  loadProjectList()
})

/**
 * 加载用户资料
 */
const loadUserProfile = () => {
  // 从localStorage加载用户资料
  const savedProfile = localStorage.getItem('userProfile')
  if (savedProfile) {
    const parsed = JSON.parse(savedProfile)
    Object.assign(userProfile, parsed)
  }
}

/**
 * 打开头像上传弹窗
 */
const openAvatarUpload = () => {
  avatarDialogVisible.value = true
}

/**
 * 触发文件选择
 */
const triggerFileInput = () => {
  fileInput.value?.click()
}

/**
 * 处理文件选择
 */
const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    validateAndSetFile(file)
  }
}

/**
 * 验证并设置文件
 */
const validateAndSetFile = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
    return
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB！')
    return
  }

  selectedFile.value = file
}

/**
 * 确认头像上传
 */
const confirmAvatarUpload = () => {
  if (!selectedFile.value) return

  const reader = new FileReader()
  reader.onload = (e) => {
    userProfile.avatar = e.target?.result as string
    saveUserProfile()
    avatarDialogVisible.value = false
    selectedFile.value = null
    ElMessage.success('头像更新成功！')
  }
  reader.readAsDataURL(selectedFile.value)
}

/**
 * 打开密码重置弹窗
 */
const openPasswordDialog = () => {
  // 重置表单
  Object.assign(passwordForm, {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  passwordDialogVisible.value = true
}

/**
 * 重置密码
 */
const resetPassword = () => {
  // 验证表单
  if (!passwordForm.oldPassword.trim()) {
    ElMessage.error('请输入原密码')
    return
  }
  if (!passwordForm.newPassword.trim()) {
    ElMessage.error('请输入新密码')
    return
  }
  if (passwordForm.newPassword.length < 6) {
    ElMessage.error('新密码长度不能少于6位')
    return
  }
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }

  // 模拟密码重置
  ElMessage.success('密码重置成功！')
  passwordDialogVisible.value = false
}

/**
 * 切换项目列表显示状态
 */
const toggleProjectList = () => {
  showProjectDropdown.value = !showProjectDropdown.value
}

/**
 * 加载项目列表
 */
const loadProjectList = async () => {
  try {
    projectLoading.value = true
    const response = await projectApi.getProjects({})
    projectList.value = response.data || []
  } catch (error) {
    console.error('加载项目列表失败:', error)
    ElMessage.error('加载项目列表失败')
  } finally {
    projectLoading.value = false
  }
}

/**
 * 获取项目状态文本
 */
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    active: '进行中',
    completed: '已完成',
    paused: '已暂停',
    archived: '已归档'
  }
  return statusMap[status] || status
}

/**
 * 保存用户资料
 */
const saveUserProfile = () => {
  localStorage.setItem('userProfile', JSON.stringify(userProfile))
}
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.profile-page {
  max-width: 600px;
  margin: 0 auto;
  padding: $spacing-6;

  .page-header {
    margin-bottom: $spacing-6;

    .page-title {
      font-size: $font-size-2xl;
      font-weight: $font-weight-bold;
      color: $text-primary;
      margin: 0;
    }
  }

  .profile-card {
    background: white;
    border-radius: 10px;
    padding: $spacing-8;
    box-shadow: $shadow-sm;
    border: 1px solid $border-color;

    // 用户头像和信息区域
    .user-header {
      display: flex;
      align-items: center;
      gap: $spacing-4;
      margin-bottom: $spacing-8;
      padding: $spacing-4;
      background: #f9fafb;
      border-radius: 10px;

      &:hover {
        background-color: #EFF2F4;
      }

      .avatar-section {
        .avatar-container {
          position: relative;
          cursor: pointer;
          border-radius: 10px;
          overflow: hidden;

          .user-avatar {
            transition: all $transition-base;
          }

          .avatar-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity $transition-base;
            border-radius: 50%;

            &.visible {
              opacity: 1;
            }

            .edit-icon {
              color: white;
              font-size: 24px;
            }
          }
        }
      }

      .user-info {
        flex: 1;

        .user-name {
          font-size: $font-size-lg;
          font-weight: $font-weight-semibold;
          color: $text-primary;
          margin: 0 0 $spacing-1 0;
        }

        .user-email {
          font-size: $font-size-sm;
          color: $text-secondary;
          margin: 0;
        }
      }
    }

    // 表单区域
    .form-section {
      margin-bottom: $spacing-6;

      .form-label {
        display: block;
        font-size: $font-size-sm;
        font-weight: $font-weight-medium;
        color: $text-primary;
        margin-bottom: $spacing-2;
      }

      .input-container {
        display: flex;
        align-items: center;
        gap: $spacing-2;

        .profile-input {
          flex: 1;

          :deep(.el-input__wrapper) {
            background-color: #f9fafb;
            border: none;
            border-radius: 10px;
            box-shadow: none;
            transition: all $transition-base;

            &:hover {
              background-color: #EFF2F4;
            }

            &.is-focus {
              background-color: white;
              border: 1px solid $primary-color;
              box-shadow: 0 0 0 2px rgba($primary-color, 0.1);
            }
          }
        }
      }

      // 密码区域
      .password-section {
        display: flex;
        align-items: center;
        gap: $spacing-4;

        .password-hint {
          font-size: $font-size-sm;
          color: $text-secondary;
          margin: 0;
          flex: 1;
        }

        .reset-password-btn {
          background-color: $gray-50;
          border: none;
          border-radius: 10px;
          color: $text-primary;
          padding: $spacing-2 $spacing-4;
          transition: all $transition-base;
          flex-shrink: 0;

          &:hover {
            background-color: $gray-100;
          }
        }
      }

      // 数据区域
      .data-section {
        .data-description {
          font-size: $font-size-sm;
          color: $text-secondary;
          margin: 0 0 $spacing-3 0;
        }

        .project-list-container {
          width: 100%;
        }

        .project-header {
          width: 100%;
          height: 40px;
          background: #f9fafb;
          border: none;
          border-radius: 10px;
          color: #666;
          font-size: 14px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 16px;
          cursor: pointer;
          transition: all 0.3s ease;

          &:hover {
            background: #EFF2F4;
          }
        }

        .arrow-icon {
          color: #999;
          font-size: 16px;
          transition: transform 0.3s ease;

          &.rotated {
            transform: rotate(180deg);
          }
        }

        .project-dropdown {
          margin-top: 8px;
          background: #fff;
          border: 1px solid #e0e0e0;
          border-radius: 10px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
          max-height: 200px;
          overflow-y: auto;
        }

        .loading-text,
        .empty-text {
          padding: 16px;
          text-align: center;
          color: #999;
          font-size: 14px;
        }

        .project-list {
          padding: 8px 0;
        }

        .project-item {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 12px 16px;
          border-bottom: 1px solid #f0f0f0;
          transition: background-color 0.2s ease;

          &:last-child {
            border-bottom: none;
          }

          &:hover {
            background-color: #f8f9fa;
          }
        }

        .project-name {
          font-size: 14px;
          color: #333;
          font-weight: 500;
        }

        .project-status {
          font-size: 12px;
          padding: 4px 8px;
          border-radius: 12px;
          font-weight: 500;
        }

        .status-active {
          background: #e7f5e7;
          color: #52c41a;
        }

        .status-completed {
          background: #e6f7ff;
          color: #1890ff;
        }

        .status-paused {
          background: #fff7e6;
          color: #fa8c16;
        }

        .status-archived {
          background: #f5f5f5;
          color: #999;
        }
      }
    }
  }
}

// 头像上传弹窗样式
:deep(.avatar-dialog) {
  .el-dialog__header {
    padding: $spacing-4 $spacing-6 0;
  }

  .el-dialog__body {
    padding: $spacing-4 $spacing-6;

    .upload-content {
      text-align: center;
      padding: $spacing-8 $spacing-4;
      border: 2px dashed $border-color;
      border-radius: 10px;
      background-color: $gray-50;

      .upload-icon {
        font-size: 48px;
        color: $text-secondary;
        margin-bottom: $spacing-4;
      }

      .upload-text {
        font-size: $font-size-base;
        color: $text-primary;
        margin: 0 0 $spacing-2 0;

        .browse-link {
          color: $primary-color;
          cursor: pointer;
          text-decoration: underline;

          &:hover {
            color: $primary-600;
          }
        }
      }

      .upload-hint {
        font-size: $font-size-sm;
        color: $text-secondary;
        margin: 0;
      }
    }
  }

  .el-dialog__footer {
    padding: 0 $spacing-6 $spacing-4;

    .dialog-footer {
      display: flex;
      justify-content: flex-end;
      gap: $spacing-3;

      .el-button {
        border-radius: 10px;
        padding: $spacing-2 $spacing-4;
      }
    }
  }
}

// 密码重置弹窗样式
:deep(.password-dialog) {
  .el-dialog__header {
    padding: $spacing-4 $spacing-6 0;
  }

  .el-dialog__body {
    padding: $spacing-4 $spacing-6;

    .password-form {
      .password-item {
        margin-bottom: $spacing-4;

        .password-label {
          display: block;
          font-size: $font-size-sm;
          font-weight: $font-weight-medium;
          color: $text-primary;
          margin-bottom: $spacing-2;
        }

        .password-input {
          :deep(.el-input__wrapper) {
            background-color: $gray-50;
            border: none;
            border-radius: 10px;
            box-shadow: none;
            transition: all $transition-base;

            &:hover {
              background-color: $gray-100;
            }

            &.is-focus {
              background-color: white;
              border: 1px solid $primary-color;
              box-shadow: 0 0 0 2px rgba($primary-color, 0.1);
            }
          }
        }
      }
    }
  }

  .el-dialog__footer {
    padding: 0 $spacing-6 $spacing-4;

    .dialog-footer {
      display: flex;
      justify-content: flex-end;
      gap: $spacing-3;

      .el-button {
        border-radius: 10px;
        padding: $spacing-2 $spacing-4;
      }
    }
  }
}

// 响应式设计
@media (max-width: $breakpoint-md) {
  .profile-page {
    padding: $spacing-4;

    .profile-card {
      padding: $spacing-4;

      .user-header {
        flex-direction: column;
        text-align: center;
        gap: $spacing-3;
      }

      .form-section {
        .input-container {
          flex-direction: column;
          align-items: stretch;
        }
      }
    }
  }
}
</style>