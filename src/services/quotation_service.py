from src.services.interfaces.iquotation_service import IQuotationService
from src.repositories.interfaces.iquotation_repository import IQuotationRepository
from src.models.quotation import Quotation
from src.models.quotationdetail import QuotationDetail
from src.schemas.quotation_schema import QuotationCreateRequest
from datetime import datetime


class QuotationService(IQuotationService):

    def __init__(self, repository: IQuotationRepository):
        self.repository = repository

    async def create_quotation(self, request: QuotationCreateRequest) -> Quotation:
        quotation = Quotation(
            quotationNo=request.quotationNo,
            quotationDate=request.quotationDate,
            customerID=request.customerID,
            subtotalAmount=request.subtotalAmount,
            discountAmount=request.discountAmount,
            vATAmount=request.vATAmount,
            totalAmount=request.totalAmount,
            createdBy=request.createdBy,
            createdDate=datetime.utcnow(),
            status="Draft",
            remarks=request.remarks,
            items=[]  # ✅ initialize relationship
        )

        for item in request.items:
            quotation.items.append(
                QuotationDetail(
                    itemID=item.itemID,
                    itemDescription=item.itemDescription,
                    quantity=item.quantity,
                    unitPrice=item.unitPrice,
                    discountAmount=item.discountAmount,
                    lineTotal=item.lineTotal
                )
            )

        return await self.repository.create(quotation)

    async def get_quotation(self, quotationID: int):
        return await self.repository.get_by_id(quotationID)

    async def list_quotations(self):
        return await self.repository.get_all()
    
    async def get_next_quotation_no(self) -> str:
        return await self.repository.get_next_quotation_no()
    
    async def get_quotation_table(self):
        quotations = await self.repository.get_quotation_table()

        return [
            {
                "quotationID": q.quotationID,
                "quotationNo": q.quotationNo,
                "quotationDate": q.quotationDate,
                "totalAmount": q.totalAmount,
                "customerID": q.customerID,
                "status": q.status,
                "customerName": q.customer.customerName if q.customer else None
            }
            for q in quotations
        ]
    
    async def get_quotation_filters(self, filter_type: str):
        return await self.repository.get_quotation_filters(filter_type)
    
