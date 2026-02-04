from abc import ABC, abstractmethod
from typing import List, Dict, Any
from typing import Optional
from typing import Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.employee import Employee
from src.schemas.employee_schema import EmployeeCreate
from src.schemas.employee_schema import EmployeeUpdate, EmployeeRead, EmployeeCreate

class IEmployeeRepository(ABC):
    
    @abstractmethod
    async def add_employee(self, controlitem: Employee) -> Employee:
        pass 
     
    @abstractmethod
    async def update_employee(self, employeeCode: str, employee: EmployeeUpdate) -> Optional[Employee]:
        pass
    
    @abstractmethod
    async def generate_next_employee_code(self) -> str:
        pass
    
    @abstractmethod
    async def get_all_active_employees(self, db: AsyncSession) -> List[Employee]:
        pass
    
    @abstractmethod
    def get_all_employee_information(self) -> List[Employee]:
        """Get all employee information (with related pay scale, etc.)"""
        pass
 
    @abstractmethod
    def get_all_employees(self) -> List[Employee]:
        """Get all employees"""
        pass
    
    @abstractmethod
    async def upload_employees_csv(self, employees: List[Dict]) -> Tuple[int, int]:
        pass