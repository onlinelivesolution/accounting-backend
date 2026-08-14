from datetime import date
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class FeeStructureCreateDTO(BaseModel):
    academicYearID: int
    classID: int
    feeHeadID: int

    amount: Decimal

    frequency: str = "Monthly"

    effectiveFrom: date | None = None
    effectiveTo: date | None = None

    status: str = "Active"


class FeeStructureDTO(FeeStructureCreateDTO):
    feeStructureID: int

    model_config = ConfigDict(from_attributes=True)