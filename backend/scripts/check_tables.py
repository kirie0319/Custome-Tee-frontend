# scripts/check_tables.py
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from dotenv import load_dotenv
import boto3

def check_tables_status():
    load_dotenv()
    
    dynamodb = boto3.client('dynamodb',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    
    tables = ['DesignRequests', 'DesignCache']
    
    for table_name in tables:
        try:
            response = dynamodb.describe_table(TableName=table_name)
            status = response['Table']['TableStatus']
            print(f"{table_name} table status: {status}")
        except Exception as e:
            print(f"Error checking {table_name}: {str(e)}")

if __name__ == "__main__":
    check_tables_status()