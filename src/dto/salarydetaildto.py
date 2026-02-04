from datetime import date, datetime
from pydantic import BaseModel, field_validator, ConfigDict
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

class SalaryDetailDTO(BaseModel):
    sl: Optional[int] = None
    employeeID: Optional[int] = None
    employeeCode: Optional[str] = None
    employeeName: Optional[str] = None
    payscaleID: Optional[int] = None
    absenceDay: Optional[float] = 0
    basicSalary: Optional[float] = 0
    houseRentAllowance: Optional[float] = 0
    medicalAllowance: Optional[float] = 0
    travelAllowance: Optional[float] = 0
    conveyance: Optional[float] = 0
    overtime: Optional[float] = 0
    otherAllowance: Optional[float] = 0   
    grossEarnings: Optional[float] = 0
    adjustUnPaidLeave: Optional[float] = 0
    taxAmount: Optional[float] = 0
    pFAmount: Optional[float] = 0
    employerContribution: Optional[float] = 0
    supplementaryPF: Optional[float] = 0
    loanAdjust: Optional[float] = 0
    houseRentDeduction: Optional[float] = 0
    excessMobileBill: Optional[float] = 0
    adjustAdvanceSalary: Optional[float] = 0
    gradedTax: Optional[float] = 0
    otherDeduction: Optional[float] = 0
    companyCode: Optional[str] = None
    departmentCode: Optional[str] = None
    sectionCode: Optional[str] = None
    status: Optional[int] = None
    isUnPaid: Optional[bool] = False
    createdBy: Optional[str] = None
    createdDate: Optional[date] = 0
    approvedDate: Optional[datetime] = 0
    settingTaxAmount: Optional[float] = 0
    totalDeduction: Optional[float] = 0
    netEarnings: Optional[float] = 0
    
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True)
        
    @field_validator("*", mode="before")
    def round_decimal(cls, v):
        if isinstance(v, (float, Decimal)):
            return Decimal(v).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return v
    
    
