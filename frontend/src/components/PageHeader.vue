<script setup lang="ts">
import { Bot } from 'lucide-vue-next'
</script>

<template>
  <div class="space-y-4 text-center py-12">
    <div class="flex justify-center items-center space-x-3">
      <Bot class="h-12 w-12 text-primary" />

      <h1 class="text-5xl font-bold tracking-tight text-foreground">
        <span class="bg-gradient-to-r from-primary via-sky-500 to-indigo-400 bg-clip-text text-transparent">
          Botify
        </span>
        <span>Text</span>
      </h1>
    </div>

    <p class="text-xl text-muted-foreground">
      一个基于文本的机器人轨迹控制平台
    </p>
    <p class="max-w-2xl mx-auto text-base text-muted-foreground pt-2">
      赋予机器人理解自然语言的能力，通过简单的文字指令，实现精准的轨迹运动控制。
    </p>
  </div>
</template>
