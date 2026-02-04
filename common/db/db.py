
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.database import AsyncSessionLocal

# Dependency to get DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
