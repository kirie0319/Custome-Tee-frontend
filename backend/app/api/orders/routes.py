# app/api/orders/routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models.order import Order, OrderItem
from app.models.user import User
from datetime import datetime
from app.utils.email import EmailService
from app.api.orders import bp

@bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order_details(order_id):
    try:
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        order = Order.query.get_or_404(order_id)
        
        # 管理者でない場合、自分の注文のみアクセス可能
        if not is_admin and order.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        return jsonify({
            'order': {
                'id': order.id,
                'total_amount': order.total_amount,
                'status': order.status,
                'shipping_address': order.shipping_address,
                'created_at': order.created_at.isoformat(),
                'items': [{
                    'id': item.id,
                    'design_id': item.design_id,
                    'quantity': item.quantity,
                    'size': item.size,
                    'color': item.color,
                    'price': item.price,
                    'design': {
                        'image_url': item.design.image_url,
                        'prompt': item.design.prompt
                    }
                } for item in order.order_items]
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500