from src.repositories.interfaces.ibankdeposit_repository import IBankDepositRepository
from src.services.interfaces.ibankdeposit_service import IBankDepositService
from src.schemas.bankdeposit_schema import BankDepositCreate, BankDepositRead
from src.models.bankdeposit_model import BankDeposit
from datetime import datetime

class BankDepositService(IBankDepositService):
    def __init__(self, repository: IBankDepositRepository):
        self.repository = repository
        
    async def add_bank_deposit(self, data: BankDepositCreate) -> BankDepositRead:
        created_date = (
            data.createdDate.replace(tzinfo=None)
            if getattr(data, "createdDate", None)
            else datetime.utcnow()
        )

        new_bankdeposit = BankDeposit(
            bankAccountID=data.bankAccountID,
            accountNumber=data.accountNumber,
            depositType=data.depositType,            
            depositRefNo=data.depositRefNo,
            depositDate=data.depositDate,
            depositedBy=data.depositedBy,            
            amount=data.amount,
            shortNote=data.shortNote,
            status=data.status,            
            isDeleted=data.isDeleted,            
            createdBy=data.createdBy,
            createdDate=created_date,
        )
        saved_item = await self.repository.add_bank_deposit(new_bankdeposit)
        return BankDepositRead.model_validate(saved_item, from_attributes=True)