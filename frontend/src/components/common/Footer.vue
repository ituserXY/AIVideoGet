<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <footer class="border-t border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900">
    <div class="mx-auto max-w-6xl px-4 py-8 sm:py-12">
      <div class="grid grid-cols-2 gap-6 sm:grid-cols-4 sm:gap-8">
        <!-- Brand -->
        <div class="col-span-2 sm:col-span-1">
          <span class="text-base font-bold text-gray-900 dark:text-white sm:text-lg">VideoGet</span>
          <p class="mt-1.5 text-xs text-gray-500 sm:text-sm">全网视频无水印下载工具</p>
        </div>
        <!-- Links -->
        <div>
          <h4 class="mb-2 text-xs font-semibold text-gray-900 dark:text-white sm:mb-3 sm:text-sm">功能</h4>
          <ul class="space-y-1.5 text-xs sm:space-y-2 sm:text-sm">
            <li><button @click="router.push('/')" class="text-gray-500 hover:text-primary-600">视频解析</button></li>
            <li><button @click="router.push('/vip')" class="text-gray-500 hover:text-primary-600">VIP 会员</button></li>
          </ul>
        </div>
        <div>
          <h4 class="mb-2 text-xs font-semibold text-gray-900 dark:text-white sm:mb-3 sm:text-sm">支持平台</h4>
          <ul class="space-y-1.5 text-xs text-gray-500 sm:space-y-2 sm:text-sm">
            <li>抖音 / TikTok</li>
            <li>快手 / 小红书</li>
            <li>哔哩哔哩 / 微博</li>
            <li>西瓜视频</li>
          </ul>
        </div>
        <div>
          <h4 class="mb-2 text-xs font-semibold text-gray-900 dark:text-white sm:mb-3 sm:text-sm">法律</h4>
          <ul class="space-y-1.5 text-xs sm:space-y-2 sm:text-sm">
            <li><button @click="router.push('/terms')" class="text-gray-500 hover:text-primary-600">用户协议</button></li>
            <li><button @click="router.push('/privacy')" class="text-gray-500 hover:text-primary-600">隐私政策</button></li>
          </ul>
        </div>
      </div>
      <div class="mt-6 border-t border-gray-200 pt-6 text-center text-xs text-gray-400 dark:border-gray-800 sm:mt-8 sm:pt-8 sm:text-sm">
        <p>本网站仅提供技术工具，所有视频版权归原作者及对应平台所有。</p>
      </div>
    </div>
  </footer>
</template>
