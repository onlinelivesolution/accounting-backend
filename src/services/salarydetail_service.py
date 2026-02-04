from src.repositories.interfaces.isalarydetail_repository import ISalaryDetailRepository
from src.services.interfaces.isalarydetail_service import ISalaryDetailService
from src.schemas.salaryschema import SalaryRead
from typing import Optional
from typing import List
from src.models.salary import Salary


class SalaryDetailService(ISalaryDetailService):
    def __init__(self, repository: ISalaryDetailRepository):
        self.repository = repository
  
    async def get_salary_with_details(self, year: str, month: int, status: int) -> List[SalaryRead]:
        salaries = await self.repository.get_salary_with_details(year, month, status)
        return [SalaryRead.from_orm(salary) for salary in salaries]
    
    async def approve_salary_details(self, detail_ids: List[int]) -> dict:
        if not detail_ids:
            return {"success": False, "message": "No salary details selected"}

        await self.repository.approve_salary_details(detail_ids)
        return {"success": True, "message": "Selected salary details approved"}