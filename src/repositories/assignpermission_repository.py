from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from src.models.role_permission_action_model import RolePermissionAction
from src.models.role_model import Role
from src.models.permission_model import Permission
from src.dto.rolepermissionassigndto import RolePermissionAssign
from common.generic.generic_repository import GenericRepository
from common.generic.igeneric_repository import IGenericRepository

class AssignPermissionRepository(GenericRepository[RolePermissionAction], IGenericRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(RolePermissionAction, db)
        
    async def get_assigned_permission_action_ids(self, role_id: int) -> List[int]:
        query = select(RolePermissionAction.permissionActionID).where(
            RolePermissionAction.roleID == role_id
        )
        result = await self.db.execute(query)
        return [row[0] for row in result.all()]

    async def save_role_permissions(self, role_id: int, permission_action_ids: List[int]) -> Dict[str, str]:
        # Delete existing
        await self.db.execute(
            delete(RolePermissionAction).where(RolePermissionAction.roleID == role_id)
        )

        # Insert new ones
        new_records = [
            RolePermissionAction(
                roleID=role_id,
                permissionActionID=pid,
                createdDate=datetime.utcnow(),
            )
            for pid in permission_action_ids
        ]

        self.db.add_all(new_records)
        await self.db.commit()

        return {"message": "Role permissions updated successfully"}

    async def assign_permissions(self, role_permissions: List[RolePermissionAssign]) -> List[RolePermissionAction]:
        # Delete existing role permissions for roles in the payload
        role_ids = list({rp.roleID for rp in role_permissions})
        await self.db.execute(delete(RolePermissionAction).where(RolePermissionAction.roleID.in_(role_ids)))

        # Insert new assignments
        new_assignments = [
            RolePermissionAction(roleID=rp.roleID, permissionID=rp.permissionIDs) for rp in role_permissions
        ]
        self.db.add_all(new_assignments)
        await self.db.commit()
        return new_assignments

    async def get_role_permissions_tree(self):
        # Returns roles with their permissions in a nested structure
        result = await self.db.execute(
            select(Role, Permission)
            .join(RolePermissionAction, Role.roleID == RolePermissionAction.roleID)
            .join(Permission, Permission.permissionID == RolePermissionAction.permissionActionID)
        )
        rows = result.all()
        tree = {}
        for role, perm in rows:
            if role.roleID not in tree:
                tree[role.roleID] = {"role": role, "permissions": []}
            tree[role.roleID]["permissions"].append(perm)
        return list(tree.values())
    
    async def add(self, entity: RolePermissionAction) -> RolePermissionAction:
        """Implements IGenericRepository.add"""
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
