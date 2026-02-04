from abc import ABC, abstractmethod
from src.schemas.banktransaction_schema import BankTransactionRequest


class IBankTransactionService(ABC):

    @abstractmethod
    async def create_transaction(self, data: BankTransactionRequest):
        pass
    
    @abstractmethod
    async def get_account_balance(self, detail_item_code: str) -> dict:
        """
        Returns bank balance in response-friendly format
        """
        pass
