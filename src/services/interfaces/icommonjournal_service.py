from abc import ABC, abstractmethod
from src.schemas.journal_schema import JournalCreate
from decimal import Decimal
from datetime import datetime
from typing import Optional
from typing import List

class ICommonJournalService(ABC):
    
    @abstractmethod
    async def create_general_journal_entry(self, rows: List[dict]) -> None:
        pass

    @abstractmethod
    async def create_opening_balance_journal(self, payload):
        pass
    
    @abstractmethod
    async def create_bank_deposit_journal(self, payload):
        pass
    
    @abstractmethod
    async def create_bank_withdraw_journal(self, payload):
        pass
    
    @abstractmethod
    async def get_next_control_item_code(self) -> str:
        pass
    
    @abstractmethod
    async def create_opening_balance(self, payload):
        pass
    
    @abstractmethod
    async def create_opening_balance(self, data):
        pass
        
