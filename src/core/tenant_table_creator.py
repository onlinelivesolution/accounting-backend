from src.services.database import Base

from src.core.tenant_database import (
    get_tenant_engine
)

# IMPORTANT:
# Import ALL models here

from src.models.tenant import Tenant

# Example:
from src.models.user_model import UserInfo
from src.models.permission_model import Permission
from src.models.permission_action_model import PermissionAction
from src.models.role_permission_action_model import RolePermissionAction


# from src.models.payroll import Payroll


async def create_tenant_tables(
    database_name: str
):

    engine = get_tenant_engine(
        database_name
    )

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )

    await engine.dispose()