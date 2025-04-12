from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.domain.user import User
from app.domain.user import UserRepository
from app.infrastructure.auth.cognito_auth import CognitoAuth

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserUpdate(BaseModel):
    email: str | None = None
    username: str | None = None
    is_active: bool | None = None

@router.get("/users", response_model=List[User])
async def list_users(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(),
    auth_service: CognitoAuth = Depends()
):
    # トークンの検証
    payload = await auth_service.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return await user_repository.list_users()

@router.post("/users", response_model=User)
async def create_user(
    user_create: UserCreate,
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(),
    auth_service: CognitoAuth = Depends()
):
    # トークンの検証
    payload = await auth_service.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 既存ユーザーのチェック
    existing_user = await user_repository.get_by_email(user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # ユーザーの作成
    user = User(
        id=str(uuid.uuid4()),
        email=user_create.email,
        username=user_create.username
    )
    
    return await user_repository.create_user(user)

@router.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(),
    auth_service: CognitoAuth = Depends()
):
    # トークンの検証
    payload = await auth_service.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(),
    auth_service: CognitoAuth = Depends()
):
    # トークンの検証
    payload = await auth_service.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # ユーザー情報の更新
    if user_update.email:
        user.email = user_update.email
    if user_update.username:
        user.username = user_update.username
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    
    return await user_repository.update_user(user)

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(),
    auth_service: CognitoAuth = Depends()
):
    # トークンの検証
    payload = await auth_service.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    success = await user_repository.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"} 