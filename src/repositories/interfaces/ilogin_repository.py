from abc import ABC, abstractmethod
from typing import Optional, List
from src.models.user_model import UserInfo
from src.schemas.permission_schema import PermissionActionInfo


class ILoginRepository(ABC):
    """Defines DB-level operations for authentication and permission fetching."""

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[UserInfo]:
        pass

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> Optional[UserInfo]:
        pass

    @abstractmethod
    async def get_user_permissions(self, role_id: int) -> List[PermissionActionInfo]:
        pass

    @abstractmethod
    async def update_password_hash(self, user_id: int, new_hash: str) -> None:
        pass
