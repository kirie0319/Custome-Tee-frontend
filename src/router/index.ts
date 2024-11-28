// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue')
    },
    {
      path: '/create-design',
      name: 'create-design',
      component: () => import('@/views/CreateDesignView.vue')
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('@/views/CartView.vue')
    },
    {
      path: '/cart/edit/:id',
      name: 'cart-item-edit',
      component: () => import('@/views/CartItemEditView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: () => import('@/views/CheckoutView.vue')
    },
    {
      path: '/order-complete/:orderId',
      name: 'order-complete',
      component: () => import('@/views/OrderCompleteView.vue')
    },
    {
      path: '/admin',
      component: () => import('@/views/AdminLayout.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: () => import('@/views/AdminDashboard.vue')
        },
        {
          path: 'orders',
          name: 'admin-orders',
          component: () => import('@/views/AdminOrders.vue')
        },
        {
          path: 'users',
          name: 'admin-users',
          component: () => import('@/views/AdminUsers.vue')
        }
      ]
    }
  ]
})

export default router