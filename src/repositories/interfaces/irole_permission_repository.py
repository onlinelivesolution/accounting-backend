from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.role_permission_action_model import RolePermissionAction
from src.dto.rolepermissiondto import RolePermissionCreate, RolePermissionRead, RolePermissionUpdate

class IRolePermissionRepository(ABC):
    
    @abstractmethod
    async def create_role_permission(self, role_permission_data: RolePermissionCreate) -> RolePermissionAction:
        pass
    
    @abstractmethod
    async def update_role_permission(self, role_permission_id: int, role_permission_data: RolePermissionUpdate) -> Optional[RolePermissionAction]:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[RolePermissionAction]:
        pass

    @abstractmethod
    async def get_by_id(self, role_permission_id: int) -> Optional[RolePermissionAction]:
        pass
