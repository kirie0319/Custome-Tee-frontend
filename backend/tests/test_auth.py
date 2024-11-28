# tests/test_auth.py
import pytest
import json

def test_register_login(client):
    # 登録
    register_response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert register_response.status_code == 201

    # ログイン
    login_response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert login_response.status_code == 200
    data = json.loads(login_response.data)
    assert 'access_token' in data