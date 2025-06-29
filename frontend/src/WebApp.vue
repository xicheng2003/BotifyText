<script setup lang="ts">
// 这里我们将使用旧的导航栏，它更适合网页浏览
import NavigationBar from '@/components/NavigationBar.vue';
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <header class="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <NavigationBar />
    </header>
    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>
