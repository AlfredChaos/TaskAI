import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Layout from '@/components/Layout/index.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表板', icon: 'Dashboard' }
      },
      {
        path: 'projects',
        name: 'Projects',
        component: () => import('@/views/Projects/index.vue'),
        meta: { title: '项目', icon: 'Folder' },
        children: [
          {
            path: '',
            name: 'ProjectList',
            component: () => import('@/views/Projects/List.vue'),
            meta: { title: '项目列表' }
          },
          {
            path: ':id',
            name: 'ProjectDetail',
            component: () => import('@/views/Projects/Detail.vue'),
            meta: { title: '项目详情' }
          },
          {
            path: ':id/board',
            name: 'ProjectBoard',
            component: () => import('@/views/Projects/Board.vue'),
            meta: { title: '项目看板' }
          }
        ]
      },
      {
        path: 'tasks',
        name: 'Tasks',
        component: () => import('@/views/Tasks/index.vue'),
        meta: { title: '任务', icon: 'List' },
        children: [
          {
            path: '',
            name: 'TaskList',
            component: () => import('@/views/Tasks/List.vue'),
            meta: { title: '任务列表' }
          },
          {
            path: ':id',
            name: 'TaskDetail',
            component: () => import('@/views/Tasks/Detail.vue'),
            meta: { title: '任务详情' }
          }
        ]
      },
      {
        path: 'messages',
        name: 'Messages',
        component: () => import('@/views/Messages/index.vue'),
        meta: { title: '消息', icon: 'ChatDotRound' }
      },
      {
        path: 'activities',
        name: 'Activities',
        component: () => import('@/views/Activities/index.vue'),
        meta: { title: '活动', icon: 'Clock' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/Profile/index.vue'),
        meta: { title: '个人资料', icon: 'User' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const requiresAuth = to.meta.requiresAuth !== false
  
  if (requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/')
  } else {
    next()
  }
})

export default router
