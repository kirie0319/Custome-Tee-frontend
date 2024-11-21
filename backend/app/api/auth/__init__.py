# app/api/auth/__init__.py
from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.api.auth import routes  # これは最後に配置する必要があります