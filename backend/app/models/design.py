# app/models/design.py
from datetime import datetime
from app import db

class Design(db.Model):
    __tablename__ = 'designs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    prompt = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    s3_key = db.Column(db.String(200), nullable=False)
    position_x = db.Column(db.Float, default=0)
    position_y = db.Column(db.Float, default=0)
    scale = db.Column(db.Float, default=1.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)