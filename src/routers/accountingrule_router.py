from fastapi import APIRouter, Depends
from src.services.interfaces.iaccountingrule_service import IAccountingRuleService
from src.depends.service_depends import get_accounting_rule_service
from src.schemas.accountingsetting_schema import AccountingRuleCreateRequest

router = APIRouter(prefix="/api/accounting-rules")

@router.get("/{ruleCode}")
async def get_rule(
    ruleCode: str,
    service: IAccountingRuleService = Depends(get_accounting_rule_service)
):

    return await service.get_rule(ruleCode)

@router.post("/createAccountingRule")
async def create_accounting_rule(
    request: AccountingRuleCreateRequest,
    service: IAccountingRuleService = Depends(get_accounting_rule_service)
):
    result = await service.create_accounting_rule(request)
    return {
        "message": "Accounting rule created successfully",
        "data": result
    }