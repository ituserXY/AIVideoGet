<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'

const router = useRouter()
const userStore = useUserStore()
const showMobileMenu = ref(false)
const showAuthModal = ref(false)
const darkMode = ref(false)

function toggleDark() {
  darkMode.value = !darkMode.value
  document.documentElement.classList.toggle('dark')
}

function goHome() {
  showMobileMenu.value = false
  router.push('/')
}

function goVip() {
  showMobileMenu.value = false
  router.push('/vip')
}

function goDashboard() {
  showMobileMenu.value = false
  if (userStore.isLoggedIn()) {
    router.push('/dashboard')
  } else {
    showAuthModal.value = true
  }
}

function handleLogout() {
  userStore.logout()
  showMobileMenu.value = false
  router.push('/')
}
</script>

<template>
  <nav class="sticky top-0 z-50 border-b border-gray-200 bg-white/80 backdrop-blur-lg dark:border-gray-700 dark:bg-gray-900/80">
    <div class="mx-auto flex h-14 items-center justify-between px-3 sm:h-16 sm:px-4 lg:max-w-6xl">
      <!-- Logo -->
      <button @click="goHome" class="flex items-center gap-1.5 text-lg font-bold text-gray-900 dark:text-white sm:gap-2 sm:text-xl">
        <span class="flex h-7 w-7 items-center justify-center rounded-lg bg-primary-600 text-xs text-white sm:h-8 sm:w-8 sm:text-sm">V</span>
        <span>VideoGet</span>
      </button>

      <!-- Desktop Nav -->
      <div class="hidden items-center gap-1 md:flex">
        <button @click="goHome" class="btn-ghost px-3 py-2 text-sm">首页</button>
        <button @click="goVip" class="btn-ghost px-3 py-2 text-sm">开通VIP</button>
        <button @click="goDashboard" class="btn-ghost px-3 py-2 text-sm">我的</button>

        <!-- Dark Mode -->
        <button @click="toggleDark" class="btn-ghost p-2">
          <svg v-if="!darkMode" class="h-4 w-4 sm:h-5 sm:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
          <svg v-else class="h-4 w-4 sm:h-5 sm:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </button>

        <!-- User -->
        <template v-if="userStore.isLoggedIn()">
          <div class="ml-3 flex items-center gap-2 sm:ml-4 sm:gap-3">
            <span class="flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400">
              <span class="hidden lg:inline">{{ userStore.user?.nickname }}</span>
              <span v-if="userStore.isVip()" class="rounded bg-amber-100 px-1.5 py-0.5 text-xs text-amber-700 dark:bg-amber-900/30 dark:text-amber-400">VIP</span>
            </span>
            <button @click="handleLogout" class="btn-ghost text-xs sm:text-sm">退出</button>
          </div>
        </template>
        <template v-else>
          <button @click="showAuthModal = true" class="btn-primary ml-3 px-4 py-2 text-sm sm:ml-4">登录</button>
        </template>
      </div>

      <!-- Mobile Menu Button -->
      <button @click="showMobileMenu = !showMobileMenu" class="rounded-lg p-2 hover:bg-gray-100 dark:hover:bg-gray-800 md:hidden">
        <svg class="h-5 w-5 sm:h-6 sm:w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Mobile Menu -->
    <transition name="slide">
      <div v-if="showMobileMenu" class="border-t border-gray-200 bg-white px-4 pb-4 dark:border-gray-700 dark:bg-gray-900 md:hidden">
        <div class="space-y-1 pt-2">
          <button @click="goHome" class="block w-full rounded-lg px-3 py-2.5 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-800">首页</button>
          <button @click="goVip" class="block w-full rounded-lg px-3 py-2.5 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-800">开通VIP</button>
          <button @click="goDashboard" class="block w-full rounded-lg px-3 py-2.5 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-800">我的</button>
          <button @click="toggleDark" class="block w-full rounded-lg px-3 py-2.5 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-800">
            {{ darkMode ? '浅色模式' : '深色模式' }}
          </button>
        </div>
        <hr class="my-3 border-gray-200 dark:border-gray-700" />
        <template v-if="userStore.isLoggedIn()">
          <div class="flex items-center gap-3 px-3 py-2">
            <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 text-xs font-bold text-primary-600">{{ userStore.user?.nickname?.charAt(0) || 'U' }}</div>
            <div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ userStore.user?.nickname }}</p>
              <p v-if="userStore.isVip()" class="text-xs text-amber-600">VIP 会员</p>
            </div>
          </div>
          <button @click="handleLogout" class="mt-2 w-full rounded-lg px-3 py-2.5 text-left text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20">退出登录</button>
        </template>
        <template v-else>
          <button @click="showAuthModal = true; showMobileMenu = false" class="btn-primary w-full">登录 / 注册</button>
        </template>
      </div>
    </transition>

    <!-- Auth Modal -->
    <Teleport to="body">
      <div v-if="showAuthModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="showAuthModal = false">
        <div class="card w-full max-w-sm animate-fade-in p-5 sm:max-w-md sm:p-6">
          <div class="mb-5 flex items-center justify-between sm:mb-6">
            <h2 class="text-base font-semibold text-gray-900 dark:text-white sm:text-lg">登录</h2>
            <button @click="showAuthModal = false" class="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-gray-700">
              <svg class="h-4 w-4 sm:h-5 sm:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <form @submit.prevent="() => {}" class="space-y-3 sm:space-y-4">
            <input type="text" placeholder="手机号 / 邮箱" class="input-field py-2.5 text-sm sm:py-3" />
            <input type="password" placeholder="密码" class="input-field py-2.5 text-sm sm:py-3" />
            <button type="submit" class="btn-primary w-full py-2.5 text-sm sm:py-3">登录</button>
          </form>
          <p class="mt-4 text-center text-xs text-gray-500 sm:text-sm">
            还没有账号？
            <button class="font-medium text-primary-600 hover:text-primary-500">立即注册</button>
          </p>
        </div>
      </div>
    </Teleport>
  </nav>
</template>

<style scoped>
.slide-enter-active, .slide-leave-active {
  transition: all 0.2s ease;
}
.slide-enter-from, .slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
