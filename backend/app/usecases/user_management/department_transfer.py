from typing import Optional

from app.domain.user.repository import UserRepository
from app.domain.department.repository import DepartmentRepository
from app.domain.department.department import Department

class DepartmentTransferUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        department_repository: DepartmentRepository,
        notification_service: NotificationService,
        approval_service: ApprovalService
    ):
        self.user_repository = user_repository
        self.department_repository = department_repository
        self.notification_service = notification_service
        self.approval_service = approval_service

    async def execute(
        self, 
        user_id: str, 
        new_department_id: str,
        transfer_date: date
    ) -> None:
        """ユーザーを部署間で異動させる"""
        # 1. ユーザーと部署の取得
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("ユーザーが見つかりません")

        new_department = await self.department_repository.get_by_id(new_department_id)
        if not new_department:
            raise ValueError("部署が見つかりません")

        # 2. 異動可能かチェック
        if not new_department.can_accept_transfer():
            raise ValueError("この部署は現在異動を受け付けていません")

        # 3. 承認プロセスの開始
        approval_request = await self.approval_service.request_transfer_approval(
            user_id=user_id,
            current_department_id=user.department_id,
            new_department_id=new_department_id,
            transfer_date=transfer_date
        )

        # 4. 関係者への通知
        await self.notification_service.notify_transfer_request(
            user_id=user_id,
            current_department_id=user.department_id,
            new_department_id=new_department_id,
            transfer_date=transfer_date,
            approval_request_id=approval_request.id
        )

        # 5. 承認待ち状態に更新
        user.update_transfer_status("pending")
        await self.user_repository.update(user)
