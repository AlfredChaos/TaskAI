<template>
  <div class="reports-container">
    <!-- 左侧报告管理 -->
    <div class="reports-sidebar">
      <!-- 搜索和过滤区域 -->
      <div class="search-section">
        <el-input v-model="searchQuery" placeholder="搜索报告..." prefix-icon="Search" clearable @input="handleSearch" />

        <!-- 创建报告按钮 -->
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon>
            <Plus />
          </el-icon>
          创建报告
        </el-button>
      </div>

      <!-- 过滤器 -->
      <div class="filters">
        <el-select v-model="selectedType" placeholder="报告类型" clearable @change="handleFilter">
          <el-option label="全部" value="" />
          <el-option label="日报" value="daily" />
          <el-option label="周报" value="weekly" />
        </el-select>

        <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始日期"
          end-placeholder="结束日期" format="YYYY-MM-DD" value-format="YYYY-MM-DD" @change="handleFilter"
          style="height: 40px; line-height: 40px; border-radius: 10px; width: 100%;" />
      </div>

      <!-- 报告列表 -->
      <div class="reports-list">
        <div v-for="report in filteredReports" :key="report.id" class="report-card"
          :class="{ active: selectedReport?.id === report.id }" @click="selectReport(report)">
          <div class="report-header">
            <div class="report-icon">
              <el-icon v-if="report.type === 'daily'">
                <Calendar />
              </el-icon>
              <el-icon v-else>
                <DataAnalysis />
              </el-icon>
            </div>
            <div class="report-date">{{ formatDate(report.createdAt) }}</div>
          </div>

          <div class="report-content">
            <h4 class="report-title">{{ report.title }}</h4>
            <p class="report-preview">{{ getPreviewText(report.content) }}</p>
          </div>

          <div class="report-footer">
            <el-badge v-if="report.isNew" is-dot class="new-badge" />
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧AI聊天界面 -->
    <div class="chat-container">
      <!-- 聊天头部 -->
      <div class="chat-header">
        <div class="ai-info">
          <div class="ai-avatar">
            <img :src="getAIProviderLogo(aiProvider)" :alt="aiProvider + ' Logo'" class="provider-logo"
              @error="handleImageError" />
          </div>
          <div class="ai-name">
            智能报告助手 | {{ aiProvider }}
            <span v-if="isTyping" class="typing-indicator">正在输入...</span>
          </div>
        </div>

        <div class="chat-actions">
          <el-button type="text" @click="clearContext">
            <el-icon>
              <Delete />
            </el-icon>
            清除上下文
          </el-button>
          <el-button type="text" @click="showProviderDialog = true">
            <el-icon>
              <Setting />
            </el-icon>
            AI供应商
          </el-button>
        </div>
      </div>

      <!-- 聊天消息区域 -->
      <div class="chat-messages" ref="messagesContainer">
        <div v-for="message in messages" :key="message.id" class="message-wrapper">
          <div class="message"
            :class="{ 'user-message': message.role === 'user', 'ai-message': message.role === 'assistant' }">
            <!-- 消息头像 -->
            <div class="message-avatar">
              <!-- 用户头像 -->
              <el-avatar v-if="message.role === 'user'" :size="32" class="user-avatar">
                {{ getNameInitials('User') }}
              </el-avatar>
              <!-- AI头像 -->
              <div v-else class="ai-message-avatar">
                <img :src="getAIProviderLogo(message.aiProvider || aiProvider)"
                  :alt="(message.aiProvider || aiProvider) + ' Logo'" class="ai-provider-logo"
                  @error="handleImageError" />
              </div>
            </div>
            <div class="message-right">
              <!-- AI思考过程 -->
              <div v-if="message.thinking && message.role === 'assistant'" class="thinking-wrapper">
                <div class="thinking-header" @click="message.expandedThinking = !message.expandedThinking">
                  <span class="thinking-title">显示思路</span>
                  <el-icon class="thinking-toggle" :class="{ expanded: message.expandedThinking }">
                    <ArrowDown />
                  </el-icon>
                </div>
                <div v-if="message.expandedThinking" class="thinking-content">
                  <div class="thinking-text">{{ message.thinking }}</div>
                </div>
              </div>

              <!-- AI回复内容 - 独立区域 -->
              <div class="message-content">
                <div class="message-text" v-html="renderMarkdown(message.content)"></div>

                <!-- 功能按钮（仅AI消息后显示） -->
                <div v-if="message.role === 'assistant' && message.showActions" class="action-buttons">
                  <el-button type="primary" @click="generateReport('daily')">
                    <el-icon>
                      <Calendar />
                    </el-icon>
                    生成日报
                  </el-button>
                  <el-button type="primary" @click="generateReport('weekly')">
                    <el-icon>
                      <DataAnalysis />
                    </el-icon>
                    生成周报
                  </el-button>
                </div>
              </div>

              <!-- 消息元信息 -->
              <div class="message-meta">
                <el-button type="text" size="small" @click="copyMessage(message.content)">
                  <el-icon>
                    <CopyDocument />
                  </el-icon>
                </el-button>
                <span v-if="message.tokens" class="token-count">{{ message.tokens }} tokens</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 流式输出指示器 -->
        <div v-if="isStreaming" class="streaming-indicator">
          <div class="message ai-message">
            <!-- AI头像 -->
            <div class="message-avatar">
              <div class="ai-message-avatar">
                <img :src="getAIProviderLogo(aiProvider)" :alt="aiProvider + ' Logo'" class="ai-provider-logo"
                  @error="handleImageError" />
              </div>
            </div>
            <div class="message-right">
              <div class="message-content">
                <div class="typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 聊天输入区域 -->
      <div class="chat-input">
        <el-input v-model="inputMessage" type="textarea" :autosize="{ minRows: 3, maxRows: 6 }"
          placeholder="输入消息... 使用@提及项目或任务，按Enter发送" @keydown.enter="sendMessage" @input="handleInputChange" />

        <!-- @提及建议 -->
        <div v-if="showMentions" class="mentions-popup">
          <div v-for="item in mentionSuggestions" :key="item.id" class="mention-item" @click="selectMention(item)">
            <span class="mention-icon">{{ item.type === 'project' ? '📁' : '📋' }}</span>
            <span>{{ item.name }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建报告对话框 -->
    <el-dialog v-model="showCreateDialog" title="创建报告" width="600px">
      <el-form :model="newReport" label-width="80px">
        <el-form-item label="报告类型">
          <el-radio-group v-model="newReport.type">
            <el-radio label="daily">日报</el-radio>
            <el-radio label="weekly">周报</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="报告标题">
          <el-input v-model="newReport.title" placeholder="请输入报告标题" />
        </el-form-item>
        <el-form-item label="报告内容">
          <el-input v-model="newReport.content" type="textarea" :rows="8" placeholder="请输入报告内容（支持Markdown格式）" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createReport">创建</el-button>
      </template>
    </el-dialog>

    <!-- 报告详情对话框 -->
    <el-dialog v-model="showReportDetail" title="报告详情" width="800px">
      <div v-if="selectedReport" class="report-detail">
        <div class="report-detail-header">
          <h3>{{ selectedReport.title }}</h3>
          <div class="report-meta">
            <el-tag :type="selectedReport.type === 'daily' ? 'primary' : 'success'">
              {{ selectedReport.type === 'daily' ? '日报' : '周报' }}
            </el-tag>
            <span class="report-date">{{ formatDate(selectedReport.createdAt) }}</span>
          </div>
        </div>

        <div class="report-detail-content">
          <div v-if="!isEditingReport" class="report-rendered" v-html="renderMarkdown(selectedReport.content)"></div>
          <el-input v-else v-model="editingContent" type="textarea" :rows="15" />
        </div>

        <div class="report-detail-actions">
          <el-button v-if="!isEditingReport" @click="startEditReport">编辑</el-button>
          <el-button v-else @click="cancelEditReport">取消</el-button>
          <el-button v-if="isEditingReport" type="primary" @click="saveReport">保存</el-button>
          <el-button type="danger" @click="deleteReport">删除</el-button>
        </div>
      </div>
    </el-dialog>

    <!-- AI供应商设置对话框 -->
    <el-dialog v-model="showProviderDialog" title="AI供应商设置" width="400px">
      <el-form label-width="100px">
        <el-form-item label="供应商">
          <el-select v-model="aiProvider">
            <el-option label="DeepSeek" value="DeepSeek" />
            <el-option label="OpenAI" value="OpenAI" />
            <el-option label="Anthropic" value="Anthropic" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showProviderDialog = false">取消</el-button>
        <el-button type="primary" @click="saveProviderSettings">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { defineOptions } from 'vue'

defineOptions({
  name: 'ReportsPage'
})
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Calendar,
  DataAnalysis,
  Delete,
  Setting,
  CopyDocument,
  ArrowDown
} from '@element-plus/icons-vue'
import MarkdownIt from 'markdown-it'
import { getNameInitials } from '@/utils'
// 移除AIProviderIcon组件导入

