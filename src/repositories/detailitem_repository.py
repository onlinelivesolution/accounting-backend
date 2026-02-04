from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from common.generic.generic_repository import GenericRepository
from common.utils.code_generator import NumericCodeGenerator

from src.repositories.interfaces.idetailitem_repository import IDetailItemRepository
from src.schemas.detailitemautocreate_schema import DetailItemAutoCreateRequest

from src.models.controlitem import ControlItem
from src.models.reportingitem import ReportingItem
from src.models.detailitem import DetailItem
from src.models.journalheader_model import JournalHeader
from src.models.journaldetail_model import JournalDetail
from src.models.accountingperiod import AccountingPeriod

from src.constants.accountMappingRules import ACCOUNT_MAPPING_RULES


class DetailItemRepository(
    GenericRepository[DetailItem],
    IDetailItemRepository
):
    def __init__(self, db: AsyncSession):
        super().__init__(DetailItem, db)
        self.db = db

    # ----------------------------------------------------
    # BASIC GETTERS
    # ----------------------------------------------------
    async def get_control_by_name(self, name: str):
        result = await self.db.execute(
            select(ControlItem)
            .where(ControlItem.controlItemName == name)
        )
        return result.scalar_one_or_none()

    async def get_reporting_by_name(self, name: str, control_code: str):
        result = await self.db.execute(
            select(ReportingItem).where(
                ReportingItem.reportingItemName == name,
                ReportingItem.controlItemCode == control_code
            )
        )
        return result.scalar_one_or_none()

    async def get_detail_by_name(self, name: str):
        result = await self.db.execute(
            select(DetailItem)
            .where(DetailItem.detailItemName == name)
        )
        return result.scalar_one_or_none()

    # ----------------------------------------------------
    # ACCOUNTING PERIOD
    # ----------------------------------------------------
    async def get_open_period(self) -> AccountingPeriod | None:
        result = await self.db.execute(
            select(AccountingPeriod)
            .where(AccountingPeriod.isClosed == False)
            .order_by(AccountingPeriod.periodStart.desc())
        )
        return result.scalars().first()

    # ----------------------------------------------------
    # OPENING EQUITY
    # ----------------------------------------------------
    async def get_opening_equity_account(self) -> DetailItem | None:
        result = await self.db.execute(
            select(DetailItem)
            .where(DetailItem.detailItemName == "Opening Balance Equity")
        )
        return result.scalar_one_or_none()

    async def create_opening_equity_account(self) -> DetailItem:

        # -------- Control (0001)
        control = await self.get_control_by_name("Equity")
        if not control:
            control_code = await NumericCodeGenerator.get_next_code(
                self.db,
                ControlItem,
                ControlItem.controlItemCode,
                length=4
            )

            control = ControlItem(
                controlItemCode=control_code,
                controlItemName="Equity",
                accountCategory="EQUITY",
                financialStatementType="BALANCE_SHEET",
                isActive=True
            )
            self.db.add(control)
            await self.db.flush()

        # -------- Reporting (000001)
        reporting = await self.get_reporting_by_name(
            "Owner's Equities",
            control.controlItemCode
        )

        if not reporting:
            reporting_code = await NumericCodeGenerator.get_next_code(
                self.db,
                ReportingItem,
                ReportingItem.reportingItemCode,
                length=6
            )

            reporting = ReportingItem(
                reportingItemCode=reporting_code,
                reportingItemName="Owner's Equities",
                controlItemCode=control.controlItemCode
            )
            self.db.add(reporting)
            await self.db.flush()

        # -------- Detail (000000001)
        detail_code = await NumericCodeGenerator.get_next_code(
            self.db,
            DetailItem,
            DetailItem.detailItemCode,
            length=9
        )

        detail = DetailItem(
            detailItemCode=detail_code,
            detailItemName="Opening Balance Equity",
            reportingItemCode=reporting.reportingItemCode,
            normalBalance="CREDIT",
            isActive=True
        )

        self.db.add(detail)
        await self.db.flush()

        return detail


    # ----------------------------------------------------
    # AUTO CREATE DETAIL ITEM
    # ----------------------------------------------------
    async def auto_create_detail_item(
        self,
        data: DetailItemAutoCreateRequest
    ) -> DetailItem:

        # 1. Mapping rule
        rule = ACCOUNT_MAPPING_RULES.get(data.accountType)
        if not rule:
            raise ValueError("Invalid account type")

        # 2. Open period
        open_period = await self.get_open_period()
        if not open_period:
            raise ValueError("No open accounting period found")

        # 3. Control Item (0001)
        control = await self.get_control_by_name(rule["control_name"])
        if not control:
            control_code = await NumericCodeGenerator.get_next_code(
                self.db,
                ControlItem,
                ControlItem.controlItemCode,
                length=4
            )

            control = ControlItem(
                controlItemCode=control_code,
                controlItemName=rule["control_name"],
                accountCategory=rule["category"],
                financialStatementType=rule["fs"],
                isActive=True
            )
            self.db.add(control)
            await self.db.flush()

        # 4. Reporting Item (000001)
        reporting = await self.get_reporting_by_name(
            data.accountType,
            control.controlItemCode
        )

        if not reporting:
            reporting_code = await NumericCodeGenerator.get_next_code(
                self.db,
                ReportingItem,
                ReportingItem.reportingItemCode,
                length=6
            )

            reporting = ReportingItem(
                reportingItemCode=reporting_code,
                reportingItemName=data.accountType,
                controlItemCode=control.controlItemCode
            )
            self.db.add(reporting)
            await self.db.flush()

        # 5. Duplicate check
        existing = await self.get_detail_by_name(data.detailItemName)
        if existing:
            raise ValueError("Detail Item already exists")

        # 6. Detail Item (000000001)
        detail_code = await NumericCodeGenerator.get_next_code(
            self.db,
            DetailItem,
            DetailItem.detailItemCode,
            length=9
        )

        detail = DetailItem(
            detailItemCode=detail_code,
            detailItemName=data.detailItemName,
            reportingItemCode=reporting.reportingItemCode,
            normalBalance=rule["normal_balance"],
            isActive=True,
            loadType=data.loadType
        )

        self.db.add(detail)
        await self.db.flush()

        # 7. Opening balance
        if data.openingBalance and Decimal(data.openingBalance) > 0:

            opening_equity = await self.get_opening_equity_account()
            if not opening_equity:
                opening_equity = await self.create_opening_equity_account()

            journal_header = JournalHeader(
                journalDate=open_period.periodStart,
                referenceNo=f"OPEN-{detail.detailItemCode}",
                description=f"Opening balance for {detail.detailItemName}",
                journalType="OPENING",
                periodID=open_period.periodID
            )

            self.db.add(journal_header)
            await self.db.flush()

            amount = Decimal(data.openingBalance)

            if detail.normalBalance == "DEBIT":
                debit_code = detail.detailItemCode
                credit_code = opening_equity.detailItemCode
            else:
                debit_code = opening_equity.detailItemCode
                credit_code = detail.detailItemCode

            self.db.add_all([
                JournalDetail(
                    journalHeaderID=journal_header.journalHeaderID,
                    detailItemCode=debit_code,
                    debitAmount=amount,
                    creditAmount=Decimal(0)
                ),
                JournalDetail(
                    journalHeaderID=journal_header.journalHeaderID,
                    detailItemCode=credit_code,
                    debitAmount=Decimal(0),
                    creditAmount=amount
                )
            ])

        return detail

