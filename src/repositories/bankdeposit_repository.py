from common.generic.generic_repository import GenericRepository
from src.repositories.interfaces.ibankdeposit_repository import IBankDepositRepository
from src.models.bankdeposit_model import BankDeposit
from sqlalchemy.ext.asyncio import AsyncSession

class BankDepositRepository(GenericRepository[BankDeposit], IBankDepositRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(BankDeposit, db)
    
    async def add_bank_deposit(self, bankdeposit: BankDeposit) -> BankDeposit:
        self.db.add(bankdeposit)
        await self.db.commit()
        await self.db.refresh(bankdeposit)
        return bankdeposit