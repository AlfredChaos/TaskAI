<template>
  <div v-if="config.isDev" class="dev-tools">
    <div class="dev-tools-toggle" @click="togglePanel">
      <i class="icon-dev">🛠️</i>
    </div>
    
    <transition name="slide-up">
      <div v-show="showPanel" class="dev-tools-panel">
        <div class="panel-header">
          <h3>开发者工具</h3>
          <button @click="togglePanel" class="close-btn">×</button>
        </div>
        
        <div class="panel-content">
          <div class="tool-item">
            <label class="switch">
              <input 
                type="checkbox" 
                :checked="mockEnabled" 
                @change="handleMockToggle"
              >
              <span class="slider"></span>
            </label>
            <div class="tool-info">
              <span class="tool-title">Mock数据模式</span>
              <span class="tool-desc">
                {{ mockEnabled ? '当前使用Mock数据' : '当前使用真实API' }}
              </span>
            </div>
          </div>
          
          <div class="tool-item">
            <button @click="clearStorage" class="action-btn">
              清除本地存储
            </button>
            <div class="tool-info">
              <span class="tool-title">清除缓存</span>
              <span class="tool-desc">清除localStorage和sessionStorage</span>
            </div>
          </div>
          
          <div class="tool-item">
            <button @click="reloadPage" class="action-btn">
              重新加载
            </button>
            <div class="tool-info">
              <span class="tool-title">刷新页面</span>
              <span class="tool-desc">重新加载当前页面</span>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { config, toggleMockData, getMockDataStatus } from '@/config'

/**
 * 组件名称
 */
defineOptions({
  name: 'DevTools'
})

// 响应式数据
const showPanel = ref(false)
const mockEnabled = computed(() => getMockDataStatus())

/**
 * 切换面板显示状态
 */
function togglePanel() {
  showPanel.value = !showPanel.value
}

/**
 * 处理Mock数据开关切换
 * @param event 事件对象
 */
function handleMockToggle(event: Event) {
  const target = event.target as HTMLInputElement
  const enabled = target.checked
  
  try {
    toggleMockData(enabled)
    ElMessage.success(`已${enabled ? '启用' : '禁用'}Mock数据模式`)
  } catch (error) {
    ElMessage.error('切换失败：' + (error as Error).message)
    // 恢复开关状态
    target.checked = !enabled
  }
}

/**
 * 清除本地存储
 */
function clearStorage() {
  try {
    localStorage.clear()
    sessionStorage.clear()
    ElMessage.success('本地存储已清除')
  } catch (error) {
    ElMessage.error('清除失败：' + (error as Error).message)
  }
}

/**
 * 重新加载页面
 */
function reloadPage() {
  window.location.reload()
}
</script>

<style scoped>
.dev-tools {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
}

.dev-tools-toggle {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.dev-tools-toggle:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.icon-dev {
  font-size: 20px;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
}

.dev-tools-panel {
  position: absolute;
  bottom: 60px;
  right: 0;
  width: 320px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border: 1px solid #e1e5e9;
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #e1e5e9;
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #6c757d;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #e9ecef;
  color: #495057;
}

.panel-content {
  padding: 16px 20px;
}

.tool-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f1f3f4;
}

.tool-item:last-child {
  border-bottom: none;
}

.tool-info {
  flex: 1;
}

.tool-title {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 2px;
}

.tool-desc {
  display: block;
  font-size: 12px;
  color: #6c757d;
}

/* 开关样式 */
.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.3s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #4CAF50;
}

input:checked + .slider:before {
  transform: translateX(20px);
}

/* 按钮样式 */
.action-btn {
  padding: 6px 12px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 80px;
}

.action-btn:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

/* 动画 */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .dev-tools-panel {
    background: #2d3748;
    border-color: #4a5568;
  }
  
  .panel-header {
    background: #1a202c;
    border-color: #4a5568;
  }
  
  .panel-header h3 {
    color: #e2e8f0;
  }
  
  .close-btn {
    color: #a0aec0;
  }
  
  .close-btn:hover {
    background: #4a5568;
    color: #e2e8f0;
  }
  
  .tool-item {
    border-color: #4a5568;
  }
  
  .tool-title {
    color: #e2e8f0;
  }
  
  .tool-desc {
    color: #a0aec0;
  }
}
</style>