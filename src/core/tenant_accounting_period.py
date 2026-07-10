from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.tenant_session_factory import get_tenant_session

from src.models.company import Company
from src.models.accountingperiod import AccountingPeriod


async def create_default_accounting_period(
    database_name: str,
):

    db: AsyncSession = get_tenant_session(database_name)

    try:

        result = await db.execute(select(Company))

        company = result.scalars().first()

        if not company:
            raise Exception("Company not found in tenant database.")

        today = date.today()

        if today.month >= 7:
            start_year = today.year
            end_year = today.year + 1
        else:
            start_year = today.year - 1
            end_year = today.year

        period = AccountingPeriod(
            companyCode=company.companyCode,
            periodStart=date(start_year, 7, 1),
            periodEnd=date(end_year, 6, 30),
            fiscalYear=f"{start_year}-{end_year}",
            isClosed=False,
        )

        db.add(period)

        await db.commit()

    finally:

        await db.close()
