from datetime import datetime
from typing import List, Optional

import boto3
from botocore.exceptions import ClientError

from app.domain.user import User
from app.domain.user import UserRepository

class DynamoDBUserRepository(UserRepository):
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    async def get_by_id(self, user_id: str) -> Optional[User]:
        try:
            response = self.table.get_item(Key={'id': user_id})
            item = response.get('Item')
            if not item:
                return None
            return self._item_to_user(item)
        except ClientError as e:
            print(f"Error getting user: {e}")
            return None

    async def get_by_email(self, email: str) -> Optional[User]:
        try:
            response = self.table.query(
                IndexName='email-index',
                KeyConditionExpression='email = :email',
                ExpressionAttributeValues={':email': email}
            )
            items = response.get('Items', [])
            if not items:
                return None
            return self._item_to_user(items[0])
        except ClientError as e:
            print(f"Error getting user by email: {e}")
            return None

    async def list_users(self) -> List[User]:
        try:
            response = self.table.scan()
            items = response.get('Items', [])
            return [self._item_to_user(item) for item in items]
        except ClientError as e:
            print(f"Error listing users: {e}")
            return []

    async def create_user(self, user: User) -> User:
        try:
            item = self._user_to_item(user)
            self.table.put_item(Item=item)
            return user
        except ClientError as e:
            print(f"Error creating user: {e}")
            raise

    async def update_user(self, user: User) -> User:
        try:
            user.updated_at = datetime.now()
            item = self._user_to_item(user)
            self.table.put_item(Item=item)
            return user
        except ClientError as e:
            print(f"Error updating user: {e}")
            raise

    async def delete_user(self, user_id: str) -> bool:
        try:
            self.table.delete_item(
                Key={'id': user_id},
                ConditionExpression='attribute_exists(id)'
            )
            return True
        except ClientError as e:
            print(f"Error deleting user: {e}")
            return False

    def _user_to_item(self, user: User) -> dict:
        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat() if user.updated_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None
        }

    def _item_to_user(self, item: dict) -> User:
        return User(
            id=item['id'],
            email=item['email'],
            username=item['username'],
            is_active=item['is_active'],
            created_at=datetime.fromisoformat(item['created_at']),
            updated_at=datetime.fromisoformat(item['updated_at']) if item.get('updated_at') else None,
            last_login=datetime.fromisoformat(item['last_login']) if item.get('last_login') else None
        ) 