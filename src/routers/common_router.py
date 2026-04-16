# src/routers/reportingitem_router.py
from fastapi import APIRouter, Depends
from common.enum.commenum import DefaultAccount
from common.enum.commenum import AdvanceOrDueAccounts
from common.enum.commenum import BankAccountType
from common.enum.commenum import BankDepositType
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.dto.bankdropdown import BankDropdown
from src.schemas.country_schemas import CountryDropdown
from src.schemas.controlitem_schema import ControlItemDropdown
from src.schemas.company_schema import CompanyDropdown
from src.schemas.bankaccount_schema import BankAccountDropdown
from src.schemas.branch_schema import BranchDropdown
from src.services.interfaces.icommon_service import ICommonService
from src.dto.companydto import CompanyDTO
from src.dto.activitycenterdto import ActivityCenterDTO
from src.dto.responsibilitycenterdto import ResponsibilityCenterDTO
from src.schemas.detailitem_schema import DetailItemDropdown
from src.depends.service_depends import get_common_service
from common.enum.commenum import LoadType
from typing import List, Dict

router = APIRouter(prefix="/api/common", tags=["Common Router"])

@router.get("/loadDetailItems", response_model=List[Dict])
async def load_detail_items(
    service: ICommonService = Depends(get_common_service)
):
    return await service.get_detail_items()

@router.get(
    "/loadBankOrCashAccount",
    response_model=List[DetailItemDropdown]
)
async def get_bank_cash_detailitems(
    service: ICommonService = Depends(get_common_service)
):
    return await service.get_bank_cash_detailitems()

@router.get("/loadAccountType")
async def get_load_account_types():
    return [
        {"value": item.value, "label": item.value.title()}
        for item in LoadType
    ]

@router.get("/loadAccountTypeDropdown", response_model=List[AccountTypeDropdown])
async def get_account_types(service: ICommonService = Depends(get_common_service)):
    return await service.get_account_types()

@router.get("/loadBankAccountDropdown", response_model=List[BankAccountDropdown])
async def get_bank_account_dropdown(service: ICommonService = Depends(get_common_service)):
    return await service.get_bank_account_dropdown()


@router.get("/getControlItemsByAccountType/{accountTypeID}", response_model=List[dict])
async def get_control_items_by_account_type(
    accountTypeID: int,
    service: ICommonService = Depends(get_common_service),
):
    items = await service.get_control_items_by_account_type(accountTypeID)
    return items

@router.get("/getReportingItemsByControlItem/{controlItemCode}", response_model=List[dict])
async def get_reporting_items_by_control_item(
    controlItemCode: str,
    service: ICommonService = Depends(get_common_service)
):
    return await service.get_reporting_items_by_control_item(controlItemCode)

@router.get("/loadDefaultAccounts")
def get_all_default_accounts():
    return [{"id": item.value, "name": item.name.replace("_", " ").title()} for item in DefaultAccount]

@router.get("/loadAdvanceOrDueAccounts")
def get_all_advance_or_due_accounts():
    return [{"id": item.value, "name": item.name.replace("_", " ").title()} for item in AdvanceOrDueAccounts]

@router.get("/loadBankDropdown", response_model=List[BankDropdown])
async def get_bank_dropdown(service: ICommonService = Depends(get_common_service)):
    return await service.get_bank_dropdown()

@router.get("/loadBranchDropdown", response_model=List[BranchDropdown])
async def get_branch_dropdown(service: ICommonService = Depends(get_common_service)):
    return await service.get_branch_dropdown()

@router.get("/loadBankAccountType")
def get_all_bank_account_types():
    return [{"id": item.value, "name": item.name.replace("_", " ").title()} for item in BankAccountType]

@router.get("/loadBankDepositType")
def get_all_bank_deposit_types():
    return [{"id": item.value, "name": item.name.replace("_", " ").title()} for item in BankDepositType]


@router.get("/loadCompanyDropdown", response_model=List[CompanyDTO])
async def get_companies(service: ICommonService = Depends(get_common_service)):
    return await service.get_all_companies()

@router.get("/loadDepartmentDropdown", response_model=List[ActivityCenterDTO])
async def get_departments(service: ICommonService = Depends(get_common_service)):
    return await service.get_all_departments()

@router.get("/loadSectionDropdown", response_model=List[ResponsibilityCenterDTO])
async def get_sections(service: ICommonService = Depends(get_common_service)):
    return await service.get_all_sections()

@router.get("/loadCountryDropdown", response_model=List[CountryDropdown])
async def get_country_dropdown(service: ICommonService = Depends(get_common_service)):
    return await service.get_country_dropdown()

@router.get("/loadCompanyDropdown", response_model=List[CompanyDropdown])
async def get_company_dropdown(service: ICommonService = Depends(get_common_service)):
    return await service.get_company_dropdown()

@router.get("/nextBankCode", response_model=str)
async def get_next_code(
    service: ICommonService = Depends(get_common_service),
):
    return await service.get_next_bank_code()

@router.get("/getNextReceiptNo")
async def get_next_receipt_no(
    service: ICommonService = Depends(get_common_service)
):
    return {
        "receiptNo": await service.get_next_receipt_no()
    }