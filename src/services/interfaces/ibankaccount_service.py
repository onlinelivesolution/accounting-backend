from abc import ABC, abstractmethod
from src.schemas.bankaccount_schema import (
    BankAccountCreate,
    BankAccountRead
)


class IBankAccountService(ABC):

    @abstractmethod
    async def create_bank_account(
        self,
        data: BankAccountCreate
    ) -> BankAccountRead:
        """
        Create bank account with:
        - DetailItem creation
        - Optional opening balance
        """
        pass
