from abc import ABC, abstractmethod
from typing import Optional
from src.models.bankaccount_model import BankAccount
from src.schemas.bankaccount_schema import BankAccountCreate


class IBankAccountRepository(ABC):

    @abstractmethod
    async def create(
        self,
        data: BankAccountCreate,
        detail_item_code: str
    ) -> BankAccount:
        """
        Create a bank account and link it with a detail item code
        """
        pass

    # @abstractmethod
    # async def get_by_account_number(
    #     self,
    #     account_number: str
    # ) -> Optional[BankAccount]:
    #     """
    #     Check duplicate bank account number
    #     """
    #     pass

    # @abstractmethod
    # async def get_by_name(
    #     self,
    #     name: str
    # ) -> Optional[BankAccount]:
    #     """
    #     Check duplicate bank account name
    #     """
    #     pass
