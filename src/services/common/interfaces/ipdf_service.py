# services/common/interfaces/ipdf_service.py

from abc import ABC, abstractmethod

class IPdfService(ABC):

    @abstractmethod
    async def generate_invoice_pdf(self, invoice):
        pass