from abc import ABC, abstractmethod
from typing import List, Dict
from src.dto.rolepermissionassigndto import RolePermissionAssign
from src.services.interfaces.iassignpermission_service import IAssignPermissionService
from src.repositories.interfaces.iassignpermission_repository import IAssignPermissionRepository

class AssignPermissionService(IAssignPermissionService):
    def __init__(self, repository: IAssignPermissionRepository):
        self.repository = repository
        
    async def get_assigned_permission_action_ids(self, role_id: int) -> List[int]:
        return await self.repository.get_assigned_permission_action_ids(role_id)

    async def save_role_permissions(self, role_id: int, permission_action_ids: List[int]) -> Dict[str, str]:
        return await self.repository.save_role_permissions(role_id, permission_action_ids)
