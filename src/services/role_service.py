from typing import List, Optional
from src.models.role_model import Role
from src.dto.roledto import RoleCreate, RoleUpdate, RoleRead
from src.dto.roledropdown import RoleDropdown
from src.repositories.interfaces.irole_repository import IRoleRepository
from src.services.interfaces.irole_service import IRoleService

class RoleService(IRoleService):
    def __init__(self, repository: IRoleRepository):
        self.repository = repository

    async def get_all_roles(self) -> List[RoleRead]:
        roles = await self.repository.get_all()
        return [RoleRead.model_validate(role, from_attributes=True) for role in roles]

    async def get_role_by_id(self, role_id: int) -> Optional[RoleRead]:
        role = await self.repository.get_by_id(role_id)
        return RoleRead.model_validate(role, from_attributes=True) if role else None

    async def create_role(self, role_data: RoleCreate) -> RoleRead:
        new_role = await self.repository.create_role(role_data)
        return RoleRead.model_validate(new_role, from_attributes=True)

    async def update_role(self, role_id: int, role_data: RoleUpdate) -> Optional[RoleRead]:
        updated_role = await self.repository.update_role(role_id, role_data)
        return RoleRead.model_validate(updated_role, from_attributes=True) if updated_role else None

    async def delete_role(self, role_id: int) -> bool:
        return await self.repository.delete_role(role_id)
    
    async def get_role_dropdown(self) -> List[RoleDropdown]:
        return await self.repository.get_role_dropdown()
