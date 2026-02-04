from fastapi import APIRouter, Depends, Body
from common.enum.commenum import DefaultPayrollItem
from typing import List
from src.services.interfaces.ipayscalemappings_service import IPayScaleMappingService
from src.depends.service_depends import get_payscalemapping_service
from src.dto.payscalerowdto import PayScaleRowDTO
from src.schemas.payscaleresponseschema import PayScaleResponseSchema


router = APIRouter(prefix="/api/payscales", tags=["Payscales"])

@router.post("/processInsertOrUpdatePayScale")
async def insert_or_update_pay_scales(
    pay_scales: List[PayScaleRowDTO] = Body(...),
    service: IPayScaleMappingService = Depends(get_payscalemapping_service),
):
    print("Received payload:", pay_scales)
    return await service.insert_or_update_pay_scales(pay_scales)

@router.get("/loadDefaultPayrollItems")
def get_all_payrollitems():
    return [{"id": item.value, "name": item.name.replace("_", " ").title()} for item in DefaultPayrollItem]

@router.get("/getAllEmployeeForPayScaleMapping", response_model=List[PayScaleResponseSchema])
async def get_all_employee_pay_scales(
    service: IPayScaleMappingService = Depends(get_payscalemapping_service),
):
    return await service.get_all_employee_pay_scales()