// frontend/vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from "path"
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    rollupOptions: {
      input: {
        // 定义两个入口
        desktop: resolve(__dirname, 'src/desktop.html'),
        web: resolve(__dirname, 'src/web.html'),
      },
    },
  },
})
