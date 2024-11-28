# app/api/admin/__init__.py
from flask import Blueprint

bp = Blueprint('admin', __name__)

from app.api.admin import routes  # これは最後に配置する必要があります