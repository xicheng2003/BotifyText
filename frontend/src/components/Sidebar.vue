<!-- frontend/src/components/Sidebar.vue (已优化布局和样式) -->
<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import { useColorMode } from '@vueuse/core';
import { Button } from '@/components/ui/button';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Home, SlidersHorizontal, Info, Share2, Sun, Moon, Loader2 } from 'lucide-vue-next';
import QrcodeVue from 'qrcode.vue';

// --- 主题切换逻辑 (已整合进此组件) ---
const mode = useColorMode();
function setTheme(theme: 'light' | 'dark' | 'auto') {
  mode.value = theme;
}

// --- 分享模态框逻辑 (保持不变) ---
const showShareModal = ref(false);
const shareUrl = ref('');
const shareError = ref('');
const isLoading = ref(false);
const openShareModal = async () => {
  showShareModal.value = true;
  isLoading.value = true;
  shareUrl.value = '';
  shareError.value = '';
  try {
    const response = await fetch('/api/server_info');
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    if (data.status === 'success' && data.ip && data.port) {
      shareUrl.value = `http://${data.ip}:${data.port}/web`;
    } else {
      shareError.value = data.message || '未能获取有效的服务器信息。';
    }
  } catch (error: any) {
    console.error("获取服务器信息时发生错误:", error);
    shareError.value = `获取服务器信息时发生网络或解析错误: ${error.message}。`;
  } finally {
    isLoading.value = false;
  }
};
const copyUrlToClipboard = async () => {
  if (!shareUrl.value) return;
  try {
    await navigator.clipboard.writeText(shareUrl.value);
    alert('链接已复制到剪贴板！');
  } catch (err) {
    console.error('复制到剪贴板失败:', err);
    alert('复制链接失败，请手动复制。');
  }
};
</script>

<template>
  <TooltipProvider :delay-duration="100">
    <div class="h-full flex flex-col justify-between items-center p-2 bg-muted/40 border-r">

      <!-- 核心修改：顶部主导航区现在包含“分享”按钮 -->
      <nav class="flex flex-col items-center gap-4 mt-4">
        <Tooltip>
          <TooltipTrigger as-child>
            <RouterLink to="/"><Button variant="outline" size="icon" class="h-12 w-12"><Home class="h-6 w-6" /></Button></RouterLink>
          </TooltipTrigger>
          <TooltipContent side="right"><p>控制台</p></TooltipContent>
        </Tooltip>
        <Tooltip>
          <TooltipTrigger as-child>
            <RouterLink to="/settings"><Button variant="outline" size="icon" class="h-12 w-12"><SlidersHorizontal class="h-6 w-6" /></Button></RouterLink>
          </TooltipTrigger>
          <TooltipContent side="right"><p>应用设置</p></TooltipContent>
        </Tooltip>
        <Tooltip>
          <TooltipTrigger as-child>
            <Button @click="openShareModal" variant="outline" size="icon" class="h-12 w-12">
              <Share2 class="h-6 w-6" />
            </Button>
          </TooltipTrigger>
          <TooltipContent side="right"><p>分享</p></TooltipContent>
        </Tooltip>
      </nav>

      <!-- 核心修改：底部功能区现在是“关于”和“主题切换” -->
      <div class="flex flex-col items-center gap-4 mb-4">
        <Tooltip>
          <TooltipTrigger as-child>
            <RouterLink to="/about"><Button variant="outline" size="icon" class="h-12 w-12"><Info class="h-6 w-6" /></Button></RouterLink>
          </TooltipTrigger>
          <TooltipContent side="right"><p>关于</p></TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger as-child>
             <DropdownMenu>
                <DropdownMenuTrigger as-child>
                  <Button variant="outline" size="icon" class="h-12 w-12">
                    <Sun class="h-6 w-6 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                    <Moon class="absolute h-6 w-6 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                    <span class="sr-only">Toggle theme</span>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem @click="setTheme('light')">浅色主题</DropdownMenuItem>
                  <DropdownMenuItem @click="setTheme('dark')">深色主题</DropdownMenuItem>
                  <DropdownMenuItem @click="setTheme('auto')">跟随系统</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
          </TooltipTrigger>
          <TooltipContent side="right"><p>切换主题</p></TooltipContent>
        </Tooltip>

      </div>
    </div>
  </TooltipProvider>

  <!-- 分享模态框 (Dialog) 保持不变 -->
  <Dialog v-model:open="showShareModal">
    <DialogContent>
      <DialogHeader>
        <DialogTitle>分享控制面板链接</DialogTitle>
        <DialogDescription>让同一局域网内的设备扫描下方二维码或访问链接：</DialogDescription>
      </DialogHeader>
      <div class="py-4 flex flex-col items-center justify-center min-h-[280px]">
        <div v-if="isLoading" class="flex items-center text-muted-foreground"><Loader2 class="mr-2 h-4 w-4 animate-spin" /> 正在获取服务器信息...</div>
        <div v-else-if="shareError" class="text-red-500 text-center">{{ shareError }}</div>
        <div v-else-if="shareUrl" class="flex flex-col items-center w-full gap-4">
          <p class="p-2 border rounded bg-muted text-muted-foreground text-sm break-all w-full text-center">{{ shareUrl }}</p>
          <!-- 核心修改：将QrcodeVue包裹在一个div中，并添加样式 -->
          <div class="p-4 bg-white rounded-lg border shadow-md">
              <QrcodeVue :value="shareUrl" :size="200" level="H" />
          </div>
        </div>
      </div>
      <DialogFooter>
        <Button v-if="shareUrl" variant="secondary" @click="copyUrlToClipboard">复制链接</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
