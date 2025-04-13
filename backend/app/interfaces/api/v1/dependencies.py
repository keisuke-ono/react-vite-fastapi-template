from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional, Union
from jose import JWTError

from app.domain.user import User
from app.main import get_auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    現在の認証済みユーザーを取得する依存関係
    """
    auth_service = get_auth_service()
    
    try:
        payload = await auth_service.verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="無効な認証情報です",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        user = User(
            id=payload.get("sub", ""),
            email=payload.get("email", ""),
            username=payload.get("username", ""),
            password_hash="",  # パスワードハッシュは認証後に必要ないため空文字
            roles=payload.get("roles", [])
        )
        return user
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効な認証情報です",
            headers={"WWW-Authenticate": "Bearer"},
        )

def has_role(required_roles: Union[str, List[str]]):
    """
    特定のロールを持つユーザーのみアクセスを許可する依存関係ファクトリ
    
    使用例:
    @router.get("/admin-only", dependencies=[Depends(has_role("admin"))])
    または
    @router.get("/manager-only", dependencies=[Depends(has_role(["manager", "admin"]))])
    """
    if isinstance(required_roles, str):
        required_roles = [required_roles]
        
    async def role_checker(current_user: User = Depends(get_current_user)) -> bool:
        user_roles = getattr(current_user, "roles", [])
        
        if not user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="このリソースにアクセスする権限がありません",
            )
            
        # 少なくとも1つの必要なロールを持っているか確認
        if not any(role in required_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="このリソースにアクセスする権限がありません",
            )
            
        return True
        
    return role_checker

def get_optional_user(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[User]:
    """
    認証トークンが提供された場合のみユーザーを返す依存関係
    認証が必須ではないエンドポイントに使用
    """
    try:
        if token:
            return get_current_user(token)
        return None
    except HTTPException:
        return None 