from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# -------------------------------
# Salary Payment Request
# -------------------------------


class SalaryPaymentItemRequest(BaseModel):
    salaryID: int
    employeeID: int
    amount: float = Field(..., gt=0)
    paymentStatus: int

    model_config = ConfigDict(from_attributes=True)


class SalaryPaymentCreateRequest(BaseModel):
    paymentNo: str
    paymentDate: datetime
    salaryMonth: str
    salaryYear: str
    bankAccountID: int
    totalAmount: float = Field(..., ge=0)
    remarks: Optional[str] = None
    status: int
    createdDate: datetime

    salaryPaymentDetails: List[SalaryPaymentItemRequest]

    model_config = ConfigDict(from_attributes=True)


# -------------------------------
# Salary Payment Response
# -------------------------------


class SalaryPaymentItemResponse(BaseModel):
    salaryPaymentDetailID: int
    salaryPaymentID: int
    salaryID: int
    employeeID: int
    amount: float
    paymentStatus: int

    model_config = ConfigDict(from_attributes=True)


class SalaryPaymentResponse(BaseModel):
    salaryPaymentID: int
    paymentNo: str
    paymentDate: datetime
    salaryMonth: str
    salaryYear: str
    bankAccountID: int
    totalAmount: float
    remarks: Optional[str] = None
    status: int
    createdBy: Optional[int] = None

    salaryPaymentDetails: List[SalaryPaymentItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
    
class SalaryPaymentCreateResponse(BaseModel):
    salaryPaymentID: int
    paymentNo: str
    message: str
