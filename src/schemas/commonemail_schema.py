from pydantic import BaseModel


class SendSalesInvoiceEmailRequest(BaseModel):
    salesInvoiceID: int
    to: str
    subject: str
    body: str