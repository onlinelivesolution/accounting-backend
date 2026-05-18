from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import sessionmaker

from sqlalchemy import text

SERVER = "DESKTOP-GCAJSDB"

USERNAME = "sa"

PASSWORD = "abcd123!"


def generate_database_name(email: str):

    safe_email = email.replace("@", "_").replace(".", "_").replace("-", "_")

    return f"ERP_{safe_email}"


# MASTER DB CONNECTION
MASTER_DB_URL = (
    f"mssql+aioodbc://{USERNAME}:{PASSWORD}"
    f"@{SERVER}/master"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
)


async def create_tenant_database(email: str):

    database_name = generate_database_name(email)

    # IMPORTANT:
    # AUTOCOMMIT is required for CREATE DATABASE
    engine = create_async_engine(
        MASTER_DB_URL, echo=True, future=True, isolation_level="AUTOCOMMIT"
    )

    async with engine.connect() as conn:

        # Check if database already exists
        result = await conn.execute(
            text("""
                SELECT name
                FROM sys.databases
                WHERE name = :db_name
            """),
            {"db_name": database_name},
        )

        existing_db = result.fetchone()

        if existing_db:
            raise Exception("Database already exists")

        # Create database
        await conn.execute(text(f"CREATE DATABASE [{database_name}]"))

    await engine.dispose()

    return database_name


def get_tenant_database_url(database_name: str):

    return (
        f"mssql+aioodbc://{USERNAME}:{PASSWORD}"
        f"@{SERVER}/{database_name}"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&TrustServerCertificate=yes"
    )


def get_tenant_engine(database_name: str):

    tenant_url = get_tenant_database_url(database_name)

    return create_async_engine(tenant_url, echo=True, future=True)


def get_tenant_session(database_name: str):

    engine = get_tenant_engine(database_name)

    SessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )

    return SessionLocal()
