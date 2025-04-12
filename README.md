# React + Vite + FastAPI Template

このプロジェクトは、React + Viteで構築されたフロントエンドと、FastAPIで構築されたバックエンドを組み合わせたフルスタックアプリケーションのテンプレートです。クリーンアーキテクチャに基づいて設計されています。

## プロジェクト構成

```
.
├── frontend/          # フロントエンド（React + Vite）
│   ├── src/
│   │   ├── components/  # 再利用可能なUIコンポーネント
│   │   ├── pages/      # ページコンポーネント
│   │   ├── services/   # APIサービス
│   │   ├── stores/     # 状態管理（Zustand）
│   │   ├── types/      # TypeScript型定義
│   │   ├── App.tsx     # アプリケーションのルートコンポーネント
│   │   └── theme.ts    # MUIテーマ設定
│   ├── package.json    # フロントエンド依存関係
│   └── tsconfig.json   # TypeScript設定
│
├── backend/           # バックエンド（FastAPI）
│   ├── app/
│   │   ├── domain/      # ドメイン層 - エンティティとビジネスルール
│   │   │   └── user/    # ユーザードメイン
│   │   │       ├── __init__.py  # パッケージエクスポート
│   │   │       ├── entity.py    # エンティティ定義
│   │   │       ├── repository.py # リポジトリインターフェース
│   │   │       └── service.py   # ドメインサービス
│   │   │
│   │   ├── usecases/    # ユースケース層 - アプリケーションの振る舞い
│   │   │   └── user_management/ # ユーザー管理ユースケース
│   │   │       ├── __init__.py
│   │   │       ├── team_assignment.py    # チーム割り当て
│   │   │       └── department_transfer.py # 部署異動
│   │   │
│   │   ├── interfaces/  # インターフェース層 - 外部とのやり取り
│   │   │   └── api/
│   │   │       └── v1/
│   │   │           ├── schemas/  # リクエスト/レスポンススキーマ
│   │   │           │   └── __init__.py
│   │   │           ├── auth.py  # 認証API
│   │   │           └── users.py # ユーザーAPI
│   │   │
│   │   ├── infrastructure/  # インフラ層 - 外部サービス連携
│   │   │   ├── auth/        # 認証サービス
│   │   │   └── repositories/ # リポジトリ実装
│   │   │
│   │   └── main.py      # アプリケーションのエントリーポイント
│   └── pyproject.toml   # バックエンド依存関係
│
├── docker/           # Docker関連ファイル
├── docker-compose.yml # コンテナ構成
└── .env.example      # 環境変数テンプレート
```

## アーキテクチャ

このプロジェクトはクリーンアーキテクチャに基づいて設計されています：

### 1. ドメイン層
- エンティティとビジネスルールの定義
- 外部依存のない中心的なビジネスロジック
- 例：ユーザー、チーム、部署など

### 2. ユースケース層
- アプリケーション固有のビジネスロジック
- ドメイン層のエンティティを操作
- 複数ドメインを跨ぐ処理を担当
- 例：チーム割り当て、部署異動など

### 3. インターフェース層
- 外部システムとのインターフェース
- API、CLI、GUIなど
- リクエスト/レスポンスの変換
- APIエンドポイントの定義

### 4. インフラストラクチャ層
- 外部サービスとの連携
- データベース、認証、APIなど
- ドメイン層のインターフェースを実装
- 例：DynamoDBリポジトリ、Cognito認証など

## 技術スタック

### フロントエンド
- React 18
- TypeScript
- Vite
- Material-UI (MUI)
- React Query
- Zustand（状態管理）
- React Router
- Axios

### バックエンド
- Python 3.11+
- FastAPI
- AWS Cognito（認証）
- Poetry（依存関係管理）
- DynamoDB（データストア）

## セットアップ

### 前提条件
- Node.js 18+ (fnmを使用)
- Python 3.11+ (pyenvを使用)
- Docker & Docker Compose
- pnpm
- Poetry

### 環境変数の設定
1. `.env.example`を`.env`にコピーし、必要な環境変数を設定します。

### フロントエンドのセットアップ
```bash
# フロントエンドディレクトリに移動
cd frontend

# 依存関係のインストール
pnpm install

# 開発サーバーの起動
pnpm dev
```

### バックエンドのセットアップ
```bash
# バックエンドディレクトリに移動
cd backend

# Poetry設定（プロジェクト内に.venvを作成）
poetry config virtualenvs.in-project true

# 依存関係のインストール
poetry install

# 開発サーバーの起動
poetry run uvicorn app.main:app --reload
```

### DynamoDB Localのセットアップ
```bash
# DynamoDB Localの起動
docker run -p 8000:8000 amazon/dynamodb-local
```

## 開発ツール

### フロントエンド
- **Linter**: ESLint
  ```bash
  pnpm lint
  ```
- **Formatter**: Prettier
  ```bash
  pnpm format
  ```
- **テスト**: Jest
  ```bash
  pnpm test
  ```

### バックエンド
- **Linter**: Ruff
  ```bash
  poetry run ruff check .
  ```
- **Formatter**: Black
  ```bash
  poetry run black .
  ```
- **テスト**: pytest
  ```bash
  poetry run pytest
  ```

## APIドキュメント
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 認証
このプロジェクトはAWS Cognitoを使用した認証システムを実装しています。
- ログイン: `/api/v1/login`
- ユーザー情報取得: `/api/v1/me`

## ライセンス
MIT
