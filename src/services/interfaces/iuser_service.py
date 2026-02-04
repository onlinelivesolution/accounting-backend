from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.user_model import UserInfo
from src.dto.userdto import UserCreate, UserRoleUpdate, UserRead, UserUpdate, ChangePasswordRequest

class IUserService(ABC):
    
    @abstractmethod
    async def create_user(self, user_data: UserCreate) -> UserInfo:
        pass
    
    @abstractmethod
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserRead]:
        pass
    
    @abstractmethod
    async def change_password(self, request: ChangePasswordRequest):
        pass

    @abstractmethod
    async def update_user_roles(self, user_data: UserRoleUpdate) -> UserInfo:
        pass

    @abstractmethod
    async def get_all_users(self, skip: int, limit: int):
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[UserInfo]:
        pass

