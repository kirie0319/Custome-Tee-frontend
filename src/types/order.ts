// src/types/order.ts
// src/types/order.ts
export interface Order {
    id: number
    user: {
        email: string
    }
    total_amount: number
    status: OrderStatus
    created_at: string
    items: OrderItem[]
    items_count: number
    shipping_address: ShippingAddress
}

export type OrderStatus = 'paid' | 'processing' | 'shipped' | 'delivered' | 'cancelled'

export interface ShippingAddress {
    address1: string
    address2?: string
    city: string
    postal_code: string
}

export interface OrderItem {
    id: number
    quantity: number
    price: number
}