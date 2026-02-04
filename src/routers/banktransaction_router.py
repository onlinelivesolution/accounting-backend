from fastapi import APIRouter, Depends
from src.schemas.banktransaction_schema import BankTransactionRequest
from src.services.interfaces.ibanktransaction_service import IBankTransactionService
from src.depends.service_depends import get_bank_transaction_service
from common.enum.commenum import DefaultPaymentMethod
from fastapi import Request

router = APIRouter(prefix="/api/banktransactions", tags=["Bank Transactions"])

@router.get("/getAccountBalance/{detail_item_code}")
async def get_account_balance(
    detail_item_code: str,
    service: IBankTransactionService = Depends(get_bank_transaction_service)
):
    return await service.get_account_balance(detail_item_code)

@router.post("/createBankTransaction")
async def create_transaction(
    request: BankTransactionRequest,
    service: IBankTransactionService = Depends(get_bank_transaction_service),
):
    return await service.create_transaction(request)

@router.get("/loadDefaultPaymentMethods")
def get_all_payment_methods():
    return [{"id": item.value, "name": item.name.replace("_", " ").title()} for item in DefaultPaymentMethod]
