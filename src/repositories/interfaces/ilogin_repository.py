# src/repositories/interfaces/ilogin_repository.py

from abc import ABC, abstractmethod
from src.models.user_model import UserInfo
from src.models.userotp import UserOTP


class ILoginRepository(ABC):

    @abstractmethod
    async def get_user_by_username(
        self,
        username: str
    ) -> UserInfo | None:
        pass

    @abstractmethod
    async def authenticate_user(
        self,
        username: str,
        password: str
    ) -> UserInfo | None:
        pass

    @abstractmethod
    async def get_user_by_id(
        self,
        user_id: int
    ) -> UserInfo | None:
        pass

    @abstractmethod
    async def get_user_permissions(
        self,
        role_id: int
    ):
        pass

    @abstractmethod
    async def update_password_hash(
        self,
        user_id: int,
        new_hash: str
    ):
        pass

    # =========================
    # OTP METHODS
    # =========================

    @abstractmethod
    async def save_otp(
        self,
        otp: UserOTP
    ):
        pass

    @abstractmethod
    async def get_valid_otp(
        self,
        user_id: int,
        otp_code: str
    ) -> UserOTP | None:
        pass

    @abstractmethod
    async def mark_otp_used(
        self,
        otp_id: int
    ):
        pass

    # =========================
    # LOGIN SECURITY METHODS
    # =========================

    @abstractmethod
    async def increment_failed_attempts(
        self,
        user_id: int
    ):
        pass

    @abstractmethod
    async def reset_failed_attempts(
        self,
        user_id: int
    ):
        pass

    @abstractmethod
    async def lock_user(
        self,
        user_id: int
    ):
        pass