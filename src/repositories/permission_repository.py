from src.models.permission_model import Permission
from sqlalchemy import select
from datetime import datetime
from sqlalchemy.orm import selectinload
from typing import List, Dict, Any, Optional
from src.dto.permissiondto import PermissionCreate, PermissionUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from common.generic.generic_repository import GenericRepository
from common.generic.igeneric_repository import IGenericRepository

class PermissionRepository(GenericRepository[Permission], IGenericRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Permission, db)
        
    async def get_full_permission_tree(self) -> List[Dict[str, Any]]:
        query = (
            select(Permission)
            .options(selectinload(Permission.actions))
            .where(Permission.isActive == True)
        )

        result = await self.db.execute(query)
        permissions = result.scalars().unique().all()

        tree = []
        for perm in permissions:
            children = [
                {
                    "permissionActionID": act.permissionActionID,
                    "actionName": act.actionName,
                    "actionKey": act.actionKey,
                    "isActive": act.isActive
                }
                for act in perm.actions if act.isActive
            ]
            tree.append({
                "permissionID": perm.permissionID,
                "permissionName": perm.permissionName,
                "children": children
            })
        return tree
        
    async def create_permission(self, permission_data: PermissionCreate) -> Permission:
        created_date = (
            permission_data.createdDate.replace(tzinfo=None)
            if getattr(permission_data, "createdDate", None)
            else datetime.utcnow()
        )

        new_permission = Permission(
            permissionName=permission_data.permissionName,
            moduleName=permission_data.moduleName,
            description=permission_data.description,
            isActive=permission_data.isActive,
            companyCode=permission_data.companyCode,
            createdBy=permission_data.createdBy,
            createdDate=created_date
        )
        return await self.add(new_permission)
    
    async def update_permission(self, permission_id: int, permission_data: PermissionUpdate) -> Optional[Permission]:
        result = await self.db.execute(select(Permission).where(Permission.permissionID == permission_id))
        existing_permission = result.scalar_one_or_none()

        if not existing_permission:
            return None

        for key, value in permission_data.model_dump(exclude_unset=True).items():
            setattr(existing_permission, key, value)

        existing_permission.updatedDate = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(existing_permission)
        return existing_permission
        
    async def get_all(self) -> List[Permission]:
        result = await self.db.execute(select(Permission))
        return result.scalars().all()

    async def get_by_id(self, permission_id: int) -> Optional[Permission]:
        result = await self.db.execute(select(Permission).where(Permission.permissionID == permission_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, permission_name: str) -> Optional[Permission]:
        result = await self.db.execute(select(Permission).where(Permission.permissionName == permission_name))
        return result.scalar_one_or_none()

    async def add(self, entity: Permission) -> Permission:
        """Implements IGenericRepository.add"""
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

