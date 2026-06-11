import axios from 'axios'
import type { ApiResponse, ParseRequest, ParseResult, UserInfo, OrderInfo, PlanType } from '../types'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: 30000,
})

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

http.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/'
    }
    return Promise.reject(err)
  },
)

// 解析视频
export async function parseVideo(data: ParseRequest): Promise<ParseResult> {
  const res = await http.post<ApiResponse<ParseResult>>('/parse', data)
  return res.data.data
}

// 获取下载链接（获取 download_token 的重定向地址）
export function getDownloadUrl(token: string): string {
  return `${http.defaults.baseURL}/download/${token}`
}

// 用户登录
export async function login(data: { account: string; password: string }): Promise<{ token: string; user: UserInfo }> {
  const res = await http.post<ApiResponse<{ token: string; user: UserInfo }>>('/auth/login', data)
  return res.data.data
}

// 用户注册
export async function register(data: { account: string; password: string; code?: string }): Promise<{ token: string; user: UserInfo }> {
  const res = await http.post<ApiResponse<{ token: string; user: UserInfo }>>('/auth/register', data)
  return res.data.data
}

// 获取用户信息
export async function getUserInfo(): Promise<UserInfo> {
  const res = await http.get<ApiResponse<UserInfo>>('/user/info')
  return res.data.data
}

// 创建订单
export async function createOrder(data: { plan_type: PlanType; payment_method: 'wxpay' | 'alipay' }): Promise<OrderInfo> {
  const res = await http.post<ApiResponse<OrderInfo>>('/order/create', data)
  return res.data.data
}

// 检查订单状态
export async function checkOrder(orderNo: string): Promise<{ status: string }> {
  const res = await http.get<ApiResponse<{ status: string }>>(`/order/status/${orderNo}`)
  return res.data.data
}

// 获取历史记录
export async function getHistory(page = 1, size = 20) {
  const res = await http.get<ApiResponse<{ list: ParseResult[]; total: number }>>('/user/history', { params: { page, size } })
  return res.data.data
}
