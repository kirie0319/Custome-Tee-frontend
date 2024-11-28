# app/api/payment/__init__.py
from flask import Blueprint

bp = Blueprint('payment', __name__)

from app.api.payment import routes