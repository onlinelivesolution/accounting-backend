from abc import ABC, abstractmethod
from src.models.bankwithdraw_model import BankWithdraw


class IBankWithdrawRepository(ABC):
    
    @abstractmethod
    async def add_bank_withdraw(self, bankwithdraw: BankWithdraw) -> BankWithdraw:
        pass 