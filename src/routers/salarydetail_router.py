from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from typing import List
from src.schemas.salaryschema import SalaryRead
from src.models.salary import Salary
from common.enum.commenum import DefaultItemStatus
from src.services.interfaces.isalarydetail_service import ISalaryDetailService
from src.depends.service_depends import get_salarydetail_service

router = APIRouter(prefix="/api/salarydetails", tags=["SalaryDetails"])

class ApproveRequest(BaseModel):
    salaryID: int
    detailIDs: List[int]

@router.get("/getSalaryDetailByYearAndMonth", response_model=List[SalaryRead])
async def get_salary_detail_by_year_and_month(
    year: str, month: int, status: int,
    service: ISalaryDetailService = Depends(get_salarydetail_service)
):
    return await service.get_salary_with_details(year, month, status)

@router.get("/loadDefaultItemStatus")
def get_all_default_item_status():
    return [{"id": item.value, "name": item.name.replace("_", " ").title()} for item in DefaultItemStatus]
    
@router.post("/approveSalaryDetails")
async def approve_salary_details(
    detail_ids: List[int],
    service: ISalaryDetailService = Depends(get_salarydetail_service),
):
    return await service.approve_salary_details(detail_ids)

