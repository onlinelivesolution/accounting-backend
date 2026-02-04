# src/services/reportingitem_service.py
from src.repositories.interfaces.icommon_repository import ICommonRepository
from src.services.interfaces.icommon_service import ICommonService
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.dto.bankdropdown import BankDropdown
from src.schemas.country_schemas import CountryDropdown
from src.schemas.branch_schema import BranchDropdown
from src.schemas.company_schema import CompanyDropdown
from src.schemas.bankaccount_schema import BankAccountDropdown
from src.schemas.controlitem_schema import ControlItemDropdown
from src.dto.companydto import CompanyDTO
from src.dto.activitycenterdto import ActivityCenterDTO
from src.dto.responsibilitycenterdto import ResponsibilityCenterDTO
from typing import List, Dict

class CommonService(ICommonService):
    def __init__(self, repository: ICommonRepository):
        self.repository = repository
    
    async def get_detail_items(self) -> List[Dict]:
        return await self.repository.get_detail_items()
    
    async def get_bank_cash_detailitems(self):
        return await self.repository.get_detail_items_by_load_type(
            load_types=["BANK", "CASH"]
        )

    async def get_detailitems_by_types(self, load_types: List[str]):
        return await self.repository.get_detail_items_by_load_type(
            load_types=load_types
        )
        
    async def get_account_types(self) -> List[AccountTypeDropdown]:
        return await self.repository.get_account_types()
    
    async def get_bank_account_dropdown(self) -> List[BankAccountDropdown]:
        return await self.repository.get_bank_account_dropdown()

    async def get_control_items_by_account_type(self, account_type_id: int) -> List[Dict]:
        return await self.repository.get_control_items_by_account_type(account_type_id)
    
    async def get_reporting_items_by_control_item(self, controlItemCode: str) -> List[dict]:
        return await self.repository.get_reporting_items_by_control_item(controlItemCode)
    
    async def get_bank_dropdown(self) -> List[BankDropdown]:
        return await self.repository.get_bank_dropdown()
    
    async def get_branch_dropdown(self) -> List[BranchDropdown]:
        return await self.repository.get_branch_dropdown()
    
    async def get_all_companies(self) -> List[CompanyDTO]:
        return await self.repository.get_all_companies()
    
    async def get_all_departments(self) -> List[ActivityCenterDTO]:
        return await self.repository.get_all_departments()
    
    async def get_all_sections(self) -> List[ResponsibilityCenterDTO]:
        return await self.repository.get_all_sections()
    
    async def get_country_dropdown(self) -> List[CountryDropdown]:
        return await self.repository.get_country_dropdown()
    
    async def get_company_dropdown(self) -> List[CompanyDropdown]:
        return await self.repository.get_company_dropdown()
    
    async def get_next_bank_code(self) -> str:
        return await self.repository.get_next_bank_code()
