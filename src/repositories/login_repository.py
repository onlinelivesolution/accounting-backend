# src/repositories/login_repository.py

from datetime import datetime, timedelta

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user_model import UserInfo
from src.models.userotp import UserOTP

from src.models.role_permission_action_model import RolePermissionAction

from src.models.permission_action_model import PermissionAction

from src.models.permission_model import Permission

from src.schemas.permission_schema import PermissionActionInfo

from src.repositories.interfaces.ilogin_repository import ILoginRepository

from common.generic.generic_repository import GenericRepository

from common.utils.security import verify_password, hash_password


class LoginRepository(GenericRepository[UserInfo], ILoginRepository):

    def __init__(self, db: AsyncSession):

        super().__init__(UserInfo, db)

    # ====================================
    # USER METHODS
    # ====================================

    async def get_user_by_username(self, username: str):

        stmt = select(UserInfo).where(
            UserInfo.userName == username, UserInfo.isActive == 1
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def authenticate_user(self, username: str, password: str):

        stmt = select(UserInfo).where(
            UserInfo.userName == username, UserInfo.isActive == 1
        )

        result = await self.db.execute(stmt)

        user = result.scalars().first()

        # =========================
        # USER NOT FOUND
        # =========================

        if not user:

            print("❌ USER NOT FOUND")

            return None

        # =========================
        # DEBUGGING
        # =========================

        print("===================================")

        print("INPUT USERNAME:", username)

        print("INPUT PASSWORD:", password)

        print("DB HASH:", user.passwordHash)

        print("===================================")

        # =========================
        # VERIFY PASSWORD
        # =========================

        is_valid, needs_rehash = verify_password(password, user.passwordHash)

        print("VERIFY RESULT:", is_valid)

        print("NEEDS REHASH:", needs_rehash)

        # =========================
        # INVALID PASSWORD
        # =========================

        if not is_valid:

            print("❌ INVALID PASSWORD")

            return None

        # =========================
        # AUTO REHASH
        # =========================

        if needs_rehash:

            print("🔄 REHASHING PASSWORD")

            new_hash = hash_password(password)

            await self.update_password_hash(user.userID, new_hash)

        print("✅ LOGIN SUCCESS")

        return user

    async def get_user_by_id(self, user_id: int):

        stmt = select(UserInfo).where(UserInfo.userID == user_id)

        result = await self.db.execute(stmt)

        return result.scalars().first()

    async def get_user_permissions(self, role_id: int):

        query = (
            select(
                Permission.permissionID,
                Permission.permissionName,
                PermissionAction.actionName,
                RolePermissionAction.isAllowed,
            )
            .join(
                PermissionAction,
                PermissionAction.permissionActionID
                == RolePermissionAction.permissionActionID,
            )
            .join(Permission, Permission.permissionID == PermissionAction.permissionID)
            .where(RolePermissionAction.roleID == role_id)
        )

        result = await self.db.execute(query)

        rows = result.all()

        return [
            PermissionActionInfo(
                permissionID=r.permissionID,
                permissionName=r.permissionName,
                actionName=r.actionName,
                isAllowed=r.isAllowed,
            )
            for r in rows
        ]

    async def update_password_hash(self, user_id: int, new_hash: str):

        stmt = (
            update(UserInfo)
            .where(UserInfo.userID == user_id)
            .values(passwordHash=new_hash)
        )

        await self.db.execute(stmt)

        await self.db.commit()

    # ====================================
    # OTP METHODS
    # ====================================

    async def save_otp(self, otp: UserOTP):

        self.db.add(otp)

        await self.db.commit()

        await self.db.refresh(otp)

        return otp


    async def get_valid_otp(self, user_id: int, otp_code: str):

        otp_code = otp_code.strip()

        print("SEARCH USER ID:", user_id)
        print("SEARCH OTP:", otp_code)

        stmt = select(UserOTP).where(
            UserOTP.userID == user_id, UserOTP.otpCode == otp_code, UserOTP.isUsed == False
        )

        result = await self.db.execute(stmt)

        otp = result.scalars().first()

        print("FOUND OTP:", otp)

        return otp

    async def mark_otp_used(self, otp_id: int):

        stmt = update(UserOTP).where(UserOTP.otpID == otp_id).values(isUsed=True)

        await self.db.execute(stmt)

        await self.db.commit()

    # ====================================
    # LOGIN SECURITY METHODS
    # ====================================

    async def increment_failed_attempts(self, user_id: int):

        stmt = (
            update(UserInfo)
            .where(UserInfo.userID == user_id)
            .values(failedLoginAttempts=UserInfo.failedLoginAttempts + 1)
        )

        await self.db.execute(stmt)

        await self.db.commit()

    async def reset_failed_attempts(self, user_id: int):

        stmt = (
            update(UserInfo)
            .where(UserInfo.userID == user_id)
            .values(failedLoginAttempts=0, lockedUntil=None)
        )

        await self.db.execute(stmt)

        await self.db.commit()

    async def lock_user(self, user_id: int):

        locked_until = datetime.utcnow() + timedelta(minutes=15)

        stmt = (
            update(UserInfo)
            .where(UserInfo.userID == user_id)
            .values(lockedUntil=locked_until)
        )

        await self.db.execute(stmt)

        await self.db.commit()
