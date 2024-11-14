import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import requests

load_dotenv()  # .envファイルから環境変数を読み込み

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return "Hello, CustomAI Tee!"

@app.route('/api/message')
def get_message():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/generate_design', methods=['POST'])
def generate_design():
    data = request.get_json()
    theme = data.get("theme", "")
    
    # Stable Diffusion APIへのリクエスト
    api_url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {os.getenv('REPLICATE_API_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "version": "stable-diffusion-1.5",
        "input": {
            "prompt": theme
        }
    }

    response = requests.post(api_url, headers=headers, json=payload)
    result = response.json()
    print("API Response:", result)

    
    # 画像URLを取得
    image_url = result["output"][0] if "output" in result else "Error generating image"
    return jsonify({"message": f"Design generated for theme: {theme}", "image_url": image_url})

if __name__ == '__main__':
    app.run(debug=True)
