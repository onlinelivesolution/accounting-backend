from src.repositories.interfaces.ibankaccount_repository import IBankAccountRepository
from src.services.interfaces.ibankaccount_service import IBankAccountService
from src.services.interfaces.idetailitem_service import IDetailItemService
from src.schemas.detailitemautocreate_schema import DetailItemAutoCreateRequest
from src.schemas.bankaccount_schema import BankAccountCreate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from typing import List
from src.models.bankaccount_model import BankAccount


class BankAccountService(IBankAccountService):
    def __init__(
        self,
        db: AsyncSession,
        bank_repo: IBankAccountRepository,
        detailitem_service: IDetailItemService
    ):
        self.db = db
        self.bank_repo = bank_repo
        self.detailitem_service = detailitem_service
        
    async def create_bank_account(self, data: BankAccountCreate):

        # 1️⃣ Create DetailItem
        detail_item = await self.detailitem_service.auto_create_detail_item(
            DetailItemAutoCreateRequest(
                accountType="Current Asset",
                detailItemName=data.bankAccountName,
                openingBalance=data.openingBalance,
                openingDate=data.openingBalanceDate
            )
        )

        # 2️⃣ Save BankAccount
        bank = await self.bank_repo.create(
            data=data,
            detail_item_code=detail_item.detailItemCode
        )

        await self.db.commit()
        return bank