from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import select, func, cast, Integer, update
from src.models.user_model import UserInfo
from src.models.company import Company
from src.models.role_model import Role
from src.dto.userdto import UserCreate, UserRoleUpdate, UserUpdate
from common.generic.generic_repository import GenericRepository
from common.generic.igeneric_repository import IGenericRepository
from common.utils.security import hash_password  # import the function, not the context


class UserRepository(GenericRepository[UserInfo], IGenericRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(UserInfo, db)

    async def create_user(self, user_data: UserCreate) -> UserInfo:
        new_user = UserInfo(
            userName=user_data.userName,
            email=user_data.email,
            fullName=user_data.fullName,
            passwordHash=hash_password(user_data.passwordHash),  # use function
            roleID=user_data.roleID,
            isActive=user_data.isActive,
            isSuperAdmin=user_data.isSuperAdmin,
            companyCode=user_data.companyCode,
            createdBy=user_data.createdBy,
            createdDate=user_data.createdDate
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    
    async def update_user(self, user_id: int, data: UserUpdate) -> Optional[UserInfo]:
        query = select(UserInfo).where(UserInfo.userID == user_id)
        result = await self.db.execute(query)
        user = result.scalars().first()

        if not user:
            return None

        update_data = data.model_dump()
        
        for key, value in update_data.items():
            setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_user_by_id(self, user_id: int):
        query = select(UserInfo).where(UserInfo.userID == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def update_password(self, user_id: int, new_hashed_password: str):
        query = select(UserInfo).where(UserInfo.userID == user_id)
        result = await self.db.execute(query)
        user = result.scalars().first()

        if not user:
            return None

        user.passwordHash = new_hashed_password
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    # async def update_password(self, user_id: int, new_password_hash: str):
    #     query = (
    #         update(UserInfo)
    #         .where(UserInfo.userID == user_id)
    #         .values(passwordHash=new_password_hash)
    #     )
    #     await self.db.execute(query)
    #     await self.db.commit()

    async def update_user_roles(self, user_data: UserRoleUpdate) -> Optional[UserInfo]:
        stmt = (
            update(UserInfo)
            .where(UserInfo.userID == user_data.userID)
            .values(
                roleIDs=user_data.roleIDs,
                updatedBy=user_data.updatedBy,
                updatedDate=user_data.updatedDate
            )
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(stmt)
        await self.db.commit()

        result = await self.db.execute(select(UserInfo).where(UserInfo.userID == user_data.userID))
        return result.scalar_one_or_none()



    async def get_all_users(self, skip: int, limit: int) -> dict: 
        db: AsyncSession = self.db
        total_query = await db.execute(select(func.count(UserInfo.userID)))
        total = total_query.scalar_one()

        query = (
            select(
                UserInfo,
                Company.companyName.label("companyName"),
                Role.roleName.label("roleName"),
            )
            .outerjoin(Company, UserInfo.companyCode == Company.companyCode)
            .outerjoin(Role, UserInfo.roleID == Role.roleID)
            .order_by(UserInfo.userID)
            .offset(skip)
            .limit(limit)
        )
        compiled = query.compile(compile_kwargs={"literal_binds": True})
        print("🔍 Executing SQL:\n", compiled, "\n")
        results = await db.execute(query)
        rows = results.mappings().all()

        if rows: 
            print(rows[0].keys())

        userInfos = []
        for row in rows:
            ui = row["UserInfo"]
            userInfos.append({
                "userID": ui.userID,
                "userName": ui.userName,
                "fullName": ui.fullName,
                "email": ui.email,
                "isActive": ui.isActive,
                "roleID": ui.roleID,
                "roleName": row["roleName"],
                "companyCode": ui.companyCode,
                "companyName": row["companyName"], 
                "createdBy": ui.createdBy,
                "createdDate": ui.createdDate,
                "updatedBy": ui.updatedBy,
                "updatedDate": ui.updatedDate,
            })

        return {
            "data": userInfos,
            "skip": skip,
            "limit": limit,
            "total": total
        }

    async def get_by_name(self, user_name: str) -> Optional[UserInfo]:
        result = await self.db.execute(select(UserInfo).where(UserInfo.userName == user_name))
        return result.scalar_one_or_none()

    async def add(self, entity: UserInfo) -> UserInfo:
        """Implements IGenericRepository.add"""
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
