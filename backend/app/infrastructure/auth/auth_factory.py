from typing import Optional

from app.infrastructure.auth.cognito_auth import CognitoAuth
from app.infrastructure.auth.mock_auth import MockAuth

class AuthFactory:
    @staticmethod
    def create_auth(
        auth_type: str,
        user_pool_id: Optional[str] = None,
        client_id: Optional[str] = None,
        region: Optional[str] = None,
        secret_key: Optional[str] = None
    ):
        if auth_type == "local":
            if not secret_key:
                raise ValueError("Secret key is required for local authentication")
            return MockAuth(secret_key=secret_key)
        
        elif auth_type in ["dev", "trial", "prod"]:
            if not all([user_pool_id, client_id, region, secret_key]):
                raise ValueError("All AWS Cognito parameters are required for AWS authentication")
            return CognitoAuth(
                user_pool_id=user_pool_id,
                client_id=client_id,
                region=region,
                secret_key=secret_key
            )
        
        raise ValueError(f"Invalid auth type: {auth_type}") 