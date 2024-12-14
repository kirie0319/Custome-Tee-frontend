// src/types/admin.ts
export interface User {
    id: number
    username: string
    email: string
    is_active: boolean
    is_admin: boolean
    orders_count: number
}

export interface OrderItem {
    id: number
    quantity: number
    price: number
    design: {
        image_url: string
        prompt: string
    }
    size: string
    color: string
}

export interface ShippingAddress {
    name: string
    address1: string
    city: string
    prefecture: string
    postal_code: string
}

export interface Order {
    id: number
    user: User
    items: OrderItem[]
    items_count: number
    total_amount: number
    status: OrderStatus
    shipping_address: ShippingAddress
    created_at: string
}

export type OrderStatus = 'paid' | 'processing' | 'shipped' | 'delivered' | 'cancelled'

export interface PaginatedResponseOrder<T> {
    orders: T[]
    total: number
    pages: number
}

export interface PaginatedResponseUser<T> {
    users: T[]
    total: number
    pages: number
}

// 既存の型定義の後に追加
export type UserAction = 'activate' | 'deactivate' | 'make_admin' | 'remove_admin'