# app/api/cart/routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.order import CartItem
from app.models.design import Design
from app.api.cart import bp

@bp.route('/items', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        current_user_id = get_jwt_identity()
        cart_items = CartItem.query.filter_by(user_id=current_user_id).all()

        return jsonify({
            'cart_items': [{
                'id': item.id,
                'design': {
                    'id': item.design.id,
                    'image_url': item.design.image_url,
                    'prompt': item.design.prompt
                },
                'quantity': item.quantity,
                'size': item.size,
                'color': item.color,
                'design_config': item.design_config
            } for item in cart_items]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/items/<int:item_id>', methods=['GET'])
@jwt_required()
def get_cart_item(item_id):
    try:
        current_user_id = get_jwt_identity()
        cart_item = CartItem.query.filter_by(
            id=item_id,
            user_id=current_user_id
        ).first_or_404()

        return jsonify({
            'id': cart_item.id,
            'design': {
                'id': cart_item.design.id,
                'image_url': cart_item.design.image_url,
                'prompt': cart_item.design.prompt
            },
            'quantity': cart_item.quantity,
            'size': cart_item.size,
            'color': cart_item.color,
            'design_config': cart_item.design_config
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        data = request.get_json()
        print("Received cart data:", data)  # デバッグ用

        if not data or not all(k in data for k in ['design_id', 'quantity', 'size', 'color']):
            return jsonify({'error': 'Missing required fields'}), 400

        current_user_id = get_jwt_identity()
        design = Design.query.get_or_404(data['design_id'])

        cart_item = CartItem(
            user_id=current_user_id,
            design_id=design.id,
            quantity=data['quantity'],
            size=data['size'],
            color=data['color'],
            design_config=data.get('design_config')  # オプショナル
        )

        db.session.add(cart_item)
        db.session.commit()

        return jsonify({
            'message': 'Item added to cart',
            'cart_item': {
                'id': cart_item.id,
                'design_id': cart_item.design_id,
                'quantity': cart_item.quantity,
                'size': cart_item.size,
                'color': cart_item.color,
                'design_config': cart_item.design_config
            }
        }), 201

    except Exception as e:
        print(f"Cart error: {str(e)}")  # デバッグ用
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    try:
        current_user_id = get_jwt_identity()
        cart_item = CartItem.query.filter_by(
            id=item_id, 
            user_id=current_user_id
        ).first_or_404()

        db.session.delete(cart_item)
        db.session.commit()

        return jsonify({'message': 'Item removed from cart'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    try:
        data = request.get_json()
        print("Update cart data:", data)  # デバッグ用

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        current_user_id = get_jwt_identity()
        cart_item = CartItem.query.filter_by(
            id=item_id, 
            user_id=current_user_id
        ).first_or_404()

        # 更新可能なフィールド
        if 'quantity' in data:
            cart_item.quantity = data['quantity']
        if 'size' in data:
            cart_item.size = data['size']
        if 'color' in data:
            cart_item.color = data['color']
        if 'design_config' in data:
            cart_item.design_config = data['design_config']

        db.session.commit()

        # 更新されたアイテムの情報を返す
        return jsonify({
            'message': 'Cart item updated',
            'cart_item': {
                'id': cart_item.id,
                'design': {
                    'id': cart_item.design.id,
                    'image_url': cart_item.design.image_url,
                    'prompt': cart_item.design.prompt
                },
                'quantity': cart_item.quantity,
                'size': cart_item.size,
                'color': cart_item.color,
                'design_config': cart_item.design_config
            }
        }), 200

    except Exception as e:
        print(f"Update error: {str(e)}")  # デバッグ用
        db.session.rollback()
        return jsonify({'error': str(e)}), 500