from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Default database (but this can be dynamic later)
DATABASE_URL = "mssql+aioodbc://sa:abcd123%21@DESKTOP-GCAJSDB/AccountBD?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
# DATABASE_URL = "mssql+aioodbc://sa:abcd123%21@DESKTOP-BMKMV1T\SQLEXPRESS/onelinedb?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
# Async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# # For Base class of all models
Base = declarative_base()

async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
