from src.models.bank_model import Bank
from src.schemas.bank_schema import BankCreate, BankUpdate
from src.dto.bankdropdown import BankDropdown
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from common.generic.generic_repository import GenericRepository
from common.generic.igeneric_repository import IGenericRepository

class BankRepository(GenericRepository[Bank], IGenericRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Bank, db)
        
    async def create_bank(self, bank_data: BankCreate) -> Bank:
        created_date = (
            bank_data.createdDate.replace(tzinfo=None)
            if getattr(bank_data, "createdDate", None)
            else datetime.utcnow()
        )

        new_bank = Bank(
            bankCode=bank_data.bankCode,
            bankName=bank_data.bankName,
            address=bank_data.address,
            isDeleted=bank_data.isDeleted,            
            createdBy=bank_data.createdBy,
            createdDate=created_date,
            companyCode=bank_data.companyCode,
        )
        return await self.add(new_bank)
    
    async def update_bank(self, bank_id: int, bank_data: BankUpdate) -> Optional[Bank]:
        result = await self.db.execute(select(Bank).where(Bank.bankID == bank_id))
        existing_bank = result.scalar_one_or_none()

        if not existing_bank:
            return None

        for key, value in bank_data.model_dump(exclude_unset=True).items():
            setattr(existing_bank, key, value)

        existing_bank.updatedDate = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(existing_bank)
        return existing_bank
        
    async def get_all(self) -> List[Bank]:
        result = await self.db.execute(select(Bank))
        return result.scalars().all()

    async def get_by_id(self, bank_id: int) -> Optional[Bank]:
        result = await self.db.execute(select(Bank).where(Bank.bankID == bank_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, bank_name: str) -> Optional[Bank]:
        result = await self.db.execute(select(Bank).where(Bank.bankName == bank_name))
        return result.scalar_one_or_none()

    async def add(self, entity: Bank) -> Bank:
        """Implements IGenericRepository.add"""
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
    
    async def get_bank_dropdown(self) -> List[BankDropdown]:
        result = await self.db.execute(select(Bank))
        banks = result.scalars().all()
        return [BankDropdown.model_validate(b) for b in banks]




