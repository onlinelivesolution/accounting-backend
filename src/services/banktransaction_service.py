from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.interfaces.ibanktransaction_service import IBankTransactionService
from src.repositories.interfaces.ibanktransaction_repository import IBankTransactionRepository
from src.schemas.banktransaction_schema import BankTransactionRequest


class BankTransactionService(IBankTransactionService):

    def __init__(self, repository: IBankTransactionRepository, db: AsyncSession):
        self.repository = repository
        self.db = db
        
    async def get_account_balance(self, detail_item_code: str):
        balance = await self.repository.get_account_balance(detail_item_code)
        return {"balance": balance}

    async def create_transaction(self, data):
        header = await self.repository.create_transaction(data)

        await self.db.commit()          # ✅ REQUIRED
        await self.db.refresh(header)   # optional

        return header

