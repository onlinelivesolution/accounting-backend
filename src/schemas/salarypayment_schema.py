from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime
from common.enum.commenum import DefaultItemStatus, MonthName


class SalaryDetailRead(BaseModel):
    salaryDetailID: int
    employeeID: int
    employeeName: str
    basicSalary: float
    houseRentAllowance: float
    medicalAllowance: float
    travelAllowance: float
    conveyance: float
    overtime: float
    otherAllowance: float
    grossEarnings: float
    adjustUnPaidLeave: float
    taxAmount: float
    pFAmount: float
    employerContribution: float
    supplementaryPF: float
    loanAdjust: float
    houseRentDeduction: float
    excessMobileBill: float
    adjustAdvanceSalary: float
    gradedTax: float
    otherDeduction: float
    status: int | None = None
    netEarnings: float | None = None



class SalaryRead(BaseModel):
    salaryID: int
    fiscalYear: str
    month: int
    workingDay: float
    companyCode: str
    departmentCode: str
    sectionCode: str
    createdDate: datetime
    status: int
    year: str
    monthName: Optional[str] = None
    statusName: Optional[str] = None
    details: List[SalaryDetailRead] = []
    
    model_config = {"from_attributes": True}
    
class SalaryPaymentItemRequest(BaseModel):
    salaryPaymentID: int
    salaryID: int
    employeeID: int    
    amount: float = Field(..., gt=0)
    paymentStatus: int

    model_config = {"from_attributes": True}

class SalaryPaymentCreateRequest(BaseModel):
    paymentNo: str
    paymentDate: datetime
    salaryMonth: str
    salaryYear: str
    bankAccountID: int
    totalAmount: float = Field(..., ge=0)
    remarks: str
    status: int
    createdBy: Optional[int] = None
    createdDate: datetime
    
    salaryPaymentDetails: List[SalaryPaymentItemRequest]
    
    model_config = {"from_attributes": True}
        
class SalaryPaymentItemResponse(BaseModel):
    salaryPaymentDetailID : int
    salaryPaymentID: int
    employeeID: int
    amount: float
    paymentStatus: int

    model_config = {"from_attributes": True}
    
class SalaryPaymentResponse(BaseModel):
    salaryPaymentID: int
    salaryID: int
    month: int
    paymentDate: datetime
    items: List[SalaryPaymentItemResponse]

    model_config = {"from_attributes": True}


    @classmethod
    def from_orm(cls, obj):
        data = obj.__dict__.copy()

        # Add readable names
        try:
            data["monthName"] = MonthName(obj.month).name
        except ValueError:
            data["monthName"] = None

        try:
            data["statusName"] = DefaultItemStatus(obj.status).name
        except ValueError:
            data["statusName"] = None

        # Handle relationships
        if hasattr(obj, "details") and obj.details is not None:
            data["details"] = [SalaryDetailRead.from_orm(d) for d in obj.details]

        return cls(**data)


