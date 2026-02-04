from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class DetailItemAutoCreateRequest(BaseModel):
    accountType: str
    detailItemName: str
    openingBalance: Optional[float] = None
    openingDate: Optional[date] = None
    loadType: str | None = None
    
class DetailItemRead(BaseModel):
    detailItemCode: str
    detailItemName: str
    reportingItemCode: str
    normalBalance: str
    isActive: bool

    accountType: Optional[str] = None
    controlItemCode: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)