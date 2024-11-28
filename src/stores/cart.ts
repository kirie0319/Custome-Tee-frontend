// src/stores/cart.ts
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

interface CartItem {
  id: number
  design: {
    id: number
    image_url: string
    prompt: string
  }
  quantity: number
  size: string
  color: string
  design_config: any
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
    loading: false,
    error: null as string | null,
  }),

  actions: {
    // 個別のカートアイテムを取得
    async getCartItem(itemId: number) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(
          `http://localhost:5000/api/cart/items/${itemId}`,
          {
            headers: { Authorization: `Bearer ${authStore.token}` }
          }
        )
        return response.data
      } catch (error) {
        this.error = 'Failed to fetch cart item'
        console.error(error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // カートアイテムを更新
    async updateCartItem(itemId: number, updateData: any) {
      const authStore = useAuthStore()
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.put(
          `http://localhost:5000/api/cart/items/${itemId}`,
          updateData,
          {
            headers: { Authorization: `Bearer ${authStore.token}` }
          }
        )
        await this.fetchCartItems()
        return response.data
      } catch (error) {
        this.error = 'Failed to update cart item'
        console.error(error)
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
        const response = await axios.get('http://localhost:5000/api/cart/items', {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })
        this.items = response.data.cart_items
      } catch (error) {
        this.error = 'Failed to fetch cart items'
        console.error(error)
      } finally {
        this.loading = false
      }
    }
  }
})