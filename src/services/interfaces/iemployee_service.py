from abc import ABC, abstractmethod
from typing import List
from typing import Optional
from src.schemas.employee_schema import EmployeeCreate, EmployeeUpdate, EmployeeRead
from fastapi import UploadFile
from src.models.employee import Employee
from typing import Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

class IEmployeeService(ABC):
    
    @abstractmethod
    async def add_employee(self, data: EmployeeCreate) -> EmployeeRead:
        pass
    
    @abstractmethod
    async def update_employee(self, employeeCode: str, employee: EmployeeUpdate) -> Optional[EmployeeRead]:
        pass
    
    @abstractmethod
    async def generate_next_employee_code(self) -> str:
        pass

    @abstractmethod
    async def get_all_active_employees(self, skip: int, limit: int):
        pass
    
    @abstractmethod
    async def get_all_employees(self) -> List[Employee]:
        pass

    @abstractmethod
    async def get_all_employee_information(self) -> List[Employee]:
        pass

    @abstractmethod
    async def upload_employees_csv(self, employees: List[Dict]) -> Tuple[int, int]:
        pass
    
