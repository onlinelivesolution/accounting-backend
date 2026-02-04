from typing import List, Optional
from src.dto.rolepermissiondto import RolePermissionCreate, RolePermissionUpdate, RolePermissionRead
from src.services.interfaces.irole_permission_service import IRolePermissionService
from src.repositories.interfaces.irole_permission_repository import IRolePermissionRepository

class RolePermissionService(IRolePermissionService):
    def __init__(self, repository: IRolePermissionRepository):
        self.repository = repository
    
    async def create_role_permission(self, role_permission_data: RolePermissionCreate) -> RolePermissionRead:
        new_role_permission = await self.repository.create_role_permission(role_permission_data)
        return RolePermissionRead.model_validate(new_role_permission, from_attributes=True)

    async def update_role_permission(self, role_permission_id: int, role_permission_data: RolePermissionUpdate) -> Optional[RolePermissionRead]:
        updated_role_permission = await self.repository.update_role_permission(role_permission_id, role_permission_data)
        return RolePermissionRead.model_validate(updated_role_permission, from_attributes=True) if updated_role_permission else None

    async def get_role_permissions(self) -> List[RolePermissionRead]:
        role_permissions = await self.repository.get_all()
        return [RolePermissionRead.model_validate(role_permission, from_attributes=True) for role_permission in role_permissions]

    async def get_role_permission_by_id(self, role_permission_id: int) -> Optional[RolePermissionRead]:
        role_permission = await self.repository.get_by_id(role_permission_id)
        return RolePermissionRead.model_validate(role_permission, from_attributes=True) if role_permission else None



