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

    def to_dict(self):
        """
        モデルを辞書に変換するメソッド
        Returns:
            dict: デザインの情報を含む辞書
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'prompt': self.prompt,
            'image_url': self.image_url,
            's3_key': self.s3_key,
            'position_x': self.position_x,
            'position_y': self.position_y,
            'scale': self.scale,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Design {self.id}>'