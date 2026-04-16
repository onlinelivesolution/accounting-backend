from common.generic.generic_repository import GenericRepository
from src.repositories.interfaces.icommon_repository import ICommonRepository
from src.models.detailitem import DetailItem
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.company import Company
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.dto.bankdropdown import BankDropdown
from src.schemas.country_schemas import CountryDropdown
from src.schemas.branch_schema import BranchDropdown
from src.models.controlitem import ControlItem
from src.models.reportingitem import ReportingItem
from src.models.accounttype import AccountType
from src.models.bank_model import Bank
from src.schemas.company_schema import CompanyDropdown
from src.schemas.bankaccount_schema import BankAccountDropdown
from src.models.branch_model import Branch
from src.models.company import Company
from src.models.bankaccount_model import BankAccount
from src.models.customerreceipt_model import CustomerReceipt
from src.models.country_model import Country
from src.dto.companydto import CompanyDTO
from src.models.activitycenter import ActivityCenter
from src.dto.activitycenterdto import ActivityCenterDTO
from src.models.responsibilitycenter import ResponsibilityCenter
from src.dto.responsibilitycenterdto import ResponsibilityCenterDTO
from sqlalchemy import select, func, cast, Integer
from sqlalchemy.sql import text
from typing import List, Optional
from typing import List, Dict
from src.schemas.controlitem_schema import ControlItemDropdown  # pydantic schema if you have one

class CommonRepository(GenericRepository[DetailItem], ICommonRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(DetailItem, db)
    
    async def get_detail_items(self):

        stmt = (
            select(
                DetailItem.detailItemCode,
                DetailItem.detailItemName,
                ReportingItem.reportingItemName
            )
            .join(
                ReportingItem,
                DetailItem.reportingItemCode == ReportingItem.reportingItemCode
            )
            .where(DetailItem.isActive == True)
            .order_by(
                ReportingItem.reportingItemName,
                DetailItem.detailItemCode
            )
        )

        result = await self.db.execute(stmt)

        return [
            {
                "detailItemCode": r.detailItemCode,
                "detailItemName": r.detailItemName,
                "reportingItemName": r.reportingItemName
            }
            for r in result.all()
        ]
    
    async def get_detail_items_by_load_type(
        self,
        load_types: List[str],
        only_active: bool = True
    ):
        stmt = select(DetailItem).where(
            DetailItem.loadType.in_(load_types)
        )

        if only_active:
            stmt = stmt.where(DetailItem.isActive == True)

        stmt = stmt.order_by(DetailItem.detailItemName)

        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_account_types(self) -> List[AccountTypeDropdown]:
        stmt = select(AccountType.accountTypeID, AccountType.accountTypeName).where(AccountType.isDeleted == False)
        result = await self.db.execute(stmt)
        rows = result.all()
        return [AccountTypeDropdown(accountTypeID=row[0], accountTypeName=row[1]) for row in rows]



    async def get_control_items_by_account_type(self, account_type_id: int) -> List[dict]:
        """
        Return list of control items filtered by accountTypeID as plain dicts.
        Using dicts avoids pydantic model_validate errors if your items are strings.
        """
        stmt = (
            select(ControlItem)
            .where(ControlItem.accountTypeID == account_type_id)
            .where(ControlItem.isDeleted == False)  # if you have this flag
            .order_by(ControlItem.controlItemCode)
        )

        result = await self.db.execute(stmt)
        items = result.scalars().all()  # list[ControlItem model instances]

        # convert sqlalchemy model -> plain dicts expected by the frontend
        return [
            {
                "controlItemCode": c.controlItemCode,
                "controlItemName": c.controlItemName,
                "accountTypeID": c.accountTypeID,
            }
            for c in items
        ]
        
    async def get_reporting_items_by_control_item(self, controlItemCode: str) -> List[dict]:
        query = select(
            ReportingItem.reportingItemCode,
            ReportingItem.reportingItemName,
            ReportingItem.controlItemCode
        ).where(ReportingItem.controlItemCode == controlItemCode)

        result = await self.db.execute(query)
        rows = result.fetchall()

        return [dict(row._mapping) for row in rows]
    
    async def get_bank_dropdown(self) -> List[BankDropdown]:
        stmt = select(Bank.bankID, Bank.bankName).where(Bank.isDeleted == False)
        result = await self.db.execute(stmt)
        rows = result.all()
        return [BankDropdown(bankID=row[0], bankName=row[1]) for row in rows]
    
    async def get_bank_account_dropdown(self) -> List[BankAccountDropdown]:
        stmt = select(BankAccount.bankAccountID, BankAccount.bankAccountName).where(Bank.isDeleted == False)
        result = await self.db.execute(stmt)
        rows = result.all()
        return [BankAccountDropdown(bankAccountID=row[0], bankAccountName=row[1]) for row in rows]
    
    async def get_branch_dropdown(self) -> List[BranchDropdown]:
        stmt = select(Branch.branchID, Branch.branchName).where(Branch.isDeleted == False)
        result = await self.db.execute(stmt)
        rows = result.all()
        return [BranchDropdown(branchID=row[0], branchName=row[1]) for row in rows]
    
    async def get_all_companies(self) -> List[CompanyDTO]:
        result = await self.db.execute(select(Company))
        companies = result.scalars().all()
        return [CompanyDTO.model_validate(c) for c in companies]
    
    async def get_all_departments(self) -> List[ActivityCenterDTO]:
        result = await self.db.execute(select(ActivityCenter))
        departments = result.scalars().all()
        return [ActivityCenterDTO.model_validate(d) for d in departments]
    
    async def get_all_sections(self) -> List[ResponsibilityCenterDTO]:
        result = await self.db.execute(select(ResponsibilityCenter))
        sections = result.scalars().all()
        return [ResponsibilityCenterDTO.model_validate(s) for s in sections]
    
    async def get_country_dropdown(self) -> List[CountryDropdown]:
        stmt = select(Country.countryID, Country.countryName)
        result = await self.db.execute(stmt)
        rows = result.all()
        return [CountryDropdown(countryID=row[0], countryName=row[1]) for row in rows]
    
    async def get_company_dropdown(self) -> List[CompanyDropdown]:
        result = await self.db.execute(select(Company))
        company = result.scalars().all()
        return [CompanyDropdown.model_validate(c) for c in company]
    
    async def get_next_bank_code(self) -> str:
        stmt = select(
            func.max(cast(Bank.bankCode, Integer))
        )
        result = await self.db.execute(stmt)
        max_code = result.scalar()

        if max_code is None:
            next_code = 1
        else:
            next_code = max_code + 1

        return f"{next_code:05d}"
    
    async def get_next_receipt_no(self) -> str:
        result = await self.db.execute(
            select(func.max(CustomerReceipt.receiptNo))
        )
        last_no = result.scalar()

        if not last_no:
            return "RCP0000001"

        number = int(last_no.replace("RCP", "")) + 1
        return f"RCP{number:07d}"

