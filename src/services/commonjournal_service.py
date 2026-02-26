from datetime import datetime
from decimal import Decimal
from typing import List
from fastapi import HTTPException
from common.enum.commenum import DefaultAccount
from src.services.interfaces.icommonjournal_service import ICommonJournalService
from src.repositories.interfaces.icommonjournal_repository import ICommonJournalRepository


class CommonJournalService(ICommonJournalService):

    def __init__(self, repository: ICommonJournalRepository):
        self.repository = repository
    
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