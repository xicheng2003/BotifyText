<!-- frontend/src/components/PageHeader.vue (已优化) -->
<script setup lang="ts">
// --- 核心修改：将导入的图标从 Bot 替换为 BotMessageSquare ---
import { BotMessageSquare } from 'lucide-vue-next'
</script>

<template>
  <!-- 增加了内边距的响应式调整 (px-4) -->
  <div class="space-y-4 text-center py-12 px-4">
    <div class="inline-block rounded-lg bg-muted p-3 shadow-sm">
      <!-- --- 核心修改：使用新的 BotMessageSquare 图标组件 --- -->
      <BotMessageSquare class="h-8 w-8 sm:h-10 sm:w-10 text-primary" />
    </div>

    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-foreground flex items-center justify-center leading-snug">
      <!--
        核心修改：
        为带有渐变的span添加一个2px的、透明的垂直边框(border-y-2 border-transparent)。
        这个技巧强制浏览器为文字的下降笔画提供足够的渲染空间，从而解决裁切问题。
      -->
      <span class="bg-gradient-to-r from-primary via-sky-500 to-indigo-400 bg-clip-text text-transparent border-y-2 border-transparent">Botify</span><span>Text</span>
    </h1>

    <!-- 为副标题和描述文本添加了响应式字体大小调整 -->
    <p class="text-lg sm:text-xl text-muted-foreground">
      一个基于文本的机器人轨迹控制平台
    </p>
    <!--
      核心修改：
      1. 通过响应式的max-width (max-w-md lg:max-w-2xl)，控制文本容器的宽度。
      2. 插入一个只在小于lg断点的屏幕上显示的换行符 <br class="lg:hidden" />。
      3. 新增响应式字体大小：默认为text-sm，在lg断点及以上变为text-base。
    -->
    <p class="max-w-md lg:max-w-2xl mx-auto text-sm lg:text-base text-muted-foreground pt-1">
      它赋予机器人理解自然语言的能力，<br class="lg:hidden" />通过简单的文字指令，实现精准、流畅的轨迹运动。
    </p>
  </div>
</template>
