from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from typing import List
from src.schemas.salaryschema import SalaryRead
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


 