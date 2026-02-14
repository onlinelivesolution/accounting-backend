from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.repositories.interfaces.icommondropdown_repository import ICommonDropdownRepository
from src.schemas.commondropdown_schema import DropdownItem
from src.schemas.commondropdown_schema import LineItemDropdown
from src.models.lineitem import LineItem
from src.models.customers import Customer
from src.models.vatrate_model import VATRate


class CommonDropdownRepository(ICommonDropdownRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_vat_rate_dropdown(self, company_code: str) -> List[DropdownItem]:

        stmt = (
            select(
                VATRate.vATRateID.label("id"),
                VATRate.ratePercent.label("name")
            )
            .where(
                VATRate.isActive == True,
                VATRate.companyCode == company_code
            )
            .order_by(VATRate.vATRateName)
        )

        result = await self.db.execute(stmt)
        rows = result.all()

        # Add "None" option manually
        dropdown = [DropdownItem(id=0, name="None")]

        dropdown.extend(
            DropdownItem(id=row.id, name=row.name)
            for row in rows
        )

        return dropdown
    
    async def get_lineitem_dropdown(self):
        stmt = (
            select(
                LineItem.itemID,
                LineItem.itemCode,
                LineItem.itemName,
                LineItem.unitPrice
                # Item.vatRateID
            )
            .where(LineItem.isActive == True)
            .order_by(LineItem.itemName)
        )

        result = await self.db.execute(stmt)
        return result.all()
    
    async def get_customer_dropdown(self):
        stmt = (
            select(
                Customer.customerID,
                Customer.customerName,
                Customer.vatReference,
                Customer.creditLimit
            )
            .where(Customer.isActive == True)
            .order_by(Customer.customerName)
        )

        result = await self.db.execute(stmt)
        return result.all()