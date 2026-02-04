from pydantic import BaseModel, ConfigDict
from typing import Optional
from src.dto.salarydetaildto import SalaryDetailDTO

class SalaryDTO(BaseModel):
    fiscalYear: str
    month: int
    workingDay: float
    companyCode: str
    departmentCode: str
    sectionCode: str
    createdBy: str
    approvedBy: str
    hRComments: Optional[str] = None
    status: int    
    year: str
    
    model_config = ConfigDict(from_attributes=True)