// 导入AI供应商Logo静态资源
import deepseekLogo from '@/assets/deepseek.png'
import openaiLogo from '@/assets/openai.png'
import anthropicLogo from '@/assets/anthropic.png'

// Markdown渲染器
const md = new MarkdownIt()

// 响应式数据
const searchQuery = ref('')
const selectedType = ref('')
const dateRange = ref<[string, string] | null>(null)
const selectedReport = ref<Report | null>(null)
const showCreateDialog = ref(false)
const showReportDetail = ref(false)
const showProviderDialog = ref(false)
const isEditingReport = ref(false)
const editingContent = ref('')
const inputMessage = ref('')
const isTyping = ref(false)
const isStreaming = ref(false)
const showMentions = ref(false)
const aiProvider = ref('DeepSeek')
const messagesContainer = ref<HTMLElement>()

// 报告类型定义
interface Report {
  id: string
  title: string
  content: string
  type: 'daily' | 'weekly'
  createdAt: string
  isNew?: boolean
}

// 消息类型定义
interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  thinking?: string
  tokens?: number
  showActions?: boolean
  expandedThinking?: boolean
  aiProvider?: string // 记录消息创建时的AI供应商
}

// 新报告表单
const newReport = reactive({
  title: '',
  content: '',
  type: 'daily' as 'daily' | 'weekly'
})

