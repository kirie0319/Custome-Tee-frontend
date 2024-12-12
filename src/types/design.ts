// src/types/design.ts
export interface DesignConfig {
    color: string
    position: {
      x: number
      y: number
    }
    scale: number
    rotation: number
  }
  
  // デフォルト値の定義
  export const DEFAULT_DESIGN_CONFIG: DesignConfig = {
    color: 'white',
    position: { x: 50, y: 50 },
    scale: 1,
    rotation: 0
  }