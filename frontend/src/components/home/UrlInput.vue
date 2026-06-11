<script setup lang="ts">
import { ref, computed } from 'vue'
import { detectPlatform, isValidUrl } from '../../utils/platform'
import { PLATFORM_INFO } from '../../types'
import type { Platform } from '../../types'

const emit = defineEmits<{
  parse: [url: string]
}>()

const url = ref('')
const detectedPlatform = computed<Platform | null>(() => {
  if (!url.value) return null
  return detectPlatform(url.value)
})

const showError = ref(false)

function handleParse() {
  const trimmed = url.value.trim()
  if (!trimmed || !isValidUrl(trimmed)) {
    showError.value = true
    setTimeout(() => { showError.value = false }, 2000)
    return
  }
  showError.value = false
  emit('parse', trimmed)
}

function handlePaste(e: ClipboardEvent) {
  const text = e.clipboardData?.getData('text') || ''
  if (detectPlatform(text)) {
    setTimeout(() => handleParse(), 100)
  }
}
</script>

<template>
  <div class="w-full max-w-2xl px-0">
    <div class="relative">
      <div class="relative flex flex-col items-stretch overflow-hidden rounded-xl border-2 bg-white shadow-lg transition-all focus-within:border-primary-500 dark:border-gray-600 dark:bg-gray-800 dark:focus-within:border-primary-400 sm:flex-row">
        <div class="relative flex flex-1 items-center">
          <!-- Platform icon inside input -->
          <div v-if="detectedPlatform" class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2">
            <img
              :src="`/icons/${detectedPlatform}.svg`"
              :alt="PLATFORM_INFO[detectedPlatform].name"
              class="h-5 w-5 opacity-40"
            />
          </div>
          <input
            v-model="url"
            @paste="handlePaste"
            type="url"
            placeholder="粘贴视频链接，自动识别平台..."
            :class="['w-full border-none bg-transparent text-sm text-gray-900 outline-none placeholder:text-gray-400 dark:text-gray-100 dark:placeholder:text-gray-500', detectedPlatform ? 'pl-10' : 'pl-4', 'py-3.5 pr-4 sm:py-4']"
          />
        </div>
        <div class="flex shrink-0 items-center gap-2 border-t border-gray-200 px-3 py-2 dark:border-gray-600 sm:border-t-0 sm:py-0 sm:pr-2">
          <div v-if="detectedPlatform" class="hidden items-center gap-1 sm:flex">
            <img
              :src="`/icons/${detectedPlatform}.svg`"
              :alt="PLATFORM_INFO[detectedPlatform].name"
              class="h-4 w-4"
              :style="{ color: PLATFORM_INFO[detectedPlatform].color }"
            />
            <span
              class="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium"
              :style="{ backgroundColor: PLATFORM_INFO[detectedPlatform].color + '15', color: PLATFORM_INFO[detectedPlatform].color }"
            >
              {{ PLATFORM_INFO[detectedPlatform].name }}
            </span>
          </div>
          <button
            @click="handleParse"
            :disabled="!url.trim()"
            class="btn-primary w-full rounded-lg px-4 py-2.5 text-sm sm:w-auto sm:px-5 sm:py-3"
          >
            <svg class="mr-1.5 inline-block h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            解析视频
          </button>
        </div>
      </div>
      <!-- Error -->
      <transition name="fade">
        <p v-if="showError" class="mt-2 text-center text-xs text-red-500 sm:text-sm">
          请输入有效的视频链接
        </p>
      </transition>
      <!-- Hint -->
      <p v-if="!showError" class="mt-2 text-center text-xs text-gray-400">
        支持：抖音 / TikTok / 快手 / 小红书 / B站 / 微博 / 西瓜视频
      </p>
    </div>
  </div>
</template>
