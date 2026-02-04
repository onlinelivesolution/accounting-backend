from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.bankdeposit_model import BankDeposit
from src.schemas.bankdeposit_schema import BankDepositCreate
from src.dto.roledropdown import RoleDropdown

class IBankDepositRepository(ABC):
    
    @abstractmethod
    async def add_bank_deposit(self, bankdeposit: BankDeposit) -> BankDeposit:
        pass 