<script setup lang="ts">
const APP_VERSION = "V1.0.0-beta";
const currentYear = new Date().getFullYear();
</script>

<template>
  <footer class="border-t border-border/40 px-6 py-4 mt-8">
    <div class="container mx-auto flex justify-between items-center text-xs text-muted-foreground">
      <span>Copyright © {{ currentYear }} BotifyText. All Rights Reserved.</span>
      <span> {{ APP_VERSION }}</span>
    </div>
  </footer>
</template>
