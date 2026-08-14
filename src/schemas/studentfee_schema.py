from datetime import date
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class StudentFeeDTO(BaseModel):
    studentFeeID: int

    studentID: int
    enrollmentID: int

    academicYearID: int
    feeHeadID: int

    feeMonth: date | None = None
    dueDate: date | None = None

    amount: Decimal
    discountAmount: Decimal
    paidAmount: Decimal
    dueAmount: Decimal

    status: str
    remarks: str | None = None

    model_config = ConfigDict(from_attributes=True)