from fastapi import APIRouter, Depends
from fastapi import Body
from typing import List, Dict, Any
from src.services.bankaccount_service import IBankAccountService
from src.depends.service_depends import get_bank_account_service
from src.schemas.bankaccount_schema import BankAccountCreate, BankAccountRead
from src.models.bankaccount_model import BankAccount

router = APIRouter(prefix="/api/bankaccounts", tags=["BankAccounts"])

@router.post("/createBankAccount")
async def create_bank_account(
    payload: BankAccountCreate,
    service: IBankAccountService = Depends(get_bank_account_service)
):
    return await service.create_bank_account(payload)

# @router.post("/createBankAccount")
# async def create_bank_account(data: BankAccountCreate = Body(...)):
#     print(data)  # 👈 see parsed payload