from fastapi import APIRouter, Depends, HTTPException, status
from src.dto.userdto import UserCreate, UserRoleUpdate, UserRead, UserUpdate, UserResponse, ChangePasswordRequest
from src.services.user_service import UserService
from src.services.interfaces.iuser_service import IUserService
from src.depends.service_depends import get_user_service
from typing import List
from passlib.hash import argon2  # <-- use Argon2 instead of bcrypt

router = APIRouter(prefix="/api/users", tags=["Users"])

# Utility function to hash passwords safely
def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password cannot be empty")
    return argon2.hash(password)  # safe for any length

# ------------------ Create User ------------------
@router.post("/createUser")
async def create_user(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    """
    Create a new user with hashed password.
    """
    # Check if password is provided
    if not user_data.passwordHash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required"
        )

    # Hash the password before saving
    user_data.passwordHash = hash_password(user_data.passwordHash)

    # Create the user via the service layer
    user = await service.create_user(user_data)
    
    return {
        "message": "User created successfully",
        "userID": user.userID,
        "userName": user.userName
    }

# ------------------ Update User ------------------
@router.put("/updateUser/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: IUserService = Depends(get_user_service)
):
    updated_user = await user_service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# ------------------ Change Password ------------------
@router.put("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    service: UserService = Depends(get_user_service)
):
    result = await service.change_password(request)  # pass the full object

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return {"message": result["message"]}

# ------------------ Assign Roles ------------------
@router.put("/assign-roles")
async def assign_roles(user_data: UserRoleUpdate, service: UserService = Depends(get_user_service)):
    user = await service.update_user_roles(user_data)
    return {"message": "User roles updated successfully", "user": user.userName}

# ------------------ Get All Users ------------------
@router.get("/getUserTable", response_model=List[UserRead])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    service: IUserService = Depends(get_user_service)
):
    return await service.get_all_users(skip=skip, limit=limit)

# ------------------ Get User By ID ------------------
@router.get("/getUserByID{user_id}")
async def get_user_by_id(user_id: int, service: UserService = Depends(get_user_service)):
    return await service.get_user_by_id(user_id)
