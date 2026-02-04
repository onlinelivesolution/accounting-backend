
from src.dto.generatesalaryrowdto import GenerateSalaryRowDTO
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from src.dto.companydto import CompanyDTO
from src.dto.fiscalyeardto import FiscalYearDTO
from src.dto.activitycenterdto import ActivityCenterDTO
from src.dto.responsibilitycenterdto import ResponsibilityCenterDTO
from src.models.salary import Salary
from src.models.salarydetail import SalaryDetail
from src.dto.generatesalaryrowdto import GenerateSalaryRowDTO
from src.dto.generatesalaryresponsedto import GenerateSalaryResponseDTO

class IGenerateSalaryRepository(ABC):
    @abstractmethod
    async def insert_all_employee_salary_detail(self, salary: Salary, details: List[SalaryDetail]) -> Dict[str, str]:
        pass
    
    @abstractmethod
    async def generate_all_active_employee_salary(self, rows: List[GenerateSalaryRowDTO]) -> GenerateSalaryResponseDTO:
        pass
    
    @abstractmethod
    async def get_last_salary(self) -> Optional[Salary]:
        pass  
    
    @abstractmethod
    async def generate_salary_number(self) -> str:
        pass
    
    async def get_all_companies(self) -> List[CompanyDTO]:
        raise NotImplementedError
    
    async def get_all_departments(self) -> List[ActivityCenterDTO]:
        raise NotImplementedError
    
    async def get_all_sections(self) -> List[ResponsibilityCenterDTO]:
        raise NotImplementedError
    
    async def get_all_fiscalyear(self) -> List[FiscalYearDTO]:
        raise NotImplementedError