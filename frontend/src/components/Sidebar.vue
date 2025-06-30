<script setup lang="ts">
import { ref } from 'vue'; // 导入 ref
import { RouterLink } from 'vue-router';
import { Button } from '@/components/ui/button';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
// --- 新增：导入分享功能所需的组件和图标 ---
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Home, SlidersHorizontal, Info, Share2, SunMoon, Loader2 } from 'lucide-vue-next';
import ThemeToggle from './ThemeToggle.vue';
import QrcodeVue from 'qrcode.vue';

// --- 新增：分享模态框的完整逻辑 ---
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
            <RouterLink to="/about"><Button variant="outline" size="icon" class="h-12 w-12"><Info class="h-6 w-6" /></Button></RouterLink>
          </TooltipTrigger>
          <TooltipContent side="right"><p>关于</p></TooltipContent>
        </Tooltip>
      </nav>

      <div class="flex flex-col items-center gap-4 mb-4">
        <Tooltip>
          <TooltipTrigger as-child>
            <Button @click="openShareModal" variant="outline" size="icon" class="h-12 w-12">
              <Share2 class="h-6 w-6" />
            </Button>
          </TooltipTrigger>
          <TooltipContent side="right">
            <p>分享</p>
          </TooltipContent>
        </Tooltip>

        <ThemeToggle />
      </div>
    </div>
  </TooltipProvider>

  <Dialog v-model:open="showShareModal">
    <DialogContent>
      <DialogHeader>
        <DialogTitle>分享控制面板链接</DialogTitle>
        <DialogDescription>
          让同一局域网内的设备扫描下方二维码或访问链接：
        </DialogDescription>
      </DialogHeader>
      <div class="py-4 flex flex-col items-center justify-center min-h-[280px]">
        <div v-if="isLoading" class="flex items-center text-muted-foreground">
          <Loader2 class="mr-2 h-4 w-4 animate-spin" /> 正在获取服务器信息...
        </div>
        <div v-else-if="shareError" class="text-red-500 text-center">{{ shareError }}</div>
        <div v-else-if="shareUrl" class="flex flex-col items-center w-full gap-4">
          <p class="p-2 border rounded bg-muted text-muted-foreground text-sm break-all w-full text-center">{{ shareUrl }}</p>
          <QrcodeVue :value="shareUrl" :size="200" level="H" />
        </div>
      </div>
      <DialogFooter>
        <Button v-if="shareUrl" variant="secondary" @click="copyUrlToClipboard">复制链接</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
