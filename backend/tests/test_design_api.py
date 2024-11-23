# tests/test_design_api.py
import os
import sys
from pathlib import Path
import unittest
import json
from datetime import datetime
from sqlalchemy import text

# モデルのインポート順序を修正
from app import create_app, db
from app.models.user import User
from app.models.design import Design
from app.models.order import Order, OrderItem, CartItem

class TestDesignAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'postgresql://mba338@localhost/customai_tee_test',
            'JWT_SECRET_KEY': 'test-secret-key'
        })
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # データベースの再作成
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # テストユーザーの作成
            self.test_user = User(
                username="testuser",
                email="test@example.com",
                is_admin=False
            )
            self.test_user.set_password("testpassword123")
            db.session.add(self.test_user)
            db.session.commit()
            
            # ログインしてトークンを取得
            response = self.client.post('/api/auth/login', json={
                "username": "testuser",
                "password": "testpassword123"
            })
            self.access_token = response.json['access_token']
    
    def test_generate_design(self):
        """デザイン生成APIのテスト"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'prompt': 'A modern mountain landscape t-shirt design'
        }
        
        response = self.client.post(
            '/api/designs/generate',
            headers=headers,
            json=data
        )
        
        print(f"Response: {response.data.decode()}")
        self.assertEqual(response.status_code, 201)
        self.assertIn('design', response.json)
        self.assertIn('image_url', response.json['design'])
    
    def test_get_designs(self):
        """デザイン一覧取得APIのテスト"""
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = self.client.get(
            '/api/designs/designs',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('designs', response.json)
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()