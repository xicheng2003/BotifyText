// frontend/src/router/index.ts (已根据您的 HomeView.vue 更新)

import { createRouter, createWebHistory } from 'vue-router'
// --- 核心修改：导入您实际在使用的 HomeView 组件 ---
import HomeView from '../views/HomeView.vue'

// 动态判断并设置路由的base路径
// 检查浏览器当前的URL路径是否以'/web'开头
const isWebApp = window.location.pathname.startsWith('/web');
// 如果是，则将路由的基准地址设为'/web/'，否则设为根'/'
const base = isWebApp ? '/web/' : '/';

const router = createRouter({
  // 使用我们动态计算出的base路径
  history: createWebHistory(base),
  routes: [
    {
      // 这个根路径'/'现在会根据base的设置，
      // 智能地匹配桌面版的'/'或网页版的'/web/'
      path: '/',
      name: 'home',
      component: HomeView, // 使用您项目中实际存在的 HomeView
    },
    {
      path: '/settings',
      name: 'settings',
      // 这个路径在网页版中会自动变为 /web/settings
      // 请确保您的设置页面文件名为 Settings.vue
      component: () => import('../views/Settings.vue')
    },
    {
      path: '/about',
      name: 'about',
      // 这个路径在网页版中会自动变为 /web/about
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
