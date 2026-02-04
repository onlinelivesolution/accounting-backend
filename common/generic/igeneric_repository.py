from typing import Generic, List, Optional, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod

# Generic type variables
T = TypeVar("T")   # Model type

class IGenericRepository(ABC, Generic[T]):
    """
    Interface for a generic repository that can be reused for any SQLAlchemy model.
    """

    @abstractmethod
    async def get_all(self) -> List[T]:
        """Fetch all entities"""
        pass

    @abstractmethod
    async def get_by_id(self, db: AsyncSession ) -> Optional[T]:
        """Fetch a single entity by primary key"""
        pass

    @abstractmethod
    async def add(self, db: AsyncSession, entity: T) -> T:
        """Insert a new entity"""
        pass

    @abstractmethod
    async def update(self, db: AsyncSession, entity: T) -> T:
        """Update an existing entity"""
        pass

