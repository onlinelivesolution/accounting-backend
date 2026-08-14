from src.repositories.interfaces.igeneratesalary_repository import (
    IGenerateSalaryRepository,
)
from src.services.interfaces.igeneratesalary_service import IGenerateSalaryService
from src.services.interfaces.icommonjournal_service import ICommonJournalService
from src.schemas.controlitem_schema import (
    ControlItemRead,
    ControlItemCreate,
    ControlItemUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.salary import Salary
from src.schemas.salaryschema import SalaryRead
from src.dto.companydto import CompanyDTO
from src.dto.fiscalyeardto import FiscalYearDTO
from src.dto.activitycenterdto import ActivityCenterDTO
from src.dto.responsibilitycenterdto import ResponsibilityCenterDTO
from datetime import datetime
from src.models.salarydetail import SalaryDetail
from src.dto.payscalerowdto import PayScaleRowDTO
from src.dto.generatesalaryrowdto import GenerateSalaryRowDTO
from src.dto.generatesalaryresponsedto import GenerateSalaryResponseDTO
from typing import List, Dict, Optional


class GenerateSalaryService(IGenerateSalaryService):
        
    def __init__(
        self,
        repository: IGenerateSalaryRepository,
        journal_service: ICommonJournalService,
    ):
        self.repository = repository
        self.journal_service = journal_service

    async def generate_all_active_employee_salary(
        self, rows: List[GenerateSalaryRowDTO]
    ) -> GenerateSalaryResponseDTO:
        return await self.repository.generate_all_active_employee_salary(rows)

    async def insert_all_employee_salary_detail(
        self,
        data: GenerateSalaryResponseDTO
    ) -> Dict[str, str]:

        salary = Salary(
            fiscalYear=data.salary.fiscalYear,
            month=datetime.now().month,
            workingDay=data.salary.workingDay,
            companyCode=data.salary.companyCode,
            departmentCode=data.salary.departmentCode,
            sectionCode=data.salary.sectionCode,
            createdBy=data.salary.createdBy,
            createdDate=datetime.now(),
            hRComments=data.salary.hRComments,
            status=data.salary.status,
            year=datetime.now().year,
        )

        # ============================================================
        # Build SalaryDetail list
        # ============================================================

        details = []

        for d in data.salaryDetails:

            details.append(
                SalaryDetail(
                    employeeID=d.employeeID,
                    payscaleID=d.payscaleID,
                    absenceDay=d.absenceDay,

                    basicSalary=d.basicSalary,
                    houseRentAllowance=d.houseRentAllowance,
                    medicalAllowance=d.medicalAllowance,
                    travelAllowance=d.travelAllowance,
                    conveyance=d.conveyance,
                    overtime=d.overtime,
                    otherAllowance=d.otherAllowance,

                    grossEarnings=d.grossEarnings,

                    adjustUnpaidLeave=d.adjustUnpaidLeave,
                    taxAmount=d.taxAmount,
                    pfAmount=d.pfAmount,
                    employerContribution=d.employerContribution,

                    supplementaryPF=d.supplementaryPF,

                    loanAdjust=d.loanAdjust,
                    houseRentDeduction=d.houseRentDeduction,
                    excessMobileBill=d.excessMobileBill,
                    adjustAdvanceSalary=d.adjustAdvanceSalary,
                    gradedTax=d.gradedTax,
                    otherDeduction=d.otherDeduction,

                    netEarnings=d.netEarnings,

                    companyCode=salary.companyCode,
                    departmentCode=salary.departmentCode,
                    sectionCode=salary.sectionCode,

                    status=salary.status,
                    isUnPaid=d.isUnPaid,

                    createdBy=d.createdBy or data.salary.createdBy,
                    createdDate=datetime.now(),

                    settingTaxAmount=d.settingTaxAmount,
                )
            )

        # ============================================================
        # Save Salary + Salary Details
        # ============================================================

        saved_salary = await self.repository.insert_all_employee_salary_detail(
            salary,
            details,
        )

        if not saved_salary or not saved_salary.salaryID:
            raise Exception(
                "Salary was saved but salaryID was not generated."
            )

        saved_salary = await self.repository.get_salary_with_details(
            saved_salary.salaryID
        )

        if not saved_salary:
            raise Exception(
                f"Salary {salary.salaryID} could not be loaded after saving."
            )

        # ============================================================
        # Create Generate Salary Journal
        # ============================================================
        
        print("====================================")
        print("SALARY JOURNAL DEBUG")
        print("Salary ID:", salary.salaryID)
        print("Salary No:", salary.salaryNo)
        print("Company:", salary.companyCode)
        print("Created:", salary.createdDate)
        print("Details:", len(salary.details))
        print("====================================")

        for d in salary.details:
            print(
                "Employee:",
                d.employeeID,
                "Gross:",
                d.grossEarnings,
                "Tax:",
                d.taxAmount,
                "PF:",
                d.pfAmount,
                "Employer:",
                d.employerContribution,
                "Loan:",
                d.loanAdjust,
                "Advance:",
                d.adjustAdvanceSalary,
                "Unpaid:",
                d.adjustUnpaidLeave,
                "Other:",
                d.otherDeduction,
                "Net:",
                d.netEarnings,
            )

        await self.journal_service.post_generate_salary_journal(
            saved_salary
        )
        # ============================================================
        # Return original repository response
        # ============================================================

        return {
            "salaryID": saved_salary.salaryID,
            "message": "Salary information saved and journal created successfully.",
        }


    async def get_next_salary_number(self) -> str:
        return await self.repository.generate_salary_number()

    async def get_all_companies(self) -> List[CompanyDTO]:
        return await self.repository.get_all_companies()

    async def get_all_departments(self) -> List[ActivityCenterDTO]:
        return await self.repository.get_all_departments()

    async def get_all_sections(self) -> List[ResponsibilityCenterDTO]:
        return await self.repository.get_all_sections()

    async def get_all_fiscalyear(self) -> List[FiscalYearDTO]:
        return await self.repository.get_all_fiscalyear()
