# app/utils/dynamodb.py
import boto3
import os
from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

class DynamoDBClient:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
    def create_design_requests_table(self):
        table = self.dynamodb.create_table(
            TableName='DesignRequests',
            KeySchema=[
                {'AttributeName': 'request_id', 'KeyType': 'HASH'},
                {'AttributeName': 'user_id', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'request_id', 'AttributeType': 'S'},
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'created_at', 'AttributeType': 'N'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user_id-created_at-index',
                    'KeySchema': [
                        {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        return table

    def create_design_cache_table(self):
        table = self.dynamodb.create_table(
            TableName='DesignCache',
            KeySchema=[
                {'AttributeName': 'design_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'design_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        return table

    def store_design_request(self, request_id, user_id, prompt):
        table = self.dynamodb.Table('DesignRequests')
        timestamp = int(datetime.now(timezone.utc).timestamp())
        expiration_time = int((datetime.now(timezone.utc) + timedelta(days=1)).timestamp())
        
        try:
            response = table.put_item(
                Item={
                    'request_id': request_id,
                    'user_id': user_id,
                    'prompt': prompt,
                    'status': 'pending',
                    'created_at': timestamp,
                    'expiration_time': expiration_time
                }
            )
            return response
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise

    def cache_design(self, design_id, image_url):
        table = self.dynamodb.Table('DesignCache')
        timestamp = int(datetime.now(timezone.utc).timestamp())
        expiration_time = int((datetime.now(timezone.utc) + timedelta(days=7)).timestamp())
        
        try:
            response = table.put_item(
                Item={
                    'design_id': design_id,
                    'image_url': image_url,
                    'created_at': timestamp,
                    'access_count': 0,
                    'last_accessed': timestamp,
                    'expiration_time': expiration_time
                }
            )
            return response
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise