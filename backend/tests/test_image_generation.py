# tests/test_image_generation.py
import os
import sys
import uuid
from pathlib import Path

# プロジェクトルートへのパスを追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.utils.stable_diffusion import StableDiffusionClient
from app.utils.s3 import S3Client

def test_image_generation_and_upload():
    """画像生成からS3アップロードまでの統合テスト"""
    print("Starting image generation test...")
    
    try:
        # Stable Diffusion で画像を生成
        sd_client = StableDiffusionClient()
        prompt = "A modern t-shirt design with mountain landscape, minimalist style"
        image_data = sd_client.generate_image(prompt)
        print("✓ Image generated successfully")
        
        # 生成された画像をS3にアップロード
        s3_client = S3Client()
        filename = f"test_design_{uuid.uuid4()}.png"
        image_url = s3_client.upload_design(image_data, filename)
        print(f"✓ Image uploaded successfully")
        print(f"Image URL: {image_url}")
        
        return True
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_image_generation_and_upload()