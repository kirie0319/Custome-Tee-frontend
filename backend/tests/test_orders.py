# tests/test_orders.py
import json

def test_create_order(client, auth_token):
    # カートにアイテムを追加
    cart_response = client.post('/api/cart/add',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'design_id': 1,
            'quantity': 1,
            'size': 'M',
            'color': 'White'
        })
    assert cart_response.status_code == 201, cart_response.data  # エラーメッセージを表示

    # 注文作成
    order_response = client.post('/api/payment/create-payment',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'shipping_address': {
                'name': 'Test User',
                'postal_code': '123-4567',
                'prefecture': 'Tokyo',
                'city': 'Shibuya',
                'address1': 'Test Address',
                'phone': '03-1234-5678'
            }
        })
    assert order_response.status_code == 200, order_response.data
    data = json.loads(order_response.data)
    assert 'payment_intent_id' in data