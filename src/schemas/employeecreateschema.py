from pydantic import BaseModel
from typing import Optional

class EmployeeCreateDTO(BaseModel):
    employeeCode: str
    employeeName: str
    departmentCode: str
    companyCode: str
    designation: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True