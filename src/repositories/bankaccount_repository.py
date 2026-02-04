from src.repositories.interfaces.ibankaccount_repository import IBankAccountRepository
from src.models.bankaccount_model import BankAccount
from src.schemas.bankaccount_schema import BankAccountCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


class BankAccountRepository(IBankAccountRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
        

    async def create(self, data: BankAccountCreate, detail_item_code: str):
        bank = BankAccount(
            bankAccountName=data.bankAccountName,
            category=data.category,
            defaultPaymentMethod=data.defaultPaymentMethod,
            bankName=data.bankName,
            accountNumber=data.accountNumber,
            branchName=data.branchName,
            branchCode=data.branchCode,
            description=data.description,
            isActive=data.isActive,
            isDefault=data.isDefault,
            openingBalanceDate=data.openingBalanceDate,
            detailItemCode=detail_item_code
        )

        self.db.add(bank)
        await self.db.flush()
        return bank

    
    

