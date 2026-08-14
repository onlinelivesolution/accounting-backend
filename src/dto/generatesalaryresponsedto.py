from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from src.dto.salarydto import SalaryDTO
from src.dto.salarydetaildto import SalaryDetailDTO

class GenerateSalaryResponseDTO(BaseModel):
    salary: Optional[SalaryDTO] = None
    salaryDetails: List[SalaryDetailDTO]
    message: str
    
    model_config = ConfigDict(from_attributes=True)
    
class GenerateSalarySaveResponseDTO(BaseModel):
    salaryID: int
    message: str

    model_config = ConfigDict(from_attributes=True)