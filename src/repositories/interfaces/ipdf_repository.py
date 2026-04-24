# src/repositories/interfaces/ipdf_repository.py

from abc import ABC, abstractmethod

class IPdfRepository(ABC):

    @abstractmethod
    async def generate_invoice_pdf(self, invoice) -> bytes:
        pass