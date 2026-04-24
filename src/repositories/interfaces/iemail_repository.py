# src/repositories/interfaces/iemail_repository.py

from abc import ABC, abstractmethod

class IEmailRepository(ABC):

    @abstractmethod
    async def send_email_with_attachment(
        self,
        to: str,
        subject: str,
        body: str,
        attachment_bytes: bytes,
        filename: str
    ) -> None:
        pass