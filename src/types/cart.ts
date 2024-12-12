// src/types/cart.ts
export interface DesignConfig {
    position: {
      x: number
      y: number
    }
    scale: number
    rotation: number
  }
  
  export interface CartItemData {
    design_id: number
    quantity: number
    size: string
    color: string
    design_config: DesignConfig
  }
  
  export interface GeneratedDesign {
    id: number
    image_url: string
    prompt: string
  }
// src/types/cart.ts に追加
export interface CartItem {
  id: number
  design_id: number
  quantity: number
  size: string
  color: string
  price: number
  design_config: DesignConfig
}