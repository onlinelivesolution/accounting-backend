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
    def __init__(self, repository: ISalaryPaymentRepository):
        self.repository = repository

    async def get_approve_salary(
        self, year: str, month: int, status: int
    ) -> List[SalaryRead]:
        salaries = await self.repository.get_approve_salary(year, month, status)
        return [SalaryRead.from_orm(salary) for salary in salaries]

        # create new sales invoice

    async def create_salary_payment(
        self, request: SalaryPaymentCreateRequest, current_user: dict
    ) -> SalaryPayment:
        salary_payment =   SalaryPayment(
            salaryID=request.salaryID,
            fiscalYear=request.fiscalYear,
            month=request.month,
            workingDay=request.workingDay,
            companyCode=request.companyCode,
            departmentCode=request.departmentCode,
            sectionCode=request.sectionCode, 
            createdDate=request.createdDate,
            status=request.status,
            year=request.year,
            salesInvoiceDate=request.salesInvoiceDate,
            expireDate=request.expireDate,
            customerID=request.customerID,
            exclusiveAmount=request.exclusiveAmount,
            discountAmount=request.discountAmount,
            vatAmount=request.vatAmount,
            totalAmount=request.totalAmount,
            createdBy=current_user["userID"],
           
     
        )

        for item in request.items:
            salary_payment.items.append(
                SalaryPaymentDetail(
                    itemID=item.itemID,
                    itemDescription=item.itemDescription,
                    quantity=item.quantity,
                    unitPrice=item.unitPrice,
                    exclusiveAmount=item.exclusiveAmount,
                    discountAmount=item.discountAmount,
                    vatAmount=item.vatAmount,
                    totalAmount=item.totalAmount,
                )
            )

        return await self.repository.create_salary_payment(salary_payment)
