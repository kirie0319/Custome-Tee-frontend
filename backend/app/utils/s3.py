# app/utils/s3.py
import boto3
import os
from dotenv import load_dotenv
import base64
from io import BytesIO

load_dotenv()

class S3Client:
    def __init__(self):
        self.s3_client = boto3.client('s3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket_name = 'custome-tee-designs'  # 作成したバケット名

    def upload_design(self, image_data, filename):
        """デザイン画像をS3にアップロード"""
        try:
            # base64データをバイナリに変換
            if isinstance(image_data, str):
                # base64文字列の場合、デコード
                image_binary = base64.b64decode(image_data)
            else:
                # すでにバイナリの場合はそのまま使用
                image_binary = image_data

            # S3にアップロード
            self.s3_client.upload_fileobj(
                BytesIO(image_binary),
                self.bucket_name,
                f'designs/{filename}',
                ExtraArgs={
                    'ContentType': 'image/png',
                    'ACL': 'public-read'
                }
            )

            # 公開URLを返す
            return f'https://{self.bucket_name}.s3.{os.getenv("AWS_REGION")}.amazonaws.com/designs/{filename}'

        except Exception as e:
            print(f"S3 upload error: {str(e)}")
            raise

    def delete_design(self, filename):
        """S3から画像を削除"""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=f'designs/{filename}'
            )
            return True
        except Exception as e:
            print(f"S3 delete error: {str(e)}")
            raise

# テスト用の関数
def test_s3_connection():
    try:
        s3 = S3Client()
        # テスト用の小さなファイルをアップロード
        test_data = b"Hello, S3!"
        result = s3.upload_design(test_data, 'test.txt')
        print(f"Upload successful! File URL: {result}")
        
        # テストファイルを削除
        s3.delete_design('test.txt')
        print("Delete successful!")
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False