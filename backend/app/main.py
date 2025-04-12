import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.auth.auth_factory import AuthFactory
from app.infrastructure.repositories.dynamodb_user_repository import DynamoDBUserRepository

app = FastAPI(
    title="Admin API",
    description="Admin API with Fast-API and Clean Architecture",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 環境変数の取得
AUTH_TYPE = os.getenv("AUTH_TYPE", "local")

def get_env_prefix(auth_type: str) -> str:
    if auth_type == "local":
        return ""
    return f"{auth_type.upper()}_"

# 依存関係の注入
def get_user_repository():
    return DynamoDBUserRepository(table_name="users")

def get_auth_service():
    env_prefix = get_env_prefix(AUTH_TYPE)
    
    if AUTH_TYPE == "local":
        return AuthFactory.create_auth(
            auth_type="local",
            secret_key=os.getenv(f"{env_prefix}LOCAL_SECRET_KEY")
        )
    
    return AuthFactory.create_auth(
        auth_type=AUTH_TYPE,
        user_pool_id=os.getenv(f"{env_prefix}AWS_COGNITO_USER_POOL_ID"),
        client_id=os.getenv(f"{env_prefix}AWS_COGNITO_CLIENT_ID"),
        region=os.getenv(f"{env_prefix}AWS_REGION"),
        secret_key=os.getenv(f"{env_prefix}AWS_COGNITO_SECRET_KEY")
    )

# ルーターのインポート
from app.interfaces.api.v1 import auth, users

# ルーターの登録
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to Admin API"} 