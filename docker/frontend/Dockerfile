FROM node:18-slim

WORKDIR /app

# pnpmをインストール
RUN npm install -g pnpm

# 依存関係ファイルをコピー
COPY package.json pnpm-lock.yaml ./

# 依存関係をインストール
RUN pnpm install

# アプリケーションのソースコードをコピー
COPY . .

# 開発サーバーを起動
CMD ["pnpm", "dev", "--host", "0.0.0.0"] 