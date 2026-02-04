from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.dto.permissiondto import PermissionCreate, PermissionRead, PermissionUpdate
from src.schemas.permission_action_schema import PermissionTreeParent
from src.services.interfaces.ipermission_service import IPermissionService
from src.depends.service_depends import get_permission_service

router = APIRouter(prefix="/api/permissions", tags=["Permissions"])

@router.get("/getPermissionTree", response_model=List[PermissionTreeParent])
async def get_full_permission_tree(service: IPermissionService = Depends(get_permission_service)):
    return await service.get_full_permission_tree()

@router.post("/insertPermission", response_model=PermissionRead, status_code=status.HTTP_201_CREATED)
async def create_permission(permission_data: PermissionCreate, service: IPermissionService = Depends(get_permission_service)):
    return await service.create_permission(permission_data)

@router.put("/updatePermission{permission_id}", response_model=PermissionRead)
async def update_permission(permission_id: int, permission_data: PermissionUpdate, service: IPermissionService = Depends(get_permission_service)):
    updated_permission = await service.update_permission(permission_id, permission_data)
    if not updated_permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="(Permission not found")
    return updated_permission

@router.get("/getAllPermissions", response_model=List[PermissionRead])
async def get_permission(service: IPermissionService = Depends(get_permission_service)):
    return await service.get_all_permissions()

@router.get("/getPermissionByID{permission_id}", response_model=PermissionRead)
async def get_permission_by_id(permission_id: int, service: IPermissionService = Depends(get_permission_service)):
    permission = await service.get_permission_by_id(permission_id)
    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return permission