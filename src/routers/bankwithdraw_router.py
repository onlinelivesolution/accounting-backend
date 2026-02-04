from fastapi import APIRouter, Depends, HTTPException, Body
from src.services.bankwithdraw_service import IBankWithdrawService
from src.depends.service_depends import get_bank_withdraw_service
from src.schemas.bankwithdraw_schema import BankWithdrawCreate, BankWithdrawRead

router = APIRouter(prefix="/api/bankwithdraws", tags=["BankWithdraws"])

@router.post("/addNewBankWithdraw", response_model=BankWithdrawRead)
async def add_bank_withdraw(
    bankwithdraw: BankWithdrawCreate,
    service: IBankWithdrawService = Depends(get_bank_withdraw_service)
):
    return await service.add_bank_withdraw(bankwithdraw)

