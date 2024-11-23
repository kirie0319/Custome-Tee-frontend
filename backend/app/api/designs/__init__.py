# app/api/designs/__init__.py
from flask import Blueprint

bp = Blueprint('designs', __name__)

from app.api.designs import routes