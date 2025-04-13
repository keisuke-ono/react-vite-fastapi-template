from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class User:
    id: str
    email: str
    username: str
    password_hash: str
    is_active: bool = True
    roles: List[str] = field(default_factory=list)
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None

    # 単純な状態の更新のみを行う
    def _set_username(self, username: str) -> None:
        self.username = username
        self.updated_at = datetime.now()

    def _set_active_status(self, is_active: bool) -> None:
        self.is_active = is_active
        self.updated_at = datetime.now()

    def update_username(self, new_username: str) -> None:
        if len(new_username) < 3:
            raise ValueError("ユーザー名は3文字以上必要です")
        self._set_username(new_username)

    def deactivate(self) -> None:
        self._set_active_status(False)

    def activate(self) -> None:
        self._set_active_status(True)
        
    def add_role(self, role: str) -> None:
        """ユーザーにロールを追加"""
        if role not in self.roles:
            self.roles.append(role)
            self.updated_at = datetime.now()
            
    def remove_role(self, role: str) -> None:
        """ユーザーからロールを削除"""
        if role in self.roles:
            self.roles.remove(role)
            self.updated_at = datetime.now()
            
    def has_role(self, role: str) -> bool:
        """ユーザーが特定のロールを持っているかチェック"""
        return role in self.roles
        
    def has_any_role(self, roles: List[str]) -> bool:
        """ユーザーが指定されたロールのいずれかを持っているかチェック"""
        return any(role in self.roles for role in roles)
