from fastapi import HTTPException, status
from src.repositories.interfaces.iuser_repository import IUserRepository
from src.services.interfaces.iuser_service import IUserService
from src.dto.userdto import UserCreate, UserRoleUpdate, UserUpdate, UserRead, UserResponse, ChangePasswordRequest
from typing import List, Optional
from common.utils.password_utils import verify_password

class UserService(IUserService):    
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def create_user(self, user_data: UserCreate):
        return await self.repository.create_user(user_data)
    
    async def update_user(self, user_id: int, user_data: UserUpdate):
        updated_user = await self.repository.update_user(user_id, user_data)
        if not updated_user:
            return None
        return UserResponse.model_validate(updated_user)
    
    async def change_password(self, request: ChangePasswordRequest):
        user = await self.repository.get_user_by_id(request.userID)
        if not user:
            return {"success": False, "message": "User not found."}

        if not verify_password(request.oldPassword, user.passwordHash):
            return {"success": False, "message": "Old password is incorrect."}

        # new_hashed = hash_password(request.newPassword)
        # await self.repository.update_password(user.userID, new_hashed)
        # return {"success": True, "message": "Password updated successfully."}
    

    async def update_user_roles(self, user_data: UserRoleUpdate):
        return await self.repository.update_user_roles(user_data)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserRead]:
        users = await self.repository.get_all_users(skip=skip, limit=limit)
        return [UserRead.model_validate(ui) for ui in users["data"]]

    async def get_user_by_id(self, user_id: int):
        return await self.repository.get_user_by_id(user_id)