from sqlalchemy.ext.asyncio import create_async_engine

from src.services.database import Base


async def create_tenant_schema(database_name: str):

    database_url = (
        f"mssql+aioodbc://sa:abcd123%21"
        f"@DESKTOP-GCAJSDB/{database_name}"
        f"?driver=ODBC+Driver+18+for+SQL+Server"
        f"&TrustServerCertificate=yes"
    )

    engine = create_async_engine(database_url, echo=True, future=True)

    try:

        async with engine.begin() as conn:

            print("====================================")
            print("CREATING TENANT SCHEMA")
            print("DATABASE:", database_name)
            print("====================================")

            # Optional - show tables being created
            print(Base.metadata.tables.keys())

            await conn.run_sync(Base.metadata.create_all)

            print("====================================")
            print("SCHEMA CREATED SUCCESSFULLY")
            print("====================================")

    finally:

        await engine.dispose()
