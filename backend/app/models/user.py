# app/models/user.py
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # デフォルトの配送情報をJSON型で追加
    default_shipping_info = db.Column(db.JSON, comment='{name, address, city, postal_code, country}')

    # リレーションシップ
    designs = db.relationship('Design', backref='user', lazy='dynamic')
    orders = db.relationship('Order', backref='customer', lazy='dynamic')
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'default_shipping_info': self.default_shipping_info
        }

    def __repr__(self):
        return f'<User {self.username}>'