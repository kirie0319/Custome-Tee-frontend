# scripts/setup_dynamodb.py
import os
import sys
from pathlib import Path

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from dotenv import load_dotenv
from app.utils.dynamodb import DynamoDBClient

def setup_dynamodb():
    # 環境変数の読み込み
    load_dotenv()
    
    print("Starting DynamoDB setup...")
    client = DynamoDBClient()
    
    try:
        # Create DesignRequests table
        print("Creating DesignRequests table...")
        design_requests = client.create_design_requests_table()
        print(f"DesignRequests table status: {design_requests.table_status}")
        
        # Create DesignCache table
        print("Creating DesignCache table...")
        design_cache = client.create_design_cache_table()
        print(f"DesignCache table status: {design_cache.table_status}")
        
    except Exception as e:
        print(f"Error setting up DynamoDB: {str(e)}")

if __name__ == "__main__":
    setup_dynamodb()