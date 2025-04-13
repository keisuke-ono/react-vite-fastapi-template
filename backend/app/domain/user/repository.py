from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.user import User

class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        """ユーザーを作成する"""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """IDでユーザーを取得する"""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """メールアドレスでユーザーを取得する"""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """ユーザーを更新する"""
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """ユーザーを削除する"""
        pass

    @abstractmethod
    async def list_users(self) -> List[User]:
        """全ユーザーを取得する"""
        pass
