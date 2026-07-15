from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.tenant_session_factory import get_tenant_session
from src.models.company import Company
from src.models.fiscalyear import FiscalYear


async def create_default_fiscal_year(database_name: str):

    db: AsyncSession = get_tenant_session(database_name)

    try:
        # Get the company
        result = await db.execute(select(Company))
        company = result.scalars().first()

        if company is None:
            raise Exception("Company not found in tenant database.")

        # Prevent duplicate fiscal years
        result = await db.execute(
            select(FiscalYear).where(FiscalYear.isCurrentFinYear == True)
        )

        if result.scalars().first():
            return

        current_year = datetime.now().year

        fiscal_year = FiscalYear(
            finYear=str(current_year),
            openClose=True,
            status="O",
            comments="Default Fiscal Year",
            dateOpen=datetime(current_year, 1, 1),
            dateClose=None,
            isCeilingLoced=False,
            isUpDateClosed=False,
            isCurrentFinYear=True,
            companyCode=company.companyCode,  # Adjust if your model uses a different field name
        )

        db.add(fiscal_year)
        await db.commit()

    finally:
        await db.close()
