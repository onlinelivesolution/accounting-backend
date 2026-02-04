from fastapi import APIRouter, Depends, HTTPException, Body
from src.services.bankdeposit_service import IBankDepositService
from src.depends.service_depends import get_bank_deposit_service
from src.schemas.bankdeposit_schema import BankDepositCreate, BankDepositRead

router = APIRouter(prefix="/api/bankdeposits", tags=["BankDeposits"])

@router.post("/addNewBankDeposit", response_model=BankDepositRead)
async def add_bank_deposit(
    bankdeposit: BankDepositCreate,
    service: IBankDepositService = Depends(get_bank_deposit_service)
):
    return await service.add_bank_deposit(bankdeposit)

