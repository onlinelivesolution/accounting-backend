from abc import ABC, abstractmethod
from src.schemas.journal_schema import JournalCreate
from src.models.journaldetail_model import JournalDetail
from src.models.journalheader_model import JournalHeader
from src.models.accountingperiod import AccountingPeriod
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import List

class ICommonJournalRepository(ABC):
    
    @abstractmethod
    async def create_general_journal_entry(self, rows: List[dict]) -> None:
        pass
    
    @abstractmethod
    async def get_detail_item_by_account_id(self, account_id: int) -> str:
        pass

    @abstractmethod
    async def resolve_detail_hierarchy(self, detail_item_code: str) -> dict:
        pass

    @abstractmethod
    async def get_default_activity_center(self, company_code: str) -> str:
        pass

    @abstractmethod
    async def get_default_resp_center(self, activity_center_code: str) -> str:
        pass

    @abstractmethod
    async def get_current_fiscal_year(self, company_code: str) -> int:
        pass

    @abstractmethod
    async def create_opening_balance_journal(self, data: dict):
        pass
    
    @abstractmethod
    async def create_bank_deposit_journal(self, data: dict):
        pass
    
    @abstractmethod
    async def create_bank_withdraw_journal(self, data: dict):
        pass
    
    @abstractmethod
    async def get_next_control_item_code(self, db: AsyncSession) -> str:
        pass
    
    @abstractmethod
    async def create_opening_balance(self, data: dict):
        pass
    
    @abstractmethod
    async def create_invoice_journal_entry(self, data: dict):
        pass

    @abstractmethod
    async def get_detail_item_by_account_id(self, account_id: int) -> str:
        pass

    @abstractmethod
    async def resolve_detail_hierarchy(self, detail_item_code: str) -> dict:
        pass

    @abstractmethod
    async def get_default_activity_center(self, company_code: str) -> str:
        pass

    @abstractmethod
    async def get_default_resp_center(self, company_code: str) -> str:
        pass

    @abstractmethod
    async def get_current_fiscal_year(self, company_code: str) -> int:
        pass
    
    @abstractmethod
    async def get_period_by_date(self, companyCode: str, txn_date: date) -> AccountingPeriod:
        pass
    
    @abstractmethod
    async def create_journal(self, header: JournalHeader, details: List[JournalDetail]) -> JournalHeader:
        pass