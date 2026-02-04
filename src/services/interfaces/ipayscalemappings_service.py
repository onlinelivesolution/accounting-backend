from abc import ABC, abstractmethod
from typing import List
from typing import List, Dict
from src.dto.payscalerowdto import PayScaleRowDTO


class IPayScaleMappingService(ABC):
    
    @abstractmethod
    async def insert_or_update_pay_scales(self, rows: List["PayScaleRowDTO"]) -> dict:
        pass
    
    @abstractmethod
    async def get_all_employee_pay_scales(self) -> List[Dict]:
        pass