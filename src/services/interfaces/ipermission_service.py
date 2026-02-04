from typing import List, Optional, Any
from abc import ABC, abstractmethod
from src.dto.permissiondto import PermissionCreate, PermissionRead, PermissionUpdate

class IPermissionService(ABC):
    
    @abstractmethod
    async def get_full_permission_tree(self) -> List[Any]:
        pass

    @abstractmethod
    async def create_permission(self, permission_data: PermissionCreate) -> PermissionRead:
        pass

    @abstractmethod
    async def update_permission(self, permission_id: int, permission_data: PermissionUpdate) -> Optional[PermissionRead]:
        pass
    
    @abstractmethod
    async def get_all_permissions(self) -> List[PermissionRead]:
        pass

    @abstractmethod
    async def get_permission_by_id(self, permission_id: int) -> Optional[PermissionRead]:
        pass