// 模拟报告数据
const reports = ref<Report[]>([
  {
    id: '1',
    title: '2024年12月15日工作日报',
    content: '# 今日工作总结\n\n## 完成任务\n- 完成了用户管理模块的开发\n- 修复了登录页面的bug\n\n## 明日计划\n- 开始项目管理模块的开发',
    type: 'daily',
    createdAt: '2024-12-15',
    isNew: true
  },
  {
    id: '2',
    title: '2024年第50周工作周报',
    content: '# 本周工作总结\n\n## 主要成果\n- 完成了整个用户系统的开发\n- 优化了系统性能\n\n## 下周计划\n- 开始新功能的设计和开发',
    type: 'weekly',
    createdAt: '2024-12-13'
  }
])

// 聊天消息
const messages = ref<Message[]>([
  {
    id: '1',
    role: 'assistant',
    content: '你好！我是智能报告助手，可以帮助你生成工作日报和周报。我能够：\n\n - 📊 分析你的项目进度和任务完成情况\n- 📝 自动生成结构化的日报和周报\n- 🔍 整理工作亮点和待改进事项\n- 📈 提供数据驱动的工作洞察\n\n请选择你需要的服务，或者直接告诉我你的需求！',
    showActions: true,
    expandedThinking: false,
    aiProvider: 'DeepSeek'
  }
])

// 提及建议数据
const mentionSuggestions = ref<Array<{ id: string; name: string; type: 'project' | 'task' }>>([])

// 计算属性
const filteredReports = computed(() => {
  let filtered = reports.value

  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(report =>
      report.title.toLowerCase().includes(query) ||
      report.content.toLowerCase().includes(query)
    )
  }

  // 类型过滤
  if (selectedType.value) {
    filtered = filtered.filter(report => report.type === selectedType.value)
  }

  // 日期过滤
  if (dateRange.value && dateRange.value.length === 2) {
    const [start, end] = dateRange.value
    filtered = filtered.filter(report => {
      const reportDate = new Date(report.createdAt)
      const startDate = new Date(start)
      const endDate = new Date(end)
      return reportDate >= startDate && reportDate <= endDate
    })
  }

  return filtered.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
})

// 方法定义

/**
 * 格式化日期显示
 */
const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

/**
 * 获取报告预览文本
 */
