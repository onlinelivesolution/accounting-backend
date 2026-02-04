from pydantic import BaseModel
from typing import Optional

class PayScaleRowDTO(BaseModel):
    employeeID: int
    payScaleCode: Optional[str]
    payscaleName: str|None=None
    payGrade: Optional[str] 
    companyCode: Optional[str]
    payrollItemID: int
    createdBy: str
    amount: float
    isBasic: bool
    isPF: bool
    basicSalary: float
    houseRent: float
    medicalAllowance: float
    conveyance: float
    
    class Config:
        from_attributes = True