# app/utils/stable_diffusion.py
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

class StableDiffusionClient:
    def __init__(self):
        self.api_key = os.getenv('STABILITY_API_KEY')
        self.api_host = 'https://api.stability.ai'
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def generate_image(self, prompt, size=1024):
        """画像を生成"""
        endpoint = f"{self.api_host}/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        payload = {
            "text_prompts": [
                {
                    "text": prompt,
                    "weight": 1
                }
            ],
            "cfg_scale": 7,
            "width": size,
            "height": size,
            "samples": 1,
            "steps": 30,
        }

        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()

            # レスポンスからbase64エンコードされた画像を取得
            data = response.json()
            if data['artifacts']:
                return data['artifacts'][0]['base64']
            raise Exception("No image generated")

        except Exception as e:
            print(f"Image generation failed: {str(e)}")
            raise

def test_stable_diffusion():
    try:
        client = StableDiffusionClient()
        prompt = "A simple mountain landscape, digital art style"
        print("Generating image...")
        
        # 画像を生成
        image_data = client.generate_image(prompt)
        
        # 生成された画像をテスト用にファイルに保存
        import base64
        with open("test_image.png", "wb") as f:
            f.write(base64.b64decode(image_data))
        
        print("Image generated and saved as test_image.png")
        return True
    
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False