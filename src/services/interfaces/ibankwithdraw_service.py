from abc import ABC, abstractmethod
from src.schemas.bankwithdraw_schema import BankWithdrawCreate, BankWithdrawRead

class IBankWithdrawService(ABC):
    
    @abstractmethod
    async def add_bank_withdraw(self, data: BankWithdrawCreate) -> BankWithdrawRead:
        pass