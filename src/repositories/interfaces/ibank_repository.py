from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.bank_model import Bank
from src.dto.roledto import RoleCreate, RoleUpdate
from src.dto.roledropdown import RoleDropdown

class IRoleRepository(ABC):
    
    @abstractmethod
    async def create_bank(self, role_data: RoleCreate) -> Bank:
        pass
    
    @abstractmethod
    async def update_bank(self, role_id: int, role_data: RoleUpdate) -> Optional[Bank]:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Bank]:
        pass

    @abstractmethod
    async def get_by_id(self, role_id: int) -> Optional[Bank]:
        pass

    @abstractmethod
    async def get_by_name(self, role_name: str) -> Optional[Bank]:
        pass

    @abstractmethod
    async def delete_bank(self, role_id: int) -> bool:
        pass
    
    @abstractmethod
    async def get_bank_dropdown(self) -> List[RoleDropdown]:
        raise NotImplementedError
