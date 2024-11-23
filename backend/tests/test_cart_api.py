# tests/test_cart_api.py
import unittest
import json
from app import create_app, db
from app.models.user import User
from app.models.design import Design
from app.models.order import CartItem

class TestCartAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'postgresql://mba338@localhost/customai_tee_test'
        })
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # データベース初期化
        db.drop_all()
        db.create_all()
        
        # テストユーザー作成
        self.test_user = User(
            username="testuser",
            email="test@example.com"
        )
        self.test_user.set_password("testpass123")
        db.session.add(self.test_user)
        
        # テストデザイン作成
        self.test_design = Design(
            user_id=1,
            prompt="Test design",
            image_url="https://example.com/test.png"
        )
        db.session.add(self.test_design)
        db.session.commit()
        
        # ログインしてトークン取得
        response = self.client.post('/api/auth/login', json={
            "username": "testuser",
            "password": "testpass123"
        })
        self.access_token = response.json['access_token']

    def test_add_to_cart(self):
        """カートへの商品追加テスト"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'design_id': self.test_design.id,
            'quantity': 1,
            'size': 'M',
            'color': 'White'
        }
        
        response = self.client.post(
            '/api/cart/add',
            headers=headers,
            json=data
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('cart_item', response.json)

    def test_get_cart(self):
        """カート内容取得テスト"""
        # テスト用カートアイテム作成
        cart_item = CartItem(
            user_id=self.test_user.id,
            design_id=self.test_design.id,
            quantity=1,
            size='M',
            color='White'
        )
        db.session.add(cart_item)
        db.session.commit()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = self.client.get(
            '/api/cart',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('cart_items', response.json)
        self.assertEqual(len(response.json['cart_items']), 1)

    def test_update_cart_item(self):
        """カートアイテム更新テスト"""
        cart_item = CartItem(
            user_id=self.test_user.id,
            design_id=self.test_design.id,
            quantity=1,
            size='M',
            color='White'
        )
        db.session.add(cart_item)
        db.session.commit()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'quantity': 2,
            'size': 'L'
        }
        
        response = self.client.put(
            f'/api/cart/{cart_item.id}',
            headers=headers,
            json=data
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['cart_item']['quantity'], 2)
        self.assertEqual(response.json['cart_item']['size'], 'L')

    def test_remove_from_cart(self):
        """カートアイテム削除テスト"""
        cart_item = CartItem(
            user_id=self.test_user.id,
            design_id=self.test_design.id,
            quantity=1,
            size='M',
            color='White'
        )
        db.session.add(cart_item)
        db.session.commit()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = self.client.delete(
            f'/api/cart/{cart_item.id}',
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.query.count(), 0)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()