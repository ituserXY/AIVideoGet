import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserInfo } from '../types'

export const useUserStore = defineStore('user', () => {
  const user = ref<UserInfo | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isLoggedIn = () => !!token.value

  const isVip = () => {
    if (!user.value) return false
    if (user.value.role !== 'vip') return false
    if (user.value.vip_expire_at && new Date(user.value.vip_expire_at) < new Date()) return false
    return true
  }

  const remainingDownloads = () => {
    if (!user.value) return 0
    if (isVip()) return Infinity
    return Math.max(0, user.value.max_daily_downloads - user.value.daily_download_count)
  }

  function setLogin(t: string, u: UserInfo) {
    token.value = t
    user.value = u
    localStorage.setItem('token', t)
  }

  function setUser(u: UserInfo) {
    user.value = u
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    isLoggedIn,
    isVip,
    remainingDownloads,
    setLogin,
    setUser,
    logout,
  }
})
