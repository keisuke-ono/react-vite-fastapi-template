from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: str
    email: str
    username: str
    password_hash: str
    is_active: bool = True
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
