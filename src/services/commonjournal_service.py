from datetime import datetime
from decimal import Decimal
from typing import List
from fastapi import HTTPException
from collections import defaultdict
from common.enum.commenum import DefaultAccount
from common.journal.journal_amount_resolver import JournalAmountResolver
from src.core.dynamic_account_resolver import DynamicAccountResolver
from src.services.interfaces.icommonjournal_service import ICommonJournalService
from src.repositories.interfaces.icommonjournal_repository import (
    ICommonJournalRepository,
)
from src.repositories.interfaces.iaccountingrule_repository import (
    IAccountingRuleRepository,
)

from sqlalchemy import select
from src.models.accountingperiod import AccountingPeriod
from src.models.journalheader_model import JournalHeader
from src.models.journaldetail_model import JournalDetail


class CommonJournalService(ICommonJournalService):

    def __init__(
        self,
        repository: ICommonJournalRepository,
        rule_repository: IAccountingRuleRepository,
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
            "activityCenterCode": await self.repository.get_default_activity_center(
                payload.companyCode
            ),
            "respCenterCode": await self.repository.get_default_resp_center(
                payload.companyCode
            ),
            "aBType": 1,
            "fiscalYear": await self.repository.get_current_fiscal_year(
                payload.companyCode
            ),
            "period": datetime.utcnow().month,
            "referenceNo": 1,
            "referenceID": payload.referenceID,
            "accountNumber": "000000",
            "createdBy": payload.createdBy,
            "projectCode": "DEFAULT",
        }

        # 🔹 Debit → Bank
        await self.repository.create_opening_balance_journal(
            {
                **common_fields,
                "controlItemCode": bank_h["controlItemCode"],
                "reportingItemCode": bank_h["reportingItemCode"],
                "detailItemCode": bank_h["detailItemCode"],
                "fAType": bank_h["fAType"],
                "debitAmount": amount,
                "creditAmount": 0,
            }
        )

        # 🔹 Credit → Capital
        await self.repository.create_opening_balance_journal(
            {
                **common_fields,
                "controlItemCode": cap_h["controlItemCode"],
                "reportingItemCode": cap_h["reportingItemCode"],
                "detailItemCode": cap_h["detailItemCode"],
                "fAType": cap_h["fAType"],
                "debitAmount": 0,
                "creditAmount": amount,
            }
        )

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
            "activityCenterCode": await self.repository.get_default_activity_center(
                payload.companyCode
            ),
            "respCenterCode": await self.repository.get_default_resp_center(
                payload.companyCode
            ),
            "aBType": 1,
            "fiscalYear": await self.repository.get_current_fiscal_year(
                payload.companyCode
            ),
            "period": datetime.utcnow().month,
            "referenceNo": 1,
            "referenceID": payload.referenceID,
            "accountNumber": "000000",
            "createdBy": payload.createdBy,
            "projectCode": "00",
        }

        # 🔹 Debit → Bank
        await self.repository.create_bank_deposit_journal(
            {
                **common_fields,
                "controlItemCode": bankAccount_h["controlItemCode"],
                "reportingItemCode": bankAccount_h["reportingItemCode"],
                "detailItemCode": bankAccount_h["detailItemCode"],
                "fAType": bankAccount_h["fAType"],
                "debitAmount": amount,
                "creditAmount": 0,
            }
        )

        # 🔹 Credit → Capital
        await self.repository.create_bank_deposit_journal(
            {
                **common_fields,
                "controlItemCode": cashAccount_h["controlItemCode"],
                "reportingItemCode": cashAccount_h["reportingItemCode"],
                "detailItemCode": cashAccount_h["detailItemCode"],
                "fAType": cashAccount_h["fAType"],
                "debitAmount": 0,
                "creditAmount": amount,
            }
        )

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
            "activityCenterCode": await self.repository.get_default_activity_center(
                payload.companyCode
            ),
            "respCenterCode": await self.repository.get_default_resp_center(
                payload.companyCode
            ),
            "aBType": 1,
            "fiscalYear": await self.repository.get_current_fiscal_year(
                payload.companyCode
            ),
            "period": datetime.utcnow().month,
            "referenceNo": 1,
            "referenceID": payload.referenceID,
            "accountNumber": "000000",
            "createdBy": payload.createdBy,
            "projectCode": "00",
        }

        # 🔹 Debit → Cash
        await self.repository.create_bank_withdraw_journal(
            {
                **common_fields,
                "controlItemCode": cashAccount_h["controlItemCode"],
                "reportingItemCode": cashAccount_h["reportingItemCode"],
                "detailItemCode": cashAccount_h["detailItemCode"],
                "fAType": cashAccount_h["fAType"],
                "debitAmount": amount,
                "creditAmount": 0,
            }
        )

        # 🔹 Credit → Bank
        await self.repository.create_bank_withdraw_journal(
            {
                **common_fields,
                "controlItemCode": bankAccount_h["controlItemCode"],
                "reportingItemCode": bankAccount_h["reportingItemCode"],
                "detailItemCode": bankAccount_h["detailItemCode"],
                "fAType": bankAccount_h["fAType"],
                "debitAmount": 0,
                "creditAmount": amount,
            }
        )

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
            select(AccountingPeriod).where(AccountingPeriod.isClosed == False)
        )
        return result.scalar_one_or_none()

    async def post_sales_invoice_journal(self, invoice):

        print("Company:", invoice.companyCode)
        print("Invoice Date:", invoice.salesInvoiceDate)

        period = await self.repository.get_period_by_date(
            invoice.companyCode,
            invoice.salesInvoiceDate,
        )

        print("Period:", period)

        if period is None:
            raise Exception(
                f"No accounting period found. "
                f"Company={invoice.companyCode}, "
                f"Date={invoice.salesInvoiceDate}"
            )

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
                fiscalYear=fiscal_year,
                periodID=periodID,
                createdDate=datetime.utcnow(),
            )

            # Use repository to insert header + details
            await self.repository.create_journal(header_obj, line_objs)



    # async def post_generate_salary_journal(self, salary):

    #     # ============================================================
    #     # 1. Get Accounting Period
    #     # ============================================================
    #     period = await self.repository.get_period_by_date(
    #         salary.companyCode,
    #         salary.createdDate,
    #     )

    #     if period is None:
    #         raise Exception(
    #             f"No accounting period found. "
    #             f"Company={salary.companyCode}, "
    #             f"Date={salary.createdDate}"
    #         )

    #     periodID = period.periodID
    #     fiscal_year = period.fiscalYear

    #     # ============================================================
    #     # 2. Get Accounting Rule
    #     # ============================================================
    #     rule = await self.rule_repository.get_rule(
    #         "SALARY_GENERATION"
    #     )
    #     print("==============================================")
    #     print("SALARY GENERATION JOURNAL DEBUG")
    #     print("Rule:", rule)

    #     if rule:
    #         print("Rule Code:", rule.ruleCode)
    #         print("Number of details:", len(rule.details))

    #         for d in rule.details:
    #             print(
    #                 "Rule Detail:",
    #                 "Account=", d.accountCode,
    #                 "Entry=", d.entryType,
    #                 "AmountSource=", d.amountSource,
    #                 "Dynamic=", d.isDynamicAccount,
    #             )

    #     print("==============================================")
    #     if not rule:
    #         raise Exception(
    #             "Accounting Rule 'SALARY_GENERATION' not configured"
    #         )

    #     # ============================================================
    #     # 3. Group Accounting Rule Details
    #     # ============================================================
    #     grouped = defaultdict(list)

    #     for detail in rule.details:
    #         grouped[detail.amountSource].append(detail)

    #     print("GROUPED AMOUNT SOURCES:")
    #     for source, details in grouped.items():
    #         print(
    #             "Source:",
    #             source,
    #             "Rules:",
    #             len(details)
    #         )
    #     # ============================================================
    #     # 4. Create ONE Journal Header
    #     # ============================================================
    #     header_obj = JournalHeader(
    #         journalDate=salary.createdDate,
    #         referenceNo=salary.salaryNo,
    #         description=(
    #             f"Salary Generation "
    #             f"{salary.month}/{salary.year}"
    #         ),
    #         journalType="GENERAL",
    #         fiscalYear=fiscal_year,
    #         periodID=periodID,
    #         createdDate=datetime.utcnow(),
    #     )

    #     # ============================================================
    #     # 5. All Journal Details
    #     # ============================================================
    #     line_objs = []

    #     # ============================================================
    #     # 6. Process Each Amount Source
    #     # ============================================================
    #     for amount_source, rule_details in grouped.items():

    #         # --------------------------------------------------------
    #         # Get amount from Salary / SalaryDetail
    #         # --------------------------------------------------------
    #         amount = JournalAmountResolver.get_amount(
    #             salary,
    #             amount_source,
    #         )

    #         print("==============================================")
    #         print("RESOLVER RESULT")
    #         print("Amount Source:", amount_source)
    #         print("Amount:", amount)
    #         print("Salary ID:", getattr(salary, "salaryID", None))
    #         print("Salary No:", getattr(salary, "salaryNo", None))
    #         print(
    #             "Salary Details:",
    #             len(getattr(salary, "salaryDetails", []) or [])
    #         )
    #         print("==============================================")
    #         amount = Decimal(str(amount or 0))

    #         print("--------------------------------")
    #         print("Amount Source :", amount_source)
    #         print("Amount        :", amount)
    #         print("--------------------------------")

    #         # --------------------------------------------------------
    #         # Skip zero amounts
    #         # --------------------------------------------------------
    #         if amount <= Decimal("0"):
    #             print(
    #                 f"Skipping '{amount_source}' "
    #                 f"because amount is zero."
    #             )
    #             continue

    #         pair_lines = []

    #         # ========================================================
    #         # 7. Create Debit/Credit Lines
    #         # ========================================================
    #         for detail in rule_details:

    #             # ----------------------------------------------------
    #             # Resolve Account
    #             # ----------------------------------------------------
    #             if detail.isDynamicAccount:

    #                 account_code = DynamicAccountResolver.resolve(
    #                     salary,
    #                     amount_source,
    #                 )

    #             else:

    #                 account_code = detail.accountCode

    #             print(
    #                 f"Amount Source : {amount_source}"
    #             )
    #             print(
    #                 f"Entry Type    : {detail.entryType}"
    #             )
    #             print(
    #                 f"Dynamic       : {detail.isDynamicAccount}"
    #             )
    #             print(
    #                 f"Account Code  : {account_code}"
    #             )

    #             if not account_code:
    #                 raise Exception(
    #                     f"No account configured for "
    #                     f"Amount Source '{amount_source}'"
    #                 )

    #             # ----------------------------------------------------
    #             # Debit / Credit
    #             # ----------------------------------------------------
    #             debit = (
    #                 amount
    #                 if detail.entryType.upper() == "DEBIT"
    #                 else Decimal("0")
    #             )

    #             credit = (
    #                 amount
    #                 if detail.entryType.upper() == "CREDIT"
    #                 else Decimal("0")
    #             )

    #             pair_lines.append(
    #                 JournalDetail(
    #                     journalType="GENERAL",
    #                     detailItemCode=str(account_code),
    #                     debitAmount=debit,
    #                     creditAmount=credit,
    #                     ratePercent=Decimal("0"),
    #                     narration=(
    #                         f"{salary.salaryNo} - "
    #                         f"{amount_source}"
    #                     ),
    #                     fiscalYear=fiscal_year,
    #                 )
    #             )

    #         # ========================================================
    #         # 8. Validate Individual Pair
    #         # ========================================================
    #         pair_debit = sum(
    #             Decimal(str(line.debitAmount or 0))
    #             for line in pair_lines
    #         )

    #         pair_credit = sum(
    #             Decimal(str(line.creditAmount or 0))
    #             for line in pair_lines
    #         )

    #         print(
    #             f"Pair -> {amount_source} | "
    #             f"Debit={pair_debit} | "
    #             f"Credit={pair_credit}"
    #         )

    #         if pair_debit != pair_credit:
    #             raise Exception(
    #                 f"Journal not balanced for "
    #                 f"'{amount_source}'. "
    #                 f"Debit={pair_debit}, "
    #                 f"Credit={pair_credit}"
    #             )

    #         # --------------------------------------------------------
    #         # Add pair to ONE journal
    #         # --------------------------------------------------------
    #         line_objs.extend(pair_lines)

    #     # ============================================================
    #     # 9. Make Sure Journal Has Lines
    #     # ============================================================
    #     if not line_objs:
    #         raise Exception(
    #             "No journal lines generated for salary generation."
    #         )

    #     # ============================================================
    #     # 10. Validate Whole Journal
    #     # ============================================================
    #     total_debit = sum(
    #         Decimal(str(line.debitAmount or 0))
    #         for line in line_objs
    #     )

    #     total_credit = sum(
    #         Decimal(str(line.creditAmount or 0))
    #         for line in line_objs
    #     )

    #     print("==============================")
    #     print("Salary Generation Journal")
    #     print("Total Debit :", total_debit)
    #     print("Total Credit:", total_credit)
    #     print("==============================")

    #     if total_debit != total_credit:
    #         raise Exception(
    #             f"Salary journal not balanced.\n"
    #             f"Debit : {total_debit}\n"
    #             f"Credit: {total_credit}"
    #         )

    #     # ============================================================
    #     # 11. Save ONE Header + ALL Details
    #     # ============================================================
    #     await self.repository.create_journal(
    #         header_obj,
    #         line_objs,
    #     )

    #     print(
    #         f"Salary generation journal created successfully. "
    #         f"Reference={salary.salaryNo}"
    #     )
    
    async def post_generate_salary_journal(self, salary):

        # ============================================
        # Get Accounting Period
        # ============================================

        period = await self.repository.get_period_by_date(
            salary.companyCode,
            salary.createdDate,
        )

        if period is None:
            raise Exception(
                f"No accounting period found. "
                f"Company={salary.companyCode}, "
                f"Date={salary.createdDate}"
            )

        # ============================================
        # Get Accounting Rule
        # ============================================

        rule = await self.rule_repository.get_rule(
            "SALARY_GENERATION"
        )

        if not rule:
            raise Exception(
                "Accounting Rule 'SALARY_GENERATION' not configured"
            )

        # ============================================
        # Debug Rule
        # ============================================

        print("==============================================")
        print("SALARY GENERATION JOURNAL")
        print("Rule Code:", rule.ruleCode)
        print("Rule Details:", len(rule.details))
        print("==============================================")

        for d in rule.details:

            print(
                "Account:",
                d.accountCode,
                "| Entry:",
                d.entryType,
                "| Source:",
                d.amountSource,
                "| Dynamic:",
                d.isDynamicAccount,
            )

        # ============================================
        # Group by Amount Source
        # ============================================

        grouped = defaultdict(list)

        for d in rule.details:

            if not d.amountSource:
                continue

            grouped[d.amountSource].append(d)

        # ============================================
        # Create ONE Journal Header
        # ============================================

        header_obj = JournalHeader(
            journalDate=salary.createdDate,
            referenceNo=salary.salaryNo,
            description=(
                f"Salary Generation "
                f"{salary.month}/{salary.year}"
            ),
            journalType="GENERAL",
            fiscalYear=period.fiscalYear,
            periodID=period.periodID,
            createdDate=datetime.utcnow(),
        )

        # ============================================
        # All Journal Lines
        # ============================================

        line_objs = []

        # ============================================
        # Process Amount Sources
        # ============================================

        for amount_source, details in grouped.items():

            amount = JournalAmountResolver.get_amount(
                salary,
                amount_source,
            )

            print("--------------------------------")
            print("Amount Source:", amount_source)
            print("Amount:", amount)
            print("Salary Detail Count:", len(salary.details))
            print("--------------------------------")

            if amount <= 0:
                continue

            pair_lines = []

            for d in details:

                # ====================================
                # Resolve Account
                # ====================================

                if d.isDynamicAccount:

                    account_code = DynamicAccountResolver.resolve(
                        salary,
                        amount_source,
                    )

                else:

                    account_code = d.accountCode

                print(
                    "Journal Line:",
                    amount_source,
                    "|",
                    d.entryType,
                    "|",
                    account_code
                )

                if not account_code:

                    raise Exception(
                        f"No account configured for "
                        f"Amount Source '{amount_source}'"
                    )

                # ====================================
                # Debit / Credit
                # ====================================

                debit = (
                    amount
                    if d.entryType.upper() == "DEBIT"
                    else Decimal("0")
                )

                credit = (
                    amount
                    if d.entryType.upper() == "CREDIT"
                    else Decimal("0")
                )

                pair_lines.append(
                    JournalDetail(
                        journalType="GENERAL",
                        detailItemCode=account_code,
                        debitAmount=debit,
                        creditAmount=credit,
                        narration=(
                            f"{salary.salaryNo} - "
                            f"{amount_source}"
                        ),
                        fiscalYear=period.fiscalYear,
                    )
                )

            # ============================================
            # Validate Pair
            # ============================================

            pair_debit = sum(
                Decimal(str(x.debitAmount or 0))
                for x in pair_lines
            )

            pair_credit = sum(
                Decimal(str(x.creditAmount or 0))
                for x in pair_lines
            )

            print(
                f"Pair {amount_source}: "
                f"Debit={pair_debit}, "
                f"Credit={pair_credit}"
            )

            if round(pair_debit, 2) != round(pair_credit, 2):

                raise Exception(
                    f"Journal not balanced for "
                    f"'{amount_source}'. "
                    f"Debit={pair_debit}, "
                    f"Credit={pair_credit}"
                )

            # ============================================
            # Add to ONE Journal
            # ============================================

            line_objs.extend(pair_lines)

        # ============================================
        # Validate Whole Journal
        # ============================================

        total_debit = sum(
            Decimal(str(x.debitAmount or 0))
            for x in line_objs
        )

        total_credit = sum(
            Decimal(str(x.creditAmount or 0))
            for x in line_objs
        )

        print("==============================================")
        print("TOTAL SALARY JOURNAL")
        print("Debit :", total_debit)
        print("Credit:", total_credit)
        print("Lines :", len(line_objs))
        print("==============================================")

        if not line_objs:

            raise Exception(
                "No journal lines generated for salary generation."
            )

        if round(total_debit, 2) != round(total_credit, 2):

            raise Exception(
                f"Salary journal not balanced. "
                f"Debit={total_debit}, "
                f"Credit={total_credit}"
            )

        # ============================================
        # Save ONE Journal Header + ALL Details
        # ============================================

        await self.repository.create_journal(
            header_obj,
            line_objs,
        )
    
    async def post_salary_payment_journal(self, payment):

        # ============================================
        # Get Accounting Period
        # ============================================
        period = await self.repository.get_period_by_date(
            payment.companyCode,
            payment.paymentDate,
        )

        if period is None:
            raise Exception(
                f"No accounting period found. "
                f"Company={payment.companyCode}, "
                f"Date={payment.paymentDate}"
            )

        # ============================================
        # Get Accounting Rule
        # ============================================
        rule = await self.rule_repository.get_rule("SALARY_PAYMENT")

        if not rule:
            raise Exception("Accounting Rule 'SALARY_PAYMENT' not configured")

        # ============================================
        # Group Rule Details
        # ============================================
        grouped = defaultdict(list)

        for d in rule.details:
            grouped[d.amountSource].append(d)

        # ============================================
        # Create ONE Journal Header
        # ============================================
        header_obj = JournalHeader(
            journalDate=payment.paymentDate,
            referenceNo=payment.paymentNo,
            description=f"Salary Payment {payment.salaryMonth}/{payment.salaryYear}",
            journalType="GENERAL",
            fiscalYear=period.fiscalYear,
            periodID=period.periodID,
            createdDate=datetime.utcnow(),
        )

        # ============================================
        # All Journal Details
        # ============================================
        line_objs = []

        # ============================================
        # Process Every Amount Source
        # ============================================
        for amount_source, details in grouped.items():

            amount = JournalAmountResolver.get_amount(
                payment,
                amount_source,
            )

            print("--------------------------------")
            print("Amount Source :", amount_source)
            print("Amount        :", amount)
            print("--------------------------------")

            if amount <= 0:
                continue

            pair_lines = []

            for d in details:

                # -----------------------------
                # Resolve Account
                # -----------------------------
                if d.isDynamicAccount:
                    account_code = DynamicAccountResolver.resolve(
                        payment,
                        amount_source,
                    )
                else:
                    account_code = d.accountCode

                print(
                    f"{amount_source} | "
                    f"{d.entryType} | "
                    f"Dynamic={d.isDynamicAccount} | "
                    f"Account={account_code}"
                )

                if not account_code:
                    raise Exception(
                        f"No account configured for Amount Source '{amount_source}'"
                    )

                debit = amount if d.entryType.upper() == "DEBIT" else 0
                credit = amount if d.entryType.upper() == "CREDIT" else 0

                pair_lines.append(
                    JournalDetail(
                        journalType="GENERAL",
                        detailItemCode=account_code,
                        debitAmount=debit,
                        creditAmount=credit,
                        narration=f"{payment.paymentNo} - {amount_source}",
                        fiscalYear=period.fiscalYear,
                    )
                )

            # ============================================
            # Validate THIS pair
            # ============================================
            pair_debit = sum(float(x.debitAmount) for x in pair_lines)
            pair_credit = sum(float(x.creditAmount) for x in pair_lines)

            print(
                f"Pair -> {amount_source} | "
                f"Debit={pair_debit} | "
                f"Credit={pair_credit}"
            )

            if round(pair_debit, 2) != round(pair_credit, 2):
                raise Exception(
                    f"Journal not balanced for '{amount_source}'. "
                    f"Debit={pair_debit}, Credit={pair_credit}"
                )

            # IMPORTANT
            line_objs.extend(pair_lines)

        # ============================================
        # Validate Whole Journal
        # ============================================
        total_debit = sum(float(x.debitAmount) for x in line_objs)
        total_credit = sum(float(x.creditAmount) for x in line_objs)

        print("==============================")
        print("Total Debit :", total_debit)
        print("Total Credit:", total_credit)
        print("==============================")

        if round(total_debit, 2) != round(total_credit, 2):
            raise Exception(
                f"Salary journal not balanced.\n"
                f"Debit : {total_debit}\n"
                f"Credit: {total_credit}"
            )

        if not line_objs:
            raise Exception("No journal lines generated.")

        # ============================================
        # Save Journal
        # ============================================
        await self.repository.create_journal(
            header_obj,
            line_objs,
        )

    async def post_customer_receipt_journal(self, receipt, request):

        # ✅ Get period
        period = await self.repository.get_period_by_date(
            receipt.companyCode, receipt.receiptDate
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
        total_paid = (
            sum(d.paidAmount for d in request.details) if request.details else 0
        )
        total_discount = (
            sum(d.discountAmount for d in request.details) if request.details else 0
        )
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
