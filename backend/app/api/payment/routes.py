# app/api/payment/routes.py
import os
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.order import Order, OrderItem, CartItem
from app.models.user import User
from app.utils.stripe import StripeService
from app.utils.email import EmailService
from app.api.payment import bp

@bp.route('/create-payment', methods=['POST'])
@jwt_required()
def create_payment():
    try:
        current_user_id = get_jwt_identity()
        
        # カート内のアイテムを取得
        cart_items = CartItem.query.filter_by(user_id=current_user_id).all()
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400

        # 合計金額を計算（実際のロジックに応じて調整）
        total_amount = sum(item.quantity * 2000 for item in cart_items)

        # Stripeの支払いインテントを作成
        payment_data = StripeService.create_payment_intent(total_amount)

        return jsonify({
            'client_secret': payment_data['client_secret'],
            'payment_intent_id': payment_data['payment_intent_id'],
            'amount': total_amount
        }), 200

    except Exception as e:
        print(f"Error in create_payment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/confirm-payment', methods=['POST'])
@jwt_required()
def confirm_payment():
    try:
        data = request.get_json()
        print("Received data:", data)  # デバッグ用
        if not data or not data.get('payment_intent_id') or not data.get('shipping_address'):
            return jsonify({'error': 'Missing required fields'}), 400

        current_user_id = get_jwt_identity()
        payment_intent_id = data['payment_intent_id']
        shipping_info = data['shipping_address']

        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # カート内のアイテムを取得
        cart_items = CartItem.query.filter_by(user_id=current_user_id).all()
        print(f"User ID: {current_user_id}")
        print(f"Cart items found: {len(cart_items)}")
        for item in cart_items:
            print(f"Cart item: design_id={item.design_id}, quantity={item.quantity}")
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400

        total_amount = sum(item.quantity * 2000 for item in cart_items)

        try:
            # 注文を作成
            order = Order(
                user_id=current_user_id,
                total_amount=total_amount,
                status='paid',
                payment_id=payment_intent_id,
                shipping_address=shipping_info
            )
            db.session.add(order)
            db.session.flush()

            # 注文アイテムを作成
            for cart_item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    design_id=cart_item.design_id,
                    quantity=cart_item.quantity,
                    size=cart_item.size,
                    color=cart_item.color,
                    price=2000  # 単価
                )
                db.session.add(order_item)

            # カートを空にする
            for item in cart_items:
                db.session.delete(item)

            db.session.commit()

            # メール送信を試行
            try:
                mail_result = EmailService.send_order_confirmation(order=order, recipient_email=user.email)
                if not mail_result:
                    print("Warning: Failed to send order confirmation email")
            except Exception as mail_error:
                print(f"Email sending error: {str(mail_error)}")
                # メール送信エラーは注文処理に影響を与えない

            return jsonify({
                'message': 'Payment confirmed and order created',
                'order_id': order.id
            }), 200

        except Exception as db_error:
            db.session.rollback()
            print(f"Database error: {str(db_error)}")
            return jsonify({'error': 'Failed to process order'}), 500

    except Exception as e:
        print(f"Error in confirm_payment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        current_user_id = get_jwt_identity()
        orders = Order.query.filter_by(user_id=current_user_id).all()

        return jsonify({
            'orders': [{
                'id': order.id,
                'total_amount': order.total_amount,
                'status': order.status,
                'created_at': order.created_at.isoformat(),
                'items': [{
                    'design_id': item.design_id,
                    'quantity': item.quantity,
                    'size': item.size,
                    'color': item.color,
                    'price': item.price
                } for item in order.order_items]
            } for order in orders]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500