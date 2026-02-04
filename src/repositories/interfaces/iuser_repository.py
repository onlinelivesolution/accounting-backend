from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.user_model import UserInfo
from src.dto.userdto import UserCreate, UserRoleUpdate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user_data: UserCreate) -> UserInfo:
        pass
    
    @abstractmethod
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserInfo]:
        pass
    
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[UserInfo]:
        pass

    @abstractmethod
    async def update_password(self, user_id: int, new_password_hash: str):
        pass
    
    @abstractmethod
    async def get_all_users(self, db: AsyncSession, skip: int, limit: int) -> List[UserInfo]:
        pass
    
    @abstractmethod
    async def update_user_roles(self, user_data: UserRoleUpdate) -> UserInfo:
        pass

    @abstractmethod
    async def get_by_name(self, user_name: str) -> Optional[UserInfo]:
        pass

