# services/common/email_service.py

import aiosmtplib
from email.message import EmailMessage
from services.common.interfaces.iemail_service import IEmailService

class EmailService(IEmailService):

    async def send_email_with_attachment(
        self,
        to: str,
        subject: str,
        body: str,
        attachment_bytes: bytes,
        filename: str
    ):
        message = EmailMessage()
        message["From"] = "ramzansr@email.com"
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)

        message.add_attachment(
            attachment_bytes,
            maintype="application",
            subtype="pdf",
            filename=filename
        )

        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username="ramzansr@email.com",
            password="your_app_password",
        )