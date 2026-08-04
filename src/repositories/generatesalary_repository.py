from abc import ABC, abstractmethod
from common.generic.generic_repository import GenericRepository
from src.repositories.interfaces.igeneratesalary_repository import IGenerateSalaryRepository
from src.dto.generatesalaryrowdto import GenerateSalaryRowDTO
from src.dto.generatesalaryresponsedto import GenerateSalaryResponseDTO
from src.dto.salarydetaildto import SalaryDetailDTO
from src.models.employee import Employee
from src.models.leave import Leave
from src.models.leavedetail import LeaveDetail
from src.models.payscalemapping import PayScaleMapping
from src.models.overtimedetail import OvertimeDetail
from src.models.overtime import Overtime
from src.models.employeeloan import EmployeeLoan
from src.models.advancesalary import AdvanceSalary
from src.models.taxdefinition import TaxDefinition
from src.models.taxband import TaxBand
from src.models.salary import Salary
from src.models.salarydetail import SalaryDetail
from src.models.employeeinvestment import EmployeeInvestment
from src.dto.payscalerowdto import PayScaleRowDTO
from sqlalchemy.orm import joinedload
from src.models.payscale import PayScale
from src.models.payscalemapping import PayScaleMapping
from src.models.employeehistory import EmployeeHistory
from src.models.employeeloan import EmployeeLoan
from src.models.advancesalary import AdvanceSalary
from decimal import Decimal
from src.models.company import Company
from src.dto.companydto import CompanyDTO
from src.models.fiscalyear import FiscalYear
from src.dto.fiscalyeardto import FiscalYearDTO
from src.models.activitycenter import ActivityCenter
from src.dto.activitycenterdto import ActivityCenterDTO
from src.models.responsibilitycenter import ResponsibilityCenter
from src.dto.responsibilitycenterdto import ResponsibilityCenterDTO
from datetime import datetime
from sqlalchemy import select, func, desc
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession


