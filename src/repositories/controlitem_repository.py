from common.generic.generic_repository import GenericRepository
from src.repositories.interfaces.icontrolitem_repository import IControlItemRepository
from src.models.controlitem import ControlItem
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.schemas.fatype_schema import FATypeDropdown
from src.schemas.controlitem_schema import ControlItemUpdate
from src.models.company import Company
from src.models.accounttype import AccountType
from typing import Optional
from src.models.fatype import FAType
from sqlalchemy import update
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Integer


class ControlItemRepository(GenericRepository[ControlItem], IControlItemRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(ControlItem, db)
        
    async def add_controlitem(self, controlitem: ControlItem) -> ControlItem:
        self.db.add(controlitem)
        await self.db.commit()
        await self.db.refresh(controlitem)
        return controlitem
    
    async def update_control_item(
        self, controlItemCode: str, controlitem: ControlItemUpdate
    ) -> Optional[ControlItem]:
        db_item = await self.db.get(ControlItem, controlItemCode)
        if not db_item:
            return None

        for key, value in controlitem.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)

        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item
 
    async def get_all_controlitems(self, skip: int, limit: int) -> dict: 
        db: AsyncSession = self.db
        total_query = await db.execute(select(func.count(ControlItem.controlItemCode)))
        total = total_query.scalar_one()

        query = (
            select(
                ControlItem,
                Company.companyName.label("companyName"),
                AccountType.accountTypeName.label("accountTypeName"),
            )
            .outerjoin(Company, ControlItem.companyCode == Company.companyCode)
            .outerjoin(AccountType, ControlItem.accountTypeID == AccountType.accountTypeID)
            .order_by(ControlItem.controlItemCode)
            .offset(skip)
            .limit(limit)
        )
        compiled = query.compile(compile_kwargs={"literal_binds": True})
        print("🔍 Executing SQL:\n", compiled, "\n")
        results = await db.execute(query)
        rows = results.mappings().all()   # ✅ get rows first

        if rows:                          # ✅ check first row keys
            print(rows[0].keys())

        controlItems = []
        for row in rows:
            c = row["ControlItem"]
            controlItems.append({
                "controlItemCode": c.controlItemCode,
                "controlItemName": c.controlItemName,
                "isActive": c.isActive,
                "accountTypeID": c.accountTypeID,
                "accountTypeName": row["accountTypeName"],   # ✅ now safe
                "fATypeID": c.fATypeID,
                "companyCode": c.companyCode,
                "companyName": row["companyName"],           # ✅ now safe
                "createdBy": c.createdBy,
                "createdDate": c.createdDate,
                "updatedBy": c.updatedBy,
                "updatedDate": c.updatedDate,
                "isDeleted": c.isDeleted,
            })

        return {
            "data": controlItems,
            "skip": skip,
            "limit": limit,
            "total": total
        }

    async def get_next_control_item_code(self) -> str:
        stmt = select(
            func.max(cast(ControlItem.controlItemCode, Integer))
        )
        result = await self.db.execute(stmt)
        max_code = result.scalar()

        if max_code is None:
            next_code = 1
        else:
            next_code = max_code + 1

        return f"{next_code:02d}"
    
    
    async def get_account_types(self) -> List[AccountTypeDropdown]:
        stmt = select(AccountType.accountTypeID, AccountType.accountTypeName).where(AccountType.isDeleted == False)
        result = await self.db.execute(stmt)
        rows = result.all()
        return [AccountTypeDropdown(accountTypeID=row[0], accountTypeName=row[1]) for row in rows]
    
    async def get_fa_types(self) -> List[FATypeDropdown]:
        stmt = select(FAType.fATypeID, FAType.fATypeName)
        result = await self.db.execute(stmt)
        rows = result.all()
        return [FATypeDropdown(fATypeID=row[0], fATypeName=row[1]) for row in rows]