const getPreviewText = (content: string): string => {
  // 移除markdown标记，获取纯文本
  const plainText = content.replace(/[#*`\[\]()]/g, '').replace(/\n/g, ' ')
  return plainText.length > 50 ? plainText.substring(0, 50) + '...' : plainText
}

/**
 * 渲染Markdown内容
 */
const renderMarkdown = (content: string): string => {
  return md.render(content)
}

/**
 * 处理搜索
 */
const handleSearch = () => {
  // 搜索逻辑已在计算属性中处理
}

/**
 * 处理过滤
 */
const handleFilter = () => {
  // 过滤逻辑已在计算属性中处理
}

/**
 * 选择报告
 */
const selectReport = (report: Report) => {
  selectedReport.value = report
  report.isNew = false // 标记为已读
  showReportDetail.value = true
}

/**
 * 创建报告
 */
const createReport = () => {
  if (!newReport.title || !newReport.content) {
    ElMessage.warning('请填写完整的报告信息')
    return
  }

  const report: Report = {
    id: Date.now().toString(),
    title: newReport.title,
    content: newReport.content,
    type: newReport.type,
    createdAt: new Date().toISOString().split('T')[0]
  }

  reports.value.unshift(report)
  showCreateDialog.value = false

  // 重置表单
  newReport.title = ''
  newReport.content = ''
  newReport.type = 'daily'

  ElMessage.success('报告创建成功')
}

/**
 * 开始编辑报告
 */
const startEditReport = () => {
  if (selectedReport.value) {
    editingContent.value = selectedReport.value.content
    isEditingReport.value = true
  }
}

/**
 * 取消编辑报告
 */
const cancelEditReport = () => {
  isEditingReport.value = false
  editingContent.value = ''
}

/**
 * 保存报告
 */
const saveReport = () => {
  if (selectedReport.value) {
    selectedReport.value.content = editingContent.value
    isEditingReport.value = false
    ElMessage.success('报告保存成功')
  }
}

/**
 * 删除报告
 */
const deleteReport = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这个报告吗？', '确认删除', {
      type: 'warning'
    })

    if (selectedReport.value) {
      const index = reports.value.findIndex(r => r.id === selectedReport.value!.id)
      if (index > -1) {
        reports.value.splice(index, 1)
        showReportDetail.value = false
        selectedReport.value = null
        ElMessage.success('报告删除成功')
      }
    }
  } catch {
    // 用户取消删除
  }
}

/**
 * 发送消息
 */
const sendMessage = (event?: KeyboardEvent) => {
  // 如果是键盘事件，阻止默认行为（防止换行）
  if (event) {
    event.preventDefault()
  }

  if (!inputMessage.value.trim() || isStreaming.value) return

  // 添加用户消息
  const userMessage: Message = {
    id: Date.now().toString(),
    role: 'user',
    content: inputMessage.value,
    expandedThinking: false
  }

  messages.value.push(userMessage)
  inputMessage.value = ''

  // 模拟AI回复
  simulateAIResponse()

  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })
}

/**
 * 模拟AI流式回复
 */
const simulateAIResponse = async () => {
  isStreaming.value = true
  isTyping.value = true

  // 模拟延迟
  await new Promise(resolve => setTimeout(resolve, 1000))

  const aiMessage: Message = {
    id: Date.now().toString(),
    role: 'assistant',
    content: '我理解你的需求。让我为你生成一份详细的报告。',
    thinking: '用户询问了关于报告生成的问题，我需要分析当前的项目和任务数据，然后生成相应的报告内容。',
    tokens: 156,
    expandedThinking: false,
    aiProvider: aiProvider.value
  }

  messages.value.push(aiMessage)
  isStreaming.value = false
  isTyping.value = false

  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })
}

/**
 * 生成报告
 */
const generateReport = async (type: 'daily' | 'weekly') => {
  isStreaming.value = true

  // 模拟AI生成报告
  await new Promise(resolve => setTimeout(resolve, 2000))

  const reportContent = type === 'daily'
    ? '# 工作日报\n\n## 今日完成\n- 完成了报告系统的开发\n- 优化了用户界面\n\n## 明日计划\n- 测试新功能\n- 准备上线部署'
    : '# 工作周报\n\n## 本周成果\n- 完成了整个报告系统\n- 提升了开发效率\n\n## 下周计划\n- 开始新项目的规划'

  const aiMessage: Message = {
    id: Date.now().toString(),
    role: 'assistant',
    content: `我为你生成了一份${type === 'daily' ? '日报' : '周报'}，请查看：\n\n${reportContent}\n\n你可以对内容进行修改，确认后我会帮你保存。`,
    tokens: 234,
    expandedThinking: false,
    aiProvider: aiProvider.value
  }

  messages.value.push(aiMessage)
  isStreaming.value = false

  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })
}

/**
 * 处理输入变化（用于@提及功能）
 */
