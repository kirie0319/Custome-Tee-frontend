# tests/test_admin.py
import pytest
from app import create_app, db
from app.models.user import User
from app.models.order import Order
import json

@pytest.fixture
def admin_token(client):
    # 管理者ユーザーを作成してトークンを取得
    admin = User(username='admin', email='admin@test.com', is_admin=True)
    admin.set_password('password')
    db.session.add(admin)
    db.session.commit()

    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'password'
    })
    return json.loads(response.data)['access_token']

def test_get_stats(client, admin_token):
    response = client.get('/api/admin/stats', 
        headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_sales' in data
    assert 'total_orders' in data
    assert 'total_users' in data

def test_search_orders(client, admin_token):
    response = client.get('/api/admin/orders/search',
        headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'orders' in data
    assert 'total' in data