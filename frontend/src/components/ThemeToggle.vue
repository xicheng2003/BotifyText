<script setup lang="ts">
import { useColorMode } from '@vueuse/core'
import { Button } from '@/components/ui/button'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { Sun, Moon } from 'lucide-vue-next'

const mode = useColorMode()

// 函数现在只负责切换前端主题，非常纯粹
function setTheme(theme: 'light' | 'dark' | 'auto') {
  mode.value = theme
}
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="outline" size="icon">
        <Sun class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
        <Moon class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
        <span class="sr-only">Toggle theme</span>
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <DropdownMenuItem @click="setTheme('light')">浅色主题</DropdownMenuItem>
      <DropdownMenuItem @click="setTheme('dark')">深色主题</DropdownMenuItem>
      <DropdownMenuItem @click="setTheme('auto')">跟随系统</DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
