// src/stores/cart.ts
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'
import type { CartItem, CartItemInput, GenerateDesignResponse } from '@/types/cart'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
    loading: false,
    error: null as string | null,
  }),

  actions: {
    // デザイン生成
    async generateDesign(prompt: string): Promise<GenerateDesignResponse> {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post<GenerateDesignResponse>(
          `${API_BASE_URL}/designs/generate`,
          { prompt },
          {
            headers: { 
              Authorization: `Bearer ${authStore.token}`,
              'Content-Type': 'application/json'
            }
          }
        )
        return response.data
      } catch (error) {
        this.error = 'Failed to generate design'
        throw error
      } finally {
        this.loading = false
      }
    },

    // カートに追加
    async addToCart(data: CartItemInput) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(
          `${API_BASE_URL}/cart/add`,
          {
            ...data,
            quantity: data.quantity || 1
          },
          {
            headers: { 
              Authorization: `Bearer ${authStore.token}`,
              'Content-Type': 'application/json'
            }
          }
        )
        await this.fetchCartItems()
        return response.data
      } catch (error) {
        this.error = 'Failed to add to cart'
        throw error
      } finally {
        this.loading = false
      }
    },
    // src/stores/cart.ts に以下のactionを追加
    async confirmPayment(paymentIntentId: string, shippingAddress: any) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await axios.post(
          `${API_BASE_URL}/payment/confirm-payment`,
          {
            payment_intent_id: paymentIntentId,
            shipping_address: shippingAddress
          },
          {
            headers: { Authorization: `Bearer ${authStore.token}` }
          }
        )
        return response.data
      } catch (error) {
        this.error = 'Failed to confirm payment'
        throw error
      } finally {
        this.loading = false
      }
    },

    // カートアイテムを取得
    async getCartItem(itemId: number) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await axios.get(
          `${API_BASE_URL}/cart/items/${itemId}`,
          {
            headers: { Authorization: `Bearer ${authStore.token}` }
          }
        )
        return response.data
      } catch (error) {
        this.error = 'Failed to fetch cart item'
        throw error
      } finally {
        this.loading = false
      }
    },

    // カートアイテムを更新
    async updateCartItem(itemId: number, updateData: Partial<CartItemInput>) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await axios.put(
          `${API_BASE_URL}/cart/items/${itemId}`,
          updateData,
          {
            headers: { 
              Authorization: `Bearer ${authStore.token}`,
              'Content-Type': 'application/json'
            }
          }
        )
        await this.fetchCartItems()
        return response.data
      } catch (error) {
        this.error = 'Failed to update cart item'
        throw error
      } finally {
        this.loading = false
      }
    },

    // カートアイテムを削除
    async removeItem(itemId: number) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        await axios.delete(
          `${API_BASE_URL}/cart/items/${itemId}`,
          {
            headers: { Authorization: `Bearer ${authStore.token}` }
          }
        )
        await this.fetchCartItems()
      } catch (error) {
        this.error = 'Failed to remove item from cart'
        throw error
      } finally {
        this.loading = false
      }
    },

    // カート全体を取得
    async fetchCartItems() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await axios.get(`${API_BASE_URL}/cart/items`, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })
        this.items = response.data.cart_items
      } catch (error) {
        this.error = 'Failed to fetch cart items'
        throw error
      } finally {
        this.loading = false
      }
    },

    // チェックアウトプロセスを開始
    async initCheckout() {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null

      try {
        const response = await axios.post(
          `${API_BASE_URL}/payment/create-payment`,
          {},
          {
            headers: { Authorization: `Bearer ${authStore.token}` }
          }
        )
        return response.data
      } catch (error) {
        this.error = 'Failed to initialize checkout'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
