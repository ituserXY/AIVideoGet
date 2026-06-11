import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomePage.vue'),
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardPage.vue'),
    },
    {
      path: '/vip',
      name: 'vip',
      component: () => import('../views/VipPage.vue'),
    },
    {
      path: '/terms',
      name: 'terms',
      component: () => import('../views/TermsPage.vue'),
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: () => import('../views/PrivacyPage.vue'),
    },
  ],
})

export default router
