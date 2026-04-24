# src/repositories/pdf_repository.py

from reportlab.pdfgen import canvas
from io import BytesIO
from src.repositories.interfaces.ipdf_repository import IPdfRepository


class PdfRepository(IPdfRepository):

    async def generate_invoice_pdf(self, invoice) -> bytes:

        buffer = BytesIO()
        c = canvas.Canvas(buffer)

        c.drawString(100, 750, f"Invoice #{invoice.salesInvoiceNo}")
        c.drawString(100, 730, f"Customer: {invoice.customerName}")
        c.drawString(100, 710, f"Amount: {invoice.totalAmount}")

        c.save()
        buffer.seek(0)

        return buffer.read()