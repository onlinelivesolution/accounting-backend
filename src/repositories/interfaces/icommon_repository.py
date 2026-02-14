# src/repositories/interfaces/ireportingitem_repository.py
from typing import List, Any
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.schemas.commondropdown_schema import LineItemDropdown
from src.dto.bankdropdown import BankDropdown
from src.schemas.branch_schema import BranchDropdown
from src.schemas.country_schemas import CountryDropdown
from src.dto.companydto import CompanyDTO
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.company_schema import CompanyDropdown
from src.schemas.bankaccount_schema import BankAccountDropdown
from src.dto.activitycenterdto import ActivityCenterDTO
from src.dto.responsibilitycenterdto import ResponsibilityCenterDTO
from abc import ABC, abstractmethod
from typing import List, Dict

class ICommonRepository(ABC):
    
    @abstractmethod
    async def get_detail_items(self) -> List[Dict]:
        pass
    
    @abstractmethod
    async def get_detail_items_by_load_type(
        self,
        load_types: List[str],
        only_active: bool = True
    ) -> List[Any]:
        """
        Get DetailItem records filtered by loadType.
        Example load_types: ["BANK", "CASH"]
        """
        pass
    
    @abstractmethod
    async def get_account_types(self) -> List[AccountTypeDropdown]:
        pass

    @abstractmethod
    async def get_bank_account_dropdown(self) -> List[BankAccountDropdown]:
        pass

    @abstractmethod
    async def get_control_items_by_account_type(self, account_type_id: int) -> List[dict]:
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
    
    @abstractmethod
    async def get_company_dropdown(self) -> List[CompanyDropdown]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_next_bank_code(self, db: AsyncSession) -> str:
        pass
