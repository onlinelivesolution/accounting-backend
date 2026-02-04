from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user_model import UserInfo
from src.models.role_permission_action_model import RolePermissionAction
from src.models.permission_action_model import PermissionAction
from src.models.permission_model import Permission
from src.schemas.permission_schema import PermissionActionInfo
from src.repositories.interfaces.ilogin_repository import ILoginRepository
from common.generic.generic_repository import GenericRepository
from common.utils.password_utils import verify_password
from passlib.hash import argon2


class LoginRepository(GenericRepository[UserInfo], ILoginRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(UserInfo, db)

    async def get_user_by_username(self, username: str):
        stmt = select(UserInfo).where(UserInfo.userName == username, UserInfo.isActive == 1)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def authenticate_user(self, username: str, password: str):
        stmt = select(UserInfo).where(UserInfo.userName == username, UserInfo.isActive == 1)
        result = await self.db.execute(stmt)
        user = result.scalars().first()
        if not user:
            return None

        # ✅ Verify Argon2 password
        if not argon2.verify(password, user.passwordHash):
            return None
        return user

    async def get_user_permissions(self, role_id: int):
        """
        Join RolePermissionAction → PermissionAction → Permission
        to retrieve all allowed permissions for this role.
        """
        query = (
            select(
                Permission.permissionID,
                Permission.permissionName,
                PermissionAction.actionName,
                RolePermissionAction.isAllowed,
            )
            .join(PermissionAction, PermissionAction.permissionActionID == RolePermissionAction.permissionActionID)
            .join(Permission, Permission.permissionID == PermissionAction.permissionID)
            .where(RolePermissionAction.roleID == role_id)
        )

        result = await self.db.execute(query)
        rows = result.all()

        return [
            PermissionActionInfo(
                permissionID=r.permissionID,
                permissionName=r.permissionName,
                actionName=r.actionName,
                isAllowed=r.isAllowed,
            )
            for r in rows
        ]

    async def update_password_hash(self, user_id: int, new_hash: str):
        stmt = (
            update(UserInfo)
            .where(UserInfo.userID == user_id)
            .values(passwordHash=new_hash)
        )
        await self.db.execute(stmt)
        await self.db.commit()
