from src.repositories.interfaces.iemployee_repository import IEmployeeRepository
from src.services.interfaces.iemployee_service import IEmployeeService
from src.schemas.employee_schema import EmployeeRead, EmployeeCreate, EmployeeUpdate
from src.schemas.employeecreateschema import EmployeeCreateDTO
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.employee import Employee
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
from src.models.failedemployeeupload import FailedEmployeeUpload
from sqlalchemy import select
from typing import List, Dict, Tuple
from typing import Dict, Any
from common.utils.sanitize import sanitize_nan_for_db
import csv
import pandas as pd

import io
from fastapi import UploadFile

class EmployeeService(IEmployeeService):
    def __init__(self, repository: IEmployeeRepository):
        self.repository = repository
    
    async def add_employee(self, employee_data: EmployeeCreate):
        # Convert Pydantic -> SQLAlchemy model
        employee_dict = employee_data.model_dump()   # Pydantic v2
        db_employee = Employee(**employee_dict)

        return await self.repository.add_employee(db_employee)    
    
    async def update_employee(
        self, employeeCode: str, employee: EmployeeUpdate
    ) -> Optional[EmployeeRead]:
        updated = await self.repository.update_employee(employeeCode, employee)
        if updated:
            return EmployeeRead.model_validate(updated, from_attributes=True)
        return None

    async def generate_next_employee_code(self) -> str:

        last_code = await self.repository.generate_next_employee_code()

        if last_code is None:
            return "00001"    # First employee

        try:
            new_number = int(last_code) + 1
        except:
            # fallback if unexpected value
            new_number = 1

        return f"{new_number:05d}"  # padding with zeros

    async def get_all_active_employees(self) -> List[EmployeeRead]:
        employees = await self.repository.get_all_active_employees()
        return [EmployeeRead.model_validate(ci) for ci in employees["data"]]
    
    async def get_all_employees(self):
        return await self.repository.get_all_employees()

    async def get_all_employee_information(self):
        return await self.repository.get_all_employee_information()

    async def upload_employees_csv(self, file: UploadFile) -> dict:

        contents = await file.read()

        try:
            decoded = contents.decode("utf-8")
        except UnicodeDecodeError:
            try:
                decoded = contents.decode("utf-8-sig")
            except UnicodeDecodeError:
                decoded = contents.decode("latin-1")

        # 🔍 Read CSV into DataFrame
        df = pd.read_csv(io.StringIO(decoded))

        # ✅ Strip spaces from headers
        df.columns = [c.strip() for c in df.columns]

        # Convert DataFrame to list of dict rows
        employees = df.to_dict(orient="records")

        # Hand over to repository for DB work
        success_count, failed_count = await self.repository.upload_employees_csv(employees)

        return {
            "success_count": success_count,
            "failed_count": failed_count,
            "total": success_count + failed_count
        }

    