# Tuscot 项目管理系统 UI/UX 设计文档

## 目录
1. [设计概述](#设计概述)
2. [整体设计系统](#整体设计系统)
3. [页面设计规范](#页面设计规范)
4. [组件设计库](#组件设计库)
5. [交互设计模式](#交互设计模式)
6. [响应式设计](#响应式设计)
7. [可访问性设计](#可访问性设计)
8. [数据可视化规范](#数据可视化规范)
9. [微交互与动画](#微交互与动画)
10. [实施指南](#实施指南)

---

## 设计概述

### 设计理念
Tuscot 项目管理系统采用现代化、简洁的设计语言，注重用户体验和工作效率。设计遵循以下核心原则：
- **简洁性**：减少视觉噪音，突出核心功能
- **一致性**：统一的设计语言和交互模式
- **效率性**：优化工作流程，提高操作效率
- **可访问性**：确保所有用户都能良好使用
- **响应性**：适配各种设备和屏幕尺寸

### 目标用户
- 项目经理和团队负责人
- 开发人员和设计师
- 产品经理和业务分析师
- 企业管理层和决策者

---

## 整体设计系统

### 色彩系统

#### 主色调
```css
/* 主色调 - 紫色系 */
--primary-50: #F5F3FF;
--primary-100: #EDE9FE;
--primary-500: #6366F1;  /* 主色 */
--primary-600: #4F46E5;
--primary-700: #4338CA;
```

#### 辅助色彩
```css
/* 功能色彩 */
--success: #10B981;      /* 成功/完成 */
--warning: #F59E0B;      /* 警告/进行中 */
--error: #EF4444;        /* 错误/延期 */
--info: #3B82F6;         /* 信息/提示 */
```

#### 中性色彩
```css
/* 中性色 */
--gray-50: #F9FAFB;
--gray-100: #F3F4F6;
--gray-200: #E5E7EB;
--gray-300: #D1D5DB;
--gray-400: #9CA3AF;
--gray-500: #6B7280;
--gray-600: #4B5563;
--gray-700: #374151;
--gray-800: #1F2937;
--gray-900: #111827;
```

### 字体系统

#### 字体族
```css
--font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
```

#### 字体大小
```css
--text-xs: 12px;     /* 辅助信息 */
--text-sm: 14px;     /* 正文小字 */
--text-base: 16px;   /* 正文 */
--text-lg: 18px;     /* 副标题 */
--text-xl: 20px;     /* 小标题 */
--text-2xl: 24px;    /* 标题 */
--text-3xl: 30px;    /* 大标题 */
--text-4xl: 36px;    /* 特大标题 */
```

#### 字重
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### 间距系统

#### 基础间距
```css
/* 基础单位：4px */
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
```

### 圆角系统
```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
--radius-full: 50%;
```

### 阴影系统
```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

---

## 页面设计规范

### 1. Dashboard 页面

#### 布局结构
- **网格系统**：12列网格布局
- **主要区域**：
  - 顶部统计卡片区域（4列布局）
  - 中部图表区域（8+4列布局）
  - 底部团队统计区域（4+4+4列布局）

#### 关键组件

**统计卡片**
```css
.stat-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--gray-200);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-number {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--gray-900);
}

.stat-trend {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--success);
}
```

**图表容器**
```css
.chart-container {
  background: white;
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
  min-height: 300px;
}

.chart-title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--gray-900);
  margin-bottom: var(--space-4);
}
```

### 2. Project Board 页面

#### 看板布局
- **三列布局**：Working、In Progress、Completed
- **列宽度**：等宽分布，最小宽度320px
- **间距**：列间距24px

#### 项目卡片设计
```css
.project-card {
  background: white;
  border-radius: var(--radius-md);
  padding: var(--space-4);
  margin-bottom: var(--space-4);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--gray-200);
  cursor: pointer;
  transition: all 0.2s ease;
}

.project-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.project-title {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.project-description {
  font-size: var(--text-sm);
  color: var(--gray-600);
  margin-bottom: var(--space-3);
}

.project-tags {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}

.project-tag {
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
}

.tag-ios { background: #FEF3C7; color: #92400E; }
.tag-android { background: #D1FAE5; color: #065F46; }
.tag-website { background: #E0E7FF; color: #3730A3; }
```

#### 拖拽交互
```css
.dragging {
  opacity: 0.8;
  transform: rotate(5deg);
  box-shadow: var(--shadow-xl);
}

.drop-zone {
  border: 2px dashed var(--primary-300);
  background: var(--primary-50);
  border-radius: var(--radius-md);
  min-height: 100px;
}
```

### 3. Task List 页面

#### 表格设计
```css
.task-table {
  background: white;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.task-header {
  background: var(--gray-50);
  border-bottom: 1px solid var(--gray-200);
  padding: var(--space-3) var(--space-4);
  font-weight: var(--font-semibold);
  color: var(--gray-700);
}

.task-row {
  border-bottom: 1px solid var(--gray-100);
  padding: var(--space-3) var(--space-4);
  transition: background-color 0.15s ease;
}

.task-row:hover {
  background: var(--gray-50);
}

.task-group {
  border-left: 4px solid var(--primary-500);
  background: var(--primary-50);
  padding: var(--space-2) var(--space-4);
  font-weight: var(--font-semibold);
}

.task-group.todo { border-left-color: var(--warning); }
.task-group.progress { border-left-color: var(--primary-500); }
.task-group.review { border-left-color: var(--success); }
```

#### 任务状态指示
```css
.task-status {
  width: 20px;
  height: 20px;
  border-radius: var(--radius-sm);
  border: 2px solid var(--gray-300);
  position: relative;
}

.task-status.completed {
  background: var(--success);
  border-color: var(--success);
}

.task-status.completed::after {
  content: '✓';
  color: white;
  font-size: 12px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

### 4. Message Chat 页面

#### 双栏布局
```css
.chat-container {
  display: flex;
  height: calc(100vh - 64px);
  background: white;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.contact-list {
  width: 320px;
  border-right: 1px solid var(--gray-200);
  background: var(--gray-50);
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}
```

#### 消息气泡设计
```css
.message-bubble {
  max-width: 70%;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-2);
  word-wrap: break-word;
}

.message-sent {
  background: var(--primary-500);
  color: white;
  margin-left: auto;
  border-bottom-right-radius: var(--radius-sm);
}

.message-received {
  background: var(--gray-100);
  color: var(--gray-900);
  border-bottom-left-radius: var(--radius-sm);
}

.message-time {
  font-size: var(--text-xs);
  color: var(--gray-500);
  margin-top: var(--space-1);
}
```

#### 联系人列表项
```css
.contact-item {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--gray-200);
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.contact-item:hover {
  background: white;
}

.contact-item.active {
  background: white;
  border-right: 3px solid var(--primary-500);
}

.contact-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  margin-right: var(--space-3);
}

.contact-info {
  flex: 1;
}

.contact-name {
  font-weight: var(--font-semibold);
  color: var(--gray-900);
}

.contact-message {
  font-size: var(--text-sm);
  color: var(--gray-600);
  margin-top: var(--space-1);
}

.contact-time {
  font-size: var(--text-xs);
  color: var(--gray-500);
}
```

### 5. Activity Timeline 页面

#### 时间轴布局
```css
.timeline-container {
  max-width: 800px;
  margin: 0 auto;
}

.timeline-section {
  margin-bottom: var(--space-8);
}

.timeline-date {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--gray-700);
  margin-bottom: var(--space-4);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.timeline-item {
  position: relative;
  padding-left: var(--space-12);
  margin-bottom: var(--space-6);
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: var(--space-4);
  top: 0;
  bottom: -var(--space-6);
  width: 2px;
  background: var(--gray-200);
}

.timeline-item:last-child::before {
  display: none;
}
```

#### 活动卡片
```css
.activity-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--gray-200);
  position: relative;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.activity-title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--gray-900);
}

.activity-progress {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: var(--gray-200);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-500), var(--success));
  transition: width 0.3s ease;
}
```

---

## 组件设计库

### 按钮组件

#### 主要按钮
```css
.btn-primary {
  background: var(--primary-500);
  color: white;
  border: none;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-primary:hover {
  background: var(--primary-600);
  box-shadow: var(--shadow-md);
}

.btn-primary:active {
  background: var(--primary-700);
  transform: translateY(1px);
}

.btn-primary:disabled {
  background: var(--gray-300);
  cursor: not-allowed;
}
```

#### 次要按钮
```css
.btn-secondary {
  background: white;
  color: var(--primary-500);
  border: 1px solid var(--primary-500);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-secondary:hover {
  background: var(--primary-50);
}
```

#### 按钮尺寸
```css
.btn-sm {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  height: 32px;
}

.btn-md {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-base);
  height: 40px;
}

.btn-lg {
  padding: var(--space-4) var(--space-6);
  font-size: var(--text-lg);
  height: 48px;
}
```

### 表单组件

#### 输入框
```css
.input {
  width: 100%;
  padding: var(--space-3);
  border: 1px solid var(--gray-300);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  transition: border-color 0.15s ease;
}

.input:focus {
  outline: none;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.input.error {
  border-color: var(--error);
}

.input::placeholder {
  color: var(--gray-400);
}
```

#### 标签
```css
.label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--gray-700);
  margin-bottom: var(--space-2);
}

.label.required::after {
  content: '*';
  color: var(--error);
  margin-left: var(--space-1);
}
```

### 卡片组件
```css
.card {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--gray-200);
  overflow: hidden;
}

.card-header {
  padding: var(--space-6) var(--space-6) var(--space-4);
  border-bottom: 1px solid var(--gray-200);
}

.card-title {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--gray-900);
}

.card-body {
  padding: var(--space-6);
}

.card-footer {
  padding: var(--space-4) var(--space-6);
  background: var(--gray-50);
  border-top: 1px solid var(--gray-200);
}
```

### 头像组件
```css
.avatar {
  border-radius: var(--radius-full);
  object-fit: cover;
  background: var(--gray-200);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-medium);
  color: var(--gray-600);
}

.avatar-sm { width: 24px; height: 24px; font-size: 10px; }
.avatar-md { width: 32px; height: 32px; font-size: 12px; }
.avatar-lg { width: 40px; height: 40px; font-size: 14px; }
.avatar-xl { width: 48px; height: 48px; font-size: 16px; }

.avatar-online {
  position: relative;
}

.avatar-online::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 25%;
  height: 25%;
  background: var(--success);
  border: 2px solid white;
  border-radius: var(--radius-full);
}
```

---

## 交互设计模式

### 悬停效果
```css
/* 通用悬停效果 */
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* 按钮悬停 */
.hover-darken:hover {
  filter: brightness(0.95);
}

/* 链接悬停 */
.hover-underline:hover {
  text-decoration: underline;
}
```

### 焦点状态
```css
.focus-ring:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.focus-visible:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
```

### 加载状态
```css
.loading {
  position: relative;
  pointer-events: none;
}

.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  margin: -10px 0 0 -10px;
  border: 2px solid var(--gray-300);
  border-top-color: var(--primary-500);
  border-radius: var(--radius-full);
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

---

## 响应式设计

### 断点系统
```css
/* 移动端 */
@media (max-width: 767px) {
  .container {
    padding: var(--space-4);
  }
  
  .sidebar {
    transform: translateX(-100%);
    position: fixed;
    z-index: 50;
  }
  
  .sidebar.open {
    transform: translateX(0);
  }
  
  .kanban-columns {
    flex-direction: column;
  }
  
  .chat-container {
    flex-direction: column;
  }
  
  .contact-list {
    width: 100%;
    height: 200px;
  }
}

/* 平板端 */
@media (min-width: 768px) and (max-width: 1023px) {
  .container {
    padding: var(--space-6);
  }
  
  .grid-cols-4 {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 桌面端 */
@media (min-width: 1024px) {
  .container {
    padding: var(--space-8);
  }
}
```

### 触摸优化
```css
/* 触摸目标最小尺寸 */
.touch-target {
  min-height: 44px;
  min-width: 44px;
}

/* 触摸反馈 */
.touch-feedback:active {
  background: var(--gray-100);
  transform: scale(0.98);
}
```

---

## 可访问性设计

### 键盘导航
```css
/* 跳转链接 */
.skip-link {
  position: absolute;
  top: -40px;
  left: 6px;
  background: var(--primary-500);
  color: white;
  padding: 8px;
  text-decoration: none;
  border-radius: 4px;
  z-index: 100;
}

.skip-link:focus {
  top: 6px;
}

/* 焦点指示器 */
.focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
```

### 屏幕阅读器支持
```css
/* 仅屏幕阅读器可见 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### 色彩对比度
- 正文文字：至少 4.5:1 对比度
- 大文字（18px+）：至少 3:1 对比度
- 非文字元素：至少 3:1 对比度

---

## 数据可视化规范

### 图表色彩
```css
/* 图表色彩系统 */
:root {
  --chart-primary: #6366F1;
  --chart-secondary: #10B981;
  --chart-tertiary: #F59E0B;
  --chart-quaternary: #EF4444;
  --chart-gradient: linear-gradient(135deg, #6366F1 0%, #10B981 100%);
}
```

### 图表样式
```css
.chart-tooltip {
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  box-shadow: var(--shadow-lg);
}

.chart-legend {
  display: flex;
  gap: var(--space-4);
  justify-content: center;
  margin-top: var(--space-4);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: var(--radius-sm);
}
```

---

## 微交互与动画

### 过渡动画
```css
/* 全局过渡 */
* {
  transition-property: color, background-color, border-color, transform, box-shadow;
  transition-duration: 0.15s;
  transition-timing-function: ease-in-out;
}

/* 页面过渡 */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}

/* 模态框动画 */
.modal-enter-active {
  transition: all 0.3s ease;
}

.modal-leave-active {
  transition: all 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
```

### 加载动画
```css
/* 骨架屏 */
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* 脉冲动画 */
.pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

### 反馈动画
```css
/* 成功动画 */
.success-checkmark {
  animation: checkmark 0.6s ease-in-out;
}

@keyframes checkmark {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

/* 错误震动 */
.error-shake {
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}
```

---

## 实施指南

### 开发优先级
1. **第一阶段**：建立设计系统基础（色彩、字体、间距）
2. **第二阶段**：开发基础组件库（按钮、表单、卡片）
3. **第三阶段**：实现页面布局和导航
4. **第四阶段**：添加交互和动画效果
5. **第五阶段**：响应式适配和可访问性优化

### 质量检查清单
- [ ] 色彩对比度符合 WCAG 2.1 AA 标准
- [ ] 所有交互元素支持键盘导航
- [ ] 移动端触摸目标不小于 44px
- [ ] 页面加载时间不超过 3 秒
- [ ] 支持屏幕阅读器
- [ ] 动画支持 `prefers-reduced-motion`
- [ ] 表单提供清晰的错误提示
- [ ] 图片提供 alt 文本

### 工具推荐
- **设计工具**：Figma、Sketch
- **原型工具**：Figma、Principle
- **色彩工具**：Coolors、Adobe Color
- **可访问性测试**：axe、WAVE
- **性能测试**：Lighthouse、WebPageTest

---

## 结语

本设计文档为 Tuscot 项目管理系统提供了完整的 UI/UX 设计指南。通过遵循这些设计规范，我们可以确保产品具有一致的用户体验、良好的可用性和现代化的视觉效果。

设计系统应该是活跃的文档，随着产品的发展和用户反馈的收集，需要持续更新和优化。建议定期回顾和更新设计规范，以保持产品的竞争力和用户满意度。

**最后更新时间**：2024年12月
**文档版本**：v1.0
**负责人**：UI/UX 设计团队