# scripts/test_dynamodb.py
import os
import sys
from pathlib import Path
import uuid
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from dotenv import load_dotenv
from app.utils.dynamodb import DynamoDBClient

def test_dynamodb_operations():
    load_dotenv()
    client = DynamoDBClient()
    
    # テストデータ作成
    request_id = str(uuid.uuid4())
    user_id = "test_user_1"
    prompt = "A modern t-shirt design with mountain landscape"
    
    print("\n=== Testing Design Request Storage ===")
    try:
        # デザインリクエストの保存テスト
        response = client.store_design_request(request_id, user_id, prompt)
        print("Stored design request:", response)
        
        # デザインキャッシュの保存テスト
        design_id = str(uuid.uuid4())
        image_url = "https://example.com/design-123.jpg"
        cache_response = client.cache_design(design_id, image_url)
        print("\n=== Testing Design Cache Storage ===")
        print("Cached design:", cache_response)
        
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"Error during test: {str(e)}")

if __name__ == "__main__":
    test_dynamodb_operations()