<!-- frontend/src/components/NavigationBar.vue (全新版本) -->
<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { Button } from '@/components/ui/button';
// 导入我们需要的图标，新增Home图标
import { BotMessageSquare, Info, Home } from 'lucide-vue-next';
import ThemeToggle from './ThemeToggle.vue';
</script>

<template>
  <div class="container mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex h-16 items-center justify-between">

      <!-- 左侧：应用Logo和标题 -->
      <div class="flex items-center">
        <RouterLink to="/" class="flex items-center gap-3">
          <BotMessageSquare class="h-8 w-8 text-primary" />
          <span class="text-xl font-bold text-foreground">
            BotifyText
          </span>
        </RouterLink>
      </div>

      <!-- 右侧：功能按钮 -->
      <div class="flex items-center gap-3">

        <!-- 新增的 Home 按钮，采用图标样式 -->
        <RouterLink to="/">
          <Button variant="outline" size="icon">
            <Home class="h-5 w-5" />
          </Button>
        </RouterLink>

        <!-- 修改后的“关于”页面按钮，采用统一的图标样式 -->
        <RouterLink to="/about">
          <Button variant="outline" size="icon">
            <Info class="h-5 w-5" />
          </Button>
        </RouterLink>

        <!-- 保留的主题切换按钮，其样式已与其他按钮统一 -->
        <ThemeToggle />

      </div>
    </div>
  </div>
</template>
