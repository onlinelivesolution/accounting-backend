from common.generic.generic_repository import GenericRepository
from src.repositories.interfaces.ibankwithdraw_repository import IBankWithdrawRepository
from src.models.bankwithdraw_model import BankWithdraw
from sqlalchemy.ext.asyncio import AsyncSession

class BankWithdrawRepository(GenericRepository[BankWithdraw], IBankWithdrawRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(BankWithdraw, db)
    
    async def add_bank_withdraw(self, bankwithdraw: BankWithdraw) -> BankWithdraw:
        self.db.add(bankwithdraw)
        await self.db.commit()
        await self.db.refresh(bankwithdraw)
        return bankwithdraw