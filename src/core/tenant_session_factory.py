from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.session_factory import Base

# Cache engines per tenant (VERY IMPORTANT)
_engines = {}
_sessions = {}


def get_engine(database_name: str):
    DATABASE_URL = (
        f"mssql+aioodbc://sa:abcd123%21@DESKTOP-GCAJSDB/"
        f"{database_name}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )

    if database_name not in _engines:
        _engines[database_name] = create_async_engine(
            DATABASE_URL, echo=True, future=True
        )

    return _engines[database_name]


def get_tenant_session(database_name: str):
    if database_name not in _sessions:
        engine = get_engine(database_name)

        _sessions[database_name] = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    return _sessions[database_name]()
