# app/api/orders/__init__.py
from flask import Blueprint

bp = Blueprint('orders', __name__)

from app.api.orders import routes