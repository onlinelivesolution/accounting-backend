from abc import ABC, abstractmethod
from typing import List
from typing import Optional
from src.schemas.detailitemautocreate_schema import DetailItemAutoCreateRequest
from src.models.detailitem import DetailItem

class IDetailItemService(ABC):
    
    @abstractmethod
    async def auto_create_detail_item(self, payload: DetailItemAutoCreateRequest) -> DetailItem:
        pass
