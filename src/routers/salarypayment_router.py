from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from typing import List
from src.core.auth_dependency import get_current_user
from src.schemas.salaryschema import SalaryRead
from src.schemas.salarypayment_schema import (
    SalaryPaymentCreateRequest,
    SalaryPaymentCreateResponse,
)
from src.models.salary import Salary
from common.enum.commenum import DefaultItemStatus
from src.services.interfaces.isalarypayment_service import ISalaryPaymentService
from src.depends.service_depends import get_salarypayment_service

router = APIRouter(prefix="/api/salarypayments", tags=["SalaryPayments"])


class ApproveRequest(BaseModel):
    salaryID: int
    detailIDs: List[int]


@router.get("/getApproveSalaryByYearAndMonth", response_model=List[SalaryRead])
async def get_approve_salary(
    year: str,
    month: int,
    status: int,
    service: ISalaryPaymentService = Depends(get_salarypayment_service),
):
    return await service.get_approve_salary(year, month, status)


@router.post(
    "/createSalaryPayment",
    response_model=SalaryPaymentCreateResponse,
)
async def create_salary_payment(
    request: SalaryPaymentCreateRequest,
    current_user: dict = Depends(get_current_user),
    service: ISalaryPaymentService = Depends(get_salarypayment_service),
):
    return await service.create_salary_payment(request, current_user)