class GenerateSalaryRepository(GenericRepository[PayScale], IGenerateSalaryRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(PayScale, db)
        
    async def generate_all_active_employee_salary(self, rows: List[GenerateSalaryRowDTO]) -> GenerateSalaryResponseDTO:
       
        salary_details = []
        sl = 1

        for row in rows:
            # 1. Get PayScaleMapping
            result = await self.db.execute(
                select(PayScaleMapping).join(PayScale).where(PayScale.employeeID == row.employeeID)
            )
            mappings = result.scalars().all()

            salary_map = {m.payrollItemID: m.amount for m in mappings}
            basic = Decimal(salary_map.get(1, 0))
            house_rent = Decimal(salary_map.get(2, 0))
            medical = Decimal(salary_map.get(3, 0))
            conveyance = Decimal(salary_map.get(4, 0))

            # ==========================================
            # Provident Fund Calculation
            # ==========================================
            pf_amount = (basic * Decimal("0.10")).quantize(Decimal("0.01"))

            # Employer Contribution = 50% of PF
            employer_contribution = (
                pf_amount * Decimal("0.50")
            ).quantize(Decimal("0.01"))

            # 2. Overtime
            result = await self.db.execute(
                select(func.coalesce(func.sum(OvertimeDetail.totalAmount), 0))
                .join(Overtime, Overtime.overtimeID == OvertimeDetail.overtimeID)
                .where(
                    Overtime.status == 2,
                    OvertimeDetail.employeeID == row.employeeID
                )
            )
            overtime = result.scalar_one()

            # 3. Gross Earnings
            gross = (
                basic
                + house_rent
                + medical
                + conveyance
                + Decimal(overtime or 0)
                + Decimal(row.otherAllowance or 0)
            )

            # 4. Tax Calculation
            result = await self.db.execute(select(TaxDefinition))
            tax_def = result.scalars().first()
            tax_amount = 0
            if tax_def:
                result = await self.db.execute(select(TaxBand).where(TaxBand.taxDefinitionID == tax_def.taxDefinitionID))
                tax_bands = result.scalars().all()
                yearly_taxable = gross * 12 - (tax_def.taxFreeAmount or 0)
                for band in tax_bands:
                    if yearly_taxable > band.startRange:
                        taxable_in_band = min(yearly_taxable, band.endRange) - band.startRange
                        tax_amount += taxable_in_band * (band.percentage / 100)
                tax_amount = tax_amount / 12  # Monthly

            # 5. Loan Deduction
            loan_deduction = Decimal(0)
            if row.loanAdjust:
                result = await self.db.execute(
                    select(EmployeeLoan).where(
                        EmployeeLoan.employeeID == row.employeeID,
                        EmployeeLoan.status == 3
                    )
                )
                employee_loan = result.scalars().first()
                loan_deduction = employee_loan.installmentAmount if employee_loan else Decimal(0)

            # 6. Advance Salary
            advance_salary_amount = Decimal(0)
            if row.adjustAdvanceSalary:
                result = await self.db.execute(
                    select(AdvanceSalary).where(
                        AdvanceSalary.employeeID == row.employeeID,
                        AdvanceSalary.status == 3
                    )
                )
                advance_salary = result.scalars().first()
                advance_salary_amount = advance_salary.amount if advance_salary else Decimal(0)

            # 7. Unpaid Leave
            adjust_Unpaid_Leave_Amount = Decimal(0)
            if row.adjustUnpaidLeave:
                result = await self.db.execute(
                    select(func.coalesce(func.sum(LeaveDetail.totalDays), 0))
                    .select_from(LeaveDetail)
                    .join(Leave, Leave.leaveID == LeaveDetail.leaveID)
                    .where(
                        Leave.status == 2,
                        LeaveDetail.isUnPaid == True,
                        LeaveDetail.employeeID == row.employeeID
                    )
                )
                unpaidLeaveDays = result.scalar_one()
                unpaidLeaveDays = Decimal(unpaidLeaveDays or 0)
                adjust_Unpaid_Leave_Amount = (gross / Decimal(22)) * unpaidLeaveDays

            # 8. Final Deduction and Salary Append (👈 OUTSIDE all ifs)
            tax_amount = Decimal(tax_amount)

            total_deduction = (
                Decimal(tax_amount or 0)
                + Decimal(loan_deduction or 0)
                + Decimal(advance_salary_amount or 0)
                + Decimal(adjust_Unpaid_Leave_Amount or 0)
                + Decimal(row.houseRentDeduction or 0)
                + Decimal(row.excessMobileBill or 0)
                + (pf_amount if row.pfDeduction else Decimal("0"))
                + Decimal(row.otherDeduction or 0)
            )
            net_earning = gross - total_deduction

            salary_details.append(SalaryDetailDTO(
                sl=sl,
                employeeID=row.employeeID,
                employeeCode=row.employeeCode,
                employeeName=row.employeeName,
                payscaleID=row.payscaleID,
                payscaleName=row.payscaleName,
                basicSalary=float(round(basic, 2)),
                houseRentAllowance=float(round(house_rent, 2)),
                medicalAllowance=float(round(medical, 2)),
                conveyance=float(round(conveyance, 2)),
                overtime=float(round(overtime, 2)),
                grossEarnings=float(round(gross, 2)),
                taxAmount=float(round(tax_amount, 2)),
                pfAmount=float(round(pf_amount, 2)),
                employerContribution=float(round(employer_contribution, 2)),
                loanAdjust=float(round(loan_deduction, 2)),
                adjustUnpaidLeave=float(round(adjust_Unpaid_Leave_Amount, 2)),
                adjustAdvanceSalary=float(round(advance_salary_amount, 2)),
                totalDeduction=float(round(total_deduction, 2)),
                netEarnings=float(round(net_earning, 2)),
            ))

            sl += 1

        return GenerateSalaryResponseDTO(salaryDetails=salary_details, message="Salary generated successfully")
    
    async def get_last_salary(self) -> Optional[Salary]:
        stmt = select(Salary).order_by(desc(Salary.salaryID)).limit(1)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def generate_salary_number(self) -> str:
        last_salary = await self.get_last_salary()
        if not last_salary:
            return "SAL0000001"

        # extract last number
        last_number = int(last_salary.salaryNumber.replace("SAL", ""))
        new_number = last_number + 1
        return f"SAL{new_number:07d}"
    
    async def insert_all_employee_salary_detail(self, salary: Salary, details: List[SalaryDetail]) -> Dict[str, str]:
            
        self.db.add(salary)
        await self.db.flush()

        for detail in details:
            detail.salaryID = salary.salaryID
            self.db.add(detail)

        await self.db.commit()
        return {"message": "Salary and SalaryDetail inserted successfully"}
    
    async def get_all_companies(self) -> List[CompanyDTO]:
        result = await self.db.execute(select(Company))
        companies = result.scalars().all()
        return [CompanyDTO.model_validate(c) for c in companies]
    
    async def get_all_departments(self) -> List[ActivityCenterDTO]:
        result = await self.db.execute(select(ActivityCenter))
        departments = result.scalars().all()
        return [ActivityCenterDTO.model_validate(d) for d in departments]
    
    async def get_all_sections(self) -> List[ResponsibilityCenterDTO]:
        result = await self.db.execute(select(ResponsibilityCenter))
        sections = result.scalars().all()
        return [ResponsibilityCenterDTO.model_validate(s) for s in sections]
    
    async def get_all_fiscalyear(self) -> List[FiscalYearDTO]:
        stmt = select(FiscalYear.finYearID, FiscalYear.finYear)
        result = await self.db.execute(stmt)
        rows = result.all()
        return [FiscalYearDTO(finYearID=row[0], finYear=row[1]) for row in rows]