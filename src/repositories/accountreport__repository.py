from typing import List, Optional
from datetime import date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.models.detailitem import DetailItem
from src.models.journaldetail_model import JournalDetail
from src.models.journalheader_model import JournalHeader
from src.schemas.accountreport_schema import AccountReportRead
from common.generic.generic_repository import GenericRepository
from src.repositories.interfaces.iaccountreport__repository import IAccountReportRepository

class AccountReportRepository(GenericRepository[JournalDetail], IAccountReportRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(JournalDetail, db)
        self.db = db

    async def get_balance_sheet(self, as_of_date: date):
        query = text(""" 
                SELECT
            am.ControlItem                    AS BalanceSheetGroup,
            ci.ControlItemName                AS ControlItemName,
            ri.ReportingItemName              AS ReportingItemName,
            di.DetailItemCode,
            di.DetailItemName,
            am.NormalBalance,

            SUM(ISNULL(jd.DebitAmount, 0))  AS TotalDebit,
            SUM(ISNULL(jd.CreditAmount, 0)) AS TotalCredit,

            CASE
                WHEN am.NormalBalance = 'Debit'
                    THEN SUM(ISNULL(jd.DebitAmount, 0))
                        - SUM(ISNULL(jd.CreditAmount, 0))
                ELSE
                    SUM(ISNULL(jd.CreditAmount, 0))
                        - SUM(ISNULL(jd.DebitAmount, 0))
            END AS ClosingBalance

        FROM dbo.AccountMapping am
        JOIN dbo.ReportingItem ri
            ON ri.ReportingItemName = am.AccountMappingType
        JOIN dbo.ControlItem ci
            ON ci.ControlItemCode = ri.ControlItemCode
        JOIN dbo.DetailItem di
            ON di.ReportingItemCode = ri.ReportingItemCode

        LEFT JOIN dbo.JournalDetail jd
            ON jd.DetailItemCode = di.DetailItemCode
        LEFT JOIN dbo.JournalHeader jh
            ON jh.JournalHeaderID = jd.JournalHeaderID
            AND jh.JournalDate <= :as_of_date

        WHERE
            am.FinancialStatement = 'BS'
            AND ci.FinancialStatementType = 'BALANCE_SHEET'
            AND di.IsActive = 1

        GROUP BY
            am.ControlItem,
            ci.ControlItemName,
            ri.ReportingItemName,
            di.DetailItemCode,
            di.DetailItemName,
            am.NormalBalance

        HAVING
            CASE
                WHEN am.NormalBalance = 'Debit'
                    THEN SUM(ISNULL(jd.DebitAmount, 0))
                        - SUM(ISNULL(jd.CreditAmount, 0))
                ELSE
                    SUM(ISNULL(jd.CreditAmount, 0))
                        - SUM(ISNULL(jd.DebitAmount, 0))
            END <> 0

        ORDER BY
            am.ControlItem,
            ri.ReportingItemName,
            di.DetailItemName;

        """)

        result = await self.db.execute(
            query,
            {"as_of_date": as_of_date}
        )
        return result.mappings().all()
    
    async def get_trial_balance(self, as_of_date: date):
        query = text("""
                SELECT
            ci.ControlItemName,
            ri.ReportingItemName,
            di.DetailItemCode,
            di.DetailItemName,
            am.NormalBalance,

            SUM(ISNULL(jd.DebitAmount, 0))  AS TotalDebit,
            SUM(ISNULL(jd.CreditAmount, 0)) AS TotalCredit,

            CASE
                WHEN am.NormalBalance = 'Debit'
                    THEN
                        CASE
                            WHEN SUM(ISNULL(jd.DebitAmount, 0))
                            - SUM(ISNULL(jd.CreditAmount, 0)) > 0
                            THEN SUM(ISNULL(jd.DebitAmount, 0))
                            - SUM(ISNULL(jd.CreditAmount, 0))
                            ELSE 0
                        END
                ELSE 0
            END AS DebitBalance,

            CASE
                WHEN am.NormalBalance = 'Credit'
                    THEN
                        CASE
                            WHEN SUM(ISNULL(jd.CreditAmount, 0))
                            - SUM(ISNULL(jd.DebitAmount, 0)) > 0
                            THEN SUM(ISNULL(jd.CreditAmount, 0))
                            - SUM(ISNULL(jd.DebitAmount, 0))
                            ELSE 0
                        END
                ELSE 0
            END AS CreditBalance

        FROM dbo.AccountMapping am
        JOIN dbo.ReportingItem ri
            ON ri.ReportingItemName = am.AccountMappingType
        JOIN dbo.ControlItem ci
            ON ci.ControlItemCode = ri.ControlItemCode
        JOIN dbo.DetailItem di
            ON di.ReportingItemCode = ri.ReportingItemCode
            AND di.IsActive = 1

        LEFT JOIN dbo.JournalDetail jd
            ON jd.DetailItemCode = di.DetailItemCode
        LEFT JOIN dbo.JournalHeader jh
            ON jh.JournalHeaderID = jd.JournalHeaderID
            AND jh.JournalDate <= :as_of_date

        GROUP BY
            ci.ControlItemName,
            ri.ReportingItemName,
            di.DetailItemCode,
            di.DetailItemName,
            am.NormalBalance

        HAVING
            SUM(ISNULL(jd.DebitAmount, 0)) <> 0
            OR SUM(ISNULL(jd.CreditAmount, 0)) <> 0

        ORDER BY
            ci.ControlItemName,
            ri.ReportingItemName,
            di.DetailItemName;

        """)
        result = await self.db.execute(
            query,
            {"as_of_date": as_of_date}
        )
        return result.mappings().all()
    
    async def get_profit_loss(self, as_of_date: date):
        query = text("""
                SELECT
            ci.ControlItemName,
            ri.ReportingItemName,
            di.DetailItemCode,
            di.DetailItemName,
            am.NormalBalance,

            SUM(ISNULL(jd.DebitAmount, 0))  AS TotalDebit,
            SUM(ISNULL(jd.CreditAmount, 0)) AS TotalCredit,

            CASE
                WHEN am.NormalBalance = 'Credit'
                    THEN SUM(ISNULL(jd.CreditAmount, 0))
                        - SUM(ISNULL(jd.DebitAmount, 0))
                ELSE
                    SUM(ISNULL(jd.DebitAmount, 0))
                        - SUM(ISNULL(jd.CreditAmount, 0))
            END AS Amount

        FROM dbo.AccountMapping am
        JOIN dbo.ReportingItem ri
            ON ri.ReportingItemName = am.AccountMappingType
        JOIN dbo.ControlItem ci
            ON ci.ControlItemCode = ri.ControlItemCode
        JOIN dbo.DetailItem di
            ON di.ReportingItemCode = ri.ReportingItemCode
            AND di.IsActive = 1

        LEFT JOIN dbo.JournalDetail jd
            ON jd.DetailItemCode = di.DetailItemCode
        LEFT JOIN dbo.JournalHeader jh
            ON jh.JournalHeaderID = jd.JournalHeaderID
            AND jh.JournalDate <= :as_of_date

        WHERE
            am.FinancialStatement = 'PL'
            AND ci.FinancialStatementType = 'PROFIT_LOSS'

        GROUP BY
            ci.ControlItemName,
            ri.ReportingItemName,
            di.DetailItemCode,
            di.DetailItemName,
            am.NormalBalance

        HAVING
            SUM(ISNULL(jd.DebitAmount, 0)) <> 0
            OR SUM(ISNULL(jd.CreditAmount, 0)) <> 0

        ORDER BY
            ci.ControlItemName,
            ri.ReportingItemName,
            di.DetailItemName;

        """)
        result = await self.db.execute(
            query,
            {"as_of_date": as_of_date}
        )
        return result.mappings().all()
    
    async def get_ledger_entries(
        self,
        detailItemCode: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[dict]:

        query = (
            select(
                JournalHeader.journalID,
                JournalHeader.journalDate,
                JournalHeader.journalType,
                JournalHeader.referenceNo,
                JournalHeader.description,
                DetailItem.detailItemCode,
                DetailItem.detailItemName,
                DetailItem.normalBalance,
                JournalDetail.debitAmount.label("debit"),
                JournalDetail.creditAmount.label("credit"),
            )
            .join(JournalHeader, JournalHeader.journalID == JournalDetail.journalID)
            .join(DetailItem, DetailItem.detailItemCode == JournalDetail.detailItemCode)
            .where(JournalDetail.detailItemCode == detailItemCode)
        )

        if start_date:
            query = query.where(JournalHeader.journalDate >= start_date)

        if end_date:
            query = query.where(JournalHeader.journalDate <= end_date)

        query = query.order_by(
            JournalHeader.journalDate,
            JournalHeader.journalID
        )

        result = await self.db.execute(query)
        return result.mappings().all()
