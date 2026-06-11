<script setup lang="ts">
import { ref, computed } from 'vue'
import { getDownloadUrl } from '../../api'
import { PLATFORM_INFO } from '../../types'
import type { ParseResult, Platform } from '../../types'

const props = defineProps<{
  result: ParseResult
}>()

const emit = defineEmits<{
  clear: []
  favorite: []
}>()

const downloading = ref(false)
const showPlayer = ref(false)

function formatDuration(seconds: number): string {
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
}

function handleDownload() {
  downloading.value = true
  const url = getDownloadUrl(props.result.download_token)
  const a = document.createElement('a')
  a.href = url
  a.download = ''
  a.click()
  setTimeout(() => { downloading.value = false }, 1000)
}

const platformInfo = computed(() => {
  return PLATFORM_INFO[props.result.platform as Platform] || null
})
</script>

<template>
  <div class="card animate-slide-up w-full overflow-hidden">
    <!-- Video Preview Area -->
    <div class="relative aspect-video overflow-hidden bg-gray-100 dark:bg-gray-700">
      <img
        :src="result.cover_url"
        :alt="result.title"
        class="h-full w-full object-cover"
        loading="lazy"
      />
      <!-- Play overlay -->
      <div class="absolute inset-0 flex items-center justify-center bg-black/20">
        <button
          @click="showPlayer = !showPlayer"
          class="flex h-12 w-12 items-center justify-center rounded-full bg-white/90 shadow-lg transition-transform hover:scale-110 sm:h-16 sm:w-16"
        >
          <svg class="ml-0.5 h-6 w-6 text-gray-900 sm:h-8 sm:w-8" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z" />
          </svg>
        </button>
      </div>
      <!-- Duration badge -->
      <span class="absolute bottom-2 right-2 rounded-md bg-black/70 px-1.5 py-0.5 text-xs text-white sm:bottom-3 sm:right-3 sm:px-2 sm:py-1">
        {{ formatDuration(result.duration) }}
      </span>
      <!-- Platform badge -->
      <div
        v-if="platformInfo"
        class="absolute left-2 top-2 flex items-center gap-1 rounded-full px-2 py-1 text-xs font-medium text-white shadow sm:left-3 sm:top-3 sm:px-3"
        :style="{ backgroundColor: platformInfo.color }"
      >
        <img
          :src="`/icons/${result.platform}.svg`"
          :alt="platformInfo.name"
          class="h-3 w-3 brightness-0 invert sm:h-3.5 sm:w-3.5"
        />
        {{ platformInfo.name }}
      </div>
    </div>

    <!-- Video Info -->
    <div class="p-3 sm:p-4 lg:p-5">
      <h3 class="text-sm font-semibold text-gray-900 line-clamp-2 dark:text-white sm:text-base lg:text-lg">
        {{ result.title || '无标题' }}
      </h3>
      <p class="mt-1 text-xs text-gray-500 dark:text-gray-400 sm:text-sm">
        {{ result.author }}
      </p>

      <!-- Meta info -->
      <div class="mt-2 flex flex-wrap items-center gap-2 text-xs text-gray-400 sm:mt-3">
        <span>{{ result.width }} × {{ result.height }}</span>
      </div>

      <!-- Action Buttons -->
      <div class="mt-3 flex flex-wrap items-center gap-2 sm:mt-4 sm:gap-3">
        <button
          @click="handleDownload"
          :disabled="downloading"
          class="btn-primary gap-1.5 px-4 py-2 text-xs sm:gap-2 sm:px-5 sm:py-2.5 sm:text-sm"
        >
          <svg v-if="!downloading" class="h-3.5 w-3.5 sm:h-4 sm:w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <svg v-else class="h-3.5 w-3.5 animate-spin sm:h-4 sm:w-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ downloading ? '下载中...' : '下载视频' }}
        </button>
        <button @click="emit('favorite')" class="btn-secondary gap-1.5 px-3 py-2 text-xs sm:gap-2 sm:px-4 sm:py-2.5 sm:text-sm">
          <svg class="h-3.5 w-3.5 sm:h-4 sm:w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
          </svg>
          <span class="hidden sm:inline">稍后下载</span>
          <span class="sm:hidden">收藏</span>
        </button>
        <button @click="emit('clear')" class="btn-ghost gap-1 px-3 py-2 text-xs sm:gap-2 sm:px-4 sm:py-2.5 sm:text-sm">
          <svg class="h-3.5 w-3.5 sm:h-4 sm:w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          再来一个
        </button>
      </div>

      <!-- Inline Video Player -->
      <div v-if="showPlayer" class="mt-3 overflow-hidden rounded-lg bg-black sm:mt-4">
        <video
          :src="getDownloadUrl(result.download_token)"
          controls
          autoplay
          class="w-full"
        ></video>
      </div>
    </div>
  </div>
</template>
