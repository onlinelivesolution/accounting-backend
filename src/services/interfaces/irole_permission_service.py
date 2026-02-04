from abc import ABC, abstractmethod
from typing import List, Optional
from src.dto.rolepermissiondto import RolePermissionCreate, RolePermissionUpdate, RolePermissionRead

class IRolePermissionService(ABC):
    
    @abstractmethod
    async def create_role_permission(self, role_permission_data: RolePermissionCreate) -> RolePermissionRead:
        pass

    @abstractmethod
    async def update_role_permission(self, role_permission_id: int, role_permission_data: RolePermissionUpdate) -> Optional[RolePermissionRead]:
        pass
    
    @abstractmethod
    async def get_role_permissions(self) -> List[RolePermissionRead]:
        pass

    @abstractmethod
    async def get_role_permission_by_id(self, role_permission_id: int) -> Optional[RolePermissionRead]:
        pass


