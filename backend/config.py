# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://mba338@localhost/customai_tee'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT config
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # CORS config
    CORS_HEADERS = 'Content-Type'

    # メール設定
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    
    # アプリケーション設定
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

    # AWS S3設定
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'ap-northeast-1')
    S3_BUCKET = os.getenv('S3_BUCKET')

    # Stripe設定
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # インメモリデータベースを使用
    WTF_CSRF_ENABLED = False