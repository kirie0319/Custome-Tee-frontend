// src/types/user.ts
export interface User {
    id: number
    username: string
    email: string
    is_active: boolean
    is_admin: boolean
    orders_count: number
}