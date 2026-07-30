from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
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
    adjustUnpaidLeave: float
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

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True
