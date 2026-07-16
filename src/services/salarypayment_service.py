from src.repositories.interfaces.isalarypayment_repository import ISalaryPaymentRepository
from src.services.interfaces.isalarypayment_service import ISalaryPaymentService
from src.schemas.salaryschema import SalaryRead
from typing import Optional
from typing import List
from src.models.salary import Salary


class SalaryPaymentService(ISalaryPaymentService):
    def __init__(self, repository: ISalaryPaymentRepository):
        self.repository = repository

    async def get_approve_salary(
        self, year: str, month: int, status: int
    ) -> List[SalaryRead]:
        salaries = await self.repository.get_approve_salary(year, month, status)
        return [SalaryRead.from_orm(salary) for salary in salaries]
