# services/common/pdf_service.py

from services.common.interfaces.ipdf_service import IPdfService
from reportlab.pdfgen import canvas
from io import BytesIO

class PdfService(IPdfService):

    async def generate_invoice_pdf(self, invoice):
        buffer = BytesIO()
        c = canvas.Canvas(buffer)

        c.drawString(100, 750, f"Invoice #{invoice.salesInvoiceNo}")
        c.drawString(100, 730, f"Customer: {invoice.customerName}")
        c.drawString(100, 710, f"Amount: {invoice.totalAmount}")

        c.save()
        buffer.seek(0)

        return buffer.read()