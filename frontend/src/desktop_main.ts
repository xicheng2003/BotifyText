/* ======================================================================== */
/* 文件: frontend/src/desktop_main.ts (桌面版入口)                      */
/* 说明: 这是桌面应用加载的主入口文件。                                 */
/* ======================================================================== */

import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

// 1. 先导入所有需要的模块
import App from './App.vue' // 确保这里指向桌面版的根组件 App.vue
import router from './router'

// 2. 创建一个应用实例
const app = createApp(App)

// 3. 依次注册所有插件
app.use(createPinia())
app.use(router)

// 4. 最后挂载应用
app.mount('#app')
