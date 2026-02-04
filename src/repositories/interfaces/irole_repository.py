from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.role_model import Role
from src.dto.roledto import RoleCreate, RoleUpdate
from src.dto.roledropdown import RoleDropdown

class IRoleRepository(ABC):
    
    @abstractmethod
    async def create_role(self, role_data: RoleCreate) -> Role:
        pass
    
    @abstractmethod
    async def update_role(self, role_id: int, role_data: RoleUpdate) -> Optional[Role]:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Role]:
        pass

    @abstractmethod
    async def get_by_id(self, role_id: int) -> Optional[Role]:
        pass

    @abstractmethod
    async def get_by_name(self, role_name: str) -> Optional[Role]:
        pass

    @abstractmethod
    async def delete_role(self, role_id: int) -> bool:
        pass
    
    @abstractmethod
    async def get_role_dropdown(self) -> List[RoleDropdown]:
        raise NotImplementedError
