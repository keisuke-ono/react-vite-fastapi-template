from typing import Optional

from app.domain.user.repository import UserRepository
from app.domain.team.repository import TeamRepository
from app.domain.team.team import Team

class TeamAssignmentUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        team_repository: TeamRepository,
        notification_service: NotificationService
    ):
        self.user_repository = user_repository
        self.team_repository = team_repository
        self.notification_service = notification_service

    async def execute(
        self, 
        user_id: str, 
        team_id: str
    ) -> None:
        """ユーザーをチームに割り当てる"""
        # 1. ユーザーとチームの取得
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("ユーザーが見つかりません")

        team = await self.team_repository.get_by_id(team_id)
        if not team:
            raise ValueError("チームが見つかりません")

        # 2. チームのメンバー数チェック
        if team.is_full():
            raise ValueError("チームのメンバー数が上限に達しています")

        # 3. ユーザーのチーム数チェック
        user_teams = await self.team_repository.get_teams_by_user_id(user_id)
        if len(user_teams) >= 3:  # 最大3チームまで
            raise ValueError("ユーザーが所属できるチーム数の上限に達しています")

        # 4. チームへの割り当て
        team.add_member(user)
        await self.team_repository.update(team)

        # 5. 通知の送信
        await self.notification_service.notify_team_assignment(
            user_id=user_id,
            team_id=team_id
        )
