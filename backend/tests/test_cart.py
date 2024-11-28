# tests/test_cart.py
import json

def test_cart_operations(client, auth_token):
    # カートに追加
    add_response = client.post('/api/cart/add',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'design_id': 1,
            'quantity': 1,
            'size': 'M',
            'color': 'White'
        })
    assert add_response.status_code == 201, add_response.data  # エラーメッセージを表示

    # カート内容取得
    get_response = client.get('/api/cart/items',
        headers={'Authorization': f'Bearer {auth_token}'})
    assert get_response.status_code == 200
    data = json.loads(get_response.data)
    assert len(data['cart_items']) > 0

    # カートアイテム更新
    item_id = data['cart_items'][0]['id']
    update_response = client.put(f'/api/cart/items/{item_id}',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'quantity': 2,
            'size': 'L'
        })
    assert update_response.status_code == 200