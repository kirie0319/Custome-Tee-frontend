# app/api/auth/routes.py
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from app import db
from app.models.user import User
from app.api.auth import bp

# ユーザー登録
@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # 必要なフィールドの確認
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # ユーザー名とメールアドレスの重複チェック
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400

        # 新規ユーザーの作成
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])

        # 最初のユーザーを管理者に設定
        if User.query.count() == 0:
            user.is_admin = True

        # データベースに保存
        db.session.add(user)
        db.session.commit()

        # アクセストークンの生成
        access_token = create_access_token(
            identity=user.id,
            additional_claims={'is_admin': user.is_admin},
            expires_delta=timedelta(days=1)
        )

        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ログイン
@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # 必要なフィールドの確認
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400

        # ユーザーの検索と認証
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(
                identity=user.id,
                additional_claims={'is_admin': user.is_admin},
                expires_delta=timedelta(days=1)
            )
            return jsonify({
                'access_token': access_token,
                'user': user.to_dict()
            }), 200

        return jsonify({'error': 'Invalid username or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ユーザープロフィール取得
@bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify(user.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 管理者用：全ユーザー一覧取得
@bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Unauthorized access'}), 403

        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# パスワード更新
@bp.route('/update-password', methods=['PUT'])
@jwt_required()
def update_password():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({'error': 'Current password and new password are required'}), 400

        if not user.check_password(data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 400

        user.set_password(data['new_password'])
        db.session.commit()

        return jsonify({'message': 'Password updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500