<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { getHistory } from '../api'
import type { ParseResult } from '../types'

const router = useRouter()
const userStore = useUserStore()

const history = ref<ParseResult[]>([])
const loading = ref(true)

onMounted(async () => {
  if (!userStore.isLoggedIn()) {
    router.push('/')
    return
  }
  try {
    const data = await getHistory()
    history.value = data.list
  } catch {
    // ignore
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="mx-auto max-w-4xl px-3 py-6 sm:px-4 sm:py-8">
    <!-- User Info Card -->
    <div class="card mb-4 p-4 sm:mb-6 sm:p-6">
      <div class="flex items-center gap-3 sm:gap-4">
        <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary-100 text-sm font-bold text-primary-600 dark:bg-primary-900/30 sm:h-14 sm:w-14 sm:text-xl">
          {{ userStore.user?.nickname?.charAt(0) || 'U' }}
        </div>
        <div class="min-w-0 flex-1">
          <h2 class="text-sm font-semibold text-gray-900 dark:text-white sm:text-lg">{{ userStore.user?.nickname || '用户' }}</h2>
          <p class="text-xs text-gray-500 sm:text-sm">
            {{ userStore.isVip() ? 'VIP 会员' : '免费用户' }}
            <span v-if="userStore.user?.vip_expire_at" class="ml-1.5 text-xs text-gray-400">
              到期：{{ userStore.user.vip_expire_at }}
            </span>
          </p>
        </div>
        <button @click="router.push('/vip')" class="btn-primary shrink-0 px-3 py-2 text-xs sm:px-4 sm:py-2.5 sm:text-sm">
          {{ userStore.isVip() ? '续费' : '开通VIP' }}
        </button>
      </div>

      <!-- Stats -->
      <div class="mt-4 grid grid-cols-3 gap-3 border-t border-gray-100 pt-4 dark:border-gray-700 sm:mt-6 sm:gap-4 sm:pt-6">
        <div class="text-center">
          <p class="text-lg font-bold text-gray-900 dark:text-white sm:text-2xl">
            {{ userStore.isVip() ? '∞' : userStore.remainingDownloads() }}
          </p>
          <p class="text-xs text-gray-500">剩余下载</p>
        </div>
        <div class="text-center">
          <p class="text-lg font-bold text-gray-900 dark:text-white sm:text-2xl">{{ userStore.isVip() ? '∞' : 3 }}</p>
          <p class="text-xs text-gray-500">每日额度</p>
        </div>
        <div class="text-center">
          <p class="text-lg font-bold text-gray-900 dark:text-white sm:text-2xl">{{ history.length }}</p>
          <p class="text-xs text-gray-500">解析记录</p>
        </div>
      </div>
    </div>

    <!-- History -->
    <div class="card p-4 sm:p-6">
      <h3 class="mb-3 text-sm font-semibold text-gray-900 dark:text-white sm:mb-4 sm:text-base">解析历史</h3>

      <div v-if="loading" class="py-8 text-center text-sm text-gray-500">加载中...</div>

      <div v-else-if="history.length === 0" class="py-8 text-center text-sm text-gray-500">
        暂无解析记录，去
        <button @click="router.push('/')" class="font-medium text-primary-600 hover:text-primary-500">首页</button>
        解析视频吧
      </div>

      <div v-else class="space-y-2 sm:space-y-3">
        <div
          v-for="item in history"
          :key="item.download_token"
          class="flex items-center gap-3 rounded-lg border border-gray-100 p-2 transition-colors hover:bg-gray-50 dark:border-gray-700 dark:hover:bg-gray-800 sm:gap-4 sm:p-3"
        >
          <img :src="item.cover_url" class="h-12 w-20 shrink-0 rounded object-cover sm:h-16 sm:w-24" />
          <div class="min-w-0 flex-1">
            <p class="truncate text-xs font-medium text-gray-900 dark:text-white sm:text-sm">{{ item.title || '无标题' }}</p>
            <p class="mt-0.5 text-xs text-gray-500">{{ item.author }}</p>
          </div>
          <button class="btn-primary shrink-0 px-3 py-1.5 text-xs sm:px-4 sm:py-2">重新下载</button>
        </div>
      </div>
    </div>
  </div>
</template>
