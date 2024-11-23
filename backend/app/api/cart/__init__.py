# app/api/cart/__init__.py
from flask import Blueprint

bp = Blueprint('cart', __name__)

from app.api.cart import routes  # Blueprint作成後にroutesをインポート