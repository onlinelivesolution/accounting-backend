from src.models.role_model import Role
from src.dto.roledto import RoleCreate, RoleUpdate
from src.dto.roledropdown import RoleDropdown
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from common.generic.generic_repository import GenericRepository
from common.generic.igeneric_repository import IGenericRepository

class RoleRepository(GenericRepository[Role], IGenericRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Role, db)
        
    async def create_role(self, role_data: RoleCreate) -> Role:
        created_date = (
            role_data.createdDate.replace(tzinfo=None)
            if getattr(role_data, "createdDate", None)
            else datetime.utcnow()
        )

        new_role = Role(
            roleName=role_data.roleName,
            description=role_data.description,
            isActive=role_data.isActive,
            companyCode=role_data.companyCode,
            createdBy=role_data.createdBy,
            createdDate=created_date
        )
        return await self.add(new_role)
    
    async def update_role(self, role_id: int, role_data: RoleUpdate) -> Optional[Role]:
        result = await self.db.execute(select(Role).where(Role.roleID == role_id))
        existing_role = result.scalar_one_or_none()

        if not existing_role:
            return None

        for key, value in role_data.model_dump(exclude_unset=True).items():
            setattr(existing_role, key, value)

        existing_role.updatedDate = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(existing_role)
        return existing_role
        
    async def get_all(self) -> List[Role]:
        result = await self.db.execute(select(Role))
        return result.scalars().all()

    async def get_by_id(self, role_id: int) -> Optional[Role]:
        result = await self.db.execute(select(Role).where(Role.roleID == role_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, role_name: str) -> Optional[Role]:
        result = await self.db.execute(select(Role).where(Role.roleName == role_name))
        return result.scalar_one_or_none()

    async def add(self, entity: Role) -> Role:
        """Implements IGenericRepository.add"""
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
    
    async def get_role_dropdown(self) -> List[RoleDropdown]:
        result = await self.db.execute(select(Role))
        roles = result.scalars().all()
        return [RoleDropdown.model_validate(c) for c in roles]




