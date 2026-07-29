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
    
    taxAmount: float = 0
    pfAmount: float = 0
    loanAdjust: float = 0
    adjustAdvanceSalary: float = 0
    adjustUnpaidLeave: float = 0
    paymentStatus: int

    model_config = ConfigDict(from_attributes=True)


class SalaryPaymentCreateRequest(BaseModel):
    paymentNo: str
    paymentDate: datetime
    salaryMonth: str
    salaryYear: str
    bankAccountCode: str
    totalAmount: float = Field(..., ge=0)
    remarks: Optional[str] = None
    status: int
    createdDate: datetime
    companyCode: str

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
    bankAccountCode: str
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
