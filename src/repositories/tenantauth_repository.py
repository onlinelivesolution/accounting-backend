from sqlalchemy import select
from src.models.tenant import Tenant
from src.models.user_model import UserInfo
from src.repositories.interfaces.itenantauth_repository import ITenantAuthRepository
from sqlalchemy import select
from src.models.role_permission_action_model import RolePermissionAction
from src.models.permission_model import Permission
from src.models.permission_action_model import PermissionAction


class TenantAuthRepository(ITenantAuthRepository):

    def __init__(self, db):
        self.db = db

    async def get_tenant_by_email(self, email: str):

        result = await self.db.execute(select(Tenant).where(Tenant.email == email))

        return result.scalars().first()

    async def get_user(self, tenant_db, username: str):

        result = await tenant_db.execute(
            select(UserInfo).where(
                UserInfo.userName == username, UserInfo.isActive == True
            )
        )

        return result.scalars().first()

    async def get_permissions(
        self,
        db,
        role_id: int
    ):

        result = await db.execute(
            select(
                Permission.permissionName.label(
                    "permissionName"
                ),
                PermissionAction.actionName.label(
                    "actionName"
                ),
                RolePermissionAction.isAllowed.label(
                    "isAllowed"
                )
            )
            .join(
                RolePermissionAction,
                Permission.permissionID
                ==
                RolePermissionAction.permissionID
            )
            .join(
                PermissionAction,
                PermissionAction.permissionActionID
                ==
                RolePermissionAction.permissionActionID
            )
            .where(
                RolePermissionAction.roleID
                ==
                role_id
            )
        )

        return [
            {
                "permissionName": row.permissionName,
                "actionName": row.actionName,
                "isAllowed": row.isAllowed
            }
            for row in result
        ]
