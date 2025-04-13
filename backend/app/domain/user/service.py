from typing import Optional

from app.domain.user import User
from app.domain.user.repository import UserRepository

import uuid

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(
        self, 
        email: str, 
        username: str, 
        password_hash: str
    ) -> User:
        """ユーザーを作成する"""
        # メールアドレスの重複チェック
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("このメールアドレスは既に使用されています")

        user = User(
            id=str(uuid.uuid4()),
            email=email,
            username=username,
            password_hash=password_hash
        )
        return await self.user_repository.create(user)

    async def update_user_status(
        self, 
        user_id: str, 
        is_active: bool
    ) -> User:
        """ユーザーのステータスを更新する"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("ユーザーが見つかりません")

        if is_active:
            user.activate()
        else:
            user.deactivate()

        return await self.user_repository.update(user)
