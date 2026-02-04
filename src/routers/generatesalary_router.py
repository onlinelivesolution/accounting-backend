from fastapi import APIRouter, Depends, Body
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from common.enum.commenum import MonthName
from src.dto.companydto import CompanyDTO
from src.dto.fiscalyeardto import FiscalYearDTO
from src.schemas.salaryschema import SalaryRead
from src.dto.activitycenterdto import ActivityCenterDTO
from src.dto.responsibilitycenterdto import ResponsibilityCenterDTO
from src.dto.generatesalaryrowdto import GenerateSalaryRowDTO
from src.dto.generatesalaryresponsedto import GenerateSalaryResponseDTO
from src.services.interfaces.igeneratesalary_service import IGenerateSalaryService
from src.services.generatesalary_service import GenerateSalaryService
from src.repositories.generatesalary_repository import GenerateSalaryRepository
from src.depends.service_depends import get_generatesalary_service

router = APIRouter(prefix="/api/generatesalary", tags=["GenerateSalary"])

@router.post("/generateActiveEmployeeSalary", response_model=GenerateSalaryResponseDTO)
async def generate_salary(
    rows: List[GenerateSalaryRowDTO] = Body(...),
    service: IGenerateSalaryService = Depends(get_generatesalary_service)
):
    return await service.generate_all_active_employee_salary(rows)

@router.post("/insertSalaryInformation", response_model=Dict[str, str])
async def save_salary(
    data: GenerateSalaryResponseDTO = Body(...),
    service: IGenerateSalaryService = Depends(get_generatesalary_service)
):
    return await service.insert_all_employee_salary_detail(data)

@router.get("/getNextSalaryNumber")
async def get_next_salary_number(service: IGenerateSalaryService = Depends(get_generatesalary_service)):
    next_number = await service.get_next_salary_number()
    return {"salaryNumber": next_number}

@router.get("/loadCompanyDropdown", response_model=List[CompanyDTO])
async def get_companies(service: IGenerateSalaryService = Depends(get_generatesalary_service)):
    return await service.get_all_companies()

@router.get("/loadDepartmentDropdown", response_model=List[ActivityCenterDTO])
async def get_departments(service: IGenerateSalaryService = Depends(get_generatesalary_service)):
    return await service.get_all_departments()

@router.get("/loadSectionDropdown", response_model=List[ResponsibilityCenterDTO])
async def get_sections(service: IGenerateSalaryService = Depends(get_generatesalary_service)):
    return await service.get_all_sections()

@router.get("/loadFiscalYearDropdown", response_model=List[FiscalYearDTO])
async def get_all_fiscalyear(service: IGenerateSalaryService = Depends(get_generatesalary_service)):
    return await service.get_all_fiscalyear()

@router.get("/loadMonthNames")
def get_all_monthnames():
    return [{"id": item.value, "name": item.name.replace("_", " ").title()} for item in MonthName]
