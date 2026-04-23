from datetime import datetime
from decimal import Decimal
from typing import List
from fastapi import HTTPException
from collections import defaultdict
from common.enum.commenum import DefaultAccount
from src.services.interfaces.icommonjournal_service import ICommonJournalService
from src.repositories.interfaces.icommonjournal_repository import ICommonJournalRepository
from src.repositories.interfaces.iaccountingrule_repository import IAccountingRuleRepository
from sqlalchemy import select
from src.models.accountingperiod import AccountingPeriod
from src.models.journalheader_model import JournalHeader
from src.models.journaldetail_model import JournalDetail

class CommonJournalService(ICommonJournalService):

    def __init__(
        self,
        repository: ICommonJournalRepository,
        rule_repository: IAccountingRuleRepository
    ):
        self.repository = repository
        self.rule_repository = rule_repository
    
    async def create_general_journal_entry(self, request):
        if not request.details:
            raise ValueError("Journal details are required")

        for row in request.details:
            if not row.debitItemCode or not row.creditItemCode or not row.amount:
                raise ValueError("Debit, Credit and Amount are required")

            if row.debitItemCode == row.creditItemCode:
                raise ValueError("Debit and Credit account cannot be same")

            if row.ratePercent and row.ratePercent not in (5, 10, 15):
                raise ValueError("Invalid VAT rate")

        return await self.repository.create_general_journal_entry(request)

        
    async def create_opening_balance_journal(self, payload):

        amount = payload.amount
        if amount <= 0:
            return

        bank_detail_code = await self.repository.get_detail_item_by_account_id(
            payload.accountID
        )

        capital_detail_code = await self.repository.get_detail_item_by_account_id(
            DefaultAccount.Capital.value
        )

        bank_h = await self.repository.resolve_detail_hierarchy(bank_detail_code)
        cap_h = await self.repository.resolve_detail_hierarchy(capital_detail_code)

        common_fields = {
            "journalDate": datetime.utcnow(),
            "companyCode": payload.companyCode,
            "activityCenterCode": await self.repository.get_default_activity_center(payload.companyCode),
            "respCenterCode": await self.repository.get_default_resp_center(payload.companyCode),
            "aBType": 1,
            "fiscalYear": await self.repository.get_current_fiscal_year(payload.companyCode),
            "period": datetime.utcnow().month,
            "referenceNo": 1,
            "referenceID": payload.referenceID,
            "accountNumber": "000000",
            "createdBy": payload.createdBy,
            "projectCode": "DEFAULT",
        }

        # 🔹 Debit → Bank
        await self.repository.create_opening_balance_journal({
            **common_fields,
            "controlItemCode": bank_h["controlItemCode"],
            "reportingItemCode": bank_h["reportingItemCode"],
            "detailItemCode": bank_h["detailItemCode"],
            "fAType": bank_h["fAType"],
            "debitAmount": amount,
            "creditAmount": 0,
        })

        # 🔹 Credit → Capital
        await self.repository.create_opening_balance_journal({
            **common_fields,
            "controlItemCode": cap_h["controlItemCode"],
            "reportingItemCode": cap_h["reportingItemCode"],
            "detailItemCode": cap_h["detailItemCode"],
            "fAType": cap_h["fAType"],
            "debitAmount": 0,
            "creditAmount": amount,
        })

        # ✅ THIS IS THE FIX
        await self.repository.db.commit()
    
    
    # Bank deposit journal entry
    async def create_bank_deposit_journal(self, payload):

        amount = payload.amount
        if amount <= 0:
            return

        bank_detail_code = await self.repository.get_detail_item_by_account_id(
            payload.accountID
        )

        cash_detail_code = await self.repository.get_detail_item_by_account_id(
            DefaultAccount.CashOnHand.value
        )

        bankAccount_h = await self.repository.resolve_detail_hierarchy(bank_detail_code)
        cashAccount_h = await self.repository.resolve_detail_hierarchy(cash_detail_code)

        common_fields = {
            "journalDate": datetime.utcnow(),
            "companyCode": payload.companyCode,
            "activityCenterCode": await self.repository.get_default_activity_center(payload.companyCode),
            "respCenterCode": await self.repository.get_default_resp_center(payload.companyCode),
            "aBType": 1,
            "fiscalYear": await self.repository.get_current_fiscal_year(payload.companyCode),
            "period": datetime.utcnow().month,
            "referenceNo": 1,
            "referenceID": payload.referenceID,
            "accountNumber": "000000",
            "createdBy": payload.createdBy,
            "projectCode": "00",
        }

        # 🔹 Debit → Bank
        await self.repository.create_bank_deposit_journal({
            **common_fields,
            "controlItemCode": bankAccount_h["controlItemCode"],
            "reportingItemCode": bankAccount_h["reportingItemCode"],
            "detailItemCode": bankAccount_h["detailItemCode"],
            "fAType": bankAccount_h["fAType"],
            "debitAmount": amount,
            "creditAmount": 0,
        })

        # 🔹 Credit → Capital
        await self.repository.create_bank_deposit_journal({
            **common_fields,
            "controlItemCode": cashAccount_h["controlItemCode"],
            "reportingItemCode": cashAccount_h["reportingItemCode"],
            "detailItemCode": cashAccount_h["detailItemCode"],
            "fAType": cashAccount_h["fAType"],
            "debitAmount": 0,
            "creditAmount": amount,
        })

        # ✅ THIS IS THE FIX
        await self.repository.db.commit()
    
    # Bank withdraw journal entry
    async def create_bank_withdraw_journal(self, payload):

        amount = payload.amount
        if amount <= 0:
            return

        bank_detail_code = await self.repository.get_detail_item_by_account_id(
            DefaultAccount.Bank.value
        )

        cash_detail_code = await self.repository.get_detail_item_by_account_id(
            DefaultAccount.CashOnHand.value
        )

        bankAccount_h = await self.repository.resolve_detail_hierarchy(bank_detail_code)
        cashAccount_h = await self.repository.resolve_detail_hierarchy(cash_detail_code)

        common_fields = {
            "journalDate": datetime.utcnow(),
            "companyCode": payload.companyCode,
            "activityCenterCode": await self.repository.get_default_activity_center(payload.companyCode),
            "respCenterCode": await self.repository.get_default_resp_center(payload.companyCode),
            "aBType": 1,
            "fiscalYear": await self.repository.get_current_fiscal_year(payload.companyCode),
            "period": datetime.utcnow().month,
            "referenceNo": 1,
            "referenceID": payload.referenceID,
            "accountNumber": "000000",
            "createdBy": payload.createdBy,
            "projectCode": "00",
        }

        # 🔹 Debit → Cash
        await self.repository.create_bank_withdraw_journal({
            **common_fields,
            "controlItemCode": cashAccount_h["controlItemCode"],
            "reportingItemCode": cashAccount_h["reportingItemCode"],
            "detailItemCode": cashAccount_h["detailItemCode"],
            "fAType": cashAccount_h["fAType"],
            "debitAmount": amount,
            "creditAmount": 0,
        })

        # 🔹 Credit → Bank
        await self.repository.create_bank_withdraw_journal({
            **common_fields,
            "controlItemCode": bankAccount_h["controlItemCode"],
            "reportingItemCode": bankAccount_h["reportingItemCode"],
            "detailItemCode": bankAccount_h["detailItemCode"],
            "fAType": bankAccount_h["fAType"],
            "debitAmount": 0,
            "creditAmount": amount,
        })

        # ✅ THIS IS THE FIX
        await self.repository.db.commit()
        
    async def get_next_control_item_code(self) -> str:
        return await self.repository.get_next_control_item_code()
    
    async def create_opening_balance(self, data):
        raise NotImplementedError("Opening balance not implemented yet")
    
    async def post_journal(self, header, lines):
        """
        Inserts journal header and all detail lines into the database.
        """
        # Save the header first
        self.repository.db.add(header)
        await self.repository.db.flush()  # flush to get journalHeaderID

        # Add details
        for line in lines:
            line.journalHeaderID = header.journalHeaderID
            self.repository.db.add(line)

        # Commit all
        await self.repository.db.commit()
        return header
    
    async def _get_open_period(self):
        result = await self.db.execute(
            select(AccountingPeriod)
            .where(AccountingPeriod.isClosed == False)
        )
        return result.scalar_one_or_none()

    async def post_sales_invoice_journal(self, invoice):
   
        period = await self.repository.get_period_by_date(
        invoice.companyCode,
        invoice.salesInvoiceDate
        )

        if not period:
            raise Exception("No accounting period found for this date")

        periodID = period.periodID
        fiscal_year = period.fiscalYear
        
        rule = await self.rule_repository.get_rule("SALES_INVOICE")
        if not rule:
            raise Exception("Rule not configured")

        from collections import defaultdict
        grouped = defaultdict(list)
        for d in rule.details:
            grouped[d.amountSource].append(d)

        for amount_source, details in grouped.items():
            amount = getattr(invoice, amount_source, 0) or 0
            if amount == 0:
                continue

            line_objs = []
            for d in details:
                debit = amount if d.entryType.upper() == "DEBIT" else 0
                credit = amount if d.entryType.upper() == "CREDIT" else 0
                line_objs.append(
                    JournalDetail(
                        journalType="GENERAL",
                        detailItemCode=d.accountCode,
                        debitAmount=debit,
                        creditAmount=credit,
                        narration=f"{invoice.salesInvoiceNo} - {amount_source}",
                        fiscalYear=fiscal_year,
                    )
                )

            total_debit = sum(l.debitAmount for l in line_objs)
            total_credit = sum(l.creditAmount for l in line_objs)
            if round(total_debit, 2) != round(total_credit, 2):
                raise Exception(f"Journal not balanced for {amount_source}")

            header_obj = JournalHeader(
                journalDate=datetime.utcnow(),
                referenceNo=f"{invoice.salesInvoiceNo}-{amount_source}",
                description=f"Sales Invoice ({amount_source})",
                journalType="GENERAL",
                fiscalYear= fiscal_year,
                periodID=periodID,
                createdDate= datetime.utcnow(),
            )

            # Use repository to insert header + details
            await self.repository.create_journal(header_obj, line_objs)
    
    async def post_customer_receipt_journal(self, receipt, request):

        # ✅ Get period
        period = await self.repository.get_period_by_date(
            receipt.companyCode,
            receipt.receiptDate
        )

        if not period:
            raise Exception("No accounting period found for this date")

        periodID = period.periodID
        fiscal_year = period.fiscalYear

        # ✅ Get rule
        rule = await self.rule_repository.get_rule("CUSTOMER_RECEIPT")
        if not rule:
            raise Exception("Rule not configured")

        # ✅ Calculate amounts
        total_paid = sum(d.paidAmount for d in request.details) if request.details else 0
        total_discount = sum(d.discountAmount for d in request.details) if request.details else 0
        total_applied = total_paid + total_discount
        total_unallocated = receipt.unallocatedAmount or 0

        # 👉 attach dynamic values
        receipt.totalPaid = total_paid
        receipt.totalDiscount = total_discount
        receipt.totalApplied = total_applied
        receipt.totalUnallocated = total_unallocated

        # ✅ Group rules
        grouped = defaultdict(list)
        for d in rule.details:
            grouped[d.amountSource].append(d)

        # =========================================================
        # 🔥 Loop per amount source (same as your invoice logic)
        # =========================================================
        for amount_source, details in grouped.items():

            amount = getattr(receipt, amount_source, 0) or 0

            if amount == 0:
                continue

            line_objs = []

            for d in details:
                debit = amount if d.entryType.upper() == "DEBIT" else 0
                credit = amount if d.entryType.upper() == "CREDIT" else 0
                
                account_code = d.accountCode

                # # ✅ Override for Cash/Bank account
                if not account_code:
                    account_code = request.accountID

                # ✅ Dynamic account handling
                if d.isDynamicAccount:
                    if not request.accountID:
                        raise Exception("Payment account is required")
                    account_code = request.accountID
                else:
                    account_code = d.accountCode

                line_objs.append(
                    JournalDetail(
                        journalType="GENERAL",
                        detailItemCode=account_code,
                        debitAmount=debit,
                        creditAmount=credit,
                        narration=f"{receipt.receiptNo} - {amount_source}",
                        fiscalYear=fiscal_year,
                    )
                )

            # ✅ Balance check
            total_debit = sum(l.debitAmount for l in line_objs)
            total_credit = sum(l.creditAmount for l in line_objs)

            if round(total_debit, 2) != round(total_credit, 2):
                raise Exception(f"Journal not balanced for {amount_source}")

            # ✅ Header
            header_obj = JournalHeader(
                journalDate=receipt.receiptDate,
                referenceNo=f"{receipt.receiptNo}-{amount_source}",
                description=f"Customer Receipt ({amount_source})",
                journalType="GENERAL",
                fiscalYear=fiscal_year,
                periodID=periodID,
                createdDate=datetime.utcnow(),
            )

            # ✅ Save via repository (same pattern)
            await self.repository.create_journal(header_obj, line_objs)