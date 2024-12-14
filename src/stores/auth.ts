// src/stores/auth.ts
import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

interface User {
  id: number
  username: string
  email: string
  is_admin: boolean
}

interface ShippingInfo {
  name: string
  address: string
  city: string
  postal_code: string
  country: string
}

interface RegistrationData {
  username: string
  email: string
  password: string
  default_shipping_info?: ShippingInfo | null
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}

interface AuthResponse {
  access_token: string
  user: User
  message?: string
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false
  }),

  getters: {
    isAdmin: (state) => state.user?.is_admin || false,
  },

  actions: {
    async login(username: string, password: string) {
      try {
        const response = await axios.post<AuthResponse>(`${API_BASE_URL}/auth/login`, {
          username,
          password
        })
        
        const { access_token, user } = response.data
        this.token = access_token
        this.user = user
        this.isAuthenticated = true
        
        localStorage.setItem('token', access_token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        
        return true
      } catch (error) {
        console.error('Login failed:', error)
        throw error
      }
    },

    async register(data: RegistrationData) {
      try {
        console.log('Registering with data:', data)  // デバッグ用
        
        const response = await axios.post<AuthResponse>(`${API_BASE_URL}/auth/register`, data)
        
        const { access_token, user } = response.data
        this.token = access_token
        this.user = user
        this.isAuthenticated = false
        
        localStorage.setItem('token', access_token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        
        return true
      } catch (error) {
        console.error('Registration failed:', error)
        throw error
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    },

    // 初期化時の認証状態の復元
    initializeAuth() {
      const token = localStorage.getItem('token')
      if (token) {
        this.token = token
        this.isAuthenticated = true
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      }
    },

    // ユーザープロフィールの取得
    async fetchUserProfile() {
      try {
        if (!this.token) return null

        const response = await axios.get<User>(`${API_BASE_URL}/auth/me`, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        
        this.user = response.data
        return response.data
      } catch (error) {
        console.error('Failed to fetch user profile:', error)
        this.logout()
        throw error
      }
    }
  }
})