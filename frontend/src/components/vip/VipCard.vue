<script setup lang="ts">
import type { PlanInfo } from '../../types'

defineProps<{
  plan: PlanInfo
  popular?: boolean
}>()

const emit = defineEmits<{
  select: [planType: string]
}>()
</script>

<template>
  <div
    :class="[
      'card relative flex flex-col p-4 transition-all hover:shadow-lg sm:p-6',
      popular ? 'ring-2 ring-primary-500' : '',
    ]"
  >
    <!-- Badge -->
    <div v-if="plan.badge" class="absolute -top-2.5 left-1/2 -translate-x-1/2 sm:-top-3">
      <span
        :class="[
          'inline-block rounded-full px-3 py-0.5 text-xs font-semibold text-white shadow sm:px-4 sm:py-1',
          popular ? 'bg-primary-600' : 'bg-gray-500',
        ]"
      >
        {{ plan.badge }}
      </span>
    </div>

    <div class="mb-3 sm:mb-4">
      <h3 class="text-base font-semibold text-gray-900 dark:text-white sm:text-lg">{{ plan.name }}</h3>
      <div class="mt-1 flex items-baseline gap-1 sm:mt-2">
        <span class="text-2xl font-bold text-gray-900 dark:text-white sm:text-3xl">¥{{ plan.price }}</span>
        <span v-if="plan.originalPrice" class="text-xs text-gray-400 line-through sm:text-sm">¥{{ plan.originalPrice }}</span>
      </div>
      <p class="mt-0.5 text-xs text-gray-500 dark:text-gray-400 sm:mt-1 sm:text-sm">
        可下载 <strong>{{ plan.credits }}</strong>
      </p>
    </div>

    <ul class="mb-4 flex-1 space-y-1.5 text-xs text-gray-600 dark:text-gray-300 sm:mb-6 sm:space-y-2 sm:text-sm">
      <li v-if="plan.type !== 'topup'" class="flex items-center gap-1.5 sm:gap-2">
        <svg class="h-3.5 w-3.5 shrink-0 text-green-500 sm:h-4 sm:w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        无限次数下载
      </li>
      <li class="flex items-center gap-1.5 sm:gap-2">
        <svg class="h-3.5 w-3.5 shrink-0 text-green-500 sm:h-4 sm:w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        高清无水印原画
      </li>
      <li class="flex items-center gap-1.5 sm:gap-2">
        <svg class="h-3.5 w-3.5 shrink-0 text-green-500 sm:h-4 sm:w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        优先解析队列
      </li>
      <li class="flex items-center gap-1.5 sm:gap-2">
        <svg class="h-3.5 w-3.5 shrink-0 text-green-500 sm:h-4 sm:w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        不限速下载
      </li>
    </ul>

    <button
      @click="emit('select', plan.type)"
      :class="[
        'w-full rounded-lg py-2 text-xs font-semibold transition-all sm:py-2.5 sm:text-sm',
        popular
          ? 'bg-primary-600 text-white shadow-sm hover:bg-primary-700'
          : 'border border-gray-300 text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-200 dark:hover:bg-gray-700',
      ]"
    >
      {{ plan.type === 'topup' ? '立即购买' : '开通' + plan.name }}
    </button>
  </div>
</template>
