from pydantic import BaseModel
from typing import Optional

class GenerateSalaryRowDTO(BaseModel):
    employeeID: int
    employeeCode: str
    employeeName: str
    payscaleID: int
    payscaleName: str
    
    otherAllowance: Optional[float] = 0
    houseRentDeduction: Optional[float] = 0
    pfDeduction: Optional[float] = 0
    excessMobileBill: Optional[float] = 0
    otherDeduction: Optional[float] = 0
    
    adjustUnpaidLeave: bool = False
    adjustAdvanceSalary: bool = False
    loanAdjust: bool = False
    
    class Config:
        from_attributes = True