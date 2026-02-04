from fastapi import APIRouter, Depends
from src.services.interfaces.idetailitem_service import IDetailItemService
from src.depends.service_depends import get_detail_item_service
from src.schemas.detailitemautocreate_schema import DetailItemAutoCreateRequest

router = APIRouter(prefix="/api/detailitems", tags=["DetailItems"])


@router.post("/auto-create")
async def auto_create_detail_item(
    payload: DetailItemAutoCreateRequest,
    service: IDetailItemService = Depends(get_detail_item_service)
):
    return await service.auto_create_detail_item(payload)
