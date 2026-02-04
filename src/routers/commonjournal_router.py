
from fastapi import APIRouter, Depends
from decimal import Decimal
from typing import List
from src.schemas.journal_schema import JournalCreate
from src.services.interfaces.icommonjournal_service import ICommonJournalService
from src.schemas.commonjournal_schema import JournalEntryRequest
from src.schemas.generaljournal_schema import JournalRequest
from src.depends.service_depends import get_commonjournal_service

router = APIRouter(prefix="/api/commonjournal", tags=["Common Journal Router"])

# @router.post("/createGeneralJournal")
# async def create_general_journal_entry(rows: List[dict],
#     service: ICommonJournalService = Depends(get_commonjournal_service)
# ):
#     await service.create_general_journal_entry(rows)
#     return {"message": "Journal saved successfully"}

@router.post("/createGeneralJournalEntry")
async def create_general_journal_entry(
    request: JournalRequest,
    service: ICommonJournalService = Depends(get_commonjournal_service)
):
    return await service.create_general_journal_entry(request)

@router.post("/journalForOpeningBankBalance")
async def create_opening_balance_journal(
    payload: JournalEntryRequest,
    service: ICommonJournalService = Depends(get_commonjournal_service)
):
    await service.create_opening_balance_journal(payload)
    return {"message": "Opening balance journal created successfully"}

@router.post("/journalForBankDeposit")
async def create_bank_deposit_journal(
    payload: JournalEntryRequest,
    service: ICommonJournalService = Depends(get_commonjournal_service)
):
    await service.create_bank_deposit_journal(payload)
    return {"message": "Bank Deposit journal created successfully"}

@router.post("/journalForBankWithdraw")
async def create_bank_withdraw_journal(
    payload: JournalEntryRequest,
    service: ICommonJournalService = Depends(get_commonjournal_service)
):
    await service.create_bank_withdraw_journal(payload)
    return {"message": "Bank Withdraw journal created successfully"}

@router.get("/nextControlItemCode", response_model=str)
async def get_next_code(
    service: ICommonJournalService = Depends(get_commonjournal_service),
):
    return await service.get_next_control_item_code()
