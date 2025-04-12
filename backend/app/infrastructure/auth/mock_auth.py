from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from app.domain.entities.user import User

class MockAuth:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        # モックユーザーデータ
        self.mock_users = {
            "test@example.com": {
                "password": "password123",
                "id": "mock-user-1",
                "username": "testuser"
            }
        }

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        # メールアドレスでユーザーを検索
        user_data = self.mock_users.get(username)
        if not user_data or user_data["password"] != password:
            return None

        return User(
            id=user_data["id"],
            email=username,
            username=user_data["username"],
            last_login=datetime.now()
        )

    async def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=['HS256']
            )
            return payload
        except jwt.JWTError:
            return None

    def create_token(self, user: User) -> str:
        expires_delta = timedelta(minutes=30)
        expire = datetime.utcnow() + expires_delta
        
        to_encode = {
            'sub': user.id,
            'email': user.email,
            'username': user.username,
            'exp': expire
        }
        
        return jwt.encode(to_encode, self.secret_key, algorithm='HS256') 