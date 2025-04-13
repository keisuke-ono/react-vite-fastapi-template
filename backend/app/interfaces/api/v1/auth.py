from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.domain.user import User
from app.interfaces.api.v1.dependencies import get_current_user, oauth2_scheme
from app.main import get_auth_service

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginResponse(BaseModel):
    token: Token
    user: User

@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service = Depends(get_auth_service)
):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth_service.create_token(user)
    return LoginResponse(
        token=Token(access_token=token, token_type="bearer"),
        user=user
    )

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user 