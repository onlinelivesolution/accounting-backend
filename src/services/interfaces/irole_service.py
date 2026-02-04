from abc import ABC, abstractmethod
from typing import List, Optional
from src.dto.roledto import RoleCreate, RoleUpdate, RoleRead
from src.dto.roledropdown import RoleDropdown

class IRoleService(ABC):
    
    @abstractmethod
    async def get_all_roles(self) -> List[RoleRead]:
        pass

    @abstractmethod
    async def get_role_by_id(self, role_id: int) -> Optional[RoleRead]:
        pass

    @abstractmethod
    async def create_role(self, role_data: RoleCreate) -> RoleRead:
        pass

    @abstractmethod
    async def update_role(self, role_id: int, role_data: RoleUpdate) -> Optional[RoleRead]:
        pass

    @abstractmethod
    async def delete_role(self, role_id: int) -> bool:
        pass
    
    @abstractmethod
    async def get_role_dropdown(self) -> List[RoleDropdown]:
        raise NotImplementedError
