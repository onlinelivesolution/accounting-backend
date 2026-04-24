# services/common/interfaces/iemail_service.py

from abc import ABC, abstractmethod

class IEmailService(ABC):

    @abstractmethod
    async def send_email_with_attachment(
        self,
        to: str,
        subject: str,
        body: str,
        attachment_bytes: bytes,
        filename: str
    ):
        pass