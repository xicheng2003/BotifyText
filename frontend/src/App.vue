<script setup lang="ts">
import Sidebar from '@/components/Sidebar.vue';
// 不再需要 onMounted 和任何API调用逻辑
</script>

<template>
  <div class="flex h-screen bg-background text-foreground">
    <aside class="w-20">
      <Sidebar />
    </aside>
    <main class="flex-1 overflow-y-auto p-6">
      <router-view />
    </main>
  </div>
</template>
