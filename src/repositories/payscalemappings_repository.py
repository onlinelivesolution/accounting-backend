from common.generic.generic_repository import GenericRepository
from src.repositories.interfaces.ipayscalemappings_repository import IPayScaleMappingRepository
from src.dto.payscalerowdto import PayScaleRowDTO
from sqlalchemy.orm import joinedload
from src.models.employee import Employee
from src.models.payscale import PayScale
from src.models.payscalemapping import PayScaleMapping
from src.models.employeehistory import EmployeeHistory
from datetime import datetime
from sqlalchemy import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession


class PayScaleMappingRepository(GenericRepository[PayScale], IPayScaleMappingRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(PayScale, db)
        
    async def insert_or_update_pay_scales(self, rows: List[PayScaleRowDTO]) -> dict:
        inserted_count = 0
        updated_count = 0

        for row in rows:
            # 🔹 Step 1: Insert or update PayScale by EmployeeID
            result = await self.db.execute(
                select(PayScale).filter_by(employeeID=row.employeeID)
            )
            pay_scale = result.scalars().first()

            if not pay_scale:
                pay_scale = PayScale(
                    employeeID=row.employeeID,
                    payscaleName=row.payscaleName,
                    payGrade=row.payGrade,
                    companyCode=row.companyCode,
                    createdBy="Admin",
                    createdDate=datetime.now(),
                    status=1,
                )
                self.db.add(pay_scale)
                await self.db.flush()
                inserted_count += 1
            else:
                pay_scale.payscaleName = row.payscaleName
                pay_scale.payGrade = row.payGrade
                pay_scale.companyCode = row.companyCode
                pay_scale.updatedBy = "Admin"
                pay_scale.updatedDate = datetime.now()
                self.db.add(pay_scale)
                await self.db.flush()
                updated_count += 1

            # 🔹 Step 2: Insert or update 4 rows in PayScaleMapping
            mapping_data = {
                1: (row.basicSalary, False, False),
                2: (row.houseRent, False, False),
                3: (row.medicalAllowance, False, False),
                4: (row.conveyance, False, False),
            }

            for payrollItemID, (amount, isBasic, isPF) in mapping_data.items():
                result = await self.db.execute(
                    select(PayScaleMapping).filter_by(
                        payscaleID=pay_scale.payscaleID,
                        payrollItemID=payrollItemID,
                    )
                )
                mapping = result.scalars().first()

                if not mapping:
                    mapping = PayScaleMapping(
                        payscaleID=pay_scale.payscaleID,
                        payrollItemID=payrollItemID,
                        amount=amount,
                        createdBy="Admin",
                        createdDate=datetime.now(),
                        companyCode=row.companyCode,
                        isBasic=isBasic,
                        isPF=isPF,
                    )
                    self.db.add(mapping)
                else:
                    mapping.amount = amount
                    mapping.updatedBy = "Admin"
                    mapping.updatedDate = datetime.now()
                    mapping.companyCode = row.companyCode
                    mapping.isBasic = isBasic
                    mapping.isPF = isPF
                    self.db.add(mapping)

            # 🔹 Step 3: Always insert a new row in EmployeeHistory
            emp_hist = EmployeeHistory(
                employeeID=row.employeeID,
                payscaleID=pay_scale.payscaleID,
                createdBy="Admin",
                createdDate=datetime.now(),
            )
            self.db.add(emp_hist)

        await self.db.commit()

        return {
            "status": "success",
            "message": f"{inserted_count} new PayScale(s) inserted, {updated_count} updated.",
        }
        
    async def get_all_employee_pay_scales(self):
        stmt = (
            select(Employee)
            .options(
                joinedload(Employee.payscales)
                .joinedload(PayScale.mappings)
                .joinedload(PayScaleMapping.payroll_item)
            )
        )

        # ✅ Async execution
        result = await self.db.execute(stmt)
        employees = result.scalars().unique().all()

        results = []

        for emp in employees:
            if emp.payscales:
                for ps in emp.payscales:
                    mappings = ps.mappings or []
                    salary_breakdown = {
                        m.payroll_item.payrollItemName: m.amount
                        for m in mappings if m.payroll_item
                    }
                    results.append({
                        "payscaleID": ps.payscaleID,
                        "payscaleName": ps.payscaleName,
                        "companyCode": ps.companyCode,
                        "createdBy": ps.createdBy,
                        "createdDate": ps.createdDate,
                        "updatedBy": ps.updatedBy,
                        "updatedDate": ps.updatedDate,
                        "employeeID": emp.employeeID,
                        "employeeName": emp.employeeName,
                        "employeeCode": emp.employeeCode,
                        "payGrade": ps.payGrade,
                        "status": ps.status,
                        "amount": sum(m.amount or 0 for m in mappings),
                        "salaryBreakdown": salary_breakdown
                    })
            else:
                results.append({
                    "payscaleID": None,
                    "payscaleName": None,
                    "companyCode": emp.companyCode,
                    "createdBy": None,
                    "createdDate": None,
                    "updatedBy": None,
                    "updatedDate": None,
                    "employeeID": emp.employeeID,
                    "employeeName": emp.employeeName,
                    "employeeCode": emp.employeeCode,
                    "payGrade": None,
                    "status": None,
                    "amount": 0,
                    "salaryBreakdown": {}
                })

        return results
        
        