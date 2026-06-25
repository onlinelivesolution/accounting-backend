from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import URL
from src.services.database import Base

# Import models here
from src.models.company import Company
from src.models.role_model import Role
from src.models.permission_model import Permission
from src.models.permission_action_model import PermissionAction
from src.models.role_permission_action_model import RolePermissionAction
from src.models.controlitem import ControlItem
from src.models.reportingitem import ReportingItem
from src.models.detailitem import DetailItem
from src.models.customers import Customer
from src.models.lineitem import LineItem
from src.models.user_model import UserInfo


async def create_tenant_schema(database_name: str):

    url = URL.create(
        drivername="mssql+aioodbc",
        username="sa",
        password="abcd123!",
        host="DESKTOP-GCAJSDB",
        port=1433,  # add this
        database=database_name,
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "TrustServerCertificate": "yes",
        },
    )

    engine = create_async_engine(url, echo=True)

    try:

        print("Database:", database_name)
        print("Tables:", list(Base.metadata.tables.keys()))

        async with engine.begin() as conn:

            await conn.run_sync(Base.metadata.create_all)

            print("Schema created")

    finally:

        await engine.dispose()
