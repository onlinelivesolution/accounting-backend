from src.repositories.interfaces.ibankwithdraw_repository import IBankWithdrawRepository
from src.services.interfaces.ibankwithdraw_service import IBankWithdrawService
from src.schemas.bankwithdraw_schema import BankWithdrawCreate, BankWithdrawRead
from src.models.bankwithdraw_model import BankWithdraw
from datetime import datetime

class BankWithdrawService(IBankWithdrawService):
    def __init__(self, repository: IBankWithdrawRepository):
        self.repository = repository
        
    async def add_bank_withdraw(self, data: BankWithdrawCreate) -> BankWithdrawRead:
        created_date = (
            data.createdDate.replace(tzinfo=None)
            if getattr(data, "createdDate", None)
            else datetime.utcnow()
        )

        new_bankwithdraw = BankWithdraw(
            bankAccountID=data.bankAccountID,
            accountNumber=data.accountNumber,
            withdrawType=data.withdrawType,            
            withdrawRefNo=data.withdrawRefNo,
            withdrawDate=data.withdrawDate,
            withdrawnBy=data.withdrawndBy,            
            amount=data.amount,
            shortNote=data.shortNote,
            status=data.status,            
            isDeleted=data.isDeleted,            
            createdBy=data.createdBy,
            createdDate=created_date,
        )
        saved_item = await self.repository.add_bank_withdraw(new_bankwithdraw)
        return BankWithdrawRead.model_validate(saved_item, from_attributes=True)