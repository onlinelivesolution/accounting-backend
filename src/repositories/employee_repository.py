from common.generic.generic_repository import GenericRepository
from src.repositories.interfaces.iemployee_repository import IEmployeeRepository
from src.models.employee import Employee
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Integer
from sqlalchemy import select, desc
from typing import List, Dict
from typing import List, Optional
from common.utils.sanitize import sanitize_nan_for_db
from src.schemas.employee_schema import EmployeeUpdate
from datetime import datetime
from src.models.failedemployeeupload import FailedEmployeeUpload
from typing import Dict, Tuple
import pandas as pd

FIELD_MAP = {
    "EmployeeCode": "employeeCode",
    "ApplicantID": "applicantID",
    "FirstName": "firstName",
    "MiddleName": "middleName",
    "LastName": "lastName",
    "EmployeeName": "employeeName",
    "FatherName": "fatherName",
    "MotherName": "motherName",
    "Gender": "gender",
    "DateOfBirth": "dateOfBirth",
    "NationalID": "nationalID",
    "Address": "address",
    "PostalAddress": "postalAddress",
    "AccountHolder": "accountHolder",
    "BankID": "bankID",
    "BankBranchID": "bankBranchID",
    "AccountNumber": "accountNumber",
    "Designation": "designation",
    "JoinDate": "joinDate",
    "Email": "email",
    "Phone": "phone",
    "CompanyCode": "companyCode",
    "ActivityCenterCode": "activityCenterCode",
    "RespCenterCode": "respCenterCode",
    "EmergencyContact": "emergencyContact",
    "EmployeeImage": "employeeImage",
    "Status": "status",
    "DeviceID": "deviceID",
    "GradedTaxNo": "gradedTaxNo",
    "TerminitionDate": "terminitionDate",
    "EmployeeSetID": "employeeSetID",
}

class EmployeeRepository(GenericRepository[Employee], IEmployeeRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Employee, db)
        
    async def add_employee(self, employee: Employee):
        self.db.add(employee)
        await self.db.commit()
        await self.db.refresh(employee)
        return employee
    
    async def update_employee(self, employeeCode: str, employee_update):
        # Find by employeeCode (NOT PK)
        stmt = select(Employee).where(Employee.employeeCode == employeeCode)
        result = await self.db.execute(stmt)
        db_item = result.scalar_one_or_none()

        if not db_item:
            return None  # Employee not found

        # Apply update fields
        update_data = employee_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)

        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item
    
    async def generate_next_employee_code(self) -> str:
        stmt = (
            select(Employee.employeeCode)
            .order_by(Employee.employeeID.desc())
            .limit(1)
        )
        result = await self.db.execute(stmt)
        row = result.scalar_one_or_none()

        return row

        
    async def get_all_active_employees(self) -> dict: 
        db: AsyncSession = self.db

        # ✅ Count only active employees
        total_query = await db.execute(
            select(func.count()).select_from(Employee).where(Employee.status == 1)
        )
        total = total_query.scalar_one()

        # ✅ Select only active employees
        query = select(Employee).where(Employee.status == 1)

        compiled = query.compile(compile_kwargs={"literal_binds": True})
        print("🔍 Executing SQL:\n", compiled, "\n")

        results = await db.execute(query)
        rows = results.mappings().all()

        employees = []
        for row in rows:
            c: Employee = row["Employee"]
            employees.append({
                "employeeID": c.employeeID,
                "employeeCode": c.employeeCode,
                "employeeName": c.employeeName,
                "status": c.status,
            })

        return {
            "total": total,
            "data": employees,
        }

    async def get_all_employee_information(self) -> List[Employee]:
        stmt = select(Employee)
        result = await self.db.execute(stmt)
        return result.scalars().all()
   
    async def get_all_employees(self) -> List[Employee]:
        stmt = select(Employee)
        result = await self.db.execute(stmt)
        return result.scalars().all()


    async def get_all_active_employees(self) -> List[Employee]:
        stmt = select(Employee).where(Employee.status == 1)
        result = await self.db.execute(stmt)
        return result.scalars().all()

        
    async def create(self, employee: Employee) -> Employee:
        self.db.add(employee)
        await self.db.commit()
        await self.db.refresh(employee)
        return employee

    async def update(self, employee_id: int, employee: Employee) -> Optional[Employee]:
        stmt = select(Employee).where(Employee.employeeID == employee_id)
        result = await self.db.execute(stmt)
        db_employee = result.scalar_one_or_none()
        if not db_employee:
            return None

        for key, value in employee.__dict__.items():
            if key != "employeeID" and value is not None:
                setattr(db_employee, key, value)

        await self.db.commit()
        await self.db.refresh(db_employee)
        return db_employee

    async def delete(self, employee_id: int) -> bool:
        stmt = select(Employee).where(Employee.employeeID == employee_id)
        result = await self.db.execute(stmt)
        db_employee = result.scalar_one_or_none()
        if not db_employee:
            return False

        await self.db.delete(db_employee)
        await self.db.commit()
        return True

    async def get_all(self) -> List[Employee]:
        stmt = select(Employee)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, employee_id: int) -> Optional[Employee]:
        stmt = select(Employee).where(Employee.employeeID == employee_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def upload_employees_csv(self, employees: List[Dict]) -> Tuple[int, int]:
        success_count = 0
        failed_count = 0
        processed_codes = set()  # ✅ Track already processed employeeCodes in this batch

        for row in employees:
            try:
                row = sanitize_nan_for_db(row)

                # 🔑 Map CSV fields
                mapped_row = {FIELD_MAP.get(k, k): v for k, v in row.items() if FIELD_MAP.get(k)}

                emp_code = mapped_row.get("employeeCode")
                comp_code = mapped_row.get("companyCode")
                activity_center_code = mapped_row.get("activityCenterCode")
                resp_center_code = mapped_row.get("respCenterCode")

                # ✅ EmployeeCode 5 digits
                if emp_code:
                    try:
                        emp_code = str(int(emp_code)).zfill(5)
                        mapped_row["employeeCode"] = emp_code
                    except ValueError:
                        await self._log_failed_row(row, f"Invalid employeeCode: {emp_code}")
                        failed_count += 1
                        continue
                else:
                    await self._log_failed_row(row, "Missing employeeCode")
                    failed_count += 1
                    continue

                # 🚫 Skip duplicate employeeCode in the same upload batch
                if emp_code in processed_codes:
                    continue
                processed_codes.add(emp_code)

                # ✅ CompanyCode 2 digits
                if comp_code:
                    try:
                        mapped_row["companyCode"] = str(int(comp_code)).zfill(2)
                    except ValueError:
                        await self._log_failed_row(row, f"Invalid companyCode: {comp_code}")
                        failed_count += 1
                        continue
                else:
                    await self._log_failed_row(row, "Missing companyCode")
                    failed_count += 1
                    continue

                # ✅ ActivityCenterCode 4 digits
                if activity_center_code:
                    try:
                        mapped_row["activityCenterCode"] = str(int(activity_center_code)).zfill(4)
                    except ValueError:
                        await self._log_failed_row(row, f"Invalid activityCenterCode: {activity_center_code}")
                        failed_count += 1
                        continue
                else:
                    await self._log_failed_row(row, "Missing activityCenterCode")
                    failed_count += 1
                    continue

                # ✅ RespCenterCode 6 digits
                if resp_center_code:
                    try:
                        mapped_row["respCenterCode"] = str(int(resp_center_code)).zfill(6)
                    except ValueError:
                        await self._log_failed_row(row, f"Invalid respCenterCode: {resp_center_code}")
                        failed_count += 1
                        continue
                else:
                    await self._log_failed_row(row, "Missing respCenterCode")
                    failed_count += 1
                    continue

                # 🔍 Check if employee exists (async)
                result = await self.db.execute(
                    select(Employee).where(Employee.employeeCode == emp_code)
                )
                existing = result.scalar_one_or_none()

                if existing:
                    # ✅ Update existing employee
                    for key, value in mapped_row.items():
                        if hasattr(existing, key) and value not in [None, ""]:
                            setattr(existing, key, value)
                else:
                    # ✅ Insert new employee only if not exists
                    new_emp = Employee(**mapped_row)
                    self.db.add(new_emp)

                success_count += 1

            except Exception as e:
                await self._log_failed_row(row, str(e))
                failed_count += 1

        try:
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            await self._log_failed_row({}, f"DB commit failed: {str(e)}")
            failed_count += 1

        return success_count, failed_count


    async def _log_failed_row(self, row: Dict, reason: str):
        failed = FailedEmployeeUpload(
            rowData=str(row),
            reason=reason,
            createdDate=datetime.utcnow()
        )
        self.db.add(failed)
        await self.db.commit()