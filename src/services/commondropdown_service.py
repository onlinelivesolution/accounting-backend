from typing import List
from src.repositories.interfaces.icommondropdown_repository import ICommonDropdownRepository
from src.services.interfaces.icommondropdown_service import ICommonDropdownService
from src.schemas.commondropdown_schema import DropdownItem, LineItemDropdown

class CommonDropdownService(ICommonDropdownService):

    def __init__(self, repository: ICommonDropdownRepository):
        self.repository = repository

    async def get_vat_rate_dropdown(self, company_code: str) -> List[DropdownItem]:
        return await self.repository.get_vat_rate_dropdown(company_code)

    async def get_lineitem_dropdown(self):
        rows = await self.repository.get_lineitem_dropdown()

        return [
            {
                "itemID": r.itemID,
                "itemCode": r.itemCode,
                "itemName": r.itemName,
                "unitPrice": float(r.unitPrice)
                # "vatRateID": r.vatRateID
            }
            for r in rows
        ]
    
    async def get_customer_dropdown(self):
        rows = await self.repository.get_customer_dropdown()

        return [
            {
                "customerID": c.customerID,
                "customerName": c.customerName,
                "vatReference": c.vatReference,
                "creditLimit": float(c.creditLimit)
            }
            for c in rows
        ]
