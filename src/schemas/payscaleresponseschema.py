from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PayScaleResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    payscaleID: Optional[int]
    payscaleName: Optional[str]
    companyCode: Optional[str]
    createdBy: Optional[str]
    createdDate: Optional[datetime]
    updatedBy: Optional[str]
    updatedDate: Optional[datetime]
    employeeID: Optional[int]
    employeeName: Optional[str]
    employeeCode: Optional[str]
    payGrade: Optional[str]
    status: Optional[int]
    amount: float
    salaryBreakdown: Optional[dict]  # Dict[str, float]
    
    