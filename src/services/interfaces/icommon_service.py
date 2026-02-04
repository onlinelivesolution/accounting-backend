# src/services/interfaces/ireportingitem_service.py
from typing import List, Dict, Any
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.dto.bankdropdown import BankDropdown
from src.schemas.country_schemas import CountryDropdown
from src.schemas.branch_schema import BranchDropdown
from src.dto.companydto import CompanyDTO
from src.schemas.company_schema import CompanyDropdown
from src.schemas.bankaccount_schema import BankAccountDropdown
from src.dto.activitycenterdto import ActivityCenterDTO
from src.dto.responsibilitycenterdto import ResponsibilityCenterDTO
from src.schemas.controlitem_schema import ControlItemDropdown
from abc import ABC, abstractmethod

class ICommonService(ABC):
    
    @abstractmethod
    async def get_detail_items(self) -> List[Dict]:
        pass
    
    @abstractmethod
    async def get_bank_cash_detailitems(self) -> List[Any]:
        """
        Used for:
        - Bank Deposit
        - Bank Withdraw
        - Cash Receive
        - Cash Payment
        """
        pass
    
    @abstractmethod
    async def get_detailitems_by_types(
        self,
        load_types: List[str]
    ) -> List[Any]:
        """
        Generic loader for dropdowns:
        Example:
        - ["EXPENSE"]
        - ["BANK", "CASH"]
        - ["PAYABLE", "RECEIVABLE"]
        """
        pass

    @abstractmethod
    async def get_bank_account_dropdown(self) -> List[BankAccountDropdown]:
        pass

    @abstractmethod
    async def get_account_types(self) -> List[AccountTypeDropdown]:
        pass

    @abstractmethod
    async def get_control_items_by_account_type(self, account_type_id: int) -> List[Dict]:
        pass
    
    @abstractmethod
    async def get_reporting_items_by_control_item(self, controlItemCode: str) -> List[Any]:
        pass
    
    @abstractmethod
    async def get_bank_dropdown(self) -> List[BankDropdown]:
        pass
    
    @abstractmethod
    async def get_branch_dropdown(self) -> List[BranchDropdown]:
        pass
    
    async def get_all_companies(self) -> List[CompanyDTO]:
        raise NotImplementedError
    
    async def get_all_departments(self) -> List[ActivityCenterDTO]:
        raise NotImplementedError
    
    async def get_all_sections(self) -> List[ResponsibilityCenterDTO]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_country_dropdown(self) -> List[CountryDropdown]:
        pass
    
    abstractmethod
    async def get_company_dropdown(self) -> List[CompanyDropdown]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_next_bank_code(self) -> str:
        pass
