from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from src.models.salary import Salary
from src.schemas.salaryschema import SalaryRead
from src.schemas.salarypayment_schema import SalaryPaymentCreateRequest
from src.dto.companydto import CompanyDTO
from src.dto.activitycenterdto import ActivityCenterDTO
from src.models.salarypayment import SalaryPayment
from src.dto.fiscalyeardto import FiscalYearDTO
from src.dto.responsibilitycenterdto import ResponsibilityCenterDTO
from src.models.salarydetail import SalaryDetail
from src.dto.generatesalaryrowdto import GenerateSalaryRowDTO
from src.dto.generatesalaryresponsedto import GenerateSalaryResponseDTO


class ISalaryPaymentService(ABC):
    
    @abstractmethod 
    async def get_approve_salary(self, year: str, month: int, status: int) -> List[SalaryRead]:
        raise NotImplementedError
    
    @abstractmethod
    async def create_salary_payment(
        self, request: SalaryPaymentCreateRequest
    ) -> SalaryPayment:
        pass
    
    @abstractmethod
    async def get_next_salary_payment_no(self) -> str:
        pass