from abc import ABC, abstractmethod
from decimal import Decimal
from src.schemas.banktransaction_schema import BankTransactionRequest


class IBankTransactionRepository(ABC):

    @abstractmethod
    async def create_transaction(self, data: BankTransactionRequest):
        pass
    
    @abstractmethod
    async def get_account_balance(self, detail_item_code: str) -> Decimal:
        """
        Returns current balance for a bank/cash detail item
        """
        pass
