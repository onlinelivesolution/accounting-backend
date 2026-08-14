from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class StudentPaymentItemCreateDTO(BaseModel):
    studentFeeID: int
    paidAmount: Decimal


class StudentPaymentCreateDTO(BaseModel):
    studentID: int

    paymentDate: datetime

    totalAmount: Decimal

    paymentMethod: str

    referenceNo: str | None = None
    bankAccountID: int | None = None

    remarks: str | None = None

    paymentDetails: list[StudentPaymentItemCreateDTO]
    
class StudentPaymentItemDTO(BaseModel):
    paymentDetailID: int
    studentFeeID: int
    paidAmount: Decimal

    model_config = ConfigDict(from_attributes=True)


class StudentPaymentDTO(BaseModel):
    paymentID: int

    studentID: int

    paymentDate: datetime

    receiptNo: str

    totalAmount: Decimal

    paymentMethod: str

    referenceNo: str | None = None
    bankAccountID: int | None = None

    remarks: str | None = None

    journalHeaderID: int | None = None

    status: str

    paymentDetails: list[StudentPaymentItemDTO] = []

    model_config = ConfigDict(from_attributes=True)