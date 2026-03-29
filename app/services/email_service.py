from __future__ import annotations
from email.message import EmailMessage
from typing import Iterable, Optional
import asyncio
import aiosmtplib

from app.config import settings
from app.services.log_service import LogService


class EmailService:
    def __init__(self) -> None:
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.smtp_from = settings.smtp_from

    # This method is used for every email sending for Fire-and-Forget (Performance wise was too slow as synchronous)
    async def _send_email_async(
        self,
        message: EmailMessage,
        recipients: list[str],
    ) -> None:
        try:
            await aiosmtplib.send(
                message,
                recipients=recipients,  
                hostname=self.smtp_host,
                port=self.smtp_port,
                start_tls=True if self.smtp_username and self.smtp_password else False,
                username=self.smtp_username,
                password=self.smtp_password,
            )
            LogService.WEB.log(f"Email sent successfully to {len(recipients)} recipients", level="INFO")
        except Exception as e:
            LogService.ERROR.log(f"Failed to send email to {message['To']}: {str(e)}", level="ERROR")

    def send(
        self,
        subject: str,
        body: str = "",
        html_body: Optional[str] = None,
        to_addrs: Optional[Iterable[str]] = None,
        cc_addrs: Optional[Iterable[str]] = None,
        bcc_addrs: Optional[Iterable[str]] = None,
        attachments: Optional[list[tuple[str, bytes, str]]] = None,
    ) -> None:
        if not self.smtp_host:
            raise RuntimeError("SMTP_HOST is not configured")

        to_addrs = list(to_addrs or [])
        cc_addrs = list(cc_addrs or [])
        bcc_addrs = list(bcc_addrs or [])

        if not (to_addrs or cc_addrs or bcc_addrs):
            LogService.WEB.log("No recipients provided for email, skipping send.", level="WARNING")
            return

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self.smtp_from
        
        if to_addrs:
            message["To"] = ", ".join(to_addrs)
        else:
            message["To"] = self.smtp_from

        if cc_addrs:
            message["Cc"] = ", ".join(cc_addrs)


        message.set_content(body)

        if html_body:
            message.set_content("This is an HTML email. Please view in an HTML-compatible email viewer.")
            message.add_alternative(html_body, subtype="html")

        if attachments:
            for filename, payload, mime_type in attachments:
                maintype, subtype = mime_type.split("/", 1)
                message.add_attachment(payload, maintype=maintype, subtype=subtype, filename=filename)

        all_recipients = to_addrs + cc_addrs + bcc_addrs

        # Fire-and-forget: schedule async send
        asyncio.create_task(self._send_email_async(message, all_recipients))