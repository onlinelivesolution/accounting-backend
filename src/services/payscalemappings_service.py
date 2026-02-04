from src.repositories.interfaces.ipayscalemappings_repository import IPayScaleMappingRepository
from src.services.interfaces.ipayscalemappings_service import IPayScaleMappingService
from src.schemas.controlitem_schema import ControlItemRead, ControlItemCreate, ControlItemUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.payscalerowdto import PayScaleRowDTO
from src.schemas.payscaleresponseschema import PayScaleResponseSchema
from typing import List


class PayScaleMappingService(IPayScaleMappingService):
    def __init__(self, repository: IPayScaleMappingRepository):
        self.repository = repository
    
    async def insert_or_update_pay_scales(self, rows: List[PayScaleRowDTO]) -> dict:
        try:
            return await self.repository.insert_or_update_pay_scales(rows)
        except Exception as e:
            return {"error": str(e)}
        
    async def get_all_employee_pay_scales(self) -> List[PayScaleResponseSchema]:
        payscales = await self.repository.get_all_employee_pay_scales()
        return payscales
