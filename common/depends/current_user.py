from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from common.utils.jwt_handler import SECRET_KEY, ALGORITHM
from common.depends.auth_depends import oauth2_scheme
from src.services.database import get_async_db
from src.models.user_model import UserInfo
from src.schemas.currentuser_schema import CurrentUser


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
) -> CurrentUser:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    stmt = select(UserInfo).where(
        UserInfo.UserID == user_id,
        UserInfo.IsActive == True
    )

    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise credentials_exception

    return CurrentUser(
        userID=user.UserID,
        userName=user.UserName,
        fullName=user.FullName,
        companyCode=user.CompanyCode,
        roleID=user.RoleID,
        isSuperAdmin=user.IsSuperAdmin
    )
