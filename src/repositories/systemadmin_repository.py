
from src.repositories.interfaces.isystemadmin_repository import ISystemAdminRepository
from sqlalchemy import select
from src.models.systemuser_model import SystemUser

class SystemAdminRepository(ISystemAdminRepository):

    def __init__(self, db):
        self.db = db


    async def get_by_username(self, username:str):

        stmt=(select(SystemUser)
               .where(SystemUser.username==username))

        result=await self.db.execute(stmt)

        return result.scalar_one_or_none()


    async def update(self,user):

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user