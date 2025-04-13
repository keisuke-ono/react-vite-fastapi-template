from datetime import datetime, timedelta
from typing import Optional

import boto3
from botocore.exceptions import ClientError
from jose import JWTError, jwt

from app.domain.user import User

class CognitoAuth:
    def __init__(
        self,
        user_pool_id: str,
        client_id: str,
        region: str,
        secret_key: str
    ):
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.region = region
        self.secret_key = secret_key
        self.cognito = boto3.client('cognito-idp', region_name=region)

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        try:
            response = self.cognito.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )

            if response['AuthenticationResult']:
                tokens = response['AuthenticationResult']
                user_info = await self._get_user_info(tokens['AccessToken'])
                
                return User(
                    id=user_info['sub'],
                    email=user_info['email'],
                    username=user_info['username'],
                    last_login=datetime.now()
                )
            return None
        except ClientError as e:
            print(f"Authentication error: {e}")
            return None

    async def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=['HS256']
            )
            return payload
        except JWTError:
            return None

    async def _get_user_info(self, access_token: str) -> dict:
        response = self.cognito.get_user(AccessToken=access_token)
        user_attributes = {
            attr['Name']: attr['Value']
            for attr in response['UserAttributes']
        }
        return {
            'sub': user_attributes.get('sub'),
            'email': user_attributes.get('email'),
            'username': user_attributes.get('username')
        }

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