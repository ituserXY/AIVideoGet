// 支持的平台
export type Platform =
  | 'douyin'
  | 'kuaishou'
  | 'xiaohongshu'
  | 'bilibili'
  | 'weibo'
  | 'xigua'
  | 'tiktok'
  | 'youtube'

export const PLATFORM_INFO: Record<Platform, { name: string; color: string; icon: string }> = {
  douyin:      { name: '抖音',     color: '#000000',   icon: 'douyin' },
  tiktok:      { name: 'TikTok',   color: '#000000',   icon: 'tiktok' },
  kuaishou:    { name: '快手',     color: '#FF4906',   icon: 'kuaishou' },
  xiaohongshu: { name: '小红书',   color: '#FF2442',   icon: 'xiaohongshu' },
  bilibili:    { name: '哔哩哔哩', color: '#00A1D6',   icon: 'bilibili' },
  weibo:       { name: '微博',     color: '#E6162D',   icon: 'weibo' },
  xigua:       { name: '西瓜视频', color: '#EE2C2C',   icon: 'xigua' },
  youtube:     { name: 'YouTube',  color: '#FF0000',   icon: 'youtube' },
}

// 用户角色
export type UserRole = 'guest' | 'free' | 'vip'

// 用户信息
export interface UserInfo {
  id: number
  nickname: string
  avatar: string
  role: UserRole
  vip_expire_at: string | null
  daily_download_count: number
  max_daily_downloads: number
}

// 解析请求
export interface ParseRequest {
  url: string
}

// 解析结果（前端可见）
export interface ParseResult {
  title: string
  author: string
  cover_url: string
  duration: number
  width: number
  height: number
  images: string[]
  download_token: string
  platform: Platform
}

// 下载令牌响应
export interface DownloadResponse {
  download_url: string
}

// 套餐
export type PlanType = 'monthly' | 'quarterly' | 'yearly' | 'topup'

export const PLANS: PlanInfo[] = [
  { type: 'monthly',   name: '月卡',   price: 9.9,   originalPrice: 19.9, credits: '无限', badge: '热门' },
  { type: 'quarterly', name: '季卡',   price: 24.9,  originalPrice: 59.7, credits: '无限', badge: '实惠' },
  { type: 'yearly',    name: '年卡',   price: 69.9,  originalPrice: 119.9, credits: '无限', badge: '最值' },
  { type: 'topup',     name: '按次包', price: 4.9,   originalPrice: null,  credits: '5次', badge: null },
]

export interface PlanInfo {
  type: PlanType
  name: string
  price: number
  originalPrice: number | null
  credits: string
  badge: string | null
}

// 订单
export interface OrderInfo {
  order_no: string
  amount: number
  plan_type: PlanType
  payment_method: 'wxpay' | 'alipay'
  status: 'pending' | 'paid' | 'expired' | 'refunded'
  pay_url: string
}

// API 通用响应
export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}
