from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mssql+aioodbc://sa:abcd123%21@DESKTOP-GCAJSDB/AccountBD?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
