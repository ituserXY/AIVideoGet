import type { Platform } from '../types'

const patterns: Record<Platform, RegExp[]> = {
  douyin:      [/v\.douyin\.com/i, /www\.douyin\.com/i, /douyin\.com/i],
  tiktok:      [/tiktok\.com/i, /vm\.tiktok\.com/i],
  kuaishou:    [/kuaishou\.com/i, /v\.kuaishou\.com/i],
  xiaohongshu: [/xiaohongshu\.com/i, /xhslink\.com/i],
  bilibili:    [/bilibili\.com/i, /b23\.tv/i],
  weibo:       [/weibo\.com/i, /m\.weibo\.cn/i],
  xigua:       [/xigua\.com/i, /ixigua\.com/i],
}

export function detectPlatform(url: string): Platform | null {
  for (const [platform, regexps] of Object.entries(patterns)) {
    for (const re of regexps) {
      if (re.test(url)) return platform as Platform
    }
  }
  return null
}

export function isValidUrl(url: string): boolean {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}
