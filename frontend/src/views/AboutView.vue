<!-- frontend/src/views/AboutView.vue (无滚动条优化版) -->
<script setup lang="ts">
import PageHeader from '@/components/PageHeader.vue';
import PageFooter from '@/components/PageFooter.vue';

const REPO_URL = "https://github.com/xicheng2003/BotifyText";
</script>

<template>
  <!--
    核心修改：
    使用Grid布局，将页面分为两行：一个占据所有剩余空间的内容区(1fr)，
    和一个高度自适应的页脚区(auto)。这能确保页脚总在底部且内容不会溢出。
  -->
  <div class="grid grid-rows-[1fr_auto] h-full">
    <!-- 主内容区，如果内容真的非常多，也只会在这里内部滚动 -->
    <main class="overflow-y-auto">
      <PageHeader />

      <!-- 为了确保内容能在一页内展示，略微减小了卡片的垂直内边距 (p-4) -->
      <div class="container mx-auto max-w-5xl px-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">

        <!-- 卡片1: 关于项目 & 致谢 -->
        <div class="md:col-span-2 p-4 bg-muted/40 rounded-lg border">
          <h4 class="font-bold text-base mb-4 text-foreground">关于本项目</h4>
          <p class="text-muted-foreground leading-relaxed mb-6">
            该项目源于一次富有挑战的大学实习项目，是对先进机器人技术的一次实践性探索。我们基于 Modbus TCP 协议，在人机交互领域开拓了新的前沿，实现了直观的、基于文本的机器人轨迹控制。
          </p>
          <div class="flex items-center gap-3 pt-4 border-t">
            <img src="https://www.gdut.edu.cn/images2020/footer-logo2.png" alt="GDUT_Logo" class="h-12 w-12 object-contain bg-white rounded-full p-1.5">
            <div>
              <p class="text-sm text-foreground">该项目亦是广东工业大学的一项生产实习实训项目成果</p>
              <p class="text-xs text-muted-foreground">Guangdong University of Technology</p>
            </div>
          </div>
          <h4 class="font-semibold text-foreground my-4 pt-4 border-t">致谢</h4>
          <div class="text-muted-foreground space-y-2">
            <p>由 Xicheng2003 用 <span class="text-red-500">❤️</span> 制作</p>
            <p class="text-xs">与 Pei Zhijie, Liu Jinhang, Lin Taimin 合作完成</p>
          </div>
        </div>

        <!-- 卡片2: 相关链接 & 技术驱动 -->
        <div class="p-4 bg-muted/40 rounded-lg border flex flex-col justify-between">
          <div>
            <h4 class="font-semibold text-foreground mb-4">相关链接</h4>
            <ul class="space-y-3 mb-6">
              <li><a :href="REPO_URL" target="_blank" rel="noopener noreferrer" class="text-primary hover:underline">项目源码</a></li>
              <li><a :href="`${REPO_URL}/releases`" target="_blank" rel="noopener noreferrer" class="text-primary hover:underline">最新版本</a></li>
              <li><a :href="`${REPO_URL}/issues`" target="_blank" rel="noopener noreferrer" class="text-primary hover:underline">报告问题</a></li>
              <li><a :href="`${REPO_URL}/blob/main/LICENSE`" target="_blank" rel="noopener noreferrer" class="text-primary hover:underline">许可证 (MIT)</a></li>
            </ul>
          </div>
          <div class="pt-3 border-t space-y-2 mt-4">
            <p class="text-xs text-muted-foreground">页面由 Vue 3, Vite & shadcn/ui 强力驱动</p>
            <a href="https://www.deepseek.com" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 text-muted-foreground hover:text-primary transition-colors">
              <span class="text-xs">NLP 由</span>
              <img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" alt="Deepseek Logo" class="h-3.5" />
              <span class="text-xs">驱动</span>
            </a>
          </div>
        </div>
      </div>
    </main>

    <!-- 页脚现在是Grid布局的一部分，会被固定在底部 -->
    <PageFooter />
  </div>
</template>
