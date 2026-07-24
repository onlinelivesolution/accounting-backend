from src.services.interfaces.icommonjournal_service import ICommonJournalService
from src.models.salarypayment import SalaryPayment
from src.models.salarypaymentdetail import SalaryPaymentDetail
from src.repositories.interfaces.isalarypayment_repository import (
    ISalaryPaymentRepository,
)
from src.services.interfaces.isalarypayment_service import ISalaryPaymentService
from src.schemas.salaryschema import SalaryRead
from src.schemas.salarypayment_schema import SalaryPaymentCreateRequest
from typing import Optional
from typing import List
from src.models.salary import Salary
from fastapi import HTTPException
from datetime import datetime


class SalaryPaymentService(ISalaryPaymentService):
    def __init__(
        self,
        repository: ISalaryPaymentRepository,
        journal_service: ICommonJournalService,
    ):
        self.repository = repository
        self.journal_service = journal_service

    async def get_approve_salary(
        self, year: str, month: int, status: int
    ) -> List[SalaryRead]:
        salaries = await self.repository.get_approve_salary(year, month, status)
        return [SalaryRead.from_orm(salary) for salary in salaries]

        # create new sales invoice

    async def create_salary_payment(
        self,
        request: SalaryPaymentCreateRequest,
        current_user: dict,
    ):

        salary_payment = SalaryPayment(
            paymentNo=request.paymentNo,
            paymentDate=request.paymentDate,
            salaryMonth=request.salaryMonth,
            salaryYear=request.salaryYear,
            bankAccountCode=request.bankAccountCode,
            totalAmount=request.totalAmount,
            remarks=request.remarks,
            status=request.status,
            createdBy=current_user["userID"],
            createdDate=datetime.utcnow(),
            companyCode=request.companyCode,
        )

        for item in request.salaryPaymentDetails:

            salary_payment.salaryPaymentDetails.append(
                SalaryPaymentDetail(
                    salaryID=item.salaryID,
                    employeeID=item.employeeID,
                    amount=item.amount,
                    paymentStatus=item.paymentStatus,
                )
            )

        # Save Payment
        payment = await self.repository.create_salary_payment(salary_payment)

        # ===============================
        # Create Journal
        # ===============================
        await self.journal_service.post_salary_payment_journal(payment)

        return {
            "salaryPaymentID": payment.salaryPaymentID,
            "paymentNo": payment.paymentNo,
            "message": "Salary payment created successfully.",
        }
        
    async def get_next_salary_payment_no(self) -> str:
        return await self.repository.get_next_salary_payment_no()
