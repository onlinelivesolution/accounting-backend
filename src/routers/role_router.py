from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.models.role_model import Role
from src.dto.roledto import RoleCreate, RoleUpdate, RoleRead
from src.dto.roledropdown import RoleDropdown
from src.services.interfaces.irole_service import IRoleService
from src.depends.service_depends import get_role_service

router = APIRouter(prefix="/api/roles", tags=["Roles"])

@router.get("/getAllRoles", response_model=List[RoleRead])
async def get_roles(service: IRoleService = Depends(get_role_service)):
    return await service.get_all_roles()

@router.get("/getRoleByID{role_id}", response_model=RoleRead)
async def get_role_by_id(role_id: int, service: IRoleService = Depends(get_role_service)):
    role = await service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role

@router.post("/insertRole", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
async def create_role(role_data: RoleCreate, service: IRoleService = Depends(get_role_service)):
    return await service.create_role(role_data)

@router.put("/updateRole{role_id}", response_model=RoleRead)
async def update_role(role_id: int, role_data: RoleUpdate, service: IRoleService = Depends(get_role_service)):
    updated_role = await service.update_role(role_id, role_data)
    if not updated_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return updated_role

@router.get("/loadRoleDropdown", response_model=List[RoleDropdown])
async def get_role_dropdown(service: IRoleService = Depends(get_role_service)):
    return await service.get_role_dropdown()