const handleInputChange = () => {
  const lastAtIndex = inputMessage.value.lastIndexOf('@')
  if (lastAtIndex !== -1 && lastAtIndex === inputMessage.value.length - 1) {
    showMentions.value = true
    // 这里可以加载项目和任务数据
    mentionSuggestions.value = [
      { id: '1', name: '项目A', type: 'project' },
      { id: '2', name: '任务B', type: 'task' }
    ]
  } else {
    showMentions.value = false
  }
}

/**
 * 选择提及项
 */
const selectMention = (item: { id: string; name: string; type: 'project' | 'task' }) => {
  inputMessage.value = inputMessage.value.replace(/@$/, `@${item.name} `)
  showMentions.value = false
}

/**
 * 复制消息内容
 */
const copyMessage = async (content: string) => {
  try {
    await navigator.clipboard.writeText(content)
    ElMessage.success('内容已复制到剪贴板')
  } catch {
    ElMessage.error('复制失败')
  }
}

/**
 * 清除聊天上下文
 */
const clearContext = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清除所有聊天记录吗？',
      '确认清除',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      })

    messages.value = [
      {
        id: '1',
        role: 'assistant',
        content: '你好！我是智能报告助手，可以帮助你生成工作日报和周报。我能够：\n\n- 📊 分析你的项目进度和任务完成情况\n- 📝 自动生成结构化的日报和周报\n- 🔍 整理工作亮点和待改进事项\n- 📈 提供数据驱动的工作洞察\n\n请选择你需要的服务，或者直接告诉我你的需求！',
        showActions: true,
        expandedThinking: false,
        aiProvider: aiProvider.value
      }
    ]

    ElMessage.success('聊天记录已清除')
  } catch {
    // 用户取消
  }
}

/**
 * 保存AI供应商设置
 */
const saveProviderSettings = () => {
  showProviderDialog.value = false
  ElMessage.success('AI供应商设置已保存')
}

/**
 * 获取AI供应商Logo路径
 */
const getAIProviderLogo = (provider: string): string => {
  const logoMap: Record<string, string> = {
    'DeepSeek': deepseekLogo,
    'OpenAI': openaiLogo,
    'Anthropic': anthropicLogo
  }
  return logoMap[provider] || deepseekLogo
}

/**
 * 处理图片加载错误
 */
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = deepseekLogo // 使用默认图片
}

/**
 * 滚动到聊天底部
 */
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 修改弹出组件样式
const style = document.createElement('style')
style.innerHTML = `
.el-message-box {
  border-radius: 10px;

  .el-button {
    border-radius: 10px;
  }
  
  .el-button--primary {
    border: none;
    box-shadow: none;
  }
}
`
document.body.appendChild(style)

// 组件挂载时的初始化
onMounted(() => {
  // 初始化逻辑
})
</script>

<style scoped>
:deep(.el-dialog) {
  border-radius: 10px;

  .el-button {
    border-radius: 10px;
  }

  .el-button--primary {
    border: none;
    box-shadow: none;
  }
}

.reports-container {
  display: flex;
  border-radius: 10px;
  height: calc(100vh - 112px);
  background: white;
}

/* 左侧报告管理 */
.reports-sidebar {
  width: 600px;
  max-width: 40%;
  display: flex;
  flex-direction: column;
}

.search-section {
  padding: 20px;
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;

  :deep(.el-input__wrapper) {
    border-radius: 10px;
    height: 40px;
    line-height: 40px;
    background: #f5f5f5;
    box-shadow: none;
    margin-right: 15px;
  }

  .el-button {
    height: 40px;
    line-height: 40px;
    border-radius: 10px;
    box-shadow: none;
    border: none;
  }
}

.filters {
  display: flex;
  flex-direction: row;
  padding-left: 20px;
  padding-right: 20px;

  :deep(.el-select__wrapper) {
    height: 40px;
    border-radius: 10px;
    margin-right: 15px;
  }
}

.reports-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.report-card {
  padding: 15px;
  margin-bottom: 10px;
  background: #EFF2F4;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.report-card:hover {
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.1);
}

.report-card.active {
  border-color: #409eff;
  background: #f0f8ff;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.report-icon {
  color: #409eff;
  font-size: 18px;
}

.report-date {
  font-size: 12px;
  color: #999;
}

.report-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 5px 0;
  color: #333;
}

