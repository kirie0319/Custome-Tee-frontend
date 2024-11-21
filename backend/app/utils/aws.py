# app/utils/aws.py
import boto3
import os

def test_aws_connection():
    """Test AWS credentials and connection"""
    try:
        # Test DynamoDB connection
        dynamodb = boto3.resource('dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        # List existing tables
        existing_tables = list(dynamodb.tables.all())
        print("Existing DynamoDB tables:", [table.name for table in existing_tables])
        
        return True
    except Exception as e:
        print("AWS Connection Error:", str(e))
        return False