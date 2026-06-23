from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import URL

from src.services.database import Base


async def create_tenant_schema(database_name: str):

    database_url = URL.create(
        "mssql+aioodbc",
        username="sa",
        password="abcd123!",
        host="DESKTOP-GCAJSDB",
        database=database_name,
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "TrustServerCertificate": "yes",
        },
    )

    engine = create_async_engine(database_url, echo=True, future=True)

    try:

        async with engine.begin() as conn:

            print("====================================")
            print("CREATING TENANT SCHEMA")
            print("DATABASE:", database_name)
            print("====================================")

            print(list(Base.metadata.tables.keys()))

            await conn.run_sync(Base.metadata.create_all)

            print("====================================")
            print("SCHEMA CREATED SUCCESSFULLY")
            print("====================================")

    finally:

        await engine.dispose()
