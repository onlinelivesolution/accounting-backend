from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.rolepermissiondto import RolePermissionCreate, RolePermissionUpdate
from src.models.role_permission_action_model import RolePermissionAction
from common.generic.generic_repository import GenericRepository
from common.generic.igeneric_repository import IGenericRepository
from datetime import datetime
from typing import Optional, List

class RolePermissionRepository(GenericRepository[IGenericRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(RolePermissionAction, db)

    async def create_role_permission(self, role_permission_data: RolePermissionCreate) -> RolePermissionAction:
        created_date = (
            role_permission_data.createdDate.replace(tzinfo=None)
            if getattr(role_permission_data, "createdDate", None)
            else datetime.utcnow()
        )

        new_role_permission = RolePermissionAction(
            roleID=role_permission_data.roleID,
            permissionID=role_permission_data.permissionID,
            companyCode=role_permission_data.companyCode,
            createdBy=role_permission_data.createdBy,
            createdDate=created_date
        )
        return await self.add(new_role_permission)
    
    async def update_role_permission(self, role_permission_id: int, role_permission_data: RolePermissionUpdate) -> Optional[RolePermissionAction]:
        result = await self.db.execute(select(RolePermissionAction).where(RolePermissionAction.rolePermissionActionID == role_permission_id))
        existing_role_permission = result.scalar_one_or_none()

        if not existing_role_permission:
            return None

        for key, value in role_permission_data.model_dump(exclude_unset=True).items():
            setattr(existing_role_permission, key, value)

        existing_role_permission.updatedDate = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(existing_role_permission)
        return existing_role_permission
        
    async def get_all(self) -> List[RolePermissionAction]:
        result = await self.db.execute(select(RolePermissionAction))
        return result.scalars().all()

    async def get_by_id(self, role_permission_id: int) -> Optional[RolePermissionAction]:
        result = await self.db.execute(select(RolePermissionAction).where(RolePermissionAction.rolePermissionActionID == role_permission_id))
        return result.scalar_one_or_none()

    async def add(self, entity: RolePermissionAction) -> RolePermissionAction:
        """Implements IGenericRepository.add"""
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