.report-preview {
  font-size: 12px;
  color: #666;
  margin: 0;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.report-footer {
  margin-top: 10px;
  text-align: right;
}

.new-badge {
  font-size: 10px;
}

/* 右侧聊天界面 */
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 0 10px 10px 0;
}

.chat-header {
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ai-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ai-avatar {
  display: flex;
  align-items: center;
}

.provider-logo {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  object-fit: cover;
  display: block;
}

.ai-name {
  font-weight: 600;
  color: #333;
}

.typing-indicator {
  margin-left: 10px;
  font-size: 12px;
  color: gray;
  font-weight: normal;
}

.chat-actions {
  display: flex;
  gap: 10px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message-wrapper {
  margin-bottom: 20px;
}

.message {
  max-width: 80%;
  display: flex;
  gap: 10px;
  align-items: flex-start;
}

.user-message {
  margin-left: auto;
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.user-avatar {
  background: #409eff;
  color: white;
  font-weight: 600;
}

.ai-message-avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ai-provider-logo {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  object-fit: cover;
  display: block;
}

.user-message .message-content {
  background: #409eff;
  color: white;
  padding: 12px 16px;
  border-radius: 18px 18px 4px 18px;
}

.ai-message .message-content {
  color: #333;
  border-radius: 18px 18px 18px 4px;
  max-width: 100%;
}

.message-right {
  margin-top: 8px;
  margin-left: 16px;
}

/* 思考过程样式 */
.thinking-wrapper {
  margin-bottom: 12px;
  border-radius: 10px;
  overflow: hidden;
}

.thinking-header {
  width: 100px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: #f2f2f2;
  cursor: pointer;
  user-select: none;
  border-radius: 10px;
}

.thinking-title {
  font-size: 13px;
  font-weight: 500;
  color: black;
}

.thinking-toggle {
  transition: transform 0.3s ease;
}

.thinking-toggle.expanded {
  transform: rotate(180deg);
}

.thinking-content {
  padding: 0;
  overflow: hidden;
  background: white;
}

.thinking-text {
  margin-top: 16px;
  padding-left: 10px;
  font-size: 13px;
  color: #666;
  line-height: 1.5;
  border-left: 2px solid #ddd;
  background: white;
}

.message-text {
  line-height: 1.6;
}

/* Markdown渲染内容样式 */
.message-text ul,
.message-text ol {
  padding-left: 20px;
  margin: 10px 0;
  margin-left: 20px;
}

.action-buttons {
  margin-top: 15px;
  display: flex;
  gap: 10px;

  .el-button {
    border-radius: 10px;
    border: none;
    box-shadow: none;

    .el-icon {
      margin-right: 4px;
    }

    &::after {
      display: none;
    }
  }
}

.message-meta {
  margin-top: 4px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  font-size: 12px;
  color: #999;

  .el-button--small {
    padding-left: 0;
    padding-right: 10px;
    font-size: 16px;
  }

  .el-icon {
    color: gray;
  }
}

.token-count {
  font-size: 16px;
  font-weight: 200;
  color: gray;
}

.streaming-indicator {
  margin-bottom: 20px;
}

.typing-dots {
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background: #999;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {

  0%,
  60%,
  100% {
    transform: translateY(0);
  }

  30% {
    transform: translateY(-10px);
  }
}

.chat-input {
  padding: 20px;
  position: relative;

  :deep(.el-textarea__inner) {
    border-radius: 20px;
    background: #EFF2F4;
    border: none;
    box-shadow: none;
    padding: 20px;
    color: black;
  }
}

.mentions-popup {
  position: absolute;
  bottom: 100%;
  left: 20px;
  right: 20px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
}

.mention-item {
  padding: 10px 15px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.mention-item:hover {
  background: #f5f5f5;
}

.mention-icon {
  font-size: 14px;
}

.input-actions {
  margin-top: 10px;
  text-align: right;
}

/* 报告详情对话框 */
.report-detail-header {
  margin-bottom: 20px;
}

.report-detail-header h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.report-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.report-detail-content {
  margin-bottom: 20px;
  min-height: 300px;
}

.report-rendered {
  line-height: 1.8;
  color: #333;
}

.report-detail-actions {
  text-align: right;
}

.report-detail-actions .el-button {
  margin-left: 10px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .reports-container {
    flex-direction: column;
  }

  .reports-sidebar {
    width: 100%;
    height: 40%;
  }

  .chat-container {
    height: 60%;
  }
}
</style>