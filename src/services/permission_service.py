from typing import List, Optional
from src.services.interfaces.ipermission_service import IPermissionService
from src.repositories.interfaces.ipermission_repository import IPermissionRepository
from src.dto.permissiondto import PermissionCreate, PermissionRead, PermissionUpdate
from src.schemas.permission_action_schema import PermissionTreeParent
from src.models.permission_model import Permission

class PermissionService(IPermissionService):
    def __init__(self, repository: IPermissionRepository):
        self.repository = repository
    
    async def get_full_permission_tree(self) -> List[PermissionTreeParent]:
        data = await self.repository.get_full_permission_tree()
        return data
    
    async def create_permission(self, permission_data: PermissionCreate) -> PermissionRead:
        new_permission = await self.repository.create_permission(permission_data)
        return PermissionRead.model_validate(new_permission, from_attributes=True)

    async def update_permission(self, permission_id: int, permission_data: PermissionUpdate) -> Optional[PermissionRead]:
        updated_permission = await self.repository.update_permission(permission_id, permission_data)
        return PermissionRead.model_validate(updated_permission, from_attributes=True) if updated_permission else None

    async def get_all_permissions(self) -> List[PermissionRead]:
        permissions = await self.repository.get_all()
        return [PermissionRead.model_validate(permission, from_attributes=True) for permission in permissions]

    async def get_permission_by_id(self, permission_id: int) -> Optional[PermissionRead]:
        permission = await self.repository.get_by_id(permission_id)
        return PermissionRead.model_validate(permission, from_attributes=True) if permission else None

