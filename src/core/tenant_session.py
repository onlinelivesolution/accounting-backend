from src.core.tenant_database import get_tenant_session
from src.core.tenant_resolver import get_database_by_email


async def get_tenant_db_by_email(email: str):

    database_name = await get_database_by_email(email)

    if not database_name:
        return None, None

    tenant_db = get_tenant_session(database_name)

    return tenant_db, database_name

async def get_tenant_db_by_database(database_name: str):

    tenant_db = get_tenant_session(database_name)

    return tenant_db, database_name
