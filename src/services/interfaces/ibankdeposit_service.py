from abc import ABC, abstractmethod
from src.schemas.bankdeposit_schema import BankDepositCreate, BankDepositRead

class IBankDepositService(ABC):
    
    @abstractmethod
    async def add_bank_deposit(self, data: BankDepositCreate) -> BankDepositRead:
        pass