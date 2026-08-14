from datetime import date
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class FeeHeadCreateDTO(BaseModel):
    feeHeadCode: str
    feeHeadName: str
    description: str | None = None
    incomeAccountID: int | None = None
    status: str = "Active"


class FeeHeadDTO(FeeHeadCreateDTO):
    feeHeadID: int

    model_config = ConfigDict(from_attributes=True)