/* ======================================================================== */
/* 文件: frontend/src/web_main.ts (网页版入口)                         */
/* 说明: 这是通过浏览器访问时加载的主入口文件。                           */
/* ======================================================================== */

import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

// 1. 先导入所有需要的模块
import App from './WebApp.vue' // 确保这里指向网页版的根组件 WebApp.vue
import router from './router'

// 2. 创建一个应用实例
const app = createApp(App)

// 3. 依次注册所有插件
app.use(createPinia())
app.use(router)

// 4. 最后挂载应用
app.mount('#app')
