from abc import ABC, abstractmethod
from typing import List, Dict
from src.models.role_permission_action_model import RolePermissionAction
from src.dto.rolepermissionassigndto import RolePermissionAssign

class IAssignPermissionRepository(ABC):
    @abstractmethod
    async def get_assigned_permission_action_ids(self, role_id: int) -> List[int]:
        pass

    @abstractmethod
    async def save_role_permissions(self, role_id: int, permission_action_ids: List[int]) -> Dict[str, str]:
        pass
