<<<<<<< HEAD
# CustomAI Tee

## プロジェクト概要
CustomAI Teeは、Stable Diffusion APIを活用して、ユーザーが独自のTシャツデザインを生成・カスタマイズし、注文できるECサイトです。

## 技術スタック
### バックエンド
- **フレームワーク**: Flask
- **データベース**: 
  - PostgreSQL (RDS): ユーザー情報、注文情報
  - DynamoDB: 一時的な生成リクエストの保存、キャッシュ
- **ストレージ**: AWS S3（デザイン画像の保存）
- **認証**: JWT (JSON Web Tokens)
- **決済**: Stripe API
- **AI生成**: Stable Diffusion API

### フロントエンド
- **フレームワーク**: Vue.js 3 + TypeScript
- **状態管理**: Pinia
- **スタイリング**: Tailwind CSS
- **ルーティング**: Vue Router

## 主要機能
1. **ユーザー認証システム**
   - ユーザー登録/ログイン
   - JWT認証
   - 管理者/一般ユーザーの権限管理

2. **デザイン生成**
   - テキストプロンプトによるデザイン生成
   - S3での画像保存
   - デザインのカスタマイズ（サイズ、位置調整）

3. **カートシステム**
   - カートへの追加/削除
   - 数量、サイズ、カラーの選択
   - カート状態の永続化

4. **注文・決済システム**
   - Stripe決済処理
   - 配送先情報管理
   - 注文履歴管理
   - 注文ステータス更新

5. **メール通知システム**
   - 注文確認メール
   - ステータス更新通知
   - パスワードリセット

## データベース構造
### PostgreSQL
1. **users テーブル**
   - id (PK)
   - username
   - email
   - password_hash
   - is_admin
   - created_at

2. **designs テーブル**
   - id (PK)
   - user_id (FK)
   - prompt
   - image_url
   - s3_key
   - position_x
   - position_y
   - scale
   - created_at

3. **orders テーブル**
   - id (PK)
   - user_id (FK)
   - total_amount
   - status
   - shipping_address (JSON)
   - payment_id
   - created_at

4. **order_items テーブル**
   - id (PK)
   - order_id (FK)
   - design_id (FK)
   - quantity
   - size
   - color
   - price

5. **cart_items テーブル**
   - id (PK)
   - user_id (FK)
   - design_id (FK)
   - quantity
   - size
   - color
   - created_at

### DynamoDB
1. **DesignRequests テーブル**
   - request_id (PK)
   - user_id (SK)
   - prompt
   - status
   - created_at
   - expiration_time (TTL)

2. **DesignCache テーブル**
   - design_id (PK)
   - image_url
   - created_at
   - access_count
   - expiration_time (TTL)

## APIエンドポイント
### 認証
- POST `/api/auth/register`: ユーザー登録
- POST `/api/auth/login`: ログイン
- GET `/api/auth/me`: ユーザー情報取得
- PUT `/api/auth/update-password`: パスワード更新

### デザイン
- POST `/api/designs/generate`: デザイン生成
- GET `/api/designs/designs`: ユーザーのデザイン一覧
- GET `/api/designs/designs/<id>`: デザイン詳細

### カート
- GET `/api/cart/items`: カート内容取得
- POST `/api/cart/add`: カートに追加
- PUT `/api/cart/items/<id>`: カートアイテム更新
- DELETE `/api/cart/items/<id>`: カートアイテム削除

### 決済・注文
- POST `/api/payment/create-payment`: 決済作成
- POST `/api/payment/confirm-payment`: 決済確認
- GET `/api/orders/<id>`: 注文詳細
- PUT `/api/orders/<id>/status`: 注文ステータス更新
- GET `/api/orders/admin/orders`: 管理者用注文一覧

## 拡張予定の機能
1. **在庫管理システム**
   - サイズごとの在庫数管理
   - 在庫切れ警告
   - 自動発注システム

2. **レポート生成機能**
   - 売上レポート
   - 人気デザインランキング
   - ユーザー分析

3. **配送追跡システム**
   - 配送ステータス更新
   - 追跡番号管理
   - 配送業者API連携

## 開発環境のセットアップ
1. **バックエンド**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

2. **フロントエンド**:
```bash
cd frontend
npm install
npm run dev
```

3. **環境変数**:
```plaintext
# .env
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://localhost/customai_tee
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=ap-northeast-1
STRIPE_SECRET_KEY=your_stripe_key
STABILITY_API_KEY=your_stability_key
```
=======
# frontend

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
>>>>>>> bbc61ed (finish Admin frontend)
