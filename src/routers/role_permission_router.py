from fastapi import APIRouter, Depends, HTTPException, status
from src.services.interfaces.irole_permission_service import IRolePermissionService
from src.depends.service_depends import get_role_permission_service
from src.dto.rolepermissiondto import RolePermissionCreate, RolePermissionUpdate, RolePermissionRead
from typing import List

router = APIRouter(prefix="/api/role-permissions", tags=["Role Permissions"])

@router.post("/insertRolePermission", response_model=RolePermissionRead, status_code=status.HTTP_201_CREATED)
async def create_role_permission(role_permission_data: RolePermissionCreate, service: IRolePermissionService = Depends(get_role_permission_service)):
    return await service.create_role_permission(role_permission_data)

@router.put("/updateRolePermission{role_permission_id}", response_model=RolePermissionRead)
async def update_role_permission(role_permission_id: int, role_permission_data: RolePermissionUpdate, service: IRolePermissionService = Depends(get_role_permission_service)):
    updated_role_permission = await service.update_role_permission(role_permission_id, role_permission_data)
    if not updated_role_permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role Permission not found")
    return updated_role_permission

@router.get("/getAllRolePermissions", response_model=List[RolePermissionRead])
async def get_role_permissions(service: IRolePermissionService = Depends(get_role_permission_service)):
    return await service.get_role_permissions()

@router.get("/getRolePermissionByID{role_permission_id}", response_model=RolePermissionRead)
async def get_role_permission_by_id(role_permission_id: int, service: IRolePermissionService = Depends(get_role_permission_service)):
    role_permission = await service.get_role_permission_by_id(role_permission_id)
    if not role_permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role Permission not found")
    return role_permission


