from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import date
from src.models.salesorder import SalesOrder
from src.repositories.interfaces.isalesorder_repository import ISalesOrderRepository

from common.generic.generic_repository import GenericRepository

class SalesOrderRepository(GenericRepository[SalesOrder], ISalesOrderRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(SalesOrder, db)
        self.db = db

    async def create_sales_order(self, salesorder: SalesOrder) -> SalesOrder:
        self.db.add(salesorder)
        await self.db.commit()

        stmt = (
            select(salesorder)
            .options(selectinload(salesorder.items))
            .where(salesorder.salesOrderID == salesorder.salesOrderID)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()
    
    async def get_by_id(self, salesOrderID: int) -> SalesOrder | None:
        stmt = (
            select(SalesOrder)
            .options(selectinload(SalesOrder.items))
            .where(SalesOrder.salesOrderID == salesOrderID)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[SalesOrder]:
        result = await self.db.execute(select(SalesOrder))
        return result.scalars().all()
    
    async def get_next_salesorder_no(self) -> str:
        result = await self.db.execute(
            select(func.max(SalesOrder.salesOrderNo))
        )
        last_no = result.scalar()

        if not last_no:
            return "SOR0000001"

        number = int(last_no.replace("SOR", "")) + 1
        return f"SOR{number:07d}"
    
    async def load_sales_order_table(self):
        stmt = (
            select(SalesOrder)
            .options(selectinload(SalesOrder.customer))
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()   

    async def get_filter_sales_order(
        self,
        filter_type: str,
        salesorder_no: Optional[str],
        page: int,
        page_size: int
    ):
        stmt = (
            select(SalesOrder)
            .options(selectinload(SalesOrder.customer))  # ✅ FIX
        )

        today = date.today()

        # ---------- FILTER ----------
        if filter_type == "TODAY":
            stmt = stmt.where(SalesOrder.salesOrderDate == today)

        elif filter_type == "THIS_MONTH":
            stmt = stmt.where(
                func.month(SalesOrder.salesOrderDate) == today.month,
                func.year(SalesOrder.salesOrderDate) == today.year
            )

        elif filter_type == "EXPIRING_TODAY":
            stmt = stmt.where(SalesOrder.expireDate == today)

        elif filter_type == "EXPIRED":
            stmt = stmt.where(SalesOrder.expireDate < today)

        elif filter_type == "PENDING":
            stmt = stmt.where(SalesOrder.status == "PENDING")

        elif filter_type == "INVOICED":
            stmt = stmt.where(SalesOrder.status == "INVOICED")

        # ---------- SEARCH ----------
        if salesorder_no:
            stmt = stmt.where(
                SalesOrder.salesOrderNo.ilike(f"%{salesorder_no}%")
            )

        # ---------- ORDER (MANDATORY FOR MSSQL) ----------
        stmt = stmt.order_by(SalesOrder.salesOrderID.desc())

        # ---------- COUNT ----------
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar()

        # ---------- PAGINATION ----------
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(stmt)
        salesorders = result.scalars().all()

        return {
            "items": [
                {
                    "salesOrderID": so.salesOrderID,
                    "salesOrderNo": so.salesOrderNo,
                    "salesOrderDate": so.salesOrderDate,
                    "totalAmount": so.totalAmount,
                    "status": so.status,
                    "customerName": so.customer.customerName if so.customer else None
                }
                for so in salesorders
            ],
            "total": total
        }