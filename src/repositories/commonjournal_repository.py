from common.generic.generic_repository import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal
from datetime import datetime
from src.models.controlitem import ControlItem
from src.models.vataccountmapping import VatAccountMapping
from src.models.journal_model import Journal
from src.models.journalheader_model import JournalHeader
from src.models.journaldetail_model import JournalDetail
from src.models.accountingperiod import AccountingPeriod
from src.models.controlitem import ControlItem
from src.models.reportingitem import ReportingItem
from src.models.detailitem import DetailItem
from sqlalchemy import select, func, cast, Integer
from src.models.activitycenter import ActivityCenter
from src.models.responsibilitycenter import ResponsibilityCenter
from src.schemas.journal_schema import JournalCreate
from src.repositories.interfaces.icommonjournal_repository import ICommonJournalRepository
from common.enum.commenum import DefaultAccount
from src.repositories.interfaces.icommonjournal_repository import ICommonJournalRepository
VAT_INPUT_ACCOUNT_CODE = "VAT_INPUT"

class CommonJournalRepository(GenericRepository[Journal], ICommonJournalRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Journal, db)
    
    # async def _get_open_period(self) -> AccountingPeriod | None:
    #     result = await self.db.execute(
    #         select(AccountingPeriod)
    #         .where(AccountingPeriod.isClosed == False)
    #         .order_by(AccountingPeriod.periodStart.desc())
    #     )
    #     return result.scalars().first()
    
    async def get_vat_detail_item(
        self,
        vat_type: str,
        company_code: str
    ):
        result = await self.db.execute(
            select(VatAccountMapping.detailItemCode)
            .where(
                VatAccountMapping.vatType == vat_type,
                VatAccountMapping.companyCode == company_code,
                VatAccountMapping.isActive == True
            )
        )
        return result.scalar_one_or_none()
    
    async def _get_open_period(self):
        result = await self.db.execute(
            select(AccountingPeriod)
            .where(AccountingPeriod.isClosed == False)
        )
        return result.scalar_one_or_none()
    

    async def get_detail_item_by_account_id(self, account_id: int) -> str:
        result = await self.db.execute(
            select(DetailItem.detailItemCode)
            .where(DetailItem.accountID == account_id)
            .limit(1)
        )
        return result.scalar_one()
    
    async def get_bank_detail_item_by_account_id(self, account_id: int) -> str:
        result = await self.db.execute(
            select(DetailItem.detailItemCode)
            .where(DetailItem.accountID == account_id)
            .limit(1)
        )
        return result.scalar_one()

    async def resolve_detail_hierarchy(self, detail_item_code: str) -> dict:
        result = await self.db.execute(
            select(
                DetailItem.detailItemCode,
                ReportingItem.reportingItemCode,
                ControlItem.controlItemCode,
                ControlItem.fATypeID
            )
            .join(ReportingItem, DetailItem.reportingItemCode == ReportingItem.reportingItemCode)
            .join(ControlItem, ReportingItem.controlItemCode == ControlItem.controlItemCode)
            .where(DetailItem.detailItemCode == detail_item_code)
        )
        row = result.one()

        return {
            "detailItemCode": row.detailItemCode,
            "reportingItemCode": row.reportingItemCode,
            "controlItemCode": row.controlItemCode,
            "fAType": row.fATypeID,
        }

    async def get_default_activity_center(self, company_code: str) -> str:
        result = await self.db.execute(
            select(ActivityCenter.activityCenterCode)
            .where(ActivityCenter.companyCode == company_code)
            .order_by(ActivityCenter.activityCenterCode)
            .limit(1)
        )
        return result.scalar_one()

    async def get_default_resp_center(self, company_code: str) -> str:
        result = await self.db.execute(
            select(ResponsibilityCenter.respCenterCode)
            .order_by(ResponsibilityCenter.respCenterCode)
            .limit(1)
        )
        return result.scalar_one()

    async def get_current_fiscal_year(self, company_code: str) -> int:
        return 2025  # or fetch dynamically

    async def create_opening_balance_journal(self, data: dict):
        journal = Journal(**data)
        self.db.add(journal)
        await self.db.flush()
    
    async def create_opening_balance(self, data: dict):
        journaldetail = JournalDetail(**data)
        self.db.add(journaldetail)
        await self.db.flush()
        
    async def create_bank_deposit_journal(self, data: dict):
        journal = Journal(**data)
        self.db.add(journal)
        await self.db.flush()
        
    async def create_bank_withdraw_journal(self, data: dict):
        journal = Journal(**data)
        self.db.add(journal)
        await self.db.flush()
        
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
    


    async def create_general_journal_entry(self, request):

<<<<<<< HEAD
        # 1. Get Open Accounting Period
=======
        # 1. Open period
>>>>>>> 0f121b107816857e7182c1b406799352dfa9c23d
        period = await self._get_open_period()
        if not period:
            raise ValueError("No open accounting period found")

<<<<<<< HEAD
        fiscal_year = period.fiscalYear
        company_code = period.companyCode

=======
>>>>>>> 0f121b107816857e7182c1b406799352dfa9c23d
        # 2. Journal Header
        header = JournalHeader(
            journalDate=request.journalDate,
            journalType=request.journalType,
            referenceNo=request.referenceNo,
            description=request.description,
            periodID=period.periodID,
            fiscalYear=fiscal_year,
            createdDate=datetime.utcnow()
        )

        self.db.add(header)
        await self.db.flush()
<<<<<<< HEAD
        
        vat_detail_item = await self.get_vat_detail_item("INPUT", company_code)
=======
>>>>>>> 0f121b107816857e7182c1b406799352dfa9c23d

        # 3. Journal Details
        for row in request.details:
            base_amount = Decimal(row.amount)
            vat_rate = Decimal(row.vatRate or 0)
            vat_amount = (base_amount * vat_rate / 100).quantize(Decimal("0.01"))
            total_amount = base_amount + vat_amount

<<<<<<< HEAD
            # Debit (Expense)
=======
            # Expense / Debit
>>>>>>> 0f121b107816857e7182c1b406799352dfa9c23d
            self.db.add(
                JournalDetail(
                    journalHeaderID=header.journalHeaderID,
                    detailItemCode=row.debitItemCode,
                    debitAmount=base_amount,
                    creditAmount=Decimal(0),
<<<<<<< HEAD
                    narration=row.narration,
                    vatRate=vat_rate,
                    fiscalYear=fiscal_year
                )
            )

            # VAT Line (Optional)
            if vat_amount > 0:
                
                if not vat_detail_item:
                   raise ValueError("VAT Input account is not configured")
               
                self.db.add(
                    JournalDetail(
                        journalHeaderID=header.journalHeaderID,
                        detailItemCode = vat_detail_item,
                        debitAmount=vat_amount,
                        creditAmount=Decimal(0),
                        narration="VAT Input",
                        vatRate=vat_rate,
                        fiscalYear=fiscal_year
=======
                    narration=row.narration
                )
            )

            # VAT line (optional)
            if vat_amount > 0:
                self.db.add(
                    JournalDetail(
                        journalHeaderID=header.journalHeaderID,
                        detailItemCode=VAT_INPUT_ACCOUNT_CODE,
                        debitAmount=vat_amount,
                        creditAmount=Decimal(0),
                        narration="VAT Input"
>>>>>>> 0f121b107816857e7182c1b406799352dfa9c23d
                    )
                )

            # Credit (Cash / Bank / Payable)
            self.db.add(
                JournalDetail(
                    journalHeaderID=header.journalHeaderID,
                    detailItemCode=row.creditItemCode,
                    debitAmount=Decimal(0),
                    creditAmount=total_amount,
<<<<<<< HEAD
                    narration=row.narration,
                    fiscalYear=fiscal_year
=======
                    narration=row.narration
>>>>>>> 0f121b107816857e7182c1b406799352dfa9c23d
                )
            )

        await self.db.commit()
<<<<<<< HEAD
        return header

    
    # async def create_general_journal_entry(self, request):

    #     # 1. Open period
    #     period = await self._get_open_period()
    #     if not period:
    #         raise ValueError("No open accounting period found")

    #     # 2. Journal Header
    #     header = JournalHeader(
    #         journalDate=request.journalDate,
    #         journalType=request.journalType,
    #         referenceNo=request.referenceNo,
    #         description=request.description,
    #         periodID=period.periodID
    #     )

    #     self.db.add(header)
    #     await self.db.flush()

    #     # 3. Journal Details
    #     for row in request.details:
    #         base_amount = Decimal(row.amount)
    #         vat_rate = Decimal(row.vatRate or 0)
    #         vat_amount = (base_amount * vat_rate / 100).quantize(Decimal("0.01"))
    #         total_amount = base_amount + vat_amount

    #         # Expense / Debit
    #         self.db.add(
    #             JournalDetail(
    #                 journalHeaderID=header.journalHeaderID,
    #                 detailItemCode=row.debitItemCode,
    #                 debitAmount=base_amount,
    #                 creditAmount=Decimal(0),
    #                 narration=row.narration,
    #                 fiscalYear=row.fiscalYear
    #             )
    #         )

    #         # VAT line (optional)
    #         if vat_amount > 0:
    #             self.db.add(
    #                 JournalDetail(
    #                     journalHeaderID=header.journalHeaderID,
    #                     detailItemCode=VAT_INPUT_ACCOUNT_CODE,
    #                     debitAmount=vat_amount,
    #                     creditAmount=Decimal(0),
    #                     narration="VAT Input",
    #                     vatRate=row.vatRate,
    #                     fiscalYear=row.fiscalYear
    #                 )
    #             )

    #         # Credit (Cash / Bank / Payable)
    #         self.db.add(
    #             JournalDetail(
    #                 journalHeaderID=header.journalHeaderID,
    #                 detailItemCode=row.creditItemCode,
    #                 debitAmount=Decimal(0),
    #                 creditAmount=total_amount,
    #                 narration=row.narration,
    #                 fiscalYear=row.fiscalYear
    #             )
    #         )

    #     await self.db.commit()
    #     return header
=======
        return header
>>>>>>> 0f121b107816857e7182c1b406799352dfa9c23d
