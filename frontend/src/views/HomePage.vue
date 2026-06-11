<script setup lang="ts">
import { ref } from 'vue'
import UrlInput from '../components/home/UrlInput.vue'
import VideoPreview from '../components/home/VideoPreview.vue'
import { parseVideo } from '../api'
import { useUserStore } from '../stores/user'
import type { ParseResult } from '../types'

const userStore = useUserStore()

const loading = ref(false)
const result = ref<ParseResult | null>(null)
const error = ref('')

async function handleParse(url: string) {
  loading.value = true
  error.value = ''
  result.value = null

  try {
    const data = await parseVideo({ url })
    result.value = data
  } catch (e: any) {
    error.value = e.response?.data?.message || e.message || '解析失败，请检查链接是否正确'
  } finally {
    loading.value = false
  }
}

function handleClear() {
  result.value = null
  error.value = ''
}

function handleFavorite() {
  if (!userStore.isLoggedIn()) {
    error.value = '请先登录再收藏视频'
    return
  }
}

const platforms = [
  { name: '抖音', icon: '/icons/douyin.svg', color: '#000000' },
  { name: 'TikTok', icon: '/icons/tiktok.svg', color: '#000000' },
  { name: '快手', icon: '/icons/kuaishou.svg', color: '#FF4906' },
  { name: '小红书', icon: '/icons/xiaohongshu.svg', color: '#FF2442' },
  { name: 'B站', icon: '/icons/bilibili.svg', color: '#00A1D6' },
  { name: '微博', icon: '/icons/weibo.svg', color: '#E6162D' },
  { name: '西瓜视频', icon: '/icons/xigua.svg', color: '#EE2C2C' },
]
</script>

<template>
  <div class="flex min-h-[calc(100vh-4rem)] flex-col items-center px-4 sm:px-6">
    <!-- Hero Section -->
    <div class="flex w-full max-w-6xl flex-col items-center pt-12 sm:pt-16 lg:pt-24">
      <h1 class="text-center text-2xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-3xl lg:text-5xl">
        全网视频
        <span class="text-primary-600">无水印</span>
        下载
      </h1>
      <p class="mt-2 max-w-xl text-center text-sm text-gray-500 dark:text-gray-400 sm:mt-4 sm:text-base lg:text-lg">
        粘贴链接，一键解析。支持抖音、快手、小红书、B站等主流平台
      </p>

      <!-- URL Input -->
      <div class="mt-6 w-full sm:mt-8 sm:flex sm:justify-center">
        <UrlInput @parse="handleParse" />
      </div>

      <!-- Loading -->
      <div v-if="loading" class="mt-8 flex flex-col items-center gap-3 sm:mt-10">
        <div class="h-8 w-8 animate-spin rounded-full border-3 border-gray-200 border-t-primary-600 sm:h-10 sm:w-10"></div>
        <p class="text-xs text-gray-500 sm:text-sm">正在解析视频...</p>
      </div>

      <!-- Error -->
      <div v-if="error && !loading" class="mt-4 w-full max-w-lg rounded-lg border border-red-200 bg-red-50 p-3 text-xs text-red-600 dark:border-red-800 dark:bg-red-900/20 dark:text-red-400 sm:p-4 sm:text-sm">
        {{ error }}
      </div>

      <!-- Result -->
      <div v-if="result && !loading" class="mt-6 w-full max-w-2xl sm:mt-8">
        <VideoPreview
          :result="result"
          @clear="handleClear"
          @favorite="handleFavorite"
        />
      </div>
    </div>

    <!-- Platform Wall -->
    <div class="mt-12 w-full max-w-4xl sm:mt-16 lg:mt-20">
      <h2 class="mb-4 text-center text-base font-semibold text-gray-900 dark:text-white sm:mb-6 sm:text-lg">支持平台</h2>
      <div class="grid grid-cols-3 gap-3 sm:grid-cols-4 lg:grid-cols-7 lg:gap-4">
        <div
          v-for="p in platforms"
          :key="p.name"
          class="card flex flex-col items-center gap-2 p-3 transition-all hover:shadow-md sm:p-4"
        >
          <img
            :src="p.icon"
            :alt="p.name"
            class="h-8 w-8 sm:h-10 sm:w-10"
            :style="{ color: p.color }"
          />
          <span class="text-xs font-medium text-gray-700 dark:text-gray-300 sm:text-sm">{{ p.name }}</span>
        </div>
      </div>
    </div>

    <!-- How it works -->
    <div class="mt-12 w-full max-w-4xl pb-12 sm:mt-16 sm:pb-16 lg:mt-20 lg:pb-20">
      <h2 class="mb-6 text-center text-base font-semibold text-gray-900 dark:text-white sm:mb-8 sm:text-lg">三步使用</h2>
      <div class="grid gap-4 sm:grid-cols-3 sm:gap-6">
        <div class="card p-4 text-center sm:p-6">
          <div class="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-primary-100 text-sm font-bold text-primary-600 dark:bg-primary-900/30 sm:h-12 sm:w-12 sm:text-lg">1</div>
          <h3 class="mt-3 text-sm font-semibold text-gray-900 dark:text-white sm:mt-4 sm:text-base">粘贴链接</h3>
          <p class="mt-1 text-xs text-gray-500 sm:mt-2 sm:text-sm">复制视频分享链接粘贴到输入框</p>
        </div>
        <div class="card p-4 text-center sm:p-6">
          <div class="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-primary-100 text-sm font-bold text-primary-600 dark:bg-primary-900/30 sm:h-12 sm:w-12 sm:text-lg">2</div>
          <h3 class="mt-3 text-sm font-semibold text-gray-900 dark:text-white sm:mt-4 sm:text-base">解析视频</h3>
          <p class="mt-1 text-xs text-gray-500 sm:mt-2 sm:text-sm">系统自动识别平台并解析无水印视频</p>
        </div>
        <div class="card p-4 text-center sm:p-6">
          <div class="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-primary-100 text-sm font-bold text-primary-600 dark:bg-primary-900/30 sm:h-12 sm:w-12 sm:text-lg">3</div>
          <h3 class="mt-3 text-sm font-semibold text-gray-900 dark:text-white sm:mt-4 sm:text-base">下载保存</h3>
          <p class="mt-1 text-xs text-gray-500 sm:mt-2 sm:text-sm">预览后点击下载，保存无水印原视频</p>
        </div>
      </div>
    </div>
  </div>
</template>
