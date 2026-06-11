<script setup lang="ts">
import { ref } from 'vue'
import { PLANS, type PlanType } from '../types'
import VipCard from '../components/vip/VipCard.vue'
import { createOrder, checkOrder } from '../api'

const selectedPlan = ref<PlanType | null>(null)
const paymentMethod = ref<'wxpay' | 'alipay'>('wxpay')
const payUrl = ref('')
const orderNo = ref('')
const showPayment = ref(false)
const polling = ref(false)

async function handleSelect(planType: string) {
  selectedPlan.value = planType as PlanType
  showPayment.value = true
  payUrl.value = ''
  orderNo.value = ''
}

async function handlePay() {
  if (!selectedPlan.value) return
  try {
    const order = await createOrder({
      plan_type: selectedPlan.value,
      payment_method: paymentMethod.value,
    })
    payUrl.value = order.pay_url
    orderNo.value = order.order_no
    polling.value = true
    const timer = setInterval(async () => {
      try {
        const status = await checkOrder(orderNo.value)
        if (status.status === 'paid') {
          clearInterval(timer)
          polling.value = false
          showPayment.value = false
          alert('支付成功！VIP 已开通')
        }
      } catch {
        // continue
      }
    }, 3000)
  } catch (e: any) {
    alert('创建订单失败：' + (e.response?.data?.message || e.message))
  }
}
</script>

<template>
  <div class="mx-auto max-w-6xl px-3 py-8 sm:px-4 sm:py-12">
    <!-- Header -->
    <div class="text-center">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white sm:text-3xl">VIP 会员</h1>
      <p class="mt-2 text-sm text-gray-500 sm:mt-3">选择适合你的套餐，畅享无限下载</p>
    </div>

    <!-- Plans Grid -->
    <div class="mt-8 grid gap-4 sm:mt-12 sm:grid-cols-2 lg:grid-cols-4 lg:gap-6">
      <VipCard
        v-for="(plan, i) in PLANS"
        :key="plan.type"
        :plan="plan"
        :popular="i === 1"
        @select="handleSelect"
      />
    </div>

    <!-- Feature comparison -->
    <div class="card mt-10 overflow-hidden sm:mt-16">
      <h2 class="border-b border-gray-200 p-4 text-base font-semibold text-gray-900 dark:border-gray-700 dark:text-white sm:p-6 sm:text-lg">权益对比</h2>
      <div class="divide-y divide-gray-200 dark:divide-gray-700">
        <div class="grid grid-cols-4 gap-2 px-4 py-3 text-xs sm:gap-4 sm:px-6 sm:py-4 sm:text-sm">
          <span class="font-medium text-gray-900 dark:text-white">功能</span>
          <span class="text-center text-gray-600 dark:text-gray-300">免费用户</span>
          <span class="text-center text-gray-600 dark:text-gray-300">VIP 月卡</span>
          <span class="text-center text-gray-600 dark:text-gray-300">VIP 年卡</span>
        </div>
        <div v-for="row in [
          { label: '每日下载', free: '3 次', vip: '无限', vip2: '无限' },
          { label: '下载速度', free: '限速', vip: '不限速', vip2: '不限速' },
          { label: '视频画质', free: '普通', vip: '高清原画', vip2: '高清原画' },
          { label: '解析优先级', free: '普通', vip: '优先', vip2: '优先' },
        ]" :key="row.label" class="grid grid-cols-4 gap-2 px-4 py-3 text-xs sm:gap-4 sm:px-6 sm:py-4 sm:text-sm">
          <span class="text-gray-700 dark:text-gray-300">{{ row.label }}</span>
          <span class="text-center text-gray-500">{{ row.free }}</span>
          <span class="text-center font-medium text-primary-600">{{ row.vip }}</span>
          <span class="text-center font-medium text-primary-600">{{ row.vip2 }}</span>
        </div>
      </div>
    </div>

    <!-- Payment Modal -->
    <Teleport to="body">
      <div v-if="showPayment" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-3" @click.self="showPayment = false">
        <div class="card w-full max-w-sm animate-fade-in p-5 sm:max-w-md sm:p-6">
          <div class="mb-5 flex items-center justify-between sm:mb-6">
            <h2 class="text-base font-semibold text-gray-900 dark:text-white sm:text-lg">支付</h2>
            <button @click="showPayment = false" class="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-gray-700">
              <svg class="h-4 w-4 sm:h-5 sm:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div v-if="!payUrl" class="space-y-4">
            <p class="text-xs text-gray-500 sm:text-sm">选择支付方式：</p>
            <div class="flex gap-3">
              <button
                @click="paymentMethod = 'wxpay'"
                :class="['flex-1 rounded-lg border-2 p-3 text-center transition-all sm:p-4', paymentMethod === 'wxpay' ? 'border-green-500 bg-green-50 dark:bg-green-900/20' : 'border-gray-200 dark:border-gray-600']"
              >
                <span class="text-xl sm:text-2xl">💚</span>
                <p class="mt-1 text-xs font-medium text-gray-900 dark:text-white sm:text-sm">微信</p>
              </button>
              <button
                @click="paymentMethod = 'alipay'"
                :class="['flex-1 rounded-lg border-2 p-3 text-center transition-all sm:p-4', paymentMethod === 'alipay' ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-200 dark:border-gray-600']"
              >
                <span class="text-xl sm:text-2xl">💙</span>
                <p class="mt-1 text-xs font-medium text-gray-900 dark:text-white sm:text-sm">支付宝</p>
              </button>
            </div>
            <button @click="handlePay" class="btn-primary w-full py-2.5 text-sm sm:py-3">
              确认支付 ¥{{ PLANS.find(p => p.type === selectedPlan)?.price }}
            </button>
          </div>

          <div v-else class="space-y-4 text-center">
            <p class="text-xs text-gray-500 sm:text-sm">请使用{{ paymentMethod === 'wxpay' ? '微信' : '支付宝' }}扫码支付</p>
            <div class="mx-auto flex h-36 w-36 items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 dark:border-gray-600 dark:bg-gray-800 sm:h-48 sm:w-48">
              <span class="text-xs text-gray-400">支付二维码</span>
            </div>
            <div v-if="polling" class="flex items-center justify-center gap-2 text-xs text-primary-600 sm:text-sm">
              <div class="h-3 w-3 animate-spin rounded-full border-2 border-gray-300 border-t-primary-600 sm:h-4 sm:w-4"></div>
              等待支付结果...
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
