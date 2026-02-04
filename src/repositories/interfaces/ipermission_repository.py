from abc import ABC, abstractmethod
from typing import Optional, List, Any, Dict
from src.models.permission_model import Permission
from src.dto.permissiondto import PermissionCreate, PermissionUpdate


class IPermissionRepository(ABC):
    
    @abstractmethod
    async def get_full_permission_tree(self) -> List[Any]:
        pass
        
    @abstractmethod
    async def create_permission(self, permission_data: PermissionCreate) -> Permission:
        pass
    
    @abstractmethod
    async def update_permission(self, permission_id: int, permission_data: PermissionUpdate) -> Optional[Permission]:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Permission]:
        pass

    @abstractmethod
    async def get_by_id(self, permission_id: int) -> Optional[Permission]:
        pass

    @abstractmethod
    async def get_by_name(self, permission_name: str) -> Optional[Permission]:
        pass
