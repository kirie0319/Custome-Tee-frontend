// src/types/cart.ts
export interface DesignConfig {
    color: string
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
  

export interface CartItemInput {
  design_id: number
  quantity: number
  size: string
  color: string
  design_config: DesignConfig
}

  // export interface GenerateDesignResponse {
  //   id: number
  //   image_url: string
  //   prompt: string
  // }

  export interface GenerateDesignResponse {
    design: {
      created_at: string
      id: number
      image_url: string
      prompt: string
    }
    message: string
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
  design: GenerateDesignResponse  // これを追加
}