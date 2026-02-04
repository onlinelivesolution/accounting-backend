from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Dict, Any
from src.services.controlitem_service import IControlItemService
from src.depends.service_depends import get_controlitem_service
from src.schemas.accounttype_schema import AccountTypeDropdown
from src.schemas.fatype_schema import FATypeDropdown
from src.schemas.controlitem_schema import ControlItemRead, ControlItemCreate, ControlItemUpdate
from src.models.controlitem import ControlItem

router = APIRouter(prefix="/api/controlitems", tags=["ControlItems"])

@router.post("/addNewControlItem", response_model=ControlItemRead)
async def add_controlitem(
    controlitem: ControlItemCreate,
    service: IControlItemService = Depends(get_controlitem_service)
):
    return await service.add_controlitem(controlitem)

@router.put("/updateControlItem/{controlItemCode}", response_model=ControlItemRead)
async def update_control_item(
    controlItemCode: str,
    controlitem: ControlItemUpdate,
    service: IControlItemService = Depends(get_controlitem_service),
):
    updated_item = await service.update_control_item(controlItemCode, controlitem)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Control item not found")
    return updated_item

@router.get("/controlItemTable", response_model=List[ControlItemRead])
async def get_all_controlitems(
    skip: int = 0,
    limit: int = 100,
    service: IControlItemService = Depends(get_controlitem_service)
):
    return await service.get_all_controlitems(skip=skip, limit=limit)

@router.get("/nextControlItemCode", response_model=str)
async def get_next_code(
    service: IControlItemService = Depends(get_controlitem_service),
):
    return await service.get_next_control_item_code()


@router.get("/accountTypeDropdown", response_model=List[AccountTypeDropdown])
async def load_account_types(service: IControlItemService = Depends(get_controlitem_service)):
    return await service.get_account_types()

@router.get("/faTypeDropdown", response_model=List[FATypeDropdown])
async def load_fa_types(service: IControlItemService = Depends(get_controlitem_service)):
    return await service.get_fa_types()
