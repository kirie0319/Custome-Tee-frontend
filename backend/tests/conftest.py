# tests/conftest.py
import pytest
from app import create_app, db
from app.models.user import User
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)  # 文字列ではなくクラスを渡す
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_token(client):
    # 通常ユーザーのトークンを取得
    user = User(username='user', email='user@test.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    response = client.post('/api/auth/login', json={
        'username': 'user',
        'password': 'password'
    })
    return response.json['access_token']