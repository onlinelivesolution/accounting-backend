from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List, Any
from src.dto.rolepermissionassigndto import RolePermissionAssign
from src.depends.service_depends import get_assign_permission_service
from src.services.assignpermission_service import AssignPermissionService

router = APIRouter(prefix="/api/rolepermissions", tags=["RolePermissions"])

@router.get("/getAssignedPermissionIDs/{role_id}")
async def get_assigned_permission_ids(role_id: int, service: AssignPermissionService = Depends(get_assign_permission_service)):
    try:
        result = await service.get_assigned_permission_action_ids(role_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assignPermission")
async def assign_permissions(payload: Dict[str, Any], service: AssignPermissionService = Depends(get_assign_permission_service)):
    try:
        role_id = payload.get("roleID")
        permission_ids = payload.get("permissionIDs", [])

        if not role_id:
            raise HTTPException(status_code=400, detail="Role ID is required")
        if not isinstance(permission_ids, list):
            raise HTTPException(status_code=400, detail="permissionIDs must be a list")

        result = await service.save_role_permissions(role_id, permission_ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
