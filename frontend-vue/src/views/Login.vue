<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <img src="/favicon.ico" alt="Tuscot" class="logo-icon" />
          <h1 class="logo-text">Tuscot</h1>
        </div>
        <p class="subtitle">智能项目管理平台</p>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="email">
          <el-input
            v-model="loginForm.email"
            type="email"
            placeholder="请输入邮箱"
            size="large"
            :prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            :prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <div class="form-options">
            <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
            <el-link type="primary" :underline="false">忘记密码？</el-link>
          </div>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
        
        <div class="register-link">
          <span>还没有账号？</span>
          <el-link type="primary" :underline="false" @click="goToRegister">
            立即注册
          </el-link>
        </div>
      </el-form>
    </div>
    
    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="decoration-circle circle-1"></div>
      <div class="decoration-circle circle-2"></div>
      <div class="decoration-circle circle-3"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()

// 响应式数据
const loginFormRef = ref<FormInstance>()
const loading = ref(false)

const loginForm = reactive({
  email: '',
  password: '',
  remember: false
})

// 表单验证规则
const loginRules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

// 方法
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return
    
    loading.value = true
    
    // 模拟登录请求
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 保存token到localStorage
    localStorage.setItem('token', 'mock-token-' + Date.now())
    
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error('登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}

const goToRegister = () => {
  ElMessage.info('注册功能暂未开放')
}
</script>

<style scoped lang="scss">
@use '@/styles/variables' as *;

.login-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
}

.login-card {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 400px;
  padding: $spacing-8;
  background: rgba(255, 255, 255, 0.95);
  border-radius: $border-radius-lg;
  box-shadow: $shadow-lg;
  backdrop-filter: blur(10px);
}

.login-header {
  text-align: center;
  margin-bottom: $spacing-8;
  
  .logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: $spacing-3;
    margin-bottom: $spacing-4;
    
    .logo-icon {
      width: 48px;
      height: 48px;
    }
    
    .logo-text {
      margin: 0;
      font-size: $font-size-2xl;
      font-weight: $font-weight-bold;
      color: $primary-color;
    }
  }
  
  .subtitle {
    margin: 0;
    font-size: $font-size-base;
    color: $text-secondary;
  }
}

.login-form {
  .form-options {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
  }
  
  .login-btn {
    width: 100%;
    height: 48px;
    font-size: $font-size-base;
    font-weight: $font-weight-medium;
  }
  
  .register-link {
    text-align: center;
    margin-top: $spacing-4;
    font-size: $font-size-sm;
    color: $text-secondary;
    
    span {
      margin-right: $spacing-2;
    }
  }
}

.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  
  .decoration-circle {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    animation: float 6s ease-in-out infinite;
    
    &.circle-1 {
      width: 200px;
      height: 200px;
      top: 10%;
      left: 10%;
      animation-delay: 0s;
    }
    
    &.circle-2 {
      width: 150px;
      height: 150px;
      top: 60%;
      right: 10%;
      animation-delay: 2s;
    }
    
    &.circle-3 {
      width: 100px;
      height: 100px;
      bottom: 20%;
      left: 20%;
      animation-delay: 4s;
    }
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

// 响应式设计
@media (max-width: $breakpoint-sm) {
  .login-card {
    margin: $spacing-4;
    padding: $spacing-6;
  }
  
  .login-header {
    .logo {
      .logo-text {
        font-size: $font-size-xl;
      }
    }
  }
}
</style>