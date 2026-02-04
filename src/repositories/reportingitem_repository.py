from common.generic.generic_repository import GenericRepository
from src.repositories.interfaces.ireportingitem_repository import IReportingItemRepository
from src.models.reportingitem import ReportingItem
from src.models.company import Company
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.models.controlitem import ControlItem
from src.models.detailitem import DetailItem
from src.models.accounttype import AccountType
from src.schemas.reportingitem_schema import ReportingItemUpdate
from src.schemas.controlitem_schema import ControlItemDropdown
from sqlalchemy import select, func, cast, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional


class ReportingItemRepository(GenericRepository[ReportingItem], IReportingItemRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(ReportingItem, db)
    
    async def add_reporting_item(self, reportingitem: ReportingItem) -> ReportingItem:
        self.db.add(reportingitem)
        await self.db.commit()
        await self.db.refresh(reportingitem)
        return reportingitem
    
    async def update_reporting_item(
        self, reportingItemCode: str, reportingitem: ReportingItemUpdate
    ) -> Optional[ReportingItem]:
        db_item = await self.db.get(ReportingItem, reportingItemCode)
        if not db_item:
            return None

        for key, value in reportingitem.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)

        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item
 
    async def get_all_reporting_items(self, skip: int, limit: int) -> dict:
        db: AsyncSession = self.db

        # Total count
        total_query = await db.execute(select(func.count(ReportingItem.reportingItemCode)))
        total = total_query.scalar_one()

        # Main query with joins
        query = (
            select(
                ReportingItem,
                Company.companyName,
                ControlItem.controlItemCode.label("ctrl_code"),
                ControlItem.controlItemName.label("ctrl_name")
            )
            .outerjoin(Company, ReportingItem.companyCode == Company.companyCode)
            .outerjoin(ControlItem, ReportingItem.controlItemCode == ControlItem.controlItemCode)
            .order_by(ReportingItem.reportingItemCode.desc())
            .offset(skip)
            .limit(limit)
        )

        results = await db.execute(query)
        rows = results.mappings().all()

        reportingItems = []
        for row in rows:
            r = row["ReportingItem"]
            reportingItems.append({
                "reportingItemCode": r.reportingItemCode,
                "controlItemCode": row["ctrl_code"],      # ← now always correct
                "controlItemName": row["ctrl_name"],      # ← FIX 🟢 now included
                "reportingItemName": r.reportingItemName,
                "isActive": r.isActive,
                "isDeleted": r.isDeleted,
                "companyCode": r.companyCode,
                "companyName": row["companyName"],
                "createdBy": r.createdBy,
                "createdDate": r.createdDate,
                "updatedBy": r.updatedBy,
                "updatedDate": r.updatedDate,
            })

        return {
            "data": reportingItems,
            "skip": skip,
            "limit": limit,
            "total": total
        }
    
    async def get_account_types(self) -> List[AccountTypeDropdown]:
        stmt = select(AccountType.accountTypeID, AccountType.accountTypeName).where(AccountType.isDeleted == False)
        result = await self.db.execute(stmt)
        rows = result.all()
        return [AccountTypeDropdown(accountTypeID=row[0], accountTypeName=row[1]) for row in rows]
    
    async def get_control_items_by_account_type(self, account_type_id: int):
        stmt = (
            select(ControlItem)
            .where(
                ControlItem.accountTypeID == account_type_id,
                ControlItem.isDeleted == False
            )
            .order_by(ControlItem.controlItemCode)
        )

        result = await self.db.execute(stmt)
        items = result.scalars().all()

        return [ControlItemDropdown.model_validate(i) for i in items]

    
    async def get_controlitem_dropdown(self) -> List[ControlItemDropdown]:
        result = await self.db.execute(select(ControlItem))
        controlitems = result.scalars().all()
        return [ControlItemDropdown.model_validate(c) for c in controlitems]
  
    async def get_max_reporting_item_code(self, control_item_code: str) -> Optional[str]:

        stmt = (
            select(func.max(ReportingItem.reportingItemCode))
            .where(ReportingItem.reportingItemCode.like(f"{control_item_code}%"))
        )

        result = await self.db.execute(stmt)
        return result.scalar()
