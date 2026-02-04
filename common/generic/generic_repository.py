from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.future import select

ModelType = TypeVar("ModelType")


class GenericRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession, primary_key_field: str = "id"):
        self.model = model
        self.db = db
        self.primary_key_field = primary_key_field
        
        if hasattr(model, "__mapper__"):
            pk_cols = list(model.__mapper__.primary_key)
            self.primary_key_field = pk_cols[0] if pk_cols else None
        else:
            self.primary_key_field = None

    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        stmt = select(self.model)
        if self.primary_key_field is not None:
            stmt = stmt.order_by(self.primary_key_field)

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, id_val: str) -> Optional[ModelType]:
        pk_attr = getattr(self.model, self.primary_key_field)
        stmt = select(self.model).where(pk_attr == id_val)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, obj_in: ModelType) -> ModelType:
        self.db.add(obj_in)
        await self.db.commit()
        await self.db.refresh(obj_in)
        return obj_in

    async def update(self, id_value: any, obj_in: dict) -> Optional[ModelType]:
        db_obj = await self.get_by_id(id_value)
        if not db_obj:
            return None

        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id_value: any) -> bool:
        db_obj = await self.get_by_id(id_value)
        if not db_obj:
            return False

        await self.db.delete(db_obj)
        await self.db.commit()
        return True
    
    async def get_next_code(self, code_length: int = 2) -> str:
        """Generate next sequential code for char-based PKs like '01', '02'."""
        pk_attr = getattr(self.model, self.primary_key_field, None)
        if pk_attr is None:
            raise ValueError("Primary key field not found on model")

        stmt = select(func.max(pk_attr))
        result = await self.db.execute(stmt)
        max_code = result.scalar()

        if max_code is None:
            return str(1).zfill(code_length)

        try:
            next_code = str(int(max_code) + 1).zfill(code_length)
        except ValueError:
            raise ValueError(f"Cannot generate numeric sequence from code {max_code}")

        return next_code
