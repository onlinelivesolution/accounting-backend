
from src.dto.generatesalaryrowdto import GenerateSalaryRowDTO
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from src.dto.companydto import CompanyDTO
from src.dto.fiscalyeardto import FiscalYearDTO
from src.dto.activitycenterdto import ActivityCenterDTO
from src.dto.responsibilitycenterdto import ResponsibilityCenterDTO
from src.models.salary import Salary
from src.models.salarydetail import SalaryDetail
from src.schemas.salaryschema import SalaryRead
from src.dto.generatesalaryrowdto import GenerateSalaryRowDTO
from src.dto.generatesalaryresponsedto import GenerateSalaryResponseDTO

class ISalaryPaymentRepository(ABC):
    
    @abstractmethod
    async def get_approve_salary(self, year: str, month: int, status: int) -> List[Salary]:
        pass
